"""Behavior tests for the portable direct-dispatch decision boundary."""

import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name('dispatch_policy.py')


def run_policy(*arguments):
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {}
    return result, payload


class DispatchPolicyTests(unittest.TestCase):
    def test_authorized_unique_existing_task_can_send(self):
        result, payload = run_policy(
            'decide', '--authorized', '--surface', 'codex',
            '--candidate-id', 'task-123', '--prior-state', 'NONE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'SEND')
        self.assertEqual(payload['task_id'], 'task-123')

    def test_unauthorized_request_stays_drafted(self):
        result, payload = run_policy(
            'decide', '--surface', 'codex',
            '--candidate-id', 'task-123', '--prior-state', 'DRAFTED')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'DRAFT')

    def test_ambiguous_recipient_requires_manual_resolution(self):
        result, payload = run_policy(
            'decide', '--authorized', '--surface', 'codex', '--candidate-id', 'task-123',
            '--candidate-id', 'task-456', '--prior-state', 'NONE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'MANUAL_FALLBACK')
        self.assertEqual(payload['reason'], 'ambiguous recipient')

    def test_definitive_send_failure_is_recorded_without_automatic_retry(self):
        result, payload = run_policy('outcome', '--result', 'failure')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['state'], 'FAILED')
        self.assertFalse(payload['automatic_retry'])

    def test_uncertain_outcome_blocks_duplicate_send(self):
        result, payload = run_policy('outcome', '--result', 'uncertain')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['state'], 'UNCERTAIN')
        self.assertFalse(payload['automatic_retry'])
        second, decision = run_policy(
            'decide', '--authorized', '--surface', 'codex', '--candidate-id', 'task-123',
            '--prior-state', 'UNCERTAIN')
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(decision['decision'], 'DO_NOT_SEND')

    def test_sent_or_delivered_baton_is_not_sent_again(self):
        for prior in ('SENT', 'DELIVERED'):
            with self.subTest(prior=prior):
                result, payload = run_policy(
                    'decide', '--authorized', '--surface', 'codex', '--candidate-id', 'task-123',
                    '--prior-state', prior)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(payload['decision'], 'DO_NOT_SEND')

    def test_claude_surfaces_prepare_manual_relay_and_never_send(self):
        for surface in ('claude-code', 'cowork'):
            with self.subTest(surface=surface):
                result, payload = run_policy(
                    'decide', '--authorized', '--surface', surface, '--prior-state', 'NONE')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(payload['decision'], 'PREPARE_MANUAL_RELAY')
                self.assertEqual(payload['state'], 'PREPARED_MANUAL')

    def test_imported_claude_history_does_not_prove_native_codex_recipient(self):
        result, payload = run_policy(
            'decide', '--authorized', '--surface', 'imported-claude-history',
            '--candidate-id', 'task-123', '--prior-state', 'NONE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'MANUAL_FALLBACK')
        self.assertEqual(payload['reason'], 'imported Claude history is not a native Codex recipient')

    def test_unknown_surface_uses_manual_fallback(self):
        result, payload = run_policy(
            'decide', '--authorized', '--surface', 'unknown',
            '--candidate-id', 'task-123', '--prior-state', 'NONE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'MANUAL_FALLBACK')
        self.assertEqual(payload['reason'], 'recipient surface is unknown')


if __name__ == '__main__':
    unittest.main(verbosity=2)
