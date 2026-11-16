# Management presentation: Big Tiny Operations Brain

[Watch or download the narrated presentation](https://github.com/caspar5911/Simple-Autonomous/raw/refs/heads/main/docs/executive-demo.mp4)

Duration: 05:53. Size: 11.9 MB. Format: 1920 x 1080 H.264 video with AAC narration. [Optional subtitles](executive-demo.srt).

A management-oriented presentation of the opportunity, current architecture, actual end-to-end demo, proposed pilot and decision request. Recorded on 2026-11-16.

## Recording notes

- Female synthetic neural narration: Microsoft en-SG-LunaNeural, Singapore English, at a slightly relaxed pace. Speech was generated through the Edge online speech service using edge-tts; only the presentation script was submitted. This is a media-production tool, not an application dependency.
- The walkthrough uses fictional notes, a separate temporary database and nine real GX10 calls through the configured Tailscale endpoint. It was recorded again for this presentation. No business-system writes, messages, purchases or model-serving changes were made.
- The final demo state was checked: one task with the revised date, still unfinished, and three approval records.
- Proposed productivity benefits and the 25% staff-time target are hypotheses and pilot criteria, not measured outcomes. No production rollout is claimed.
- Narration is aligned by scene; model processing runs in real time. Subtitles are paragraph-level cues aligned to each narration segment.

## Chapters and narration

### 00:00 - The opportunity

Meet the Big Tiny Operations Brain. This proof of concept explores a simple idea: spend less time organising updates, and make the next action easier to see.

### 00:14 - The problem to validate

For a property operations team, the challenge is often turning scattered updates into a reliable handover. Which issue is still open? Who owns the next step? Has a follow up changed the plan? Our hypothesis is that preparing and checking this information is a useful place to reduce administrative effort.

### 00:38 - Proposed business value

The proposed value is straightforward: clearer handovers, fewer duplicate tasks, and less time chasing context. The current proof of concept demonstrates the workflow. It does not yet prove a productivity gain. That is what a focused pilot should establish.

### 00:59 - Architecture

Here is how it works. Streamlit provides the workspace. LangGraph coordinates three specialist roles. They use the same on premises G X ten model through Tailscale. SQLite remembers approved tasks, so each new update has context.

### 01:22 - Live application

This is the working application. We will use fictional maintenance notes and real model responses. Notes are stored when submitted, but task changes always wait for a person to approve.

### 01:36 - Create a maintenance task

First, a staff member reports a dripping tap at Cedar Grove cabin. Maya needs to arrange a plumber. The note also includes a deadline.

### 01:49 - Agent workflow

The extractor finds the facts. The coordinator checks saved tasks and proposes what should happen next. The reviewer checks that the proposal is supported by the note.

### 02:02 - Human review

Here is the proposed task, with an owner, a due date, and the original evidence. The reviewer has passed it, but the final decision is still yours. Let us approve it.

### 02:18 - Saved memory

The first task is now saved in local memory. This is what allows the brain to connect future updates to the same issue.

### 02:27 - A follow-up update

Now there is a follow up. Maya has booked the plumber, and the visit is scheduled for November twenty fourth. The repair is not yet complete.

### 02:39 - Match existing work

This time, the coordinator receives the existing task as context. It can propose an update to the same record instead of creating another task.

### 02:51 - Approve the update

The proposed change keeps the same task identity and revises the visit date. After approval, there is still one task, and it remains in progress.

### 03:07 - An ambiguous request

Finally, someone asks to mark the maintenance job complete, but cannot say which cabin or which job. This is where guessing would be a problem.

### 03:18 - Check before changing

The workflow checks the request against what it knows. An unclear completion request should become a question, not an unsupported change to a property record.

### 03:30 - Clarification

The result is a clarification. We can acknowledge the question and provide more detail later. The existing task stays unfinished.

### 03:45 - Current scope and future options

Today, the system can propose new tasks, update remembered tasks, and ask for clarification. It does not connect to booking systems, contact vendors, or make purchases. Property readiness checks, procedure lookup, and weekly reporting are possible next steps, if staff evidence supports them.

### 04:09 - Recommended pilot

Our recommendation is a small pilot for daily handovers and maintenance follow ups. Name an operations owner, select a representative property group, and evaluate approved examples with staff. Keep the current operational register authoritative. Compare this workflow with the manual process and a simpler single prompt.

### 04:34 - Success measures

Measure net staff time, including checking and corrections. Also measure missed actions, wrong task matches, and unsupported changes. A proposed initial target is a twenty five percent reduction in median active staff time, with no critical incorrect changes accepted. These are pilot targets, not achieved results.

### 05:00 - Decision request

The decision requested is approval to run a bounded discovery and pilot, with an owner, authorised examples, and agreed success measures. If the evidence is strong, extend one workflow at a time. If it is not, revise or stop. Start small, keep people in control, and let measured results guide the investment.

## Supporting material

- [Architecture diagrams](architecture.md)
- [Discovery and pilot proposal](discovery-proposal.md)
- [Brainstorming workshop](brainstorm-workshop.md)
- [Application setup](../README.md)
