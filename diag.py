#!/usr/bin/env python3
"""
diag.py — answers one question: what identity, if any, does this sandbox have?

The "Metadata Auth Error" message collapses several very different causes
into one string. This separates them, because the fix for each is
different and some have no fix at all.

Run:  python3 scripts/diag.py
"""

import json
import os
import socket
import subprocess
import sys
import urllib.error
import urllib.request

METADATA_HOST = "metadata.google.internal"
METADATA_BASE = f"http://{METADATA_HOST}/computeMetadata/v1"
results = {}


def record(name, ok, detail, **extra):
    results[name] = {"ok": ok, "detail": detail, **extra}


def check_dns():
    try:
        ip = socket.gethostbyname(METADATA_HOST)
        record("dns", True, f"{METADATA_HOST} resolves to {ip}")
    except Exception as exc:
        record(
            "dns", False, f"{type(exc).__name__}: {exc}",
            means="No metadata server is reachable by name. Either this "
                  "sandbox is not a GCE-style VM, or DNS is isolated.",
        )


def check_tcp():
    try:
        sock = socket.create_connection((METADATA_HOST, 80), timeout=5)
        sock.close()
        record("tcp_80", True, "TCP connection to metadata server succeeded")
    except Exception as exc:
        record(
            "tcp_80", False, f"{type(exc).__name__}: {exc}",
            means="Name may resolve but nothing is listening, or egress is "
                  "blocked by the sandbox network policy.",
        )


def metadata_get(path, timeout=5):
    req = urllib.request.Request(f"{METADATA_BASE}{path}")
    req.add_header("Metadata-Flavor", "Google")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8")


def check_service_accounts():
    try:
        body = metadata_get("/instance/service-accounts/")
        accounts = [line for line in body.split("\n") if line.strip()]
        record(
            "service_accounts", True, "Metadata server responded",
            accounts=accounts,
            means="An identity exists. If the token call still fails, the "
                  "issue is scopes or IAM, not the absence of an account.",
        )
    except urllib.error.HTTPError as exc:
        record(
            "service_accounts", False, f"HTTP {exc.code}: {exc.reason}",
            means="Metadata server is present but exposes no service "
                  "account. Nothing is attached to this sandbox.",
        )
    except Exception as exc:
        record("service_accounts", False, f"{type(exc).__name__}: {exc}")


def check_token():
    try:
        body = metadata_get("/instance/service-accounts/default/token")
        data = json.loads(body)
        record(
            "token", True, "Access token issued",
            expires_in=data.get("expires_in"),
            scope_hint=data.get("scope", "not reported"),
            means="Auth works. Any remaining failure is IAM permissions on "
                  "the dataset, not authentication.",
        )
    except urllib.error.HTTPError as exc:
        record("token", False, f"HTTP {exc.code}: {exc.reason}")
    except Exception as exc:
        record("token", False, f"{type(exc).__name__}: {exc}")


def check_egress():
    """Can the sandbox reach Google APIs at all, separate from metadata?"""
    for host in ("bigquery.googleapis.com", "oauth2.googleapis.com"):
        try:
            socket.create_connection((host, 443), timeout=5).close()
            record(f"egress_{host}", True, "TCP 443 reachable")
        except Exception as exc:
            record(
                f"egress_{host}", False, f"{type(exc).__name__}: {exc}",
                means="Even with a token, BigQuery would be unreachable. "
                      "The network allowlist needs this host.",
            )


def check_environment():
    keys = [
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_CLOUD_PROJECT",
        "GCLOUD_PROJECT",
        "GCE_METADATA_HOST",
        "CLOUDSDK_CORE_PROJECT",
    ]
    present = {k: os.environ.get(k) for k in keys if os.environ.get(k)}
    record(
        "env_vars", bool(present),
        "Credential-related environment variables found" if present
        else "No credential-related environment variables set",
        found=present,
    )

    adc = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    record("adc_file", os.path.exists(adc), adc)


def check_libraries():
    for mod in ("google.cloud.bigquery", "google.auth"):
        try:
            __import__(mod)
            record(f"lib_{mod}", True, "importable")
        except ImportError as exc:
            record(
                f"lib_{mod}", False, str(exc),
                means="Use the BigQuery REST API over urllib instead of the "
                      "client library.",
            )


def check_identity_tools():
    try:
        out = subprocess.run(
            ["gcloud", "auth", "list", "--format=json"],
            capture_output=True, text=True, timeout=15,
        )
        record("gcloud", out.returncode == 0, (out.stdout or out.stderr).strip()[:500])
    except Exception as exc:
        record("gcloud", False, f"{type(exc).__name__}: {exc}")


def verdict():
    if results.get("token", {}).get("ok"):
        return ("AUTH_WORKS",
                "The sandbox has a usable identity. Investigate IAM grants "
                "on the dataset next.")
    if not results.get("dns", {}).get("ok"):
        return ("NO_METADATA_SERVER",
                "This sandbox is not a GCE-style environment, so there is no "
                "metadata identity to fetch. Credentials must be supplied "
                "another way, or this approach cannot work in a GE skill.")
    if results.get("dns", {}).get("ok") and not results.get("service_accounts", {}).get("ok"):
        return ("NO_SERVICE_ACCOUNT_ATTACHED",
                "A metadata server exists but carries no service account. "
                "This is a configuration question for whoever provisions the "
                "sandbox.")
    return ("UNCLEAR", "Review the individual checks below.")


def main():
    check_dns()
    check_tcp()
    check_service_accounts()
    check_token()
    check_egress()
    check_environment()
    check_libraries()
    check_identity_tools()

    code, explanation = verdict()
    print(json.dumps(
        {"verdict": code, "explanation": explanation, "checks": results},
        indent=2, default=str,
    ))


if __name__ == "__main__":
    main()
