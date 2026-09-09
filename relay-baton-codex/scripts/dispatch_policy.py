#!/usr/bin/env python3
"""Classify a Codex baton dispatch before and after the native tool call."""

from __future__ import annotations

import argparse
import json


BLOCKING_PRIOR_STATES = {'SENT', 'DELIVERED', 'UNCERTAIN'}


def decide(authorized: bool, surface: str, candidate_ids: list[str], prior_state: str) -> dict:
    prior_state = prior_state.upper()
    if prior_state in BLOCKING_PRIOR_STATES:
        return {
            'decision': 'DO_NOT_SEND',
            'reason': f'prior state {prior_state} blocks duplicate dispatch',
        }
    if surface in {'claude-code', 'cowork'}:
        return {
            'decision': 'PREPARE_MANUAL_RELAY',
            'state': 'PREPARED_MANUAL',
            'reason': f'native Codex task transport does not address {surface}',
        }
    if surface == 'imported-claude-history':
        return {
            'decision': 'MANUAL_FALLBACK',
            'reason': 'imported Claude history is not a native Codex recipient',
        }
    if surface != 'codex':
        return {'decision': 'MANUAL_FALLBACK', 'reason': 'recipient surface is unknown'}
    if not authorized:
        return {'decision': 'DRAFT', 'reason': 'direct dispatch is not authorized'}
    if not candidate_ids:
        return {'decision': 'MANUAL_FALLBACK', 'reason': 'recipient not found'}
    if len(candidate_ids) > 1:
        return {'decision': 'MANUAL_FALLBACK', 'reason': 'ambiguous recipient'}
    if prior_state == 'FAILED':
        return {
            'decision': 'MANUAL_FALLBACK',
            'reason': 'prior definitive failure requires review before another attempt',
        }
    return {'decision': 'SEND', 'task_id': candidate_ids[0], 'reason': 'authorized unique recipient'}


def outcome(result: str) -> dict:
    states = {'success': 'SENT', 'failure': 'FAILED', 'uncertain': 'UNCERTAIN'}
    return {'state': states[result], 'automatic_retry': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)

    before = commands.add_parser('decide')
    before.add_argument('--authorized', action='store_true')
    before.add_argument(
        '--surface', required=True,
        choices=['codex', 'claude-code', 'cowork', 'imported-claude-history', 'unknown'],
    )
    before.add_argument('--candidate-id', action='append', default=[])
    before.add_argument(
        '--prior-state',
        default='NONE',
        choices=['NONE', 'DRAFTED', 'EMITTED', 'SENT', 'DELIVERED', 'FAILED', 'UNCERTAIN'],
    )

    after = commands.add_parser('outcome')
    after.add_argument('--result', required=True, choices=['success', 'failure', 'uncertain'])
    args = parser.parse_args()

    payload = (decide(args.authorized, args.surface, args.candidate_id, args.prior_state)
               if args.command == 'decide' else outcome(args.result))
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
