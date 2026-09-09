"""Hand-computed controls, including replay, cache subsets and context denominator."""
import unittest
from codex_session_signature import analyse, benchmark, load_rows, plan_line, render


def event(t, **kw):
    return {'timestamp': '2026-09-08T12:00:00Z', 'type': t, 'payload': kw}


def usage(rid, input=100, cached=60, write=10, output=20, turn='t1'):
    return event('token_usage_record', thread_id='s', turn_id=turn, response_id=rid,
                 usage=dict(input_tokens=input, cached_input_tokens=cached,
                            cache_write_input_tokens=write, output_tokens=output,
                            reasoning_output_tokens=5, total_tokens=input+output))


def prefix():
    return [event('event_msg', type='task_started', turn_id='t1', model_context_window=1000),
            event('turn_context', turn_id='t1', model='gpt-6-astra', effort='medium')]


class SignatureTests(unittest.TestCase):
    def test_codex_cache_write_is_not_a_separate_charge_column(self):
        d=analyse(prefix()+[usage('a')],'s')
        rendered=render(d,'SEAT')
        # Input100 minus cached60 = uncached40, including the reported10 writes.
        self.assertIn('in(noncache) 40',rendered)
        self.assertIn('cache-write n/a*',rendered)
        self.assertIn('native field reports 10 tokens',rendered)
        self.assertIn('not proof that no cache entries were created',rendered)
        self.assertEqual(d['totals']['cache_write_input_tokens'],10)

    def test_settings_before_first_context_identify_compaction_model(self):
        settings=event('event_msg',type='thread_settings_applied',thread_settings={'model':'gpt-6-astra','reasoning_effort':'high'})
        d=analyse([settings,prefix()[0],usage('a')],'s')
        self.assertAlmostEqual(d['benchmark'],.001485)
        self.assertEqual(d['model'],'gpt-6-astra')

    def test_replay_once_and_independent_negative_control(self):
        d = analyse(prefix()+[usage('a'), usage('b'), usage('a')], 's')
        self.assertEqual(len(d['records']), 2)
        self.assertEqual(d['totals']['input_tokens'], 200)
        self.assertEqual(d['totals']['output_tokens'], 40)
        control = analyse(prefix()+[usage('a'), usage('b'), usage('c')], 's')
        self.assertEqual(control['totals']['output_tokens'], 60)
        self.assertNotEqual(control['totals']['output_tokens'], d['totals']['output_tokens'])

    def test_missing_ids_survive(self):
        d = analyse(prefix()+[usage(None), usage(None)], 's')
        self.assertEqual(d['totals']['output_tokens'], 40)
        self.assertEqual(d['missing_ids'], 2)

    def test_conflict_is_visible(self):
        d = analyse(prefix()+[usage('a'), usage('a', output=99)], 's')
        self.assertEqual(d['conflicting_duplicates'], 1)

    def test_cache_subsets_and_reasoning_not_added_twice(self):
        # 30*10 + 60*1 + 10*12.5 + 20*50 = $0.001485, not $0.002185.
        self.assertAlmostEqual(benchmark(usage('a')['payload']['usage'], 'gpt-6-astra'), .001485)

    def test_long_context_whole_request_multiplier(self):
        # fresh 200k*10*2 + cached100k*1*2 + output100*50*1.5 = $4.2075.
        u = usage('a', input=300000, cached=100000, write=0, output=100)['payload']['usage']
        self.assertAlmostEqual(benchmark(u, 'gpt-6-astra'), 4.2075)

    def test_unknown_rate_not_zero(self):
        self.assertIsNone(benchmark(usage('a')['payload']['usage'], 'unrecognized-model'))

    def test_no_usage_not_zero(self):
        d = analyse(prefix(), 's')
        self.assertIsNone(d['benchmark'])
        self.assertIsNone(d['totals']['input_tokens'])

    def test_imported_turns_and_nested_compaction_usage_excluded(self):
        d = analyse(prefix()+[usage('a'), usage('b',turn='external-import-turn-1'),
                    event('compacted',window_id='w1',latest_token_usage_record=usage('a')['payload']),
                    event('compacted',window_id='w1')], 's')
        self.assertEqual(d['totals']['input_tokens'], 100)
        self.assertEqual(d['compactions'], 1)

    def test_context_uses_request_and_runtime_not_lifetime(self):
        rows=prefix()+[usage('a'),event('event_msg',type='token_count',info={
            'last_token_usage':{'total_tokens':120},'total_token_usage':{'total_tokens':999999},
            'model_context_window':1000})]
        s=render(analyse(rows,'s'),'SEAT')
        self.assertIn('12.0% capacity',s)
        self.assertNotIn('999999',s)

    def test_cumulative_line_has_no_cost_and_prompt_rows_uncapped(self):
        rows=prefix()+[usage('a')]
        for n in range(2,22):
            rows += [event('event_msg',type='task_started',turn_id=f't{n}'),usage(str(n),turn=f't{n}')]
        s=render(analyse(rows,'s'),'SEAT')
        self.assertNotIn('$',next(x for x in s.splitlines() if x.startswith('cumulat.')))
        self.assertEqual(sum(x.startswith('  p') and not x.startswith('  p#') for x in s.splitlines()),21)

    def test_main_bucket_windows_only_and_credits_not_money(self):
        snap={'observed_at':'2026-09-08T12:00:00Z','account':{'plan':'pro'},'buckets':{
            'codex':{'primary':{'windowDurationMins':10080,'usedPercent':2},'credits':{'balance':'0'}},
            'spark':{'primary':{'windowDurationMins':300,'usedPercent':70}}}}
        s=plan_line(snap)
        self.assertIn('5h unavailable',s)
        self.assertIn('7d 2% used',s)
        self.assertIn('credits 0 provider units',s)
        self.assertNotIn('$0',s)


if __name__ == '__main__':
    unittest.main(verbosity=2)
