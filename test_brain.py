import copy
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch
import brain

NOTE = 'Maya will arrange a plumber for Cedar Grove kitchen tap by 2026-11-23.'
TASK = {'title': 'Arrange plumber for Cedar Grove tap', 'owner': 'Maya', 'due_date': '2026-11-23', 'status': 'open', 'details': 'Kitchen tap needs a plumber.'}


def outputs(kind='create', task_id=None, approved=True):
    action = {'kind': kind, 'task_id': task_id, 'task': copy.deepcopy(TASK), 'question': None, 'reason': 'Explicit request.', 'evidence': NOTE}
    if kind == 'clarify':
        action.update(task=None, question='Which cabin?', task_id=None)
    return [{'summary': 'A maintenance request.', 'items': [{'fact': 'Plumber requested.', 'evidence': NOTE}]},
            {'summary': 'Proposed maintenance task.', 'actions': [action]},
            {'approved': approved, 'summary': 'Supported.' if approved else 'Ambiguous.', 'issues': [] if approved else ['Unclear task.']}]


class BrainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_db = brain.DB
        brain.DB = Path(self.temp.name) / 'test.sqlite3'
        brain.init()

    def tearDown(self):
        brain.DB = self.old_db
        self.temp.cleanup()

    def run_graph(self, values):
        with patch.object(brain, 'model_call', side_effect=values) as model:
            run_id = brain.create_run(NOTE)
            deadline = time.monotonic() + 10
            while brain.LOCK.locked() and time.monotonic() < deadline:
                time.sleep(.01)
            self.assertFalse(brain.LOCK.locked())
            run = next(r for r in brain.state()['runs'] if r['id'] == run_id)
            self.assertEqual(model.call_count, 3)
            return run

    def test_graph_requires_human_then_persists(self):
        run = self.run_graph(outputs())
        self.assertEqual(run['status'], 'pending')
        self.assertEqual(brain.state()['tasks'], [])
        brain.decide(run['id'], 'approve')
        self.assertEqual(brain.state()['tasks'][0]['title'], TASK['title'])
        with self.assertRaises(ValueError):
            brain.decide(run['id'], 'approve')
        brain.init()
        self.assertEqual(len(brain.state()['tasks']), 1)
        self.assertEqual(len(brain.state()['history']), 1)

    def test_stale_approval_does_not_overwrite_memory(self):
        first = self.run_graph(outputs())
        second = self.run_graph(outputs())
        brain.decide(first['id'], 'approve')
        with self.assertRaisesRegex(ValueError, 'changed'):
            brain.decide(second['id'], 'approve')
        self.assertEqual(len(brain.state()['tasks']), 1)

    def test_update_uses_saved_identity(self):
        first = self.run_graph(outputs())
        brain.decide(first['id'], 'approve')
        task_id = brain.state()['tasks'][0]['id']
        data = outputs('update', task_id)
        data[1]['actions'][0]['task']['status'] = 'in_progress'
        second = self.run_graph(data)
        brain.decide(second['id'], 'approve')
        self.assertEqual(len(brain.state()['tasks']), 1)
        self.assertEqual(brain.state()['tasks'][0]['status'], 'in_progress')

    def test_clarification_is_recorded_without_creating_task(self):
        run = self.run_graph(outputs('clarify'))
        self.assertEqual(run['stages'][1]['route'], 'clarify')
        brain.decide(run['id'], 'approve')
        self.assertEqual(brain.state()['tasks'], [])
        self.assertIn('Which cabin?', brain.state()['history'][0]['payload'])

    def test_reviewer_blocks_approval_and_rejection_changes_no_tasks(self):
        run = self.run_graph(outputs(approved=False))
        with self.assertRaisesRegex(ValueError, 'blocked'):
            brain.decide(run['id'], 'approve')
        brain.decide(run['id'], 'reject')
        self.assertEqual(brain.state()['tasks'], [])

    def test_bad_evidence_fails_closed_without_retry(self):
        data = outputs()[0]
        data['items'][0]['evidence'] = 'Invented quote'
        with patch.object(brain, 'model_call', return_value=data) as model:
            run_id = brain.create_run(NOTE)
            deadline = time.monotonic() + 10
            while brain.LOCK.locked() and time.monotonic() < deadline:
                time.sleep(.01)
            run = next(r for r in brain.state()['runs'] if r['id'] == run_id)
            self.assertEqual(run['status'], 'failed')
            self.assertEqual(model.call_count, 1)
            self.assertEqual(brain.state()['tasks'], [])

    def test_invalid_update_and_fabricated_date_rejected(self):
        data = outputs('update', 999)[1]
        with self.assertRaises(ValueError):
            brain.validate_proposal(data, [], NOTE)
        data = outputs()[1]
        data['actions'][0]['task']['due_date'] = '2026-02-30'
        with self.assertRaises(ValueError):
            brain.validate_proposal(data, [], NOTE)

    def test_streamlit_initial_render(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(brain.ROOT / 'app.py')).run(timeout=15)
        self.assertEqual(len(app.exception), 0)
        self.assertIn('Small notes. Clear next steps.', [t.value for t in app.title])

    def test_streamlit_examples_and_approval(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(brain.ROOT / 'app.py')).run(timeout=15)
        for example in ('New maintenance task', 'Follow-up to saved task', 'Ambiguous request'):
            app.selectbox[0].select(example).run()
            next(b for b in app.button if b.label == 'Use selected example').click().run()
            self.assertEqual(len(app.exception), 0)
            self.assertTrue(app.text_area[0].value.startswith('Fictional'))
        app.text_area[0].set_value(NOTE).run()
        with patch.object(brain, 'model_call', side_effect=outputs()):
            next(b for b in app.button if b.label == 'Send to your agents ↗').click().run()
            deadline = time.monotonic() + 10
            while brain.LOCK.locked() and time.monotonic() < deadline:
                time.sleep(.01)
            app.run()
        self.assertEqual(len(app.exception), 0)
        next(b for b in app.button if b.label == 'Approve proposal').click().run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(len(brain.state()['tasks']), 1)


if __name__ == '__main__':
    unittest.main()
