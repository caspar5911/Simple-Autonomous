"""Streamlit presentation. LangGraph and SQLite behavior lives in brain.py."""
import json
import streamlit as st
import brain

st.set_page_config(page_title='Big Tiny · Operations Brain', page_icon='🌿', layout='wide')


@st.cache_resource
def startup():
    brain.init()
    return True


startup()
SAMPLES = {
    'New maintenance task': 'Fictional training note — Cedar Grove cabin: the kitchen tap is dripping. Ask Maya to arrange a plumber visit by 2026-11-23.',
    'Follow-up to saved task': 'Fictional follow-up — Cedar Grove cabin: Maya has booked the plumber for the dripping kitchen tap. The visit is now scheduled for 2026-11-24. The repair is not yet complete.',
    'Ambiguous request': 'Fictional training note — Please mark the maintenance job as done. I cannot remember which cabin or which job it was.',
}

with st.sidebar:
    st.title('🌿 big tiny')
    st.caption('OPERATIONS BRAIN')
    st.divider()
    st.markdown('**Your local team**')
    st.markdown('**① Extraction**  \nFind the facts\n\n**② Coordinator**  \nConnect saved context\n\n**③ Reviewer**  \nCheck the proposal')
    st.divider()
    st.caption('One model. Three roles. You make the final call.')
    st.badge('Local workspace', icon=':material/lock:')
    with st.expander('Connection & framework'):
        st.caption('LangGraph orchestration · Streamlit dashboard · SQLite memory')
        st.code(brain.BASE, language=None)
        st.caption(f'Model: {brain.MODEL} · Timezone: {brain.TIMEZONE}')
        st.caption('Three bounded calls per note. No retries, simulated outputs, external tracing or automatic task changes.')

st.caption('WORKSPACE / OPERATIONS DESK')
st.title('Small notes. Clear next steps.')
st.write('Turn an operations update into a considered plan. Your agents connect the dots. You stay in control.')


@st.fragment(run_every='2s')
def workspace():
    s = brain.state()
    running = any(r['status'] == 'running' for r in s['runs'])
    metrics = st.columns(4)
    for col, label, value in zip(metrics,
                                 ['Saved tasks', 'Awaiting decision', 'Memory revision', 'Serving model'],
                                 [len(s['tasks']), sum(r['status'] in ('pending', 'blocked') for r in s['runs']), s['revision'], s['model']]):
        col.metric(label, value)
    left, right = st.columns([.85, 1.15], gap='large')
    with left:
        with st.container(border=True):
            st.subheader('01 · What needs attention?')
            st.caption('Paste a maintenance note or an operations update.')
            sample = st.selectbox('Fictional training examples', ['Write my own note', *SAMPLES], key='sample')
            if st.button('Use selected example', disabled=sample not in SAMPLES):
                st.session_state.note = SAMPLES[sample]
                st.rerun()
            note = st.text_area('Internal note', height=230, max_chars=12000,
                                placeholder='What happened? What needs doing? Add any owners, dates or context you have.', key='note')
            st.caption('Notes and agent outputs are stored locally when submitted. Notes are sent to the configured model endpoint. Only approval changes task memory.')
            if st.button('Send to your agents ↗', type='primary', width='stretch', disabled=running or not note.strip()):
                try:
                    st.session_state.selected_run = brain.create_run(note.strip())
                    st.rerun()
                except ValueError as exc:
                    st.error(str(exc))
            if running:
                st.info('The agents are working. You can follow their results alongside this note.')
    with right:
        with st.container(border=True):
            st.subheader('02 · Your agent workspace')
            st.caption('LangGraph routes the proposal, then an independent role reviews it.')
            if not s['runs']:
                st.info('Add a note to see facts, proposed task changes and the reviewer’s decision.')
                st.caption('TASK MEMORY CHANGES ONLY AFTER APPROVAL')
            else:
                ids = [r['id'] for r in s['runs']]
                selected = st.session_state.get('selected_run', ids[0])
                if selected not in ids:
                    selected = ids[0]
                choice = st.selectbox('Note history', ids, index=ids.index(selected),
                                      format_func=lambda value: next(f"{r['created_at']} · {r['status']} · {r['note'][:45]}" for r in s['runs'] if r['id'] == value))
                st.session_state.selected_run = choice
                run = next(r for r in s['runs'] if r['id'] == choice)
                st.caption(f"Status: {run['status']} · Based on memory revision {run['base_revision']}")
                cols = st.columns(3)
                stages = run['stages'] or [{'name': n, 'status': 'waiting'} for n in ('Extraction', 'Coordination', 'Review')]
                for col, stage in zip(cols, stages):
                    col.markdown('**' + stage['name'] + '**')
                    col.caption({'running':'⏳ Running','complete':'✓ Complete','failed':'✕ Failed','waiting':'○ Waiting'}[stage['status']])
                    if stage.get('route'):
                        col.caption('Route: ' + stage['route'])
                with st.expander('Original note'):
                    st.text(run['note'])
                if run['error']:
                    st.error(run['error'])
                    st.caption('No task changes were applied by this run. Correct the connection or note and submit again.')
                if run['extraction']:
                    with st.expander('Extraction results'):
                        st.text(run['extraction']['summary'])
                        for item in run['extraction']['items']:
                            st.text(item['fact'])
                            st.text('Evidence: ' + item['evidence'])
                if run['proposal']:
                    st.text(run['proposal']['summary'])
                    for action in run['proposal']['actions']:
                        with st.container(border=True):
                            st.badge(action['kind'].upper())
                            if action['kind'] == 'clarify':
                                st.text(action['question'])
                                st.caption('A question for you; this does not create a task.')
                            else:
                                task = action['task']
                                st.markdown('**Proposed task**')
                                st.text(task['title'])
                                st.caption(f"Owner: {task['owner'] or 'Unassigned'} · Due: {task['due_date'] or 'Not set'} · Status: {task['status']}")
                                st.text(task['details'])
                                if action['kind'] == 'update':
                                    old = next((t for t in s['tasks'] if t['id'] == action['task_id']), None)
                                    with st.expander(f"Current task #{action['task_id']}"):
                                        st.json(old)
                            st.text(action['reason'])
                            st.text('Evidence: ' + action['evidence'])
                    if not run['proposal']['actions']:
                        st.info('No task changes proposed.')
                if run['review']:
                    if run['review']['approved']:
                        st.success('Reviewer approved this proposal for your decision.')
                        st.text(run['review']['summary'])
                    else:
                        st.warning('Reviewer blocked this proposal.')
                        st.text(run['review']['summary'])
                        for issue in run['review']['issues']:
                            st.text('• ' + issue)
                if run['status'] in ('pending', 'blocked'):
                    stale = run['base_revision'] != s['revision']
                    if stale:
                        st.warning('Task memory changed after this proposal. Submit the note again before approval.')
                    clarify_only = bool(run['proposal']['actions']) and all(a['kind'] == 'clarify' for a in run['proposal']['actions'])
                    approve, reject = st.columns(2)
                    if approve.button('Acknowledge questions' if clarify_only else 'Approve proposal', type='primary',
                                      disabled=stale or run['status'] != 'pending', width='stretch'):
                        try:
                            brain.decide(run['id'], 'approve')
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                    if reject.button('Reject', width='stretch'):
                        try:
                            brain.decide(run['id'], 'reject')
                            st.rerun()
                        except ValueError as exc:
                            st.error(str(exc))
                    st.caption('Clarifications are recorded in history. Add their answers to a new note to continue.')
                elif run['status'] == 'approved':
                    st.info('Your approval was recorded. Proposed task changes and questions are saved in local history.')
                elif run['status'] == 'rejected':
                    st.info('Rejected by you. No task changes were applied.')
    st.divider()
    st.subheader('03 · Task memory')
    st.caption('Approved work, ready for the next conversation.')
    if s['tasks']:
        st.dataframe(s['tasks'], hide_index=True, width='stretch',
                     column_order=['id', 'title', 'owner', 'due_date', 'status', 'details', 'updated_at'])
    else:
        st.info('A clean slate. Approved tasks will appear here.')
    with st.expander('Decision history', expanded=bool(s['history'])):
        if not s['history']:
            st.caption('Your human decisions will build a traceable history here.')
        for event in s['history']:
            proposal = json.loads(event['payload'])
            st.markdown(f"**{event['action'].upper()}** · {event['created_at']}")
            st.text(proposal['summary'] if proposal else 'Proposal')
            for action in (proposal or {}).get('actions', []):
                if action['kind'] == 'clarify':
                    st.text('Question: ' + action['question'])
            with st.expander('Recorded proposal · ' + str(event['id'])):
                st.json(proposal)
    st.caption('Big Tiny · Local proof of concept · LangGraph + Streamlit + SQLite')


workspace()
