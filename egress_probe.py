#!/usr/bin/env python3
"""
egress_probe.py — is this sandbox missing a DNS resolver, or missing a network?

"Temporary failure in name resolution" is ambiguous. It appears both when
egress is fully blocked and when egress works fine but no resolver is
configured. The fix for the second case exists; for the first it does not.

This probe separates them by bypassing DNS entirely:
  1. Read the resolver configuration, if any.
  2. Speak DNS directly to public resolvers over raw UDP.
  3. Open raw TCP to known-good IPs, no hostname involved.
  4. If any of that works, attempt a real TLS request to Google by IP.

Run:  python3 scripts/egress_probe.py
"""

import json
import os
import random
import socket
import ssl
import struct
import sys

results = {}

# Public resolvers, addressed by IP so no DNS is needed to reach them.
RESOLVERS = ["8.8.8.8", "8.8.4.4", "1.1.1.1"]

# Well-known IPs for raw TCP reachability. These are stable anycast
# addresses, used only to answer "does any packet leave this box".
RAW_TCP_TARGETS = [
    ("8.8.8.8", 53, "Google public DNS"),
    ("1.1.1.1", 443, "Cloudflare"),
]


def record(name, ok, detail, **extra):
    results[name] = {"ok": ok, "detail": detail, **extra}


def read_resolv_conf():
    path = "/etc/resolv.conf"
    try:
        with open(path) as fh:
            content = fh.read().strip()
        nameservers = [
            line.split()[1]
            for line in content.splitlines()
            if line.strip().startswith("nameserver") and len(line.split()) > 1
        ]
        record(
            "resolv_conf", bool(nameservers),
            content[:400] if content else "(empty)",
            nameservers=nameservers,
            means="No nameserver line means the resolver is simply absent. "
                  "That is fixable in code if egress works."
                  if not nameservers else
                  "A resolver is configured. If lookups still fail, the "
                  "resolver itself is unreachable.",
        )
    except Exception as exc:
        record("resolv_conf", False, f"{type(exc).__name__}: {exc}")


def build_dns_query(hostname):
    """Minimal DNS A-record query. No external library needed."""
    txid = random.randint(0, 0xFFFF)
    header = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    qname = b"".join(
        bytes([len(part)]) + part.encode("ascii")
        for part in hostname.split(".")
    ) + b"\x00"
    question = qname + struct.pack(">HH", 1, 1)  # type A, class IN
    return txid, header + question


def parse_dns_answer(payload, txid):
    rtxid, flags, _, ancount = struct.unpack(">HHHH", payload[:8])
    if rtxid != txid:
        raise ValueError("transaction id mismatch")
    if ancount == 0:
        raise ValueError(f"no answer records (flags 0x{flags:04x})")

    # Skip the question section.
    idx = 12
    while payload[idx] != 0:
        idx += payload[idx] + 1
    idx += 5

    for _ in range(ancount):
        if payload[idx] & 0xC0 == 0xC0:
            idx += 2
        else:
            while payload[idx] != 0:
                idx += payload[idx] + 1
            idx += 1
        rtype, _, _, rdlength = struct.unpack(">HHIH", payload[idx:idx + 10])
        idx += 10
        if rtype == 1 and rdlength == 4:
            return socket.inet_ntoa(payload[idx:idx + 4])
        idx += rdlength
    raise ValueError("no A record in answer")


def manual_dns(hostname="bigquery.googleapis.com"):
    """Resolve without the system resolver, by talking UDP to 8.8.8.8."""
    for resolver in RESOLVERS:
        txid, query = build_dns_query(hostname)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(query, (resolver, 53))
            payload, _ = sock.recvfrom(4096)
            sock.close()
            ip = parse_dns_answer(payload, txid)
            record(
                f"manual_dns_via_{resolver}", True,
                f"{hostname} resolved to {ip}",
                resolved_ip=ip,
                means="UDP egress works and DNS can be done in code. The "
                      "system resolver was the only thing missing.",
            )
            return ip
        except Exception as exc:
            record(f"manual_dns_via_{resolver}", False, f"{type(exc).__name__}: {exc}")
    return None


def raw_tcp():
    reachable = False
    for host, port, label in RAW_TCP_TARGETS:
        try:
            sock = socket.create_connection((host, port), timeout=5)
            sock.close()
            record(f"raw_tcp_{host}_{port}", True, f"{label} reachable by IP")
            reachable = True
        except Exception as exc:
            record(
                f"raw_tcp_{host}_{port}", False, f"{type(exc).__name__}: {exc}",
                means="No packets leave the sandbox even to a raw IP. "
                      "This is full network isolation, not a DNS problem.",
            )
    return reachable


def tls_by_ip(ip, hostname="bigquery.googleapis.com"):
    """Real TLS handshake to Google, connecting by IP with SNI set."""
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((ip, 443), timeout=10) as raw:
            with ctx.wrap_socket(raw, server_hostname=hostname) as tls:
                request = (
                    f"GET /discovery/v1/apis HTTP/1.1\r\n"
                    f"Host: {hostname}\r\n"
                    f"Connection: close\r\n\r\n"
                ).encode()
                tls.send(request)
                head = tls.recv(120).decode("utf-8", "replace")
        record(
            "tls_by_ip", True, head.splitlines()[0] if head else "(empty)",
            means="Full HTTPS path works. A skill CAN reach BigQuery by "
                  "resolving manually and connecting by IP. Authentication "
                  "is then the only remaining problem.",
        )
        return True
    except Exception as exc:
        record("tls_by_ip", False, f"{type(exc).__name__}: {exc}")
        return False


def verdict():
    manual_ok = any(k.startswith("manual_dns_via_") and v["ok"] for k, v in results.items())
    tcp_ok = any(k.startswith("raw_tcp_") and v["ok"] for k, v in results.items())
    tls_ok = results.get("tls_by_ip", {}).get("ok")

    if tls_ok:
        return ("EGRESS_WORKS_DNS_WAS_MISSING",
                "The sandbox can reach Google APIs. Only the system resolver "
                "was absent, and code can work around that. Authentication "
                "is now the remaining blocker, not the network.")
    if manual_ok or tcp_ok:
        return ("PARTIAL_EGRESS",
                "Some packets leave the sandbox but the HTTPS path to Google "
                "did not complete. Review the individual checks.")
    return ("NO_EGRESS",
            "Nothing leaves the sandbox, even to a raw IP with no DNS "
            "involved. This is full network isolation. No code change can "
            "reach BigQuery from a skill here.")


def main():
    read_resolv_conf()
    tcp_ok = raw_tcp()
    ip = manual_dns()
    if ip:
        tls_by_ip(ip)
    elif tcp_ok:
        record("tls_by_ip", False, "skipped — no IP resolved to connect to")

    code, explanation = verdict()
    print(json.dumps(
        {"verdict": code, "explanation": explanation, "checks": results},
        indent=2, default=str,
    ))


if __name__ == "__main__":
    main()
