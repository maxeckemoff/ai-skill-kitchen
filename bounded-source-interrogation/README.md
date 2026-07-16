# bounded-source-interrogation

A Claude Cowork skill for reading or profiling a large external data source (a big Google Sheet, a wide export, a broad Zoho COQL pull) for its structure, size, and a sample, without loading it whole into context, so a session does not saturate and start auto-compacting.

## Why it exists

Eager ingestion of a large source is the fastest way to fill a context window and trigger compaction every turn (this is what happened to BI-YOUNITY). This skill is the prevention half of the context-saturation problem. The recovery half (bifurcate, author a lean successor) lives in `cowork-progressive-disclosure-helper` and `bridge-handoff-authoring`; this skill keeps a session from needing that rescue.

It is a standalone discipline for any data-touching lane, not only sessions near compaction.

## The four recipes

1. **gviz bounded read**: query the Google Visualization endpoint for headers, a small sample (`select * limit 20`), and a row count (`select count(A)`), without opening the sheet in context. With the caveats that gviz can serve a stale cache and can time out on big aggregate reads.
2. **Apps Script offload**: run a bound server-side script that writes a results tab and an errors tab, and read back only the run summary and the errors, never the rows. Reconcile the summary against expected counts; a material gap is a finding.
3. **Connector caps**: design around the hard limits, Zoho COQL `IN` caps at 100 (chunk it), the Drive MCP is inline-only with a per-call cap and base64 corruption risk (do not inline big files), and native Drive/Sheets pickers cannot be browser-driven (stage IDs manually).
4. **Durable state**: keep schema, counts, source IDs, and run summaries in the bridge and saved artifacts, so a saturated session can be replaced by a lean successor that rebuilds from those rather than re-reading the source.

## How it fits

- `bounded-source-interrogation` (this skill) reads big sources cheaply, the prevention half.
- `live-source-watch` is the companion that watches sources for change (also cheap, trigger-only).
- `cowork-progressive-disclosure-helper` + `bridge-handoff-authoring` are the recovery half when a session does saturate.

## Compatibility

Works in any Cowork session. The gviz recipe needs the sheet reachable by URL; the Apps Script recipe needs a bound script in the workbook (a one-time setup). No new MCP.

## License

MIT.
