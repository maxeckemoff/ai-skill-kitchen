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
            'decide', '--authorized', '--candidate-id', 'task-123', '--prior-state', 'NONE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'SEND')
        self.assertEqual(payload['task_id'], 'task-123')

    def test_unauthorized_request_stays_drafted(self):
        result, payload = run_policy(
            'decide', '--candidate-id', 'task-123', '--prior-state', 'DRAFTED')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(payload['decision'], 'DRAFT')

    def test_ambiguous_recipient_requires_manual_resolution(self):
        result, payload = run_policy(
            'decide', '--authorized', '--candidate-id', 'task-123',
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
            'decide', '--authorized', '--candidate-id', 'task-123',
            '--prior-state', 'UNCERTAIN')
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(decision['decision'], 'DO_NOT_SEND')

    def test_sent_or_delivered_baton_is_not_sent_again(self):
        for prior in ('SENT', 'DELIVERED'):
            with self.subTest(prior=prior):
                result, payload = run_policy(
                    'decide', '--authorized', '--candidate-id', 'task-123',
                    '--prior-state', prior)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(payload['decision'], 'DO_NOT_SEND')


if __name__ == '__main__':
    unittest.main(verbosity=2)
