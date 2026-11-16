# Company-wide opportunity catalogue

**Discussion draft for senior management and functional leaders · 2026-11-16.** These are candidate uses, not Big Tiny's confirmed departments, an approved roadmap or demonstrated benefits.

Big Tiny publicly describes modular accommodation and hospitality offerings. Its company page discusses property management and production facilities. These support exploring work across a property and accommodation lifecycle; they do not establish internal processes or systems. [Company website](https://www.bigtiny.com.sg/), [company information](https://www.bigtiny.com.sg/aboutbigtiny).

The ownership programme also describes tiny-house ownership alongside managed guest stays and maintenance. Owners and guests therefore represent distinct customer perspectives in this catalogue. No investment or financial-return claims are assessed here. [Ownership and managed stays](https://owntinyhouse.sg/).

We have not reviewed an organisation chart, internal systems, staff/customer datasets or operating baselines. Every benefit below is a **hypothesis**; every metric is a **proposed evaluation measure**, not a target already achieved. Some customer benefits are indirect.

## What exists versus what is proposed

**Implemented today:** paste one note; extract facts; propose task creation, updates or clarification; review; obtain human approval; retain local tasks/history. Three roles use the same on-prem model. Notes and run outputs persist before approval; only task mutations require approval. [Current architecture](architecture.md), [implementation](../README.md).

**Everything else below is hypothetical extension.** Saved task memory is not a connection to finance, booking, HR, factory or customer systems. Each proposed source integration needs an authorised owner, permissions, reliable identifiers, freshness checks and a pilot. Cloning the code creates separate local memory, not a shared company brain. Recommendations would need source citations; missing evidence must remain visible. No automatic cloud fallback is proposed.

## Commercial, financial and customer workflows

“Approval” identifies the accountable human decision; drafting permission does not authorise execution.

| Functional area | Candidate tool / output | Required authorised data | Staff benefit hypothesis | Customer benefit hypothesis | Human approval | Proposed metric |
| --- | --- | --- | --- | --- | --- | --- |
| 1. Finance: AP / AR | Invoice-match exceptions and collection follow-up draft | Invoices, orders, receipts, balances | Less document matching | Indirect: clearer billing | Finance checks postings, payments and collection sends | Review time; mismatch precision |
| 2. Finance planning | Cited variance brief and scenario assumptions | Approved budgets, actuals, definitions | Faster explanations | Indirect: better-informed service allocation | Finance validates numbers; management approves budgets | Reconciliation errors; preparation time |
| 3. Tiny-house / B2B sales | Requirements summary and proposal checklist | Approved specifications, prices, enquiry | Less proposal assembly | Clearer scope and expectations | Sales approves prices, terms and send | Revision count; missing requirements |
| 4. Marketing | Campaign brief and claim-checked content draft | Brand guide, verified facts, consented assets | Faster first draft | More accurate information | Marketing approves claims and publication | Review time; factual corrections |
| 5. Reservations / revenue | Booking exceptions and demand-review brief | Availability, bookings, policies, approved rates | Less cross-checking | Fewer contradictory booking details | Authorised staff approve rate or booking changes | Exception accuracy; handling time |
| 6. Guest service | Sourced reply draft and escalation summary | Guest enquiry, relevant booking, current policies | Less repetitive writing | Clearer, more consistent answers | Staff approve sends, refunds and remedies | Correction rate; response preparation time |
| 7. Property operations | Daily handover and unresolved-action draft | Staff notes, task register, property IDs | Less status chasing | More reliable follow-through | Operations approves assignments and closures | Missed actions; handover review time |
| 8. Housekeeping | Turnover exception and supply checklist | Arrival/departure feed, cleaning records | Clearer priorities | Better-prepared accommodation | Supervisor confirms physical readiness | Missed checklist items; late escalations |
| 9. Maintenance | Repair follow-up and recurring-fault brief | Work orders, equipment IDs, service records | Less duplicate reporting | Fewer unresolved faults | Qualified staff approve diagnosis, dispatch and completion | Match accuracy; repeat reports |
| 10. Owner relations | Owner-update draft with evidence links | Authorised owner records, contracts, approved statements | Less information assembly | Clearer owner communication | Owner-relations and finance approve statements/send | Corrections; enquiry handling time |

## Delivery, support and management workflows

| Functional area | Candidate tool / output | Required authorised data | Staff benefit hypothesis | Customer benefit hypothesis | Human approval | Proposed metric |
| --- | --- | --- | --- | --- | --- | --- |
| 11. Procurement / inventory | Quote comparison and shortage exceptions | Quotes, stock, specifications, purchasing rules | Easier scope comparison | Indirect: fewer missing service materials | Buyer approves suppliers, orders and spend | Omitted exclusions; comparison time |
| 12. Engineering / design | Requirement-traceability and drawing-review checklist | Controlled drawings, specifications, applicable requirements | Easier revision checking | Clearer requirement coverage | Qualified professionals retain engineering sign-off | Missed requirements; review rework |
| 13. Manufacturing / quality | Defect summary and inspection evidence pack | Controlled BOMs, inspections, defect records | Less report consolidation | Better-documented quality checks | Quality lead approves release or rejection | Traceability completeness; report time |
| 14. Logistics / installation | Delivery dependency and site-handover draft | Shipment status, site checklist, installation plans | Earlier visibility of gaps | Clearer delivery expectations | Responsible leads approve dispatch and site acceptance | Missing prerequisites; schedule corrections |
| 15. Landowner partnerships / expansion | Site-questionnaire gaps and feasibility brief | Consented site information, approved criteria | Faster initial screening | Clearer partner expectations | Specialists approve site feasibility and commitments | Missing evidence; screening time |
| 16. HR / learning | Sourced onboarding guide and training-gap summary | Approved policies, role guides, permitted training records | Less repeated explanation | Indirect: better-informed service teams | HR approves guidance; humans retain all employment decisions | Answer accuracy; onboarding search time |
| 17. IT / knowledge / security | Permission-aware SOP lookup and incident draft | Approved knowledge, access rules, sanitised incident records | Faster relevant information | Indirect: more dependable service | IT approves access and operational changes | Citation accuracy; unauthorised disclosure count |
| 18. Legal / contracts / compliance | Clause comparison and obligation checklist | Authorised contracts, jurisdiction, counsel-approved templates | Less first-pass extraction | Clearer documented commitments | Counsel and authorised signatories approve advice and terms | Missed obligations; reviewer corrections |
| 19. Sustainability | Evidence register and reporting-gap brief | Metered data, methods, supplier evidence | Easier evidence collection | More substantiated environmental information | Responsible specialists approve claims | Unsupported claims; evidence coverage |
| 20. Leadership / research / strategy | Cross-functional options memo with assumptions | Approved reports, cited research, constraints | Less briefing assembly | Indirect: better-informed service priorities | Leaders approve strategy and experiments | Source coverage; decision preparation time |

## Two cross-team scenarios to evaluate

### Guest fault before arrival

A fictional cleaner reports a water-system fault shortly before an arrival. Operations captures the issue; maintenance checks the equipment and advises next steps. With separately approved integrations, a tool could compare the fault record with the arrival schedule, identify missing readiness evidence, and draft a handover, repair follow-up and guest-service briefing.

The maintenance lead confirms the diagnosis and physical repair. Operations confirms readiness. Guest-service staff decide what to communicate; authorised staff approve any relocation or refund. Finance reviews related invoice exceptions later. The model must not infer “safe to occupy” from a closed task alone.

**Test:** were blockers surfaced earlier, were handoffs complete, and did checking/correction take less staff time? Customer benefit remains a hypothesis until readiness and communication outcomes are measured.

### New property launch

A fictional prospective site moves from partner enquiry to design, procurement, manufacturing, delivery and guest operations. A shared evidence checklist could expose an unanswered access question, a drawing revision affecting materials, or an incomplete housekeeping handover before launch communications are prepared.

Each team validates its own record. Qualified professionals retain engineering and compliance sign-off; management approves commitments and launch timing. Marketing and reservations use only approved specifications and availability. Owner relations receives a checked update. No AI-generated checklist proves a property is compliant or ready.

**Test:** missing prerequisites discovered before handover, revision mismatches, and time spent reconciling status across teams.

## Indicative shortlist and decision gates

1. **Discover:** interview functional leads; observe recurring work; identify customers affected, source owners, baseline effort and critical errors. Do not select twenty simultaneous projects.
2. **Shortlist bounded drafting:** consider handover/follow-up, sourced SOP lookup or quote comparison where authorised examples and a reviewer exist. Use a checklist/report instead when deterministic rules suffice.
3. **Evaluate in shadow mode:** compare with existing work using controlled data. Measure net staff time including review, factual/citation accuracy, missed actions and customer-relevant outcomes. Keep the existing system authoritative.
4. **Decide whether to integrate:** proceed only if data access, permission boundaries, review burden, value and error handling justify it. Shared authentication, backups and audit ownership precede shared deployment.

These stages are selection criteria, not implementation commitments or financial-return promises. No autonomous payments, refunds, hiring, legal advice, engineering sign-off, publication or customer sends are proposed. Adding agents is optional; a verified improvement in real work is the decision criterion.
