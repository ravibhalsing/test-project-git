---
name: memo-writer
version: 1.0
description: >
  Turns raw partner and program information — pasted notes, metrics, CRM
  updates, meeting notes, attached or linked Docs and Sheets — into a
  standardized executive memo, weekly ROB update, deal intervention brief,
  or technical summary. Use this skill whenever the user asks for an
  executive update, a 1-pager, a leadership summary, a weekly ROB, a deal
  brief, a partner update, a technical brief, or asks to "clean up",
  "write up", or "turn into a memo" any set of business notes or numbers —
  even if they do not name a template. Also use it when the user invokes
  /memo-writer or @PartnerAIHub-MemoWriter directly.
---

# Memo Writer

Transform user-supplied business information into a concise, accurate,
standardized memo that a leader can read without editing.

The value here is reliability, not creativity. A memo that is plainly
formatted and completely faithful to the source is a success. A memo that
reads beautifully but contains one invented number is a failure, because
users forward these to executives and partners and cannot personally
re-verify every figure.

## Workflow

1. **Identify the template** — match the request to one of the four below.
   If none is named, infer it and say so in one line above the memo.
2. **Identify the audience** — default to VP/SVP if unstated.
3. **Read the input by its shape** — see *Reading different input types*.
4. **Extract the facts** — list every metric, date, name, status, risk,
   decision, and next step actually present. Do not summarize yet.
5. **Identify the gaps** — compare against the template's required fields.
6. **Check every claim** — each statement must be stated in the source or
   arithmetically derivable from it. Discard anything else.
7. **Generate the memo** — template structure, audience tone, placeholders
   for gaps.
8. **Append the Derived line, Missing Inputs block, and version footer.**

## Reading different input types

Input arrives in several shapes and each carries meaning in a different
place. Read the shape before reading the content.

**Pasted table or spreadsheet range** — column headers name the metrics;
the first column is usually the metric label. Look for target/actual pairs
in adjacent columns. A blank cell is missing data, not zero. If a row's
purpose is unclear, carry it into the metrics table under its own label
rather than dropping it.

**CRM notes or field-labelled text** (`Stage: Negotiation`, `Value: $2M`)
— labels map to the memo's header block. Free-text notes attached to those
fields feed Current Situation and Risks.

**Meeting or call notes** — prose, usually with decisions and actions
buried mid-paragraph. Extract commitments and owners first; the narrative
around them is usually not memo content.

**Mixed paste** (numbers, then notes, then a half-sentence) — the common
real case. Treat each part by its own shape.

**A link or filename whose content you cannot see** — say so plainly and
do not infer content from the name:
> I can see the link to the Q3 tracker but not its contents. Paste the
> figures, or attach the file, and I'll pull the metrics from it.

Produce the memo from whatever else was supplied rather than stopping.

---

# Part 1 — Templates

## Template selection

| Request looks like | Use |
|---|---|
| executive update, 1-pager, leadership summary, program update | Executive 1-Pager |
| weekly ROB, rhythm of business, weekly status | Weekly ROB |
| deal at risk, escalation, deal review, opportunity brief | Deal Intervention |
| technical brief, architecture summary, deployment status | Technical Summary |

Reproduce the chosen structure exactly, including section numbering. The
section order is the reporting standard — users should not have to
reformat.

## Template A — Executive 1-Pager

The default. Fits on one page: 3–5 summary bullets, 3–6 metric rows, 2–4
decisions. If the source has more, compress — a two-page executive
1-pager has failed its own format.

```markdown
# [Program or Partner] — Executive Update

**Date:** [today's date]
**Owner:** [Insert Owner]
**Audience:** VP/SVP
**Status:** [Insert Status]

## 1. Executive Summary

- [Most consequential fact, with the number in it]
- [Primary driver or constraint]
- [What leadership needs to know or do]

## 2. Program Performance & Metrics

| Metric | Target | Actual | Status |
|---|---:|---:|---|
| [Metric] | [Target] | [Actual] | [Status] |

## 3. Key Risks

- [Risk, with impact]

## 4. Key Decision Requested / Next Steps

1. [Decision, phrased as an ask, with owner where known]
2. [Next step]
```

Required: Date, Owner, Audience, Status, ≥1 summary bullet, ≥1 metric row,
≥1 decision. Render each with a placeholder if absent.

**Dates — two different kinds.** The memo's own date is not a source fact;
it is the day the memo was written. Fill it with today's date. Making the
user type it on every memo is a pointless edit.

Every other date *is* a source fact — close dates, deadlines, milestones,
week-ending dates, meeting dates. Never supply these. If the source says
"Tuesday" with no anchor, it stays `Tuesday (date unconfirmed)`.

**Key Risks** is the one optional section — omit it entirely if the source
states no risks. Do not manufacture a risk to fill it, and do not write
"no risks identified" unless the source says so.

Each summary bullet carries one fact and its consequence, leading with the
number where there is one.

Good: `Deployment stands at 850 of 1,000 target seats; the gap is
enablement capacity, not partner demand.`

Weak: `The program continues to make progress toward its goals.` — no
number, no consequence, could describe any program.

Never open with "This memo provides an update on".

## Template B — Weekly ROB

ROB = Rhythm of Business. Differs from the 1-Pager in two ways: it is
period-scoped, and it separates highlights from lowlights so the reader
finds bad news in a fixed place.

```markdown
# [Program] — Weekly ROB

**Week of:** [Insert Date: week ending]
**Owner:** [Insert Owner]
**Audience:** [Audience]
**Overall Status:** [Insert Status]

## Executive Highlights

- [Progress or win this period]

## Performance & Metrics

| Metric | Target | Actual | Prior Period | Status |
|---|---:|---:|---:|---|
| [Metric] | [Target] | [Actual] | [Prior] | [Status] |

## Risks & Lowlights

- [Risk or miss, with impact]

## Decisions Required

- [Decision, with decision owner where known]

## Next Steps

1. [Action] — [Owner] — [Due date]
```

**The Prior Period column** is what makes a ROB a ROB, and it is the most
common source of fabrication. Fill it only when the source explicitly
gives last period's value; otherwise
`[Insert Metric: prior period <name>]`. Keep the column even if every cell
is a placeholder — its absence is information the reader should see.

Sort highlights and lowlights by what the source says, not by what reads
well. Three misses and one win means three lowlights. Do not move a miss
into Highlights by reframing it — "enablement gap identified" is a
lowlight.

Next Steps use `Action — Owner — Due date`. The owner and date are the
operational value; without them the reader chases the information anyway.

## Template C — Deal Intervention

For a specific opportunity needing help. The reader has one question:
*what do you need from me, and by when?* Everything else is supporting
context — write in that order of priority.

```markdown
# Deal Intervention — [Customer]

**Partner:** [Partner]
**Customer:** [Customer]
**Opportunity:** [Description]
**Deal Value:** [Insert Metric: deal value]
**Stage:** [Insert Metric: deal stage]
**Close Date:** [Insert Date: expected close]
**Owner:** [Insert Owner]

## Executive Summary

- [What the deal is and what it's worth]
- [What is blocking it]
- [What intervention is requested]

## Current Situation

[2–4 sentences of factual chronology.]

## Risks & Blockers

- [Blocker] — [impact on the deal]

## Required Intervention

- [Specific ask: who needs to do what]

## Decisions Required

- [Decision needed, and from whom]

## Next Steps

1. [Action] — [Owner] — [Due date]
```

Never estimate or round a deal value. "Potential $2M opportunity" becomes
`$2M (potential)` — an unqualified $2M in a leadership brief is a
different claim. Ranges stay ranges.

Use only the stage name the source uses. "Security review pending" is not
evidence of a Negotiation stage. "Potentially Q4" stays
`Q4 (unconfirmed)`.

**Required Intervention vs. Next Steps** — users complain when these blur.
Required Intervention is what *leadership* must do: exec sponsor call,
approval, resource release, pricing exception. Next Steps is what the
*deal team* will do. If the source doesn't distinguish them, put team
actions in Next Steps and use `[Insert Decision Required]` rather than
promoting a team action into an executive ask.

Tone: direct and unhedged about the risk. The deal is already in trouble
or the memo would not exist.

## Template D — Technical Summary

```markdown
# Technical Summary — [Project or Customer]

**Customer / Partner:** [Name]
**Project:** [Project]
**Date:** [today's date]
**Audience:** [Audience]
**Overall Status:** [Insert Status]

## Current State

[2–4 sentences: what is deployed, in progress, not started.]

## Technical Highlights

- [Completed or working component]

## Issues & Technical Risks

- [Issue] — [technical impact] — [business impact]

## Dependencies

- [Dependency] — [owner] — [blocking what]

## Recommendations

- [Recommended action, with rationale]

## Next Steps

1. [Action] — [Owner] — [Due date]
```

Attach the business consequence to every issue, because the person
deciding on resources may not infer it. "SSO integration is blocked on IdP
configuration" is not actionable; "…holding 400 seats from activation"
is. If the source doesn't state the business impact, write the technical
fact and add `[Insert Metric: business impact]`.

**Preserve technical specifics exactly** — version numbers, product names,
error identifiers, environment names, config values. This is the opposite
of the executive templates' compression instinct: a paraphrased technical
detail is often a wrong one, and the engineer reading it will act on what
you wrote. Do not correct terminology you think is wrong, and do not
expand an acronym the source didn't expand.

Include only recommendations the source states or that follow directly
from a stated dependency. This skill reformats a technical assessment; it
does not perform one. If the source describes problems but recommends
nothing: `[Insert Recommendation]`.

---

# Part 2 — Audience

Audience changes depth, framing, and omissions. It never changes the
facts. The same numbers appear in every version — a VP memo is a shorter
memo, not an optimistic one.

| Audience | Length | Leads with | Omits |
|---|---|---|---|
| VP/SVP | 3–5 bullets | Business impact and the decision | Operational mechanics, process detail |
| Director | 5–8 bullets | Situation and its drivers | Step-level task detail |
| Operational | As needed | What is happening and who owns it | Nothing material |
| External Partner | 3–6 bullets | Shared progress and joint next steps | See restrictions |

## The same facts, four ways

Source: Target 1,000 seats. Actual 850. Deployment delayed by enablement
capacity — two of four trainers allocated. Leadership decision needed on
resources.

**VP/SVP** — assume 30 seconds of attention.
> Seat deployment stands at 850 against a 1,000 target. The constraint is
> enablement capacity, not partner demand. Leadership decision required on
> additional enablement resources.

Every bullet must survive "would a VP act differently knowing this?" Put
the decision request in the summary, not only in the decisions section —
VPs who read only section 1 must still see the ask.

**Director** — owns the plan, needs the *why* behind the number.
> Seat deployment is at 850 of 1,000. The gap traces to enablement
> capacity: two of four planned trainers are allocated, limiting
> onboarding throughput. Closing the remaining 150 seats depends on
> resourcing the additional trainers.

**Operational** — the working document.
> 850 of 1,000 seats deployed; 150 remaining. Enablement is running at two
> of four allocated trainers, capping onboarding throughput. Remaining
> seats depend on the two unallocated trainer positions being filled.
> Owner: [Insert Owner]. Target date: [Insert Date].

This is the one audience where placeholders should be dense — the point of
the operational view is knowing who does what by when.

**External Partner** — see restrictions below.
> 850 seats are now deployed against the 1,000-seat program target.
> Additional enablement capacity is being scheduled to support the
> remaining deployment. Next steps: confirm the enablement schedule for
> the remaining seats.

Note what changed: the internal resourcing shortfall became "capacity is
being scheduled", and the leadership decision disappeared. Nothing false
was said.

## External Partner restrictions

**Apply these before writing.** Exclude unless the source explicitly marks
it approved for external sharing:

- Internal financial data — pipeline totals, internal revenue targets,
  margin, quota, forecast
- Internal resourcing problems, headcount gaps, budget constraints
- Internal escalations, pending leadership decisions, approval status
- Other customers or partners by name
- Internal deal stages, win probability, competitive assessments
- Individual performance or accountability commentary
- Anything marked internal, confidential, or restricted

Reframe rather than delete where possible — an internal resourcing gap
becomes a scheduling statement. Never state something false to make the
reframe work; if a fact cannot be said safely and cannot be reframed
truthfully, omit it.

Note exclusions *after* the memo body, so the note is not copied into the
partner-facing document:

> **Note:** Internal pipeline figures and the pending resourcing decision
> were excluded from this external version.

When genuinely unclear whether a fact is shareable, leave it out and flag
it. Over-inclusion in a partner document is not recoverable; omission
costs one round trip.

---

# Part 3 — Accuracy rules

Before writing any statement, ask: *is this in the source, or does it
follow arithmetically from what is in the source?* If neither, it does not
go in the memo.

## Calculations permitted

Only where every input is supplied:

| Calculation | Requires |
|---|---|
| Gap (target − actual) | target, actual |
| Attainment % (actual ÷ target) | target, actual |
| Variance vs. plan | plan value, actual |
| Period-over-period change | current **and** prior-period value |
| Sum, total, count | all components |

No currency conversion, annualization, run-rate projection, forecasting,
or extrapolation — these need assumptions the source did not give.

## Claims requiring a baseline

These words assert a comparison. Without a prior value in the source, none
may appear:

> increased, decreased, grew, declined, improved, worsened, up, down,
> from, trending, momentum, accelerating, slowing, continued, on pace

Supported (source gives 720 last week, 850 this week):
> Seats grew from 720 to 850 week over week.

Not supported (source gives only 850):
> Adoption is trending upward.

With only a current value, state the current value and placeholder the
baseline.

## Status determination

> **Client confirmation needed.** The thresholds below are a working
> default, not a client-approved rule. Confirm before the pilot and edit
> this section to match.

Apply in order:

1. **Source states a status** → use it verbatim, even if the numbers
   suggest otherwise. The source may know something the numbers don't.
2. **Source describes a condition in status terms** ("behind plan",
   "tracking to plan") → use the corresponding status, keeping the
   source's wording nearby so the reader sees the basis.
3. **Only target and actual available** → apply thresholds:
   ≥95% On Track · 80–94% At Risk · <80% Off Track
4. **Otherwise** → `[Insert Status]`.

If the client confirms status must always come from the source, delete
step 3. That is the only edit needed.

Never assign a status to a metric with no target — 850 seats against no
stated target is neither good nor bad.

**Check the metric's direction before dividing.** The thresholds above
assume higher is better. Many metrics are the reverse — days to value,
cost per seat, open tickets, churn, latency, defects, time to resolution.
For these, invert the ratio (target ÷ actual) before applying thresholds.

Time to first value of 21 days against a 14-day target is a 50% miss, not
150% attainment. Applying the ratio the wrong way round turns a serious
miss into On Track, which is the most damaging single error this skill can
make — it tells leadership the opposite of the truth.

If the direction is not obvious from the metric name, do not guess:
`[Insert Status]` and add the metric to Missing Inputs.

Use plain text markers (`On Track`, `At Risk`, `Off Track`). Add emoji
(🟢 🟡 🔴) only if the user's own request or template uses them, since
they do not always survive the paste into Docs.

## Preserve qualifiers

A hedge is part of the fact. Stripping it is the most common way a memo
becomes false while every individual word stays technically defensible.

| Source | Correct | Wrong |
|---|---|---|
| "potential $2M opportunity" | $2M (potential) | $2M |
| "close date potentially Q4" | Q4 (unconfirmed) | Closes Q4 |
| "customer seemed interested" | Customer expressed interest | Customer is committed |
| "roughly 850 seats" | ~850 seats | 850 seats |

## Conflicts, names, dates

Never silently pick between conflicting values. Report both, flag it, add
it to Missing Inputs:
> Seats: 850 (weekly tracker) / 870 (partner report) — conflict, please
> confirm.

Copy names, dates, and identifiers exactly. Do not correct spelling,
expand acronyms, normalize a company name to its legal form, or convert a
relative date ("Tuesday", "next quarter") into a specific one. An
unanchored relative date stays relative or becomes a placeholder.

## Pre-output checklist

1. Every number appears in the source or derives from supplied values.
2. Every comparison word has a baseline in the source.
3. Every date, name, and identifier matches the source exactly.
4. Every source qualifier is preserved.
5. Every status is stated, derived per the rules, or a placeholder — and
   for any derived status, the metric's direction was checked first.
6. The memo's own date is filled in; every other date is from the source
   or a placeholder.
7. No required section was dropped for lack of content.
8. Placeholders use the exact standard forms.
9. For External Partner: restrictions applied.
10. Closing block complete: Derived line, Missing Inputs matching the
    placeholders actually used, and the version footer.

---

# Part 4 — Placeholders and output

## Placeholder forms

Use these exact forms so users can find them quickly and compliance can be
checked automatically:

```
[Insert Metric: <metric name>]
[Insert Target: <metric name>]
[Insert Date: <what date>]
[Insert Owner]
[Insert Status]
[Insert Decision Required]
[Insert Next Step]
```

Keep the placeholder in the position the real value would occupy — inside
the table cell, on the header line, as the list item. Never drop a
required section because its content is missing.

## Closing block

Every memo ends with three elements in this order.

```
---
**Derived:** 85% attainment and the 150-seat gap were calculated from the
supplied target and actual. All other figures are as provided.

**Missing inputs** — supply these and I'll regenerate:
- Owner
- Pipeline target

_memo-writer v1.0_
```

**The Derived line** names every number in the memo that was calculated
rather than supplied, and states plainly that nothing else was. A reviewer
can then verify the whole memo by checking two things: that the derived
figures are correct arithmetic, and that every remaining figure appears in
the source. Without this line, verification means re-reading the entire
memo against the entire source.

If nothing was calculated: `**Derived:** none — all figures as provided.`

**Missing inputs** turns the placeholders into a request the user can act
on, which is what finishes the document in one more round trip. If nothing
is missing: `**Missing inputs** — none.`

**The version footer** identifies which version of the skill produced the
memo. This matters during the pilot: memos get pasted into Docs and
circulated, and when someone reports a problem three weeks later, the
footer is the only way to know whether the version they used is the
version running now. Keep it on every memo.

## Handling ambiguity

**No template named** — infer, then open with one line:
`Using the Executive 1-Pager template for a VP audience — tell me if you'd
prefer a different format.` Then produce the memo. Do not stop to ask; a
draft the user can react to beats a question.

**No audience named** — default to VP/SVP, note it on the same line.

**Unusable input** (`Target = ?`, a metric with no number, a leftover
placeholder) — treat as missing. Never guess at intent.

**Very thin input** — still produce the memo. A mostly-placeholder memo
shows the user exactly what the format needs, which beats a refusal.

**User asks for an unsupported claim** ("say adoption is up 20%" with no
baseline) — produce the memo without it and note it once, briefly, after:
> I left the adoption trend out — the source has this week's 850 seats but
> no prior-week figure to compare against. Send me last week's number and
> I'll add it.

One line. Do not argue at length or refuse the whole task.

## Output format

Markdown, ready to copy into Google Docs. Right-align numeric table
columns with `|---:|`.

No preamble, and nothing after the memo except the closing block described
above. The only permitted additions are the template inference line before
the memo, and — where they apply — the External Partner exclusion note or
the one-line explanation of a dropped unsupported claim. The user is
copying this straight into a document, and anything else must be manually
deleted.

For revisions, return the full revised memo, not a description of the
change.

---

# Part 5 — Worked example

**User:**
> exec update for VP. ABC 850 seats target 1000, enablement issue only 2
> of 4 trainers, pipeline 2.5m, customer meeting tuesday went well,
> leadership needs decide resources

**Output:**

```markdown
Using the Executive 1-Pager template for a VP audience — tell me if you'd
prefer a different format.

# ABC Partner — Executive Update

**Date:** 4 September 2026
**Owner:** [Insert Owner]
**Audience:** VP/SVP
**Status:** At Risk

## 1. Executive Summary

- Deployment stands at 850 of 1,000 target seats (85% attainment).
- The constraint is enablement capacity: two of four trainers are
  allocated.
- Leadership decision required on additional enablement resources.

## 2. Program Performance & Metrics

| Metric | Target | Actual | Status |
|---|---:|---:|---|
| Seats | 1,000 | 850 | At Risk |
| Pipeline | [Insert Target: pipeline] | $2.5M | [Insert Status] |

## 3. Key Risks

- Enablement capacity at half of plan constrains the remaining 150-seat
  deployment.

## 4. Key Decision Requested / Next Steps

1. Approve additional enablement resources.
2. [Insert Next Step]

---
**Derived:** 85% attainment and the 150-seat gap were calculated from the
supplied target and actual. All other figures are as provided.

**Missing inputs** — supply these and I'll regenerate:
- Memo owner
- Pipeline target
- Timeline for the resourcing decision

_memo-writer v1.0_
```

What happened there:

- **The memo date was filled in** — it is the day the memo was written,
  not a source fact. The owner stayed a placeholder because it is.
- **85% attainment** was calculated from two supplied values, and the
  Derived line says so.
- **At Risk** came from the threshold. Seats is a higher-is-better metric,
  so the ratio applies directly. Pipeline got `[Insert Status]` because it
  has no target.
- **"customer meeting tuesday"** was dropped from the VP version — no
  decision-relevant consequence, and "Tuesday" has no anchor date. It
  would appear in an Operational memo.
- No invented owner, close date, or pipeline target anywhere.
