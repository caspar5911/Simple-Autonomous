"""Opt-in REAL GX10 test. Fictional notes only; isolated temporary SQLite database."""
import json
from pathlib import Path
import tempfile
import time
import brain

NOTES = [
    'Fictional training note — Cedar Grove cabin: the kitchen tap is dripping. Ask Maya to arrange a plumber visit by 2026-11-23.',
    'Fictional follow-up — Cedar Grove cabin: Maya has booked the plumber for the dripping kitchen tap. The visit is now scheduled for 2026-11-24. The repair is not yet complete.',
    'Fictional training note — Please mark the maintenance job as done. I cannot remember which cabin or which job it was.',
]


if __name__ == '__main__':
    with tempfile.TemporaryDirectory() as directory:
        brain.DB = Path(directory) / 'smoke.sqlite3'
        brain.init()
        for index, note in enumerate(NOTES):
            run_id = brain.create_run(note)
            deadline = time.monotonic() + 390
            while brain.LOCK.locked() and time.monotonic() < deadline:
                time.sleep(.5)
            if brain.LOCK.locked():
                raise RuntimeError('Smoke run exceeded bounded three-call processing budget')
            run = next(r for r in brain.state()['runs'] if r['id'] == run_id)
            print(json.dumps({'step': index + 1, 'status': run['status'], 'stages': run['stages'],
                              'proposal': run['proposal'], 'review': run['review'], 'error': run['error']}), flush=True)
            assert run['status'] == 'pending', run['error'] or run['review']
            assert all(stage['status'] == 'complete' for stage in run['stages'])
            assert len(brain.state()['tasks']) == (0 if index == 0 else 1)
            kinds = [a['kind'] for a in run['proposal']['actions']]
            assert ['create', 'update', 'clarify'][index] in kinds, kinds
            brain.decide(run_id, 'approve')
            assert len(brain.state()['tasks']) == 1
        print('PASS: real GX10 create → approval → saved-memory update → clarification; 9 model calls.', flush=True)
