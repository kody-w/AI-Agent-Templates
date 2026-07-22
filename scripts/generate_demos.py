#!/usr/bin/env python3
"""
Demo page generator for AI-Agent-Templates.

Regenerates every HTML demo in agent_stacks/demos_needing_videos/ from a
single modern template so they all stay consistent. Each demo is:

  - a single self-contained file (renders from file:// with no network),
  - a scripted conversation showcasing the vertical's use case, and
  - a "Live data" panel that fetches real records in-browser from the
    matching system of the simulated enterprise estate (the 14 schema-true
    public sandbox APIs sharing the Aster Lane Office Systems world:
    https://kody-w.github.io/RAR/ -> skill.md, section 9). Offline, the
    panel degrades to a friendly message; the scripted demo still plays.

Usage (from the repository root):

    python3 scripts/generate_demos.py

Filenames are a stable contract (external tooling links to them) — this
script only ever rewrites the existing agent_stacks/demos_needing_videos/
*.html files listed in DEMOS; it never renames or removes them.
"""

import html
import json
from pathlib import Path

OUT_DIR = Path("agent_stacks/demos_needing_videos")

# ---------------------------------------------------------------------------
# Estate sources (verified live endpoints, July 2026)
# shape: how to read the payload
#   odata  -> {"@odata.count", "value":[...]}
#   plain  -> {"count", "value":[...]}
#   sf     -> {"totalSize", "records":[...]}
#   sn     -> {"result":[...]}
# ---------------------------------------------------------------------------

D365 = "https://kody-w.github.io/static-dynamics-365/api/data/v9.2"
SFDC = "https://kody-w.github.io/static-salesforce/services/data/v59.0/query"
BANK = "https://kody-w.github.io/static-core-banking/api/v1"
HRIS = "https://kody-w.github.io/static-hris/api/v1"
ERP = "https://kody-w.github.io/static-erp/api/v1"
ITSM = "https://kody-w.github.io/static-itsm/api/now/table"

SOURCES = {
    "d365_accounts": {
        "label": "Dynamics 365 — Accounts",
        "url": f"{D365}/accounts.json",
        "shape": "odata",
        "cols": [["Account", "name"], ["City", "address1_city"], ["No.", "accountnumber"]],
    },
    "d365_opportunities": {
        "label": "Dynamics 365 — Opportunities",
        "url": f"{D365}/opportunities.json",
        "shape": "odata",
        "cols": [["Opportunity", "name"], ["Customer", "customeridname"], ["Win %", "closeprobability"]],
    },
    "d365_contacts": {
        "label": "Dynamics 365 — Contacts",
        "url": f"{D365}/contacts.json",
        "shape": "odata",
        "cols": [["Contact", "fullname"], ["Title", "jobtitle"], ["City", "address1_city"]],
    },
    "d365_incidents": {
        "label": "Dynamics 365 — Cases",
        "url": f"{D365}/incidents.json",
        "shape": "odata",
        "cols": [["Case", "ticketnumber"], ["Title", "title"], ["Customer", "customerid@OData.Community.Display.V1.FormattedValue"]],
    },
    "sfdc_opportunities": {
        "label": "Salesforce — Opportunities",
        "url": f"{SFDC}/Opportunity.json",
        "shape": "sf",
        "cols": [["Opportunity", "Name"], ["Amount", "Amount"], ["Close", "CloseDate"]],
    },
    "sfdc_contacts": {
        "label": "Salesforce — Contacts",
        "url": f"{SFDC}/Contact.json",
        "shape": "sf",
        "cols": [["Contact", "Name"], ["Title", "Title"], ["Email", "Email"]],
    },
    "sfdc_cases": {
        "label": "Salesforce — Cases",
        "url": f"{SFDC}/Case.json",
        "shape": "sf",
        "cols": [["Case", "CaseNumber"], ["Subject", "Subject"], ["Status", "Status"]],
    },
    "bank_members": {
        "label": "Core Banking — Members",
        "url": f"{BANK}/members.json",
        "shape": "plain",
        "cols": [["Member", "full_name"], ["No.", "member_number"], ["Status", "status"]],
    },
    "bank_accounts": {
        "label": "Core Banking — Accounts",
        "url": f"{BANK}/accounts.json",
        "shape": "plain",
        "cols": [["Member", "member_name"], ["Type", "account_type"], ["Balance", "balance"]],
    },
    "bank_transactions": {
        "label": "Core Banking — Transactions",
        "url": f"{BANK}/transactions.json",
        "shape": "plain",
        "cols": [["Merchant", "merchant"], ["Amount", "amount"], ["Channel", "channel"]],
    },
    "hris_workers": {
        "label": "HRIS — Workers",
        "url": f"{HRIS}/workers.json",
        "shape": "plain",
        "cols": [["Worker", "full_name"], ["Role", "job_title"], ["Dept", "department_name"]],
    },
    "hris_time_off": {
        "label": "HRIS — Time-off Requests",
        "url": f"{HRIS}/time_off_requests.json",
        "shape": "plain",
        "cols": [["Request", "request_number"], ["Days", "days"], ["Status", "status"]],
    },
    "erp_pos": {
        "label": "ERP — Purchase Orders",
        "url": f"{ERP}/purchase_orders.json",
        "shape": "plain",
        "cols": [["PO", "po_number"], ["Supplier", "supplier_name"], ["Status", "status"]],
    },
    "erp_suppliers": {
        "label": "ERP — Suppliers",
        "url": f"{ERP}/suppliers.json",
        "shape": "plain",
        "cols": [["Supplier", "name"], ["Category", "category"], ["Terms", "payment_terms"]],
    },
    "itsm_incidents": {
        "label": "ITSM — Incidents",
        "url": f"{ITSM}/incident.json",
        "shape": "sn",
        "cols": [["Incident", "number"], ["Summary", "short_description"], ["Priority", "priority"]],
    },
}

# ---------------------------------------------------------------------------
# Demo definitions. Keys are the exact existing filenames (stable contract).
# turns = [(user, assistant), ...] — assistant answers stay one-screen short.
# ---------------------------------------------------------------------------

DEMOS = {
    # ------------------------------------------------------------- B2B sales
    "b2b_account_intelligence_demo.html": {
        "title": "B2B Account Intelligence",
        "vertical": "B2B Sales",
        "tagline": "A 360-degree pre-meeting brief assembled from CRM, news, and pipeline signals.",
        "persona": "Alex Chen, Enterprise Account Executive",
        "sources": ["d365_accounts", "d365_opportunities"],
        "turns": [
            ("Brief me on Beacon Hill Staffing Partners before my 2pm call.",
             "Beacon Hill Staffing Partners — Boston, MA (AST-1020).\n"
             "- Relationship: active customer, office-systems refresh completed last quarter.\n"
             "- Open pipeline: printer fleet expansion, mid-stage, 40% probability.\n"
             "- Recent signal: headcount growth in their Louisville branch suggests a device add-on.\n"
             "- Risk: two support cases open this month — worth acknowledging up front.\n"
             "Suggested opener: reference the smooth refresh, then probe the branch expansion."),
            ("Who are my strongest champions there?",
             "Two contacts stand out:\n"
             "- Operations lead — sponsored the original refresh, responds within a day.\n"
             "- Facilities manager — logged both support cases; turning them into a win restores the champion.\n"
             "I'd bring a one-slide case-resolution summary to the call."),
            ("Draft my three talking points.",
             "1. Refresh results: uptime and cost numbers from last quarter's rollout.\n"
             "2. Louisville expansion: propose a pilot bundle sized for the new branch.\n"
             "3. Service: confirm both open cases have owners and dates — then ask for the renewal conversation."),
        ],
    },
    "b2b_deal_progression_demo.html": {
        "title": "B2B Deal Progression",
        "vertical": "B2B Sales",
        "tagline": "Pipeline analysis that spots stalled deals and recommends the next best action.",
        "persona": "Priya Nair, Regional Sales Manager",
        "sources": ["d365_opportunities", "sfdc_opportunities"],
        "turns": [
            ("Which of my deals are stalled this quarter?",
             "Three deals show no stage movement in 21+ days:\n"
             "- Marigold Field Services — qualified, stuck at 40%; no meeting since intro.\n"
             "- Riverbend Medical printer refresh — proposal sent, no response in 3 weeks.\n"
             "- Prairie Wind Energy add-on — waiting on procurement contact.\n"
             "Combined value at risk: roughly a third of your quarter."),
            ("What should I do about Riverbend Medical?",
             "The proposal went quiet after their facilities review. Recommended sequence:\n"
             "1. Re-engage the clinical ops sponsor, not procurement — she drove the evaluation.\n"
             "2. Attach the uptime benchmark from their sister site.\n"
             "3. Offer a 30-minute working session this week; silence usually means an internal blocker, not a no."),
            ("Update the forecast with what you see.",
             "Done. Marigold stays Commit at 40%, Riverbend moves to Best Case pending re-engagement, Prairie Wind slips one month. Forecast delta logged to the opportunity records with today's notes."),
        ],
    },
    "b2b_proposal_generation_demo.html": {
        "title": "B2B Proposal Generation",
        "vertical": "B2B Sales",
        "tagline": "First-draft proposals assembled from CRM context, pricing, and past wins.",
        "persona": "Marcus Todd, Solutions Consultant",
        "sources": ["d365_opportunities", "d365_accounts"],
        "turns": [
            ("Draft a proposal for the Summit Trail Software office refresh.",
             "Draft assembled from the opportunity record and two comparable wins:\n"
             "- Scope: 3 floors, managed print plus device refresh, phased over 6 weeks.\n"
             "- Pricing: mid-tier bundle with the software-vertical discount applied.\n"
             "- Proof points: two anonymized case studies with 18% cost reduction.\n"
             "Sections ready for review: Executive Summary, Scope, Timeline, Pricing, Terms."),
            ("Tighten the executive summary to five sentences.",
             "Done:\n"
             "\"Summit Trail Software is scaling faster than its office infrastructure. This proposal replaces aging devices across three floors with a managed fleet sized to your growth plan. Rollout completes in six weeks with zero downtime to your teams. Comparable customers cut print and device costs by 18% in year one. We can begin the pilot floor within two weeks of signature.\""),
            ("What's the riskiest assumption in this draft?",
             "The 6-week timeline assumes their IT team can provision network access per floor within 3 business days each phase. Flag it in Terms, or pad phase two by a week — that's where comparable projects slipped."),
        ],
    },
    "b2b_sales_qualification_demo.html": {
        "title": "B2B Sales Qualification",
        "vertical": "B2B Sales",
        "tagline": "Inbound leads scored and qualified against your ideal customer profile.",
        "persona": "Dana Whitfield, Sales Development Rep",
        "sources": ["d365_accounts", "sfdc_contacts"],
        "turns": [
            ("Qualify this inbound: facilities director at a 175-person software company asking about managed print.",
             "Strong fit — score 82/100.\n"
             "- Size: 51–200 employees is your core segment.\n"
             "- Role: facilities director is a typical economic buyer.\n"
             "- Intent: 'managed print' is a solution-aware query, not research.\n"
             "- Match: profile resembles Summit Trail Software, a closed-won account.\n"
             "Suggested route: AE-led discovery call, not nurture."),
            ("What discovery questions should the AE open with?",
             "1. What triggered the search now — growth, cost, or a contract expiring?\n"
             "2. How many devices and floors are in scope?\n"
             "3. Who besides you signs off on facilities spend?\n"
             "4. What would make this a win in 90 days?"),
            ("Log it and set the follow-up.",
             "Lead created, scored, and routed to the enterprise queue. Discovery call proposed for Thursday; confirmation email drafted for your review. The account is linked to its firmographic profile so the AE sees headcount and funding stage at a glance."),
        ],
    },
    "b2b_win_loss_analysis_demo.html": {
        "title": "B2B Win/Loss Analysis",
        "vertical": "B2B Sales",
        "tagline": "Patterns across closed deals turned into coaching and playbook updates.",
        "persona": "Elena Vasquez, VP of Sales",
        "sources": ["sfdc_opportunities", "d365_opportunities"],
        "turns": [
            ("What patterns separate our wins from losses this half?",
             "Across closed deals:\n"
             "- Wins averaged 2.4 stakeholders engaged; losses averaged 1.1 — single-threaded deals lose.\n"
             "- Deals with a pilot phase won 3x more often than proposal-only pursuits.\n"
             "- Losses cluster where first response took over 2 days.\n"
             "- Pricing was cited in only 1 of 5 losses — access, not price, is the problem."),
            ("Which rep behaviors should we coach on?",
             "Two, in order of impact:\n"
             "1. Multi-threading: require a second stakeholder before stage 3. Reps who do this already show 20 points higher win rate.\n"
             "2. Pilot-first proposals: replace the big-bang quote with a pilot floor or branch. It shortened cycles by two weeks in winning deals."),
            ("Summarize this for Monday's pipeline review.",
             "One slide, three bullets: single-threaded deals lose twice as often; pilots win 3x; respond in 48 hours or don't bother. Full breakdown with the deal list is attached to the review notes."),
        ],
    },
    # ------------------------------------------------------------- B2C sales
    "b2c_cart_abandonment_recovery_demo.html": {
        "title": "B2C Cart Abandonment Recovery",
        "vertical": "B2C Sales",
        "tagline": "Abandoned carts recovered with personalized, well-timed outreach.",
        "persona": "Jamie Fox, E-commerce Manager",
        "sources": ["sfdc_contacts", "d365_contacts"],
        "turns": [
            ("Who abandoned carts in the last 24 hours and what do we know about them?",
             "Overnight: 47 abandoned carts, 12 above the $100 threshold.\n"
             "- 8 are repeat customers — highest recovery odds.\n"
             "- Top cart: returning customer, standing desk bundle, exited at shipping cost.\n"
             "- Pattern: 60% of exits happened on the shipping step, not payment.\n"
             "Recommended: free-shipping nudge for the shipping-step cohort only."),
            ("Draft the recovery email for the standing desk customer.",
             "Subject: Your desk is still here — shipping's on us\n\n"
             "\"Hi — you left the standing desk bundle in your cart yesterday. Good news: we'll cover shipping on this order. Your cart is saved and ready; this offer holds for 48 hours. Questions about setup or delivery? Just reply.\"\n\n"
             "Tone matches their two previous purchases; no discount on the product itself, so margin holds."),
            ("What results should I expect?",
             "For repeat customers with a shipping incentive, comparable campaigns recover 18–25%. For the 12-cart cohort that's 2–3 orders. I'll track opens and recoveries and report in 48 hours when the offer window closes."),
        ],
    },
    "b2c_customer_360_speech_demo.html": {
        "title": "B2C Customer 360 (Speech)",
        "vertical": "B2C Sales",
        "tagline": "A spoken query becomes a full customer profile before the call connects.",
        "persona": "Riley Santos, Contact Center Agent",
        "sources": ["d365_contacts", "d365_incidents"],
        "turns": [
            ("\"Pull up the customer calling from the Louisville area code.\"",
             "Match: Marcus Webb, Member Services Manager, Louisville KY.\n"
             "- Customer for 2 years, 6 orders, no returns.\n"
             "- Open case: delivery inquiry from last week, still unassigned.\n"
             "- Sentiment: last survey positive.\n"
             "Likely reason for call: the open delivery case. Suggested opener: acknowledge it before he asks."),
            ("\"What happened with that delivery case?\"",
             "Order shipped in two packages; the second missed its delivery window and the case sat unassigned for 5 days. Carrier now shows it out for delivery today. Recommended: confirm today's delivery, apologize for the silence, and offer to stay on the case until it lands."),
            ("\"Log the call and close the loop.\"",
             "Logged: call summary attached to the case, follow-up task set for tomorrow to confirm delivery, and the case owner assigned so nothing sits unowned again. Marcus gets a confirmation text with the tracking link."),
        ],
    },
    "b2c_customer_loyalty_rewards_demo.html": {
        "title": "B2C Customer Loyalty & Rewards",
        "vertical": "B2C Sales",
        "tagline": "Loyalty balances, tier moves, and reward offers handled conversationally.",
        "persona": "Morgan Blake, Loyalty Program Manager",
        "sources": ["d365_contacts", "sfdc_contacts"],
        "turns": [
            ("Which members are close to the next tier and worth a nudge?",
             "23 members are within 15% of Gold.\n"
             "- 9 have purchased in the last 30 days — momentum cohort, best nudge candidates.\n"
             "- 5 have been inactive 60+ days — a tier nudge alone won't move them.\n"
             "- Top candidate: 2-year customer, 40 points from Gold, browses weekly.\n"
             "Suggested: '40 points to Gold' message with a small accelerator on their usual category."),
            ("What does the accelerator cost us versus the upside?",
             "Double points on one category purchase costs roughly $4 per redemption. Gold members historically spend 30% more in the following 6 months. Break-even is one incremental purchase; the momentum cohort averages 1.8 per month. The economics favor the nudge for all 9."),
            ("Launch it for the momentum cohort.",
             "Done — 9 personalized messages queued with each member's points-to-Gold number and category accelerator. Results dashboard tracks tier conversions over 30 days; I'll flag anyone who converts so their welcome-to-Gold message goes out same-day."),
        ],
    },
    "b2c_omnichannel_engagement_demo.html": {
        "title": "B2C Omnichannel Engagement",
        "vertical": "B2C Sales",
        "tagline": "One customer, one conversation — across store, web, and support channels.",
        "persona": "Sam Porter, Customer Experience Lead",
        "sources": ["d365_contacts", "d365_incidents"],
        "turns": [
            ("A customer emailed, then called, then walked into the Erie store about the same order. What's the full picture?",
             "Timeline stitched across channels:\n"
             "- Mon: email asking to change delivery address — auto-reply only.\n"
             "- Tue: call, 8 minutes, agent updated the address but didn't confirm by email.\n"
             "- Today: store visit — order still shows the old address in the store system.\n"
             "Root cause: the address change synced to shipping but not to the store view. The customer was right three times."),
            ("What should the store associate say right now?",
             "\"You're all set — the address change did go through on Tuesday; our store screen just hadn't caught up. Your order ships to the new address tomorrow. I've flagged the sync issue so this doesn't happen again, and you'll get a confirmation email in the next few minutes.\" Send the confirmation now; it was the missing step."),
            ("Prevent this class of issue.",
             "Two fixes logged: (1) address changes now trigger a customer confirmation on every channel, (2) a sync-lag alert flags orders whose store view is older than the CRM record. Both routed to the platform backlog with this case as the evidence."),
        ],
    },
    "b2c_personalized_shopping_assistant_demo.html": {
        "title": "B2C Personalized Shopping Assistant",
        "vertical": "B2C Sales",
        "tagline": "Recommendations grounded in purchase history, not generic bestsellers.",
        "persona": "Taylor Kim, Digital Commerce Lead",
        "sources": ["sfdc_contacts", "d365_contacts"],
        "turns": [
            ("A returning customer asks: \"I need to outfit a small home office, what do you recommend?\"",
             "Based on their history (ergonomic chair, cable kit — quality-tier buyer):\n"
             "- Desk: the mid-depth standing desk that pairs with their chair, in the walnut finish they browsed twice.\n"
             "- Lighting: the glare-free task lamp — they bought a monitor last quarter.\n"
             "- Skip: the budget bundle; their history says they trade up.\n"
             "Total lands inside the typical home-office budget with room for delivery."),
            ("They ask if the desk works in a small apartment.",
             "Yes — recommend the 48-inch width: it fits a 9-foot wall with a chair beside it, and the frame is the same one in the larger sizes so stability doesn't drop. If space is the top concern, the wall-fold desk is the alternative, but it won't hold their dual-monitor setup. Honest answer: 48-inch standing desk."),
            ("Close the conversation well.",
             "\"The 48-inch walnut standing desk fits your space and matches your chair. It's in stock — delivery Thursday, free assembly included this month. Want me to add the cable tray so the setup stays clean?\" One relevant add-on, then stop selling."),
        ],
    },
    "b2c_returns_exchange_demo.html": {
        "title": "B2C Returns & Exchange",
        "vertical": "B2C Sales",
        "tagline": "Returns resolved in one conversation — policy, label, and refund status included.",
        "persona": "Jordan Avery, Returns Team Lead",
        "sources": ["d365_incidents", "sfdc_cases"],
        "turns": [
            ("Customer wants to return a desk chair bought 35 days ago. Policy is 30 days. What do we do?",
             "Recommend the exception. The record shows:\n"
             "- First return in 6 orders across 2 years.\n"
             "- The chair model has an elevated return rate for a known armrest defect.\n"
             "- Cost of the exception: restocking. Cost of refusing: likely the customer.\n"
             "Offer: full refund or exchange for the updated model, their choice. Exception logged with the defect code so it counts toward the quality report."),
            ("They choose the exchange. Handle it.",
             "Done:\n- Exchange order created for the updated model, ships tomorrow.\n- Prepaid return label emailed; pickup available Thursday.\n- No charge difference — price-protected as a defect exchange.\n- Case linked to the armrest defect tally (that's the 14th this quarter — flagged to quality)."),
            ("What should the confirmation message say?",
             "\"Your exchange is confirmed. The updated chair ships tomorrow; your return label is in your inbox and pickup is available Thursday. No charge for the swap. Thanks for giving us the chance to make it right.\" Short, no policy lecture, no survey link in the same message."),
        ],
    },
    "b2c_sales_chat_demo.html": {
        "title": "B2C Sales Chat",
        "vertical": "B2C Sales",
        "tagline": "Website chat that answers, recommends, and closes without handing off.",
        "persona": "Website visitor, evening traffic",
        "sources": ["sfdc_contacts", "d365_accounts"],
        "turns": [
            ("Do you have standing desks under $400 that ship this week?",
             "Yes — two options in stock:\n"
             "- 48-inch electric standing desk, $349: ships tomorrow, arrives Thursday.\n"
             "- 42-inch compact model, $289: ships tomorrow, arrives Thursday.\n"
             "Both include the 30-day trial. The 48-inch is the better pick if you run two monitors. Want dimensions or the weight limit?"),
            ("What's the weight limit on the 48-inch, and is assembly hard?",
             "Weight limit: 220 lbs — dual monitors, a desktop tower, and accessories are fine. Assembly is about 25 minutes with the included tool; most of it is attaching the top to the frame. This month assembly service is free if you'd rather skip it."),
            ("OK, I'll take it with the free assembly.",
             "Great choice. I've added the 48-inch desk with free assembly — $349 total, delivery and setup Thursday. Checkout takes about a minute from here; your cart is saved if you need to step away. Anything else for the office?"),
        ],
    },
    # ---------------------------------------------------- Financial services
    "fsi_claims_processing_demo.html": {
        "title": "FSI Claims Processing",
        "vertical": "Financial Services",
        "tagline": "Claims triaged, verified against policy terms, and routed in minutes.",
        "persona": "Angela Torres, Claims Supervisor",
        "sources": ["bank_members", "bank_transactions"],
        "turns": [
            ("Triage this morning's new claims queue.",
             "14 new claims triaged:\n"
             "- 9 straight-through candidates: complete documentation, within policy limits, no fraud flags — ready for auto-approval review.\n"
             "- 3 need documents: one missing repair estimate, two missing incident dates.\n"
             "- 2 escalations: one exceeds authority limit, one has a date inconsistency worth a human look.\n"
             "Fastest win: approve the 9 clean ones before lunch."),
            ("Show me the date inconsistency case.",
             "Claim filed Monday for an incident dated Sunday — but the attached statement shows a related transaction posted the previous Wednesday. Could be an honest date error; could be a backdated claim. Recommendation: request clarification, not denial. Drafted a neutral message asking the member to confirm the incident date."),
            ("Approve the clean nine and send the clarification.",
             "Done. Nine claims approved and queued for payment — members get status notifications now. The clarification request went out with a 5-day response window, and the two document requests include upload links. Queue is clear; next batch arrives at 1pm."),
        ],
    },
    "fsi_customer_sentiment_churn_demo.html": {
        "title": "FSI Sentiment & Churn",
        "vertical": "Financial Services",
        "tagline": "Early churn signals from balances, transactions, and support tone.",
        "persona": "David Osei, Head of Member Experience",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            ("Which members show churn risk this month?",
             "7 members flagged, 3 high-priority:\n"
             "- MBR-2001: payroll deposit stopped 6 weeks ago — the classic leaving-signal.\n"
             "- One member moved 80% of savings out over two months, no product complaints.\n"
             "- One had two disputed transactions and a frustrated support call in 30 days.\n"
             "The payroll-stop member has been with you 6 years — highest lifetime value at risk."),
            ("What's the right intervention for the payroll-stop member?",
             "Not a retention offer — a check-in. Payroll stops usually mean a job change; the account decision hasn't been made yet. Recommended: personal call from her branch, ask how the transition is going, and mention direct-deposit switching takes one form. If she's already decided, ask what would have changed it — that's your churn data."),
            ("Set up the outreach for all three.",
             "Done: branch call task for the payroll-stop member (assigned to the banker she's met), a savings-rate review invitation for the mover, and a service-recovery call plus dispute-fee refund for the frustrated member. All three logged with follow-up dates; I'll report outcomes in two weeks."),
        ],
    },
    "fsi_financial_advisor_copilot_demo.html": {
        "title": "FSI Financial Advisor Copilot",
        "vertical": "Financial Services",
        "tagline": "Meeting prep, portfolio context, and follow-ups for advisors.",
        "persona": "Sarah Lindqvist, Financial Advisor",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            ("Prep me for my 10am with Denise Calloway.",
             "Denise Calloway (MBR-2001), member since 2020:\n"
             "- Checking healthy; savings up 12% this year — consistent saver.\n"
             "- Last meeting: asked about education savings for her daughter.\n"
             "- Open item: the 529 comparison you promised — attached, ready to walk through.\n"
             "- Life signal: payroll deposits show a recent raise.\n"
             "Agenda: 529 decision first, then the raise is a natural opening for retirement contribution."),
            ("Summarize the 529 comparison in plain language.",
             "Two solid options: the state plan gives her a tax deduction now and good-enough funds; the national plan has slightly better fund choices but no deduction. For her bracket the deduction wins unless she expects to move states. Plain recommendation: state plan, automatic monthly contribution sized to the raise."),
            ("Log the meeting plan and set follow-ups.",
             "Logged. After the meeting I'll capture decisions against this plan. Pre-set follow-ups: 529 enrollment check-in (2 weeks), contribution confirmation (next statement), and an annual review placeholder. Compliance note attached — education-savings discussion, no securities recommendations made."),
        ],
    },
    "fsi_financial_insights_demo.html": {
        "title": "FSI Financial Insights",
        "vertical": "Financial Services",
        "tagline": "Member-facing spending insight that's specific, not generic.",
        "persona": "Member self-service, mobile app",
        "sources": ["bank_transactions", "bank_accounts"],
        "turns": [
            ("Where did my money go last month?",
             "Your month at a glance:\n"
             "- Income: payroll deposits as usual, plus one refund.\n"
             "- Biggest categories: rent, groceries (up 8%), and subscriptions.\n"
             "- Noticed: three subscriptions renewed within 4 days — about $47/month combined.\n"
             "- Good news: you saved 11% of income, above your 3-month average.\n"
             "Want the subscription list?"),
            ("Yes — which subscriptions, and which should I cancel?",
             "The three renewals: streaming ($15.99), fitness app ($12.99), cloud storage ($17.99). Usage signal: the fitness app hasn't had a linked-card gym or store transaction in 4 months. I can't know what you value — but that's the one to look at. Canceling it saves $156/year."),
            ("Move that $13 a month into savings automatically.",
             "Done — a $13 monthly auto-transfer to savings starts on your next payroll date. Small but real: $156/year plus dividends. I'll flag it in next month's summary so you can see the habit forming."),
        ],
    },
    "fsi_fraud_detection_alert_demo.html": {
        "title": "FSI Fraud Detection & Alert",
        "vertical": "Financial Services",
        "tagline": "Suspicious activity caught, explained, and resolved without drama.",
        "persona": "Fraud Operations, real-time queue",
        "sources": ["bank_transactions", "bank_accounts"],
        "turns": [
            ("Why did the system flag this card transaction?",
             "Three stacked signals, not one:\n"
             "- Merchant category the member has never used, 900 miles from home.\n"
             "- Amount 6x their average card transaction.\n"
             "- Second transaction attempt 90 seconds after a decline.\n"
             "Individually weak; together they cross the threshold. Card is soft-held pending member confirmation — nothing is declined permanently yet."),
            ("The member confirmed it's fraud. Walk through the response.",
             "Executing now:\n1. Card blocked, replacement issued — arrives in 3 business days, digital card usable immediately.\n2. Provisional credit posted for the disputed amount.\n3. Dispute case opened with the network, evidence packet attached.\n4. Recent transactions scanned — no other anomalies on this account.\nMember gets a plain-language summary of all four steps."),
            ("Any pattern across other members?",
             "Yes — same merchant descriptor hit two other members this week, both declined by the same rule. Pattern packaged and reported: merchant added to the watch list and the network notified. Your rule caught a small ring, not a one-off."),
        ],
    },
    "fsi_loan_origination_assistant_demo.html": {
        "title": "FSI Loan Origination Assistant",
        "vertical": "Financial Services",
        "tagline": "Applications completed, verified, and decision-ready in one pass.",
        "persona": "Kevin Marsh, Lending Officer",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            ("Review the auto loan application that just came in.",
             "Application from a 4-year member, $24,000 auto loan:\n"
             "- Income: verified from 12 months of payroll deposits — no paystub chase needed.\n"
             "- Debt-to-income: 31%, inside guideline.\n"
             "- Banking behavior: no overdrafts in 24 months, stable balances.\n"
             "- Missing: the vehicle purchase agreement.\n"
             "Everything else is decision-ready. Request the purchase agreement and this can close this week."),
            ("What rate does she qualify for?",
             "Based on tier-2 credit and the relationship discount (checking + direct deposit), she qualifies for your posted rate minus 0.25%. The relationship discount is the difference between you and the dealer's financing offer — lead with it. Monthly payment lands around $455 on a 60-month term."),
            ("Send the offer and the document request together.",
             "Sent — one message, not two: conditional approval at the relationship rate, payment example, and a secure upload link for the purchase agreement. The application auto-advances the moment the document lands. Average close time on this path: 2 days."),
        ],
    },
    "fsi_portfolio_rebalancing_demo.html": {
        "title": "FSI Portfolio Rebalancing",
        "vertical": "Financial Services",
        "tagline": "Drift detection and rebalancing proposals an advisor can defend.",
        "persona": "Rachel Yoon, Portfolio Manager",
        "sources": ["bank_accounts", "bank_members"],
        "turns": [
            ("Which client portfolios have drifted past tolerance?",
             "12 of 240 portfolios exceed the 5% drift band:\n"
             "- 8 drifted from equity outperformance — standard trim-and-redeploy.\n"
             "- 3 drifted from a concentrated position appreciating — needs a client conversation, not just a trade.\n"
             "- 1 is a cash buildup from an inheritance deposit — allocation conversation.\n"
             "None require same-day action; all 12 have proposals drafted."),
            ("Show me the concentrated-position case.",
             "Client holds a single stock now at 19% of the portfolio (policy cap: 10%). Complication: low cost basis, so a full trim triggers meaningful capital gains. Proposal: staged trim across two tax years, harvesting available losses against the first tranche, with a collar considered if they want downside protection meanwhile. Talking points drafted in plain language."),
            ("Approve the 8 standard rebalances.",
             "Approved and queued for execution at tomorrow's open. Trade rationale, before/after allocations, and cost estimates are attached to each client record — audit-ready. The 3 concentrated cases and the cash-buildup client are on your call list with proposals attached."),
        ],
    },
    "fsi_regulatory_compliance_demo.html": {
        "title": "FSI Regulatory Compliance",
        "vertical": "Financial Services",
        "tagline": "Monitoring, evidence, and exam-ready answers without the scramble.",
        "persona": "Nina Petrova, Chief Compliance Officer",
        "sources": ["bank_transactions", "bank_members"],
        "turns": [
            ("What needs my attention in this week's compliance review?",
             "Three items, one urgent:\n"
             "- Urgent: 2 currency transaction reports approach their filing deadline tomorrow — drafted, awaiting your sign-off.\n"
             "- A structuring pattern: one member made 4 deposits just under the reporting threshold in 10 days — SAR evaluation recommended.\n"
             "- Routine: monthly OFAC screening completed, zero matches, evidence archived.\n"
             "Sign-offs first; they're time-boxed."),
            ("Walk me through the structuring pattern before I decide.",
             "Four cash deposits of $9,200–$9,800 across three branches in 10 days — amounts, timing, and branch-hopping all consistent with structuring. Context that matters: the member owns a cash-heavy business but historically deposited weekly at one branch. Behavior change is the signal. Recommendation: file the SAR; the narrative is drafted with the transaction table attached. Filing is protective either way."),
            ("File it, and show me our exam readiness.",
             "SAR filed with confirmation number logged. Exam readiness: all filings current, monitoring rules documented with change history, and every alert this quarter shows a decision trail — including the ones we chose not to escalate, with reasons. That last part is what examiners actually test."),
        ],
    },
    "fsi_underwriting_support_demo.html": {
        "title": "FSI Underwriting Support",
        "vertical": "Financial Services",
        "tagline": "Files assembled, ratios computed, exceptions surfaced — underwriters decide.",
        "persona": "Tom Garrett, Senior Underwriter",
        "sources": ["bank_members", "bank_transactions"],
        "turns": [
            ("Prepare the mortgage file that came in overnight.",
             "File assembled and verified:\n"
             "- Income: two salaried borrowers, verified against deposit history — matches stated within 2%.\n"
             "- DTI: 36% front, 41% back — inside guideline, no compensating factors needed.\n"
             "- Assets: down payment sourced and seasoned; one $8,000 deposit needs a letter of explanation.\n"
             "- Property: appraisal ordered, due Friday.\n"
             "One document request, then this file is decision-ready."),
            ("What's the story on that $8,000 deposit?",
             "It arrived 6 weeks ago from an account with a matching surname — almost certainly a family gift. That's fine, but it needs the gift letter and donor statement to satisfy sourcing rules. Request drafted. Flag for you: if it were a loan, the DTI moves to 43% — still passing, but tighter. The letter settles it either way."),
            ("Anything in the bank activity an automated score would miss?",
             "Two things worth knowing:\n- A recurring monthly transfer out that looks like informal rent-to-family — doesn't appear on the credit report but is a real obligation.\n- Deposit consistency through a job change last year — they never missed savings contributions. One caution, one strength. Both noted in the file summary."),
        ],
    },
    "fsi_wealth_insights_generator_demo.html": {
        "title": "FSI Wealth Insights Generator",
        "vertical": "Financial Services",
        "tagline": "Client-ready portfolio narratives generated from real positions.",
        "persona": "Leah Armstrong, Wealth Advisor",
        "sources": ["bank_accounts", "bank_members"],
        "turns": [
            ("Generate the quarterly insight letter for my top client.",
             "Draft ready. The quarter in three points:\n"
             "- Portfolio up modestly, tracking the plan benchmark within half a percent — allocation working as designed.\n"
             "- Cash from the business sale is now 14% of assets — above target and the letter's main conversation starter.\n"
             "- Tax: harvested losses from the spring rotation offset most realized gains.\n"
             "Tone matches your previous letters; two paragraphs, then the numbers table."),
            ("Make the cash point feel like an opportunity, not a scolding.",
             "Revised: \"The proceeds from the sale give us a rare position of flexibility — 14% in cash while markets are choppy is a comfortable place to decide from, not a problem to fix. When we meet, I'd like to walk through three ways to put it to work at your pace, including keeping a larger reserve if that's what lets you sleep well.\" Choice framing, no urgency pressure."),
            ("Add a personal touch and send for my review.",
             "Added a closing line referencing the daughter's graduation he mentioned last call (from your meeting notes, not assumed). Letter is in your drafts with the numbers table and disclosure block attached. Nothing sends without your sign-off."),
        ],
    },
    # ------------------------------------------------------------ General/HR
    "general_ai_customer_assistant_demo.html": {
        "title": "AI Customer Assistant",
        "vertical": "Cross-Industry",
        "tagline": "First-line support that resolves, escalates, or gets out of the way.",
        "persona": "Customer support widget, business hours",
        "sources": ["d365_incidents", "d365_accounts"],
        "turns": [
            ("My order arrived damaged — the desk top has a crack across the corner.",
             "I'm sorry — that shouldn't have made it out of the warehouse. Here's what I can do right now:\n"
             "- Replacement top ships free, arrives in 3–4 business days, or\n"
             "- 20% refund if the crack is cosmetic and you'd rather keep it.\n"
             "No need to return the damaged piece either way. Which works better? A photo helps me file the carrier claim, but it won't hold up your resolution."),
            ("Replacement please. Will someone install it?",
             "Replacement ordered — case CAS-260142 created, confirmation on its way to your email. Installation: swapping the top takes about 15 minutes with the included tool, and I've attached the 4-step guide. If you'd rather not, I can schedule a technician visit for a flat $35 — most people find the swap easy, honestly."),
            ("I'll do it myself. Thanks for making that painless.",
             "Glad it was easy — that's the goal. Your replacement top arrives Thursday with tracking in your inbox, and case CAS-260142 stays open until you confirm it's sorted. Reply to any of our emails if something's off. Enjoy the desk once it's whole again."),
        ],
    },
    "general_ask_hr_demo.html": {
        "title": "Ask HR",
        "vertical": "Cross-Industry",
        "tagline": "Policy answers and HR transactions in the flow of work.",
        "persona": "Employee self-service, Teams",
        "sources": ["hris_workers", "hris_time_off"],
        "turns": [
            ("How much vacation do I have left, and can I take the first week of March off?",
             "You have 9 vacation days remaining this year.\n"
             "March 2–6 looks workable: no team blackout dates, and only one teammate (out of six) has overlapping time off. Your manager Morgan Ellis typically approves within a day. Want me to submit the request?"),
            ("Yes, submit it. Also — what's the policy if I need to extend by a day or two?",
             "Submitted — request TOR-1044, 5 days, March 2–6, routed to Morgan. You'll get a notification on decision.\n"
             "Extensions: just submit the extra days as a new request, even mid-trip. If you're out of vacation balance, up to 2 days can go as unpaid with manager approval. No penalty for asking late, though earlier is kinder to the team calendar."),
            ("What happens to unused days at year end?",
             "You can carry over up to 5 days into next year; they expire March 31. Anything beyond 5 is use-it-or-lose-it. With 4 days left after this request, you're under the cap — nothing at risk. I'll nudge you in November if you still have days on the table."),
        ],
    },
    "general_customer_360_demo.html": {
        "title": "Customer 360",
        "vertical": "Cross-Industry",
        "tagline": "Every system's view of one customer, stitched into a single brief.",
        "persona": "Account team, weekly review",
        "sources": ["d365_accounts", "sfdc_contacts"],
        "turns": [
            ("Give me the full picture on Silver Elm Logistics.",
             "Silver Elm Logistics — stitched from CRM, support, and finance:\n"
             "- Commercial: active customer, mid-market tier, renewal in 4 months.\n"
             "- Support: 2 cases this quarter, both resolved inside SLA — health is good.\n"
             "- Finance: invoices current, no disputes.\n"
             "- Signal: their ops director just changed — new stakeholder, relationship not yet built.\n"
             "One risk, one action: meet the new ops director before renewal season."),
            ("What do we know about the new ops director?",
             "Limited but useful: promoted internally from the warehouse team, so she's lived with your product daily — an informed buyer, which cuts both ways. No direct contact history with your team yet. Best introduction path: your implementation engineer worked with her during rollout and is remembered well. Warm intro beats cold outreach here."),
            ("Set up the renewal play.",
             "Done: intro request drafted for your implementation engineer, renewal opportunity created at 4-month horizon, and a health snapshot pinned to the account so anyone touching Silver Elm sees the same picture. Next review will flag if the intro hasn't happened in 3 weeks."),
        ],
    },
    "general_procurement_support_demo.html": {
        "title": "Procurement Support",
        "vertical": "Cross-Industry",
        "tagline": "PO status, supplier answers, and exception handling without the email chase.",
        "persona": "Procurement operations, daily standup",
        "sources": ["erp_pos", "erp_suppliers"],
        "turns": [
            ("Which purchase orders need attention today?",
             "Of 15 open POs, three need action:\n"
             "- PO-47012 (Granite Peak Manufacturing): delivery due in 2 days, no shipping confirmation yet — chase now.\n"
             "- One PO has a goods receipt posted but quantity short by 12 units — needs a decision: partial accept or claim.\n"
             "- One invoice arrived 4% over PO price — blocked for tolerance, awaiting your review.\n"
             "The other 12 are on track."),
            ("Chase Granite Peak and give me context for the call.",
             "Status request sent through the supplier portal. Context: Granite Peak is NET30, precision machining category, historically reliable — 94% on-time over 12 months, and their two late deliveries were both flagged in advance. Silence is unusual for them, which suggests a portal miss rather than a real delay. If they confirm slippage, the cart frame line is the one that gates your production schedule."),
            ("Resolve the price-variance invoice.",
             "Reviewed: the 4% increase matches the supplier's announced surcharge effective last month — the PO was cut at the old price. Options: accept with a note (surcharge is contractual), or dispute and delay payment on a valid charge. Recommended: accept, and I've queued a price-list update so the next PO prices correctly. Block released pending your click."),
        ],
    },
    "general_sales_coach_demo.html": {
        "title": "Sales Coach",
        "vertical": "Cross-Industry",
        "tagline": "Deal-specific coaching grounded in your own pipeline, not platitudes.",
        "persona": "Rep one-on-one prep",
        "sources": ["d365_opportunities", "d365_accounts"],
        "turns": [
            ("Coach me on my Prairie Wind Energy deal before the demo tomorrow.",
             "Where the deal actually stands:\n"
             "- Strength: technical evaluator is engaged — 3 meetings, fast replies.\n"
             "- Gap: no economic buyer contact in 6 weeks of activity. That's the deal risk, not the demo.\n"
             "- Tomorrow's job: use the demo to earn the exec intro, not to close.\n"
             "One move: end the demo by asking your evaluator, \"Who besides you needs to see this before a decision?\""),
            ("How do I handle it if they bring up our competitor's lower price?",
             "Don't defend the price — reframe the comparison. \"You're right, their sticker is lower. Customers who switched to us from them cite two costs that didn't show on the quote: implementation overruns and per-seat add-ons in year two. Happy to walk through a 3-year comparison with your numbers.\" Then stop talking. If price is truly the only criterion, better to learn that tomorrow than in month three."),
            ("What should my close look like?",
             "Three sentences, then silence: \"It sounds like this solves the monitoring gap your team flagged. What I'd suggest next is a 30-minute session with whoever owns the budget decision, where we show exactly this with your data. Who should that be?\" You're closing for the intro — the deal close comes after."),
        ],
    },
    "general_speech_to_crm_demo.html": {
        "title": "Speech to CRM",
        "vertical": "Cross-Industry",
        "tagline": "Talk through your meeting on the drive back — the CRM writes itself.",
        "persona": "Field seller, voice capture after a customer visit",
        "sources": ["d365_contacts", "d365_opportunities"],
        "turns": [
            ("\"Just left Maple Thread Textiles. Met with their ops manager, they want the fleet proposal by Friday, budget's approved for Q3, and their plant manager Diane needs to sign off. Oh, and their old scanner contract ends in August.\"",
             "Captured and structured:\n"
             "- Meeting logged: Maple Thread Textiles, ops manager, today.\n"
             "- Task: fleet proposal due Friday — assigned to you.\n"
             "- Opportunity updated: budget approved, Q3 close timeframe.\n"
             "- New stakeholder: Diane, plant manager, marked as approver.\n"
             "- Signal: scanner contract expires August — logged as a competitive displacement flag.\n"
             "Anything I misheard?"),
            ("\"Make the proposal task Thursday instead, and remind me to find Diane on LinkedIn tonight.\"",
             "Updated: proposal task moved to Thursday, and a personal reminder set for 7pm tonight — \"Find Diane (plant manager, Maple Thread) on LinkedIn.\" Both changes synced to the opportunity record."),
            ("\"What's my day look like tomorrow?\"",
             "Tomorrow: two customer meetings — morning demo at Blue Heron Stationery, afternoon check-in with Copper Kite Design. One task due: the pricing follow-up you promised City of Alder Creek. Gap from 1–3pm; that's your window for the Maple Thread proposal if you want a head start on Thursday."),
        ],
    },
    "general_voice_to_crm_demo.html": {
        "title": "Voice to CRM",
        "vertical": "Cross-Industry",
        "tagline": "Hands-free CRM: query, update, and log records by voice.",
        "persona": "Field seller, hands-free in transit",
        "sources": ["d365_accounts", "d365_opportunities"],
        "turns": [
            ("\"What's my pipeline looking like this month?\"",
             "Your month: 6 open opportunities.\n"
             "- 2 in Commit — Marigold Field Services and the Beacon Hill add-on.\n"
             "- 3 mid-stage, 1 early.\n"
             "- Attention flag: the Beacon Hill add-on has a proposal due tomorrow that isn't marked sent.\n"
             "Want me to open that one?"),
            ("\"Yes — push the Beacon Hill proposal date to Monday and note that their signer is traveling this week.\"",
             "Done: proposal due date moved to Monday, and I've added the note \"Signer traveling this week\" to the Beacon Hill opportunity. The Commit forecast keeps its close date — the slip is inside the buffer. You'll get a Monday-morning reminder."),
            ("\"Log a quick call note: spoke with Prairie Wind, they're happy, renewal conversation in September.\"",
             "Logged: call activity on Prairie Wind Energy Cooperative — positive sentiment, renewal conversation targeted for September. I also created a September follow-up task so the renewal doesn't depend on memory. Anything else while you're driving?"),
        ],
    },
    "hr_ask_hr_demo.html": {
        "title": "Ask HR (HR Operations)",
        "vertical": "Human Resources",
        "tagline": "The HR team's view: caseload down, employees answered instantly.",
        "persona": "Maria Gonzalez, HR Business Partner",
        "sources": ["hris_workers", "hris_time_off"],
        "turns": [
            ("What did the assistant handle for employees this week, and what needs me?",
             "This week: 142 employee questions handled, 9 escalated to you.\n"
             "- Self-served: PTO balances, policy lookups, payslip questions, address changes.\n"
             "- Escalations: 4 leave-of-absence consults, 3 manager coaching requests, 2 sensitive matters routed directly (no bot handling, per policy).\n"
             "- Pattern worth noting: 18 questions about the new parental leave policy — the FAQ needs a clearer example."),
            ("Show me the time-off picture for Customer Service before I approve the March requests.",
             "Customer Service, March: 5 requests pending.\n- TOR-1001 and two others don't overlap — safe approvals.\n- Two requests overlap March 9–11, which would put the team below minimum coverage for two days.\n- Option: one requester has flexible dates per their note.\nSuggested: approve three now, ask the flexible requester to shift two days, then all five can be honored."),
            ("Draft the message to the flexible requester.",
             "Draft: \"Hi Jordan — your March time-off request overlaps with a teammate's on the 9th–11th, which would leave the team short. You mentioned flexibility: if you can shift to start March 12, I can approve the full week today. If those exact dates matter, tell me and we'll figure it out — that's a real option too.\" Honest, choice-preserving, and it keeps trust in the process."),
        ],
    },
    "it_helpdesk_demo.html": {
        "title": "IT Helpdesk",
        "vertical": "IT Management",
        "tagline": "Diagnosis, fix, and ticket hygiene — before the user finishes their coffee.",
        "persona": "Employee, urgent pre-meeting issue",
        "sources": ["itsm_incidents"],
        "turns": [
            ("Help me fix my laptop — it's running really slow and I have a meeting in 30 minutes.",
             "Let's get you to that meeting. Quick diagnosis from your device telemetry:\n"
             "- Memory is at 96% — a browser with 40+ tabs and two conferencing apps running.\n"
             "- Disk and CPU look healthy; this is a memory squeeze, not a hardware problem.\n"
             "Fastest fix (2 minutes): close the idle conferencing app and restart the browser — it will restore your tabs. That typically frees 30% memory. Try that first?"),
            ("Did it — much faster already. Why does this keep happening though?",
             "Because your laptop has 8GB of RAM and your workload has outgrown it. You've hit this three times this quarter (INC0010021, INC0010034, and today). Two real fixes:\n- A RAM upgrade to 16GB — your model supports it, ~2 day turnaround.\n- Or a refresh device from the current catalog if you're due (you are, next month).\nI'd wait for the refresh. Meanwhile, the browser restart trick holds you over."),
            ("Book the refresh and close today's ticket.",
             "Done: device refresh request submitted for next month's cycle — you'll pick a model from the catalog link in your email. Today's incident is resolved-with-workaround and linked to the two prior tickets so the pattern is visible to asset planning. Enjoy the meeting — you've got 24 minutes to spare."),
        ],
    },
}


# ---------------------------------------------------------------------------
# SVG glyphs (no emojis — inline vector icons only)
# ---------------------------------------------------------------------------

GLYPH_SPARK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/></svg>'
)
GLYPH_USER = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="12" cy="8" r="3.5"/><path d="M4.5 20c1.6-3.2 4.3-4.8 7.5-4.8s5.9 1.6 7.5 4.8"/></svg>'
)
GLYPH_DB = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/>'
    '<path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13"/>'
    '<path d="M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/></svg>'
)
GLYPH_PLAY = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M8 5.5v13l11-6.5z"/></svg>'
)
GLYPH_RESET = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M4 10a8 8 0 1 1 2.3 6.9"/><path d="M4 16v-6h6"/></svg>'
)
GLYPH_BACK = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M15 5l-7 7 7 7"/></svg>'
)


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ — AI Agent Templates Demo</title>
<style>
:root {
  --bg: #0b0e14; --bg-soft: #11151f; --panel: #151a26; --panel-2: #1a2130;
  --border: #232b3d; --text: #e6e9f0; --text-dim: #9aa3b5; --text-faint: #6b7488;
  --accent: #5b9dff; --accent-soft: rgba(91,157,255,.12);
  --user-bubble: #24304a; --ok: #3fb97f; --warn: #e0a63f;
  --shadow: 0 8px 28px rgba(0,0,0,.35); --radius: 14px;
}
[data-theme="light"] {
  --bg: #f4f6fa; --bg-soft: #eceff5; --panel: #ffffff; --panel-2: #f6f8fc;
  --border: #dde3ee; --text: #1c2333; --text-dim: #5a6478; --text-faint: #8b94a8;
  --accent: #2f6fdb; --accent-soft: rgba(47,111,219,.10);
  --user-bubble: #e3ecfb; --ok: #1f8f5c; --warn: #b07d1e;
  --shadow: 0 6px 20px rgba(28,35,51,.10);
}
* { margin:0; padding:0; box-sizing:border-box; }
html, body { max-width:100%; overflow-x:hidden; }
body {
  font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  background: var(--bg); color: var(--text);
  min-height: 100vh; line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
svg { width: 1em; height: 1em; display: inline-block; vertical-align: -0.12em; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  position: sticky; top: 0; z-index: 10;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  max-width: 1160px; margin: 0 auto; padding: 12px 20px;
  display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
}
.back-link {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--text-dim); font-size: 13px; white-space: nowrap;
}
.back-link:hover { color: var(--text); text-decoration: none; }
.header-title { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; min-width: 0; }
.header-title h1 { font-size: 16px; font-weight: 650; letter-spacing: -0.01em; }
.badge {
  font-size: 11px; font-weight: 600; letter-spacing: .04em; text-transform: uppercase;
  color: var(--accent); background: var(--accent-soft);
  border: 1px solid color-mix(in srgb, var(--accent) 30%, transparent);
  padding: 2px 9px; border-radius: 999px; white-space: nowrap;
}
.header-actions { margin-left: auto; display: flex; gap: 8px; }
.icon-btn {
  background: var(--panel); border: 1px solid var(--border); color: var(--text-dim);
  width: 32px; height: 32px; border-radius: 9px; cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center; font-size: 15px;
}
.icon-btn:hover { color: var(--text); border-color: var(--text-faint); }

.page {
  max-width: 1160px; margin: 0 auto; padding: 22px 20px 48px;
}
.intro { margin-bottom: 18px; }
.intro p.tagline { color: var(--text-dim); font-size: 14.5px; max-width: 62ch; }
.intro p.persona { color: var(--text-faint); font-size: 12.5px; margin-top: 4px; }

.layout { display: grid; grid-template-columns: minmax(0,1fr) 340px; gap: 18px; align-items: start; }
@media (max-width: 920px) { .layout { grid-template-columns: 1fr; } }

.chat-panel {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow);
  display: flex; flex-direction: column; min-height: 420px;
}
.chat-head {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 16px; border-bottom: 1px solid var(--border);
}
.chat-head .glyph { color: var(--accent); font-size: 17px; display: inline-flex; }
.chat-head span { font-size: 13.5px; font-weight: 600; }
.chat-controls { margin-left: auto; display: flex; gap: 8px; }
.ctl-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--accent); color: #fff; border: none; cursor: pointer;
  font-size: 13px; font-weight: 600; padding: 7px 14px; border-radius: 9px;
  font-family: inherit;
}
.ctl-btn.secondary { background: var(--panel-2); color: var(--text-dim); border: 1px solid var(--border); }
.ctl-btn:hover { filter: brightness(1.08); }
.ctl-btn:disabled { opacity: .45; cursor: default; filter: none; }
.chat-body { padding: 18px 16px; display: flex; flex-direction: column; gap: 14px; flex: 1; }
.msg { display: flex; gap: 10px; max-width: 92%; animation: rise .28s ease both; }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
.msg .avatar {
  flex: 0 0 30px; width: 30px; height: 30px; border-radius: 9px;
  display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.msg.user { align-self: flex-end; flex-direction: row-reverse; }
.msg.user .avatar { background: var(--user-bubble); color: var(--text-dim); }
.msg.bot .avatar { background: var(--accent-soft); color: var(--accent); }
.bubble {
  padding: 10px 14px; border-radius: 12px; font-size: 14px; white-space: pre-wrap;
  overflow-wrap: break-word; min-width: 0;
}
.msg.user .bubble { background: var(--user-bubble); border-top-right-radius: 4px; }
.msg.bot .bubble { background: var(--panel-2); border: 1px solid var(--border); border-top-left-radius: 4px; }
.typing { display: inline-flex; gap: 4px; padding: 4px 2px; }
.typing i {
  width: 6px; height: 6px; border-radius: 50%; background: var(--text-faint);
  animation: blink 1.1s infinite;
}
.typing i:nth-child(2) { animation-delay: .18s; } .typing i:nth-child(3) { animation-delay: .36s; }
@keyframes blink { 0%,70%,100% { opacity: .25 } 30% { opacity: 1 } }
.chat-hint { color: var(--text-faint); font-size: 12.5px; text-align: center; padding: 8px 0 2px; }

.live-panel { display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.live-card {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden;
}
.live-card .lc-head {
  display: flex; align-items: center; gap: 9px; padding: 11px 14px;
  border-bottom: 1px solid var(--border);
}
.lc-head .glyph { color: var(--accent); display: inline-flex; font-size: 15px; }
.lc-head .lc-title { font-size: 12.5px; font-weight: 650; }
.lc-head .lc-count {
  margin-left: auto; font-size: 11.5px; font-weight: 600; color: var(--ok);
  background: color-mix(in srgb, var(--ok) 12%, transparent);
  padding: 2px 8px; border-radius: 999px; white-space: nowrap;
}
.lc-head .lc-count.err { color: var(--warn); background: color-mix(in srgb, var(--warn) 12%, transparent); }
.lc-body { padding: 0; }
.lc-note { padding: 12px 14px; font-size: 12.5px; color: var(--text-dim); }
.lc-table-wrap { overflow-x: auto; }
table.lc { width: 100%; border-collapse: collapse; font-size: 12px; }
table.lc th {
  text-align: left; padding: 7px 12px; color: var(--text-faint);
  font-weight: 600; font-size: 10.5px; letter-spacing: .05em; text-transform: uppercase;
  border-bottom: 1px solid var(--border); white-space: nowrap;
}
table.lc td {
  padding: 7px 12px; border-bottom: 1px solid var(--border); color: var(--text-dim);
  max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
table.lc tr:last-child td { border-bottom: none; }
.lc-src { padding: 8px 14px; font-size: 11px; color: var(--text-faint); border-top: 1px solid var(--border); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.live-blurb { font-size: 12px; color: var(--text-faint); line-height: 1.5; padding: 0 2px; }
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <a class="back-link" href="../../index.html">__GLYPH_BACK__ All templates</a>
    <div class="header-title">
      <h1>__TITLE__</h1>
      <span class="badge">__VERTICAL__</span>
    </div>
    <div class="header-actions">
      <button class="icon-btn" id="themeToggle" title="Toggle light/dark" aria-label="Toggle theme">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5 5l1.7 1.7M17.3 17.3L19 19M19 5l-1.7 1.7M6.7 17.3L5 19"/></svg>
      </button>
    </div>
  </div>
</header>

<div class="page">
  <div class="intro">
    <p class="tagline">__TAGLINE__</p>
    <p class="persona">Scenario: __PERSONA__ &middot; Fictional world: Aster Lane Office Systems (simulated enterprise estate)</p>
  </div>

  <div class="layout">
    <section class="chat-panel" aria-label="Scripted demo conversation">
      <div class="chat-head">
        <span class="glyph">__GLYPH_SPARK__</span><span>Agent conversation</span>
        <div class="chat-controls">
          <button class="ctl-btn" id="playBtn">__GLYPH_PLAY__ Play demo</button>
          <button class="ctl-btn secondary" id="resetBtn" title="Restart">__GLYPH_RESET__</button>
        </div>
      </div>
      <div class="chat-body" id="chatBody">
        <div class="chat-hint" id="chatHint">Press Play to walk through the scripted scenario.</div>
      </div>
    </section>

    <aside class="live-panel" aria-label="Live data from the simulated enterprise estate">
      __LIVE_CARDS__
      <p class="live-blurb">This panel fetches real records from the public simulated enterprise estate — schema-true sandbox APIs sharing one fictional world. Point the production agents at your own tenant by swapping the base URL. Explore the estate at <a href="https://kody-w.github.io/RAR/" target="_blank" rel="noopener">the RAR registry</a>.</p>
    </aside>
  </div>
</div>

<script>
(function () {
  "use strict";
  // ----- theme -----
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("aat-theme"); } catch (e) {}
  if (saved === "light" || (saved === null && window.matchMedia && matchMedia("(prefers-color-scheme: light)").matches)) {
    root.setAttribute("data-theme", "light");
  }
  document.getElementById("themeToggle").addEventListener("click", function () {
    var light = root.getAttribute("data-theme") === "light";
    if (light) { root.removeAttribute("data-theme"); } else { root.setAttribute("data-theme", "light"); }
    try { localStorage.setItem("aat-theme", light ? "dark" : "light"); } catch (e) {}
  });

  // ----- scripted conversation -----
  var TURNS = __TURNS_JSON__;
  var GLYPH_USER = __GLYPH_USER_JSON__;
  var GLYPH_SPARK = __GLYPH_SPARK_JSON__;
  var body = document.getElementById("chatBody");
  var hint = document.getElementById("chatHint");
  var playBtn = document.getElementById("playBtn");
  var resetBtn = document.getElementById("resetBtn");
  var idx = 0, playing = false, timer = null;

  function bubble(role, text) {
    var msg = document.createElement("div");
    msg.className = "msg " + role;
    var av = document.createElement("div");
    av.className = "avatar";
    av.innerHTML = role === "user" ? GLYPH_USER : GLYPH_SPARK;
    var b = document.createElement("div");
    b.className = "bubble";
    b.textContent = text;
    msg.appendChild(av); msg.appendChild(b);
    body.appendChild(msg);
    msg.scrollIntoView({ behavior: "smooth", block: "end" });
    return b;
  }

  function typingBubble() {
    var msg = document.createElement("div");
    msg.className = "msg bot";
    var av = document.createElement("div");
    av.className = "avatar"; av.innerHTML = GLYPH_SPARK;
    var b = document.createElement("div");
    b.className = "bubble";
    b.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
    msg.appendChild(av); msg.appendChild(b);
    body.appendChild(msg);
    msg.scrollIntoView({ behavior: "smooth", block: "end" });
    return { msg: msg, b: b };
  }

  function step() {
    if (idx >= TURNS.length) { playing = false; playBtn.disabled = true; return; }
    var t = TURNS[idx];
    bubble("user", t[0]);
    var tb = typingBubble();
    timer = setTimeout(function () {
      tb.b.textContent = t[1];
      tb.msg.scrollIntoView({ behavior: "smooth", block: "end" });
      idx += 1;
      if (playing && idx < TURNS.length) { timer = setTimeout(step, 1600); }
      else if (idx >= TURNS.length) { playing = false; playBtn.disabled = true; }
    }, 900);
  }

  playBtn.addEventListener("click", function () {
    if (playing) return;
    if (hint) { hint.remove(); hint = null; }
    playing = true;
    step();
  });
  resetBtn.addEventListener("click", function () {
    clearTimeout(timer); playing = false; idx = 0; playBtn.disabled = false;
    body.innerHTML = '<div class="chat-hint">Press Play to walk through the scripted scenario.</div>';
    hint = body.firstChild;
  });

  // ----- live estate data -----
  var SOURCES = __SOURCES_JSON__;

  function rowsOf(shape, data) {
    if (shape === "odata" || shape === "plain") return data.value || [];
    if (shape === "sf") return data.records || [];
    if (shape === "sn") return data.result || [];
    return [];
  }
  function countOf(shape, data, rows) {
    if (shape === "odata") return data["@odata.count"] != null ? data["@odata.count"] : rows.length;
    if (shape === "plain") return data.count != null ? data.count : rows.length;
    if (shape === "sf") return data.totalSize != null ? data.totalSize : rows.length;
    return rows.length;
  }
  function cell(v) {
    if (v == null) return "";
    if (typeof v === "object") return v.display_value || v.value || "";
    return String(v);
  }

  SOURCES.forEach(function (src, i) {
    var countEl = document.getElementById("lcCount" + i);
    var bodyEl = document.getElementById("lcBody" + i);
    fetch(src.url).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function (data) {
      var rows = rowsOf(src.shape, data);
      var count = countOf(src.shape, data, rows);
      countEl.textContent = count + " records";
      var html = '<div class="lc-table-wrap"><table class="lc"><thead><tr>';
      src.cols.forEach(function (c) { html += "<th>" + c[0] + "</th>"; });
      html += "</tr></thead><tbody>";
      rows.slice(0, 5).forEach(function (row) {
        html += "<tr>";
        src.cols.forEach(function (c) {
          var v = cell(row[c[1]]);
          html += "<td title=\\"" + v.replace(/"/g, "&quot;") + "\\">" + v + "</td>";
        });
        html += "</tr>";
      });
      html += "</tbody></table></div>";
      bodyEl.innerHTML = html;
    }).catch(function () {
      countEl.textContent = "offline";
      countEl.classList.add("err");
      bodyEl.innerHTML = '<div class="lc-note">Live data unavailable — you appear to be offline or the sandbox is unreachable. The scripted demo above still works; reconnect to see real records from this system.</div>';
    });
  });
})();
</script>
</body>
</html>
"""


def live_card(i, src):
    return (
        '<div class="live-card">'
        '<div class="lc-head"><span class="glyph">' + GLYPH_DB + "</span>"
        '<span class="lc-title">' + html.escape(src["label"]) + "</span>"
        '<span class="lc-count" id="lcCount' + str(i) + '">loading&hellip;</span></div>'
        '<div class="lc-body" id="lcBody' + str(i) + '">'
        '<div class="lc-note">Fetching live records&hellip;</div></div>'
        '<div class="lc-src">GET ' + html.escape(src["url"]) + "</div>"
        "</div>"
    )


def render(fname, spec):
    sources = [SOURCES[s] for s in spec["sources"]]
    cards = "\n      ".join(live_card(i, s) for i, s in enumerate(sources))
    page = (
        TEMPLATE
        .replace("__TITLE__", html.escape(spec["title"]))
        .replace("__VERTICAL__", html.escape(spec["vertical"]))
        .replace("__TAGLINE__", html.escape(spec["tagline"]))
        .replace("__PERSONA__", html.escape(spec["persona"]))
        .replace("__LIVE_CARDS__", cards)
        .replace("__GLYPH_BACK__", GLYPH_BACK)
        .replace("__GLYPH_SPARK__", GLYPH_SPARK)
        .replace("__GLYPH_PLAY__", GLYPH_PLAY)
        .replace("__GLYPH_RESET__", GLYPH_RESET)
        .replace("__TURNS_JSON__", json.dumps([[u, a] for u, a in spec["turns"]]))
        .replace("__GLYPH_USER_JSON__", json.dumps(GLYPH_USER))
        .replace("__GLYPH_SPARK_JSON__", json.dumps(GLYPH_SPARK))
        .replace("__SOURCES_JSON__", json.dumps(
            [{"label": s["label"], "url": s["url"], "shape": s["shape"], "cols": s["cols"]}
             for s in sources]))
    )
    (OUT_DIR / fname).write_text(page, encoding="utf-8")


def main():
    existing = {p.name for p in OUT_DIR.glob("*.html")}
    missing = set(DEMOS) - existing
    if missing:
        raise SystemExit("Refusing to create NEW demo files (filenames are a "
                         "contract): " + ", ".join(sorted(missing)))
    for fname, spec in DEMOS.items():
        render(fname, spec)
        print("wrote", OUT_DIR / fname)
    uncovered = existing - set(DEMOS)
    if uncovered:
        print("NOTE: not regenerated (no spec):", ", ".join(sorted(uncovered)))


if __name__ == "__main__":
    main()
