---
name: bounded-source-interrogation
description: "Reads or profiles a large external data source (Google Sheet, CSV or Excel export, Zoho COQL pull, big Doc) for structure, row counts, and small samples WITHOUT loading it whole into context, to prevent context saturation and auto-compaction. Use when a session must inspect a big sheet, workbook, or export, is about to ingest a large source, or is at risk of compaction. Covers the Google Sheets gviz bounded-range plus count-query read (headers, counts, a small sample), server-side Apps Script offload that returns only a run summary and an errors tab rather than the rows, and the connector caps that shape any large pull (Zoho COQL IN capped at 100 values, the Drive MCP inline-only per-call cap with base64 corruption risk, native Drive and Sheets pickers not being browser-drivable). Also keeps durable state in the bridge and saved artifacts so a saturated session can be replaced without loss."
---

# Bounded source interrogation

Eager ingestion of a large source (a big Google Sheet, a wide export, a broad COQL pull) is the fastest way to saturate a session's context and trigger auto-compaction every turn. This skill is the prevention half: it interrogates a large source for its structure, its row counts, and a small sample, without ever loading it whole, and pushes heavy transforms to the server side so only summaries come back. The recovery half (when to bifurcate, how to author a lean successor) already lives in `cowork-progressive-disclosure-helper` and `bridge-handoff-authoring`; this skill keeps a session from needing that rescue in the first place.

It is a standalone discipline that applies to any data-touching lane (BI, Zoho CRM, FP&A, diligence), not only sessions near compaction.

## Core principle

Never read a large source into context to "see what's in it." Get three cheap things instead: the headers (structure), the row or record count (size), and a small sample (shape). Decide the real work from those, then do the work server-side or in bounded chunks and read back only results.

## Recipe 1: Google Sheets via the gviz endpoint (bounded range + count query)

The Google Visualization query endpoint returns JSON for a query without opening the sheet in context:

`https://docs.google.com/spreadsheets/d/SHEET_ID/gviz/tq?tqx=out:json&sheet=TAB_NAME&tq=QUERY`

- **Headers + sample**: `tq=select * limit 20` gives column labels and a 20-row shape. Enough to design against.
- **Row count**: `tq=select count(A)` (or count of a always-present column) gives size without pulling rows.
- **Targeted profile**: `tq=select A, count(B) group by A` and similar to profile a column cheaply.

Caveats learned live (BI-YOUNITY):
- gviz can serve a STALE cache; a read may lag the sheet's true state. Cross-check the sheet's own "Last Synced" / last-modified where one exists before trusting counts.
- gviz aggregate reads can TIME OUT on big sheets. If it times out, fall back to a saved export or the Apps Script path below rather than retrying a whole-sheet read.

## Recipe 2: server-side Apps Script offload (read back summaries, not rows)

For a heavy transform or consolidation, do not pull the rows into context and transform them here. Install a bound Apps Script in the workbook that does the transform server-side and writes two tabs: a results tab (for example `Consolidated_X`) and an `X_Errors` tab (columns like Cohort, Tab, Type, Message; types such as DUP, WARN, HEADER, DATE, CONFIG, SOURCE). Then read back ONLY:

- the run summary (row counts in, out, per-group), and
- the errors tab.

Never read the result rows into context. Reconcile the run summary against known/expected counts; a material gap is a real finding to surface, not to paper over. This is how a session processes a large dataset while keeping its own context small.

## Recipe 3: design around connector caps

Any large pull is shaped by hard caps; plan for them up front:

- **Zoho COQL `IN` caps at 100 values.** Chunk id lists into batches of 100 and page; never send a 500-id IN.
- **The Drive MCP is inline-only with a per-call size cap, and base64 inlining risks corruption on large files.** Do not pull a big file through the Drive MCP as inline base64. Prefer gviz (for Sheets), a server-side export, or staged file handling over inline base64 for anything large.
- **Native Drive and Sheets pickers cannot be browser-driven.** Do not try to automate the file picker; stage the file ID / path manually and pass it in.

## Recipe 4: keep durable state so a saturated session is replaceable

Treat the bridge and saved artifacts as the source of truth, not the session's context. Record schema decisions, counts, the source file IDs, the Apps Script location, and each run summary in the bridge or a saved file. Then if a session does saturate, its lean successor reconstructs state from the bridge and the saved files rather than re-reading the sources, which is exactly how BI-YOUNITY recovered. Durable state is what makes eager re-ingestion unnecessary after a warm transfer.

## When to reach for this

- Before reading any sheet, workbook, or export you have not sized (profile first).
- When a task says "read this big sheet and ..." (interrogate, then work server-side).
- When a session is doing repeated large reads and slowing down or nearing compaction.
- Any COQL / Drive / Sheets pull large enough to hit the caps in Recipe 3.

## Anti-patterns to avoid

- Do not read a large source whole to inspect it; profile with gviz count + bounded sample first.
- Do not pull big files through the Drive MCP as inline base64; use gviz, an export, or Apps Script.
- Do not trust a single gviz read for a load-bearing count; it may be a stale cache, cross-check last-modified.
- Do not send a COQL `IN` over 100 values; chunk it.
- Do not try to browser-drive a Drive or Sheets picker; stage IDs manually.
- Do not hold the dataset in context as your state; put durable state in the bridge and saved artifacts.
- Do not use em dashes or AI-tone phrasing in outputs.

## Test triggers

Examples that SHOULD fire this skill:

- "Read this Google Sheet (thousands of rows) and tell me what columns and how many rows it has."
- "I need to consolidate four big cohort sheets into one; how do I do it without blowing up context?"
- "Pull these 400 record IDs from Zoho COQL." (the IN-100 cap and chunking apply)

Examples that should NOT fire this skill:

- "Watch these three docs and tell me if any changed." (that is `live-source-watch`)
- "Read this short 20-row config sheet." (small source; no interrogation discipline needed)
- "Summarize this paragraph I pasted." (already in context, nothing large to interrogate)
