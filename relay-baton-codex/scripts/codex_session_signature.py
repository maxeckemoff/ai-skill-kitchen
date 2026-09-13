#!/usr/bin/env python3
"""FULL ThreadOps signature from native Codex records, never imported Claude usage.

Read-only. A response_id is counted once across rollout segments. Per-response
usage is summed; turn/thread cumulative counters are only coverage checks.
Input includes its cache subsets and output includes reasoning: neither is added
twice. Dollar figures are explicitly Standard API benchmarks, not account spend.
"""
import argparse
from collections import Counter
import datetime as dt
import json
import os
from pathlib import Path
import sqlite3
import sys
from zoneinfo import ZoneInfo

FIELDS = ('input_tokens', 'cached_input_tokens', 'cache_write_input_tokens',
          'output_tokens', 'reasoning_output_tokens', 'total_tokens')
RATE_VERSION = 'OpenAI-2026-09-08'
RATE_SOURCE = 'https://developers.openai.com/api/docs/models/gpt-6-astra'
CACHE_SOURCE = 'https://help.openai.com/en/articles/11481834'
# Standard USD / million; >272k input doubles input/cache and multiplies output 1.5x.
RATES = {'gpt-6-astra': (10, 1, 12.5, 50)}
EASTERN = ZoneInfo('America/New_York')


def abbrev(n):
    if n is None:
        return 'unavailable'
    if abs(n) < 1000:
        return str(n)
    return f'{n / 1e6:.2f}M' if abs(n) >= 1e6 else f'{n / 1000:.1f}k'


def stamp(value=None, fmt='%Y-%m-%d %H:%M %Z'):
    value = dt.datetime.fromisoformat(value.replace('Z', '+00:00')) if value else dt.datetime.now(dt.timezone.utc)
    return value.astimezone(EASTERN).strftime(fmt)


def instant(value):
    return dt.datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(dt.timezone.utc)


def benchmark(usage, model):
    if model not in RATES or any(usage.get(k) is None for k in FIELDS[:4]):
        return None
    inp, cr, cw, out = (usage[k] for k in FIELDS[:4])
    fresh = inp - cr - cw
    if min(fresh, cr, cw, out) < 0:
        return None
    ri, rr, rw, ro = RATES[model]
    long = inp > 272000
    return ((fresh * ri + cr * rr + cw * rw) * (2 if long else 1)
            + out * ro * (1.5 if long else 1)) / 1e6


def summed(records):
    return {k: sum(r['usage'][k] for r in records)
            if records and all(r['usage'].get(k) is not None for r in records) else None
            for k in FIELDS}


def dollars(records):
    vals = [benchmark(r['usage'], r['model']) for r in records]
    return None if not vals or any(v is None for v in vals) else sum(vals)


def money(n):
    return 'unavailable' if n is None else f'${n:,.2f}'


def tokens(u):
    # Codex's charging categories are uncached input, cached input, output.
    # Cache creation processing is included in full-rate noncached input.
    # The native write field does not establish actual cache creation volume.
    inp, cached = u.get('input_tokens'), u.get('cached_input_tokens')
    noncache = inp - cached if inp is not None and cached is not None else None
    return (f'in(noncache) {abbrev(noncache)} · cache-write unmeasured*'
            f' · cache-read {abbrev(u.get("cached_input_tokens"))} · out {abbrev(u.get("output_tokens"))}')


def analyse(rows, session):
    starts, models, tools, calls, seen_responses, records = {}, {}, Counter(), set(), {}, []
    compactions, malformed, missing_ids, duplicates, conflicts = set(), 0, 0, 0, 0
    active, runtime, context, context_at, newest_model, newest_effort = None, None, None, None, None, None
    latest_counter = None
    for r in rows:
        p = r.get('payload') or {}
        typ, when = r.get('type'), r.get('timestamp')
        if typ == 'event_msg' and p.get('type') == 'task_started':
            active = p.get('turn_id')
            if active and not active.startswith('external-import-'):
                starts.setdefault(active, {'id': active, 'at': when, 'tools': Counter()})
                runtime = p.get('model_context_window') or runtime
            continue
        if typ == 'turn_context':
            tid = p.get('turn_id') or active
            models[tid] = p.get('model')
            newest_model, newest_effort = p.get('model'), p.get('effort')
        if typ == 'event_msg' and p.get('type') == 'thread_settings_applied':
            settings = p.get('thread_settings') or p
            newest_model = settings.get('model') or newest_model
            newest_effort = settings.get('reasoning_effort') or newest_effort
            if active in starts and newest_model:
                models.setdefault(active, newest_model)
        if typ == 'event_msg' and p.get('type') == 'token_count' and p.get('info'):
            info = p['info']
            runtime = info.get('model_context_window') or runtime
            # The last request is a snapshot, lifetime usage is not context size.
            context = (info.get('last_token_usage') or {}).get('total_tokens')
            context_at = when
        if typ == 'compacted':
            compactions.add(p.get('window_id') or p.get('compaction_response_id') or when)
            # Do not count replacement_history or latest_token_usage_record again.
        if typ == 'response_item' and active in starts and p.get('type') in ('function_call', 'custom_tool_call'):
            cid = p.get('call_id') or p.get('id')
            if cid and cid in calls:
                continue
            if cid:
                calls.add(cid)
            name = p.get('name') or 'unnamed tool'
            tools[name] += 1
            starts[active]['tools'][name] += 1
        if typ != 'token_usage_record' or p.get('thread_id') != session:
            continue
        rid, tid, u = p.get('response_id'), p.get('turn_id'), p.get('usage') or {}
        if tid and tid.startswith('external-import-'):
            continue
        if rid in seen_responses and rid is not None:
            duplicates += 1
            if seen_responses[rid] != u:
                conflicts += 1
            continue
        if rid:
            seen_responses[rid] = u
        else:
            missing_ids += 1  # Retain unidentifiable records; do not collapse them.
        if not u:
            malformed += 1
            continue
        starts.setdefault(tid, {'id': tid, 'at': when, 'tools': Counter()})
        records.append({'id': rid, 'turn': tid, 'at': when, 'usage': u, 'model': models.get(tid) or newest_model})
        latest_counter = p.get('thread_token_usage') or latest_counter
    for record in records:
        record['model'] = record['model'] or models.get(record['turn'])
    groups = list(starts.values())
    for g in groups:
        g['records'] = [r for r in records if r['turn'] == g['id']]
        g['usage'], g['benchmark'] = summed(g['records']), dollars(g['records'])
    groups.sort(key=lambda g: g['at'] or '')
    return dict(session=session, groups=groups, records=records, totals=summed(records),
                benchmark=None if conflicts else dollars(records), tools=dict(tools), compactions=len(compactions),
                runtime_window=runtime, context=context, context_at=context_at,
                model=newest_model, effort=newest_effort, duplicates=duplicates,
                rates_version=RATE_VERSION, rates_source=RATE_SOURCE,
                cache_write_billing='included_in_full_rate_noncache_codex_credits', cache_write_source=CACHE_SOURCE,
                conflicting_duplicates=conflicts, missing_ids=missing_ids,
                malformed=malformed, latest_thread_counter=latest_counter)


def load_rows(paths):
    rows = []
    for path in paths:
        with path.open(encoding='utf-8') as f:
            for line in f:
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue  # A live writer can leave its final line incomplete.
                # Avoid retaining huge imported messages and replacement histories.
                typ, p = r.get('type'), r.get('payload') or {}
                if typ == 'compacted':
                    r['payload'] = {k: p.get(k) for k in ('window_id', 'compaction_response_id')}
                elif typ == 'response_item':
                    if p.get('type') not in ('function_call', 'custom_tool_call'):
                        continue
                    r['payload'] = {k: p.get(k) for k in ('type', 'call_id', 'id', 'name')}
                elif typ not in ('event_msg', 'turn_context', 'token_usage_record'):
                    continue
                if typ == 'event_msg' and p.get('type') not in ('task_started', 'token_count', 'thread_settings_applied'):
                    continue
                rows.append(r)
    rows.sort(key=lambda r: (r.get('timestamp') or '', r.get('ordinal') or 0))
    return rows


def plan_line(snapshot):
    if not snapshot or snapshot.get('error'):
        return 'plan      5h unavailable · 7d unavailable · extra usage USD unavailable · plan unavailable'
    b = snapshot.get('buckets', {}).get('codex', {})
    windows = {w['windowDurationMins']: w.get('usedPercent')
               for w in [b.get('primary'), b.get('secondary')] if w and 'windowDurationMins' in w}
    fmt = lambda n: 'unavailable' if n is None else f'{n:g}% used'
    credit = (b.get('credits') or {}).get('balance')
    return (f'plan      5h {fmt(windows.get(300))} · 7d {fmt(windows.get(10080))}'
            f' · extra usage USD unavailable · ChatGPT {snapshot.get("account", {}).get("plan", "unavailable")}'
            f' · credits {credit if credit is not None else "unavailable"} provider units'
            f' · observed {stamp(snapshot["observed_at"], "%m-%d %H:%M %Z")}')


def render(data, seat, snapshot=None, condensed=False, full_history=False, history_now=None):
    d, u = data, data['totals']
    pct = f'{100*d["context"]/d["runtime_window"]:.1f}%' if d['context'] is not None and d['runtime_window'] else 'unavailable'
    head = (f'{seat} · {d["session"]} · {pct} capacity · turn {len(d["records"])}'
            f' · {d["compactions"]} compactions · {len(d["groups"])} native prompt runs')
    if condensed:
        return head + f' · {abbrev(u["input_tokens"])} input · {money(d["benchmark"])} API-equiv · {stamp()}'
    lines = [head]
    if d['groups']:
        last = d['groups'][-1]
        lines.append(f'last      p{len(d["groups"])} · {stamp(last["at"], "%m-%d %H:%M")} · {len(last["records"])} model calls · {tokens(last["usage"])} · {money(last["benchmark"])}')
    else:
        lines.append('last      no native prompt usage recorded')
    lines.append('cumulat.  ' + tokens(u))
    hit = f'{100*u["cached_input_tokens"]/u["input_tokens"]:.1f}%' if u.get('input_tokens') and u.get('cached_input_tokens') is not None else 'unavailable'
    context_stamp = stamp(d['context_at'], '%m-%d %H:%M:%S %Z') if d['context_at'] else 'unavailable'
    lines.append(f'context   last-request {abbrev(d["context"])} · window {abbrev(d["runtime_window"])} · fill {pct} · cache hit {hit} · as of {context_stamp}')
    lines.append(plan_line(snapshot))
    lines.append(f'benchmark {money(d["benchmark"])} reported-token Standard API-equiv · {pct} capacity · rates {RATE_VERSION} · live TTL unobserved · {d["model"]} / {d["effort"]}')
    lines.append('tools     ' + (' · '.join(f'{k} {v}' for k, v in sorted(d['tools'].items(), key=lambda x: -x[1])) or 'no native tool calls recorded'))
    history_label = 'full-history override' if full_history else 'default last 24h intersect newest 20'
    lines.append(f'prompts   {history_label}; native runs include aborted runs; model calls, not tool calls')
    lines.append('For all prompt rows on your next reply, say: relay-baton-codex full-history.')
    lines.append('  p#   date  time   calls   noncache       cw*        cr       out    API-equiv  heaviest model call')
    numbered = list(enumerate(d['groups'], 1))
    if not full_history:
        numbered = numbered[-20:]
        history_now = (history_now or dt.datetime.now(dt.timezone.utc)).astimezone(dt.timezone.utc)
        cutoff = history_now - dt.timedelta(hours=24)
        numbered = [(n, g) for n, g in numbered if g.get('at') and instant(g['at']) >= cutoff]
    for n, g in reversed(numbered):
        gu = g['usage']; vals = [gu.get(k) for k in FIELDS[:2]]
        fresh = vals[0]-vals[1] if all(x is not None for x in vals) else None
        h = max(g['records'], key=lambda r: r['usage'].get('total_tokens') or 0, default=None)
        label = (f'{stamp(h["at"], "%H:%M:%S")} {h["id"][-8:] if h["id"] else "no-id"} {abbrev(h["usage"].get("total_tokens"))} tokens' if h else 'usage unavailable')
        lines.append(f'  p{n:<3} {stamp(g["at"], "%m-%d %H:%M")} {len(g["records"]):>5} {abbrev(fresh):>10} {"unmeas.":>9} {abbrev(gu.get("cached_input_tokens")):>9} {abbrev(gu.get("output_tokens")):>9} {money(g["benchmark"]):>12}  {label}')
    caveats = ["Codex records only; imported Claude turns excluded; turn = unique recorded model responses",
               "current run provisional through the last persisted response; this final answer is not yet included",
               "context is the latest token_count request snapshot, not cumulative tokens",
               f'reasoning {abbrev(u.get("reasoning_output_tokens"))} is included in output; cached input is included in input',
               f'*cw: native field reports {abbrev(u.get("cache_write_input_tokens"))} tokens; actual cache creation volume is not established; full-rate noncache=input minus cache-read already includes any cache creation without an extra write surcharge; reused cache-read is 0.1x; not every noncached input token necessarily becomes cached',
               "reported-token API benchmark is not Codex spend/credits; API write billing and long-input pricing differ; excludes unreported cache creation and Fast/tool charges; actual billed extra usage unavailable",
               f'{d["duplicates"]} replayed response records removed; {d["conflicting_duplicates"]} conflicting; {d["missing_ids"]} unidentifiable retained']
    counter = d.get('latest_thread_counter') or {}
    if counter.get('total_tokens') is not None and counter['total_tokens'] != u.get('total_tokens'):
        caveats.append(f'coverage gap: provider cumulative {counter["total_tokens"]:,} vs observed unique {u.get("total_tokens")}; displayed sums cover observed records only')
    lines.append('caveats   ' + ' · '.join(caveats))
    lines.append(stamp())
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', default=os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_SESSION_ID'))
    parser.add_argument('--seat', required=True)
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex'))))
    parser.add_argument('--snapshot', type=Path, default=Path.home()/'.threadops/usage/CODEX_USAGE_SNAPSHOT.json')
    parser.add_argument('--condensed', action='store_true')
    parser.add_argument('--full-history', action='store_true',
                        help='show all prompt rows for this invocation only')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if not args.session:
        parser.error('Pass --session with the actual Codex task ID')
    paths = list((args.codex_home/'sessions').rglob(f'*{args.session}*.jsonl'))
    db = args.codex_home/'state_5.sqlite'
    if db.exists():
        with sqlite3.connect(db.as_uri()+'?mode=ro', uri=True) as conn:
            row = conn.execute('select rollout_path from threads where id=?', (args.session,)).fetchone()
        if row and Path(row[0]).exists() and not any(Path(row[0]).samefile(p) for p in paths):
            paths.append(Path(row[0]))
    if not paths:
        parser.error('No native Codex rollout found for this task')
    d = analyse(load_rows(paths), args.session)
    snapshot = json.loads(args.snapshot.read_text(encoding='utf-8')) if args.snapshot.exists() else None
    output = (json.dumps(d, indent=2) if args.json
              else render(d, args.seat, snapshot, args.condensed, args.full_history))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output+'\n', encoding='utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(output)


if __name__ == '__main__':
    main()
