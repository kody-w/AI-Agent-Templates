#!/usr/bin/env python3
"""
Demo page generator for AI-Agent-Templates.

Regenerates every HTML demo in agent_stacks/demos_needing_videos/ from a
single template that faithfully reproduces the M365 Copilot chat surface
(recreated with CSS/SVG/text only — no Microsoft logo assets, and a
"simulated interface" disclaimer in the footer). Each demo is:

  - a single self-contained file (renders from file:// with no network),
  - a scripted agent conversation playing inside the Copilot chrome:
    user turns as right-aligned bubbles, agent turns attributed to the
    named agent (@-mention chip), replies rendered as MARKDOWN with
    Copilot-style numbered citations linking to the LIVE simulated
    source systems, and suggested-prompt pills like Copilot starters,
  - adaptive-card-style result cards INSIDE the agent's replies that
    fetch real records in-browser from the matching estate API
    (graceful offline fallback; citations still render offline since
    they point at globally public URLs).

The simulated enterprise estate: 14 schema-true public sandbox APIs
sharing the Aster Lane Office Systems world — see
https://kody-w.github.io/RAR/ -> skill.md, section 9.

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
# Estate endpoints (verified live, July 2026)
# ---------------------------------------------------------------------------

D365 = "https://kody-w.github.io/static-dynamics-365/api/data/v9.2"
D365_UI = "https://kody-w.github.io/static-dynamics-365/"
SFDC = "https://kody-w.github.io/static-salesforce/services/data/v59.0/query"
BANK = "https://kody-w.github.io/static-core-banking/api/v1"
HRIS = "https://kody-w.github.io/static-hris/api/v1"
ERP = "https://kody-w.github.io/static-erp/api/v1"
ITSM = "https://kody-w.github.io/static-itsm/api/now/table"
ENRICH = "https://kody-w.github.io/static-enrichment/api/v1"

# Live-data sources rendered as adaptive cards inside agent replies.
# shape: odata {"@odata.count","value"} | plain {"count","value"} |
#        sf {"totalSize","records"} | sn {"result"}
SOURCES = {
    "d365_accounts": {
        "label": "Accounts", "system": "Dynamics 365",
        "url": f"{D365}/accounts.json", "shape": "odata",
        "cols": [["Account", "name"], ["City", "address1_city"], ["No.", "accountnumber"]],
    },
    "d365_opportunities": {
        "label": "Opportunities", "system": "Dynamics 365",
        "url": f"{D365}/opportunities.json", "shape": "odata",
        "cols": [["Opportunity", "name"], ["Customer", "customeridname"], ["Win %", "closeprobability"]],
    },
    "d365_contacts": {
        "label": "Contacts", "system": "Dynamics 365",
        "url": f"{D365}/contacts.json", "shape": "odata",
        "cols": [["Contact", "fullname"], ["Title", "jobtitle"], ["City", "address1_city"]],
    },
    "d365_incidents": {
        "label": "Cases", "system": "Dynamics 365",
        "url": f"{D365}/incidents.json", "shape": "odata",
        "cols": [["Case", "ticketnumber"], ["Title", "title"], ["Customer", "customerid@OData.Community.Display.V1.FormattedValue"]],
    },
    "sfdc_opportunities": {
        "label": "Opportunities", "system": "Salesforce",
        "url": f"{SFDC}/Opportunity.json", "shape": "sf",
        "cols": [["Opportunity", "Name"], ["Amount", "Amount"], ["Close", "CloseDate"]],
    },
    "sfdc_contacts": {
        "label": "Contacts", "system": "Salesforce",
        "url": f"{SFDC}/Contact.json", "shape": "sf",
        "cols": [["Contact", "Name"], ["Title", "Title"], ["Email", "Email"]],
    },
    "sfdc_cases": {
        "label": "Cases", "system": "Salesforce",
        "url": f"{SFDC}/Case.json", "shape": "sf",
        "cols": [["Case", "CaseNumber"], ["Subject", "Subject"], ["Status", "Status"]],
    },
    "bank_members": {
        "label": "Members", "system": "Core banking",
        "url": f"{BANK}/members.json", "shape": "plain",
        "cols": [["Member", "full_name"], ["No.", "member_number"], ["Status", "status"]],
    },
    "bank_accounts": {
        "label": "Accounts", "system": "Core banking",
        "url": f"{BANK}/accounts.json", "shape": "plain",
        "cols": [["Member", "member_name"], ["Type", "account_type"], ["Balance", "balance"]],
    },
    "bank_transactions": {
        "label": "Transactions", "system": "Core banking",
        "url": f"{BANK}/transactions.json", "shape": "plain",
        "cols": [["Merchant", "merchant"], ["Amount", "amount"], ["Channel", "channel"]],
    },
    "hris_workers": {
        "label": "Workers", "system": "HRIS",
        "url": f"{HRIS}/workers.json", "shape": "plain",
        "cols": [["Worker", "full_name"], ["Role", "job_title"], ["Dept", "department_name"]],
    },
    "hris_time_off": {
        "label": "Time-off requests", "system": "HRIS",
        "url": f"{HRIS}/time_off_requests.json", "shape": "plain",
        "cols": [["Request", "request_number"], ["Days", "days"], ["Status", "status"]],
    },
    "erp_pos": {
        "label": "Purchase orders", "system": "ERP",
        "url": f"{ERP}/purchase_orders.json", "shape": "plain",
        "cols": [["PO", "po_number"], ["Supplier", "supplier_name"], ["Status", "status"]],
    },
    "erp_suppliers": {
        "label": "Suppliers", "system": "ERP",
        "url": f"{ERP}/suppliers.json", "shape": "plain",
        "cols": [["Supplier", "name"], ["Category", "category"], ["Terms", "payment_terms"]],
    },
    "itsm_incidents": {
        "label": "Incidents", "system": "ITSM",
        "url": f"{ITSM}/incident.json", "shape": "sn",
        "cols": [["Incident", "number"], ["Summary", "short_description"], ["Priority", "priority"]],
    },
}

# Citation targets. Dynamics list views deep-link the simulator's browsable
# UI (verified routes); other systems cite the raw live collection JSON —
# globally valid even when the demo viewer is offline.
CITES = {
    "d365_cases_ui": ("Cases — Dynamics 365 (simulated)", D365_UI + "#/cs/cases"),
    "d365_accounts_ui": ("Accounts — Dynamics 365 (simulated)", D365_UI + "#/cs/accounts"),
    "d365_contacts_ui": ("Contacts — Dynamics 365 (simulated)", D365_UI + "#/cs/contacts"),
    "d365_opps": ("Opportunities — Dynamics 365 (simulated)", f"{D365}/opportunities.json"),
    "sfdc_opps": ("Opportunities — Salesforce (simulated)", f"{SFDC}/Opportunity.json"),
    "sfdc_contacts": ("Contacts — Salesforce (simulated)", f"{SFDC}/Contact.json"),
    "sfdc_cases": ("Cases — Salesforce (simulated)", f"{SFDC}/Case.json"),
    "bank_members": ("Members — Core banking (simulated)", f"{BANK}/members.json"),
    "bank_accounts": ("Accounts — Core banking (simulated)", f"{BANK}/accounts.json"),
    "bank_transactions": ("Transactions — Core banking (simulated)", f"{BANK}/transactions.json"),
    "hris_workers": ("Workers — HRIS (simulated)", f"{HRIS}/workers.json"),
    "hris_time_off": ("Time-off requests — HRIS (simulated)", f"{HRIS}/time_off_requests.json"),
    "hris_departments": ("Departments — HRIS (simulated)", f"{HRIS}/departments.json"),
    "erp_pos": ("Purchase orders — ERP (simulated)", f"{ERP}/purchase_orders.json"),
    "erp_suppliers": ("Suppliers — ERP (simulated)", f"{ERP}/suppliers.json"),
    "erp_grn": ("Goods receipts — ERP (simulated)", f"{ERP}/goods_receipts.json"),
    "itsm_incidents": ("Incidents — ITSM (simulated)", f"{ITSM}/incident.json"),
    "enrich_summittrail": ("Company profile: summittrail.example — Enrichment (simulated)", f"{ENRICH}/companies/summittrail.example.json"),
}

# Record-id autolinks used by the in-page markdown renderer.
ID_LINKS = [
    ["CAS-\\d{4,}", D365_UI + "#/cs/cases"],
    ["INC\\d{6,}", f"{ITSM}/incident.json"],
    ["PO-\\d{4,}", f"{ERP}/purchase_orders.json"],
    ["GR-\\d{4,}", f"{ERP}/goods_receipts.json"],
    ["TOR-\\d{3,}", f"{HRIS}/time_off_requests.json"],
    ["MBR-\\d{3,}", f"{BANK}/members.json"],
    ["AL-\\d{4}", f"{HRIS}/workers.json"],
    ["AST-\\d{4}", D365_UI + "#/cs/accounts"],
]

# ---------------------------------------------------------------------------
# Demo definitions. Keys are the exact existing filenames (stable contract).
# turns = [{u, a (markdown w/ [n] cite markers), c: [cite keys]}, ...]
# Live adaptive card rule: agent turn i embeds the card for sources[i].
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
            {"u": "Brief me on Beacon Hill Staffing Partners before my 2pm call.",
             "a": "**Beacon Hill Staffing Partners** — Boston, MA (AST-1020) [1].\n"
                  "- **Relationship:** active customer; office-systems refresh completed last quarter.\n"
                  "- **Open pipeline:** printer fleet expansion, mid-stage, 40% probability [2].\n"
                  "- **Signal:** headcount growth at the Louisville branch suggests a device add-on.\n"
                  "- **Risk:** two support cases open this month — acknowledge them up front.\n"
                  "Suggested opener: reference the smooth refresh, then probe the branch expansion.",
             "c": ["d365_accounts_ui", "d365_opps"]},
            {"u": "Who are my strongest champions there?",
             "a": "Two contacts stand out [1]:\n"
                  "- **Operations lead** — sponsored the original refresh, responds within a day.\n"
                  "- **Facilities manager** — logged both support cases [2]; turning them into a win restores the champion.\n"
                  "I'd bring a one-slide case-resolution summary to the call.",
             "c": ["d365_contacts_ui", "d365_cases_ui"]},
            {"u": "Draft my three talking points.",
             "a": "1. **Refresh results** — uptime and cost numbers from last quarter's rollout.\n"
                  "2. **Louisville expansion** — propose a pilot bundle sized for the new branch.\n"
                  "3. **Service** — confirm both open cases have owners and dates [1], then ask for the renewal conversation.",
             "c": ["d365_cases_ui"]},
        ],
    },
    "b2b_deal_progression_demo.html": {
        "title": "B2B Deal Progression",
        "vertical": "B2B Sales",
        "tagline": "Pipeline analysis that spots stalled deals and recommends the next best action.",
        "persona": "Priya Nair, Regional Sales Manager",
        "sources": ["d365_opportunities", "sfdc_opportunities"],
        "turns": [
            {"u": "Which of my deals are stalled this quarter?",
             "a": "Three deals show **no stage movement in 21+ days** [1]:\n"
                  "- **Marigold Field Services** — qualified, stuck at 40%; no meeting since intro.\n"
                  "- **Riverbend Medical printer refresh** — proposal sent, silent for 3 weeks [2].\n"
                  "- **Prairie Wind Energy add-on** — waiting on a procurement contact.\n"
                  "Combined value at risk: roughly a third of your quarter.",
             "c": ["d365_opps", "sfdc_opps"]},
            {"u": "What should I do about Riverbend Medical?",
             "a": "The proposal went quiet after their facilities review [1]. Recommended sequence:\n"
                  "1. Re-engage the **clinical ops sponsor**, not procurement — she drove the evaluation.\n"
                  "2. Attach the uptime benchmark from their sister site.\n"
                  "3. Offer a 30-minute working session this week; silence usually means an internal blocker, not a no.",
             "c": ["sfdc_opps"]},
            {"u": "Update the forecast with what you see.",
             "a": "Done. **Marigold** stays Commit at 40%, **Riverbend** moves to Best Case pending re-engagement, **Prairie Wind** slips one month. Forecast delta logged to the opportunity records with today's notes [1].",
             "c": ["d365_opps"]},
        ],
    },
    "b2b_proposal_generation_demo.html": {
        "title": "B2B Proposal Generation",
        "vertical": "B2B Sales",
        "tagline": "First-draft proposals assembled from CRM context, pricing, and past wins.",
        "persona": "Marcus Todd, Solutions Consultant",
        "sources": ["d365_opportunities", "d365_accounts"],
        "turns": [
            {"u": "Draft a proposal for the Summit Trail Software office refresh.",
             "a": "Draft assembled from the opportunity record [1] and two comparable wins:\n"
                  "- **Scope:** 3 floors, managed print plus device refresh, phased over 6 weeks.\n"
                  "- **Pricing:** mid-tier bundle with the software-vertical discount applied.\n"
                  "- **Proof points:** two anonymized case studies with 18% cost reduction.\n"
                  "Sections ready: Executive Summary, Scope, Timeline, Pricing, Terms. Firmographics pulled from the enrichment profile [2].",
             "c": ["d365_opps", "enrich_summittrail"]},
            {"u": "Tighten the executive summary to five sentences.",
             "a": "Done:\n"
                  "\"Summit Trail Software [1] is scaling faster than its office infrastructure. This proposal replaces aging devices across three floors with a managed fleet sized to your growth plan. Rollout completes in six weeks with zero downtime to your teams. Comparable customers cut print and device costs by 18% in year one. We can begin the pilot floor within two weeks of signature.\"",
             "c": ["d365_accounts_ui"]},
            {"u": "What's the riskiest assumption in this draft?",
             "a": "The **6-week timeline** assumes their IT team can provision network access per floor within 3 business days each phase. Flag it in Terms, or pad phase two by a week — that's where comparable projects slipped.",
             "c": []},
        ],
    },
    "b2b_sales_qualification_demo.html": {
        "title": "B2B Sales Qualification",
        "vertical": "B2B Sales",
        "tagline": "Inbound leads scored and qualified against your ideal customer profile.",
        "persona": "Dana Whitfield, Sales Development Rep",
        "sources": ["d365_accounts", "sfdc_contacts"],
        "turns": [
            {"u": "Qualify this inbound: facilities director at a 175-person software company asking about managed print.",
             "a": "**Strong fit — score 82/100.**\n"
                  "- **Size:** 51–200 employees is your core segment [1].\n"
                  "- **Role:** facilities director is a typical economic buyer.\n"
                  "- **Intent:** \"managed print\" is a solution-aware query, not research.\n"
                  "- **Match:** profile resembles Summit Trail Software, a closed-won account [2].\n"
                  "Suggested route: AE-led discovery call, not nurture.",
             "c": ["enrich_summittrail", "d365_accounts_ui"]},
            {"u": "What discovery questions should the AE open with?",
             "a": "1. What triggered the search now — growth, cost, or a contract expiring?\n"
                  "2. How many devices and floors are in scope?\n"
                  "3. Who besides you signs off on facilities spend?\n"
                  "4. What would make this a win in 90 days?",
             "c": []},
            {"u": "Log it and set the follow-up.",
             "a": "**Lead created, scored, and routed** to the enterprise queue [1]. Discovery call proposed for Thursday; confirmation email drafted for your review. The account is linked to its firmographic profile [2] so the AE sees headcount and funding stage at a glance.",
             "c": ["d365_accounts_ui", "enrich_summittrail"]},
        ],
    },
    "b2b_win_loss_analysis_demo.html": {
        "title": "B2B Win/Loss Analysis",
        "vertical": "B2B Sales",
        "tagline": "Patterns across closed deals turned into coaching and playbook updates.",
        "persona": "Elena Vasquez, VP of Sales",
        "sources": ["sfdc_opportunities", "d365_opportunities"],
        "turns": [
            {"u": "What patterns separate our wins from losses this half?",
             "a": "Across closed deals [1][2]:\n"
                  "- Wins averaged **2.4 stakeholders** engaged; losses averaged 1.1 — single-threaded deals lose.\n"
                  "- Deals with a **pilot phase** won 3x more often than proposal-only pursuits.\n"
                  "- Losses cluster where first response took **over 2 days**.\n"
                  "- Pricing was cited in only 1 of 5 losses — access, not price, is the problem.",
             "c": ["sfdc_opps", "d365_opps"]},
            {"u": "Which rep behaviors should we coach on?",
             "a": "Two, in order of impact:\n"
                  "1. **Multi-threading:** require a second stakeholder before stage 3. Reps who do this show a 20-point higher win rate [1].\n"
                  "2. **Pilot-first proposals:** replace the big-bang quote with a pilot floor or branch. It shortened cycles by two weeks in winning deals.",
             "c": ["sfdc_opps"]},
            {"u": "Summarize this for Monday's pipeline review.",
             "a": "One slide, three bullets: **single-threaded deals lose twice as often; pilots win 3x; respond in 48 hours or don't bother.** Full breakdown with the deal list [1] is attached to the review notes.",
             "c": ["d365_opps"]},
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
            {"u": "Who abandoned carts in the last 24 hours and what do we know about them?",
             "a": "Overnight: **47 abandoned carts, 12 above the $100 threshold.**\n"
                  "- 8 are repeat customers [1] — highest recovery odds.\n"
                  "- **Top cart:** returning customer, standing desk bundle, exited at shipping cost.\n"
                  "- **Pattern:** 60% of exits happened on the shipping step, not payment.\n"
                  "Recommended: free-shipping nudge for the shipping-step cohort only.",
             "c": ["sfdc_contacts"]},
            {"u": "Draft the recovery email for the standing desk customer.",
             "a": "**Subject:** Your desk is still here — shipping's on us\n"
                  "\"Hi — you left the standing desk bundle in your cart yesterday. Good news: we'll cover shipping on this order. Your cart is saved and ready; this offer holds for 48 hours. Questions about setup or delivery? Just reply.\"\n"
                  "Tone matches their two previous purchases [1]; no discount on the product itself, so margin holds.",
             "c": ["d365_contacts_ui"]},
            {"u": "What results should I expect?",
             "a": "For repeat customers with a shipping incentive, comparable campaigns recover **18–25%**. For the 12-cart cohort that's 2–3 orders. I'll track opens and recoveries and report in 48 hours when the offer window closes.",
             "c": []},
        ],
    },
    "b2c_customer_360_speech_demo.html": {
        "title": "B2C Customer 360 (Speech)",
        "vertical": "B2C Sales",
        "tagline": "A spoken query becomes a full customer profile before the call connects.",
        "persona": "Riley Santos, Contact Center Agent",
        "sources": ["d365_contacts", "d365_incidents"],
        "turns": [
            {"u": "\"Pull up the customer calling from the Louisville area code.\"",
             "a": "**Match: Marcus Webb**, Member Services Manager, Louisville KY [1].\n"
                  "- Customer for 2 years, 6 orders, no returns.\n"
                  "- **Open case:** delivery inquiry from last week, still unassigned [2].\n"
                  "- **Sentiment:** last survey positive.\n"
                  "Likely reason for call: the open delivery case. Suggested opener: acknowledge it before he asks.",
             "c": ["d365_contacts_ui", "d365_cases_ui"]},
            {"u": "\"What happened with that delivery case?\"",
             "a": "Order shipped in two packages; the second missed its window and the case sat unassigned for 5 days [1]. Carrier now shows it **out for delivery today**. Recommended: confirm today's delivery, apologize for the silence, and offer to stay on the case until it lands.",
             "c": ["d365_cases_ui"]},
            {"u": "\"Log the call and close the loop.\"",
             "a": "**Logged:** call summary attached to the case [1], follow-up task set for tomorrow to confirm delivery, and a case owner assigned so nothing sits unowned again. Marcus gets a confirmation text with the tracking link.",
             "c": ["d365_cases_ui"]},
        ],
    },
    "b2c_customer_loyalty_rewards_demo.html": {
        "title": "B2C Customer Loyalty & Rewards",
        "vertical": "B2C Sales",
        "tagline": "Loyalty balances, tier moves, and reward offers handled conversationally.",
        "persona": "Morgan Blake, Loyalty Program Manager",
        "sources": ["d365_contacts", "sfdc_contacts"],
        "turns": [
            {"u": "Which members are close to the next tier and worth a nudge?",
             "a": "**23 members are within 15% of Gold** [1].\n"
                  "- 9 purchased in the last 30 days — the momentum cohort, best nudge candidates.\n"
                  "- 5 have been inactive 60+ days — a tier nudge alone won't move them.\n"
                  "- **Top candidate:** 2-year customer, 40 points from Gold, browses weekly.\n"
                  "Suggested: \"40 points to Gold\" message with a small accelerator on their usual category.",
             "c": ["d365_contacts_ui"]},
            {"u": "What does the accelerator cost us versus the upside?",
             "a": "Double points on one category purchase costs roughly **$4 per redemption**. Gold members historically spend 30% more over the following 6 months [1]. Break-even is one incremental purchase; the momentum cohort averages 1.8 per month. The economics favor the nudge for all 9.",
             "c": ["sfdc_contacts"]},
            {"u": "Launch it for the momentum cohort.",
             "a": "Done — **9 personalized messages queued** with each member's points-to-Gold number and category accelerator. The results dashboard tracks tier conversions over 30 days; anyone who converts gets their welcome-to-Gold message same-day.",
             "c": []},
        ],
    },
    "b2c_omnichannel_engagement_demo.html": {
        "title": "B2C Omnichannel Engagement",
        "vertical": "B2C Sales",
        "tagline": "One customer, one conversation — across store, web, and support channels.",
        "persona": "Sam Porter, Customer Experience Lead",
        "sources": ["d365_contacts", "d365_incidents"],
        "turns": [
            {"u": "A customer emailed, then called, then walked into the Erie store about the same order. What's the full picture?",
             "a": "Timeline stitched across channels [1][2]:\n"
                  "- **Mon:** email asking to change the delivery address — auto-reply only.\n"
                  "- **Tue:** call, 8 minutes; agent updated the address but never confirmed by email.\n"
                  "- **Today:** store visit — the store system still shows the old address.\n"
                  "**Root cause:** the address change synced to shipping but not to the store view. The customer was right three times.",
             "c": ["d365_contacts_ui", "d365_cases_ui"]},
            {"u": "What should the store associate say right now?",
             "a": "\"You're all set — the address change **did** go through on Tuesday; our store screen just hadn't caught up. Your order ships to the new address tomorrow. I've flagged the sync issue so this doesn't happen again, and you'll get a confirmation email in the next few minutes.\" Send the confirmation now [1]; it was the missing step.",
             "c": ["d365_cases_ui"]},
            {"u": "Prevent this class of issue.",
             "a": "Two fixes logged:\n"
                  "1. Address changes now trigger a **customer confirmation on every channel**.\n"
                  "2. A **sync-lag alert** flags orders whose store view is older than the CRM record [1].\n"
                  "Both routed to the platform backlog with this case as the evidence.",
             "c": ["d365_cases_ui"]},
        ],
    },
    "b2c_personalized_shopping_assistant_demo.html": {
        "title": "B2C Personalized Shopping Assistant",
        "vertical": "B2C Sales",
        "tagline": "Recommendations grounded in purchase history, not generic bestsellers.",
        "persona": "Taylor Kim, Digital Commerce Lead",
        "sources": ["sfdc_contacts", "d365_contacts"],
        "turns": [
            {"u": "A returning customer asks: \"I need to outfit a small home office, what do you recommend?\"",
             "a": "Based on their history [1] (ergonomic chair, cable kit — a quality-tier buyer):\n"
                  "- **Desk:** the mid-depth standing desk that pairs with their chair, in the walnut finish they browsed twice.\n"
                  "- **Lighting:** the glare-free task lamp — they bought a monitor last quarter.\n"
                  "- **Skip:** the budget bundle; their history says they trade up.\n"
                  "Total lands inside the typical home-office budget with room for delivery.",
             "c": ["sfdc_contacts"]},
            {"u": "They ask if the desk works in a small apartment.",
             "a": "Yes — recommend the **48-inch width**: it fits a 9-foot wall with a chair beside it, and the frame is the same one in the larger sizes so stability doesn't drop. If space is the top concern, the wall-fold desk is the alternative, but it won't hold their dual-monitor setup [1]. Honest answer: 48-inch standing desk.",
             "c": ["d365_contacts_ui"]},
            {"u": "Close the conversation well.",
             "a": "\"The 48-inch walnut standing desk fits your space and matches your chair. It's in stock — **delivery Thursday, free assembly included this month**. Want me to add the cable tray so the setup stays clean?\" One relevant add-on, then stop selling.",
             "c": []},
        ],
    },
    "b2c_returns_exchange_demo.html": {
        "title": "B2C Returns & Exchange",
        "vertical": "B2C Sales",
        "tagline": "Returns resolved in one conversation — policy, label, and refund status included.",
        "persona": "Jordan Avery, Returns Team Lead",
        "sources": ["d365_incidents", "sfdc_cases"],
        "turns": [
            {"u": "Customer wants to return a desk chair bought 35 days ago. Policy is 30 days. What do we do?",
             "a": "**Recommend the exception.** The record shows [1]:\n"
                  "- First return in 6 orders across 2 years.\n"
                  "- The chair model has an elevated return rate for a **known armrest defect** [2].\n"
                  "- Cost of the exception: restocking. Cost of refusing: likely the customer.\n"
                  "Offer: full refund or exchange for the updated model, their choice. Exception logged with the defect code so it counts toward the quality report.",
             "c": ["d365_cases_ui", "sfdc_cases"]},
            {"u": "They choose the exchange. Handle it.",
             "a": "Done:\n"
                  "- Exchange order created for the updated model, **ships tomorrow**.\n"
                  "- Prepaid return label emailed; pickup available Thursday.\n"
                  "- No charge difference — price-protected as a defect exchange.\n"
                  "- Case linked to the armrest defect tally [1] — that's the 14th this quarter, flagged to quality.",
             "c": ["sfdc_cases"]},
            {"u": "What should the confirmation message say?",
             "a": "\"Your exchange is confirmed. The updated chair ships tomorrow; your return label is in your inbox and pickup is available Thursday. No charge for the swap. Thanks for giving us the chance to make it right.\" Short, no policy lecture, no survey link in the same message.",
             "c": []},
        ],
    },
    "b2c_sales_chat_demo.html": {
        "title": "B2C Sales Chat",
        "vertical": "B2C Sales",
        "tagline": "Website chat that answers, recommends, and closes without handing off.",
        "persona": "Website visitor, evening traffic",
        "sources": ["sfdc_contacts", "d365_accounts"],
        "turns": [
            {"u": "Do you have standing desks under $400 that ship this week?",
             "a": "Yes — two options in stock:\n"
                  "| Model | Price | Arrives |\n"
                  "| 48-inch electric standing desk | $349 | Thursday |\n"
                  "| 42-inch compact model | $289 | Thursday |\n"
                  "Both include the 30-day trial. The 48-inch is the better pick if you run two monitors. Want dimensions or the weight limit?",
             "c": []},
            {"u": "What's the weight limit on the 48-inch, and is assembly hard?",
             "a": "**Weight limit: 220 lbs** — dual monitors, a desktop tower, and accessories are fine. Assembly is about 25 minutes with the included tool; most of it is attaching the top to the frame. This month **assembly service is free** if you'd rather skip it.",
             "c": []},
            {"u": "OK, I'll take it with the free assembly.",
             "a": "Great choice. I've added the **48-inch desk with free assembly — $349 total**, delivery and setup Thursday. Checkout takes about a minute from here; your cart is saved to your profile [1] if you need to step away. Anything else for the office?",
             "c": ["sfdc_contacts"]},
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
            {"u": "Triage this morning's new claims queue.",
             "a": "**14 new claims triaged** [1]:\n"
                  "- **9 straight-through candidates:** complete documentation, within policy limits, no fraud flags — ready for auto-approval review.\n"
                  "- **3 need documents:** one missing a repair estimate, two missing incident dates.\n"
                  "- **2 escalations:** one exceeds the authority limit, one has a date inconsistency worth a human look.\n"
                  "Fastest win: approve the 9 clean ones before lunch.",
             "c": ["bank_members"]},
            {"u": "Show me the date inconsistency case.",
             "a": "Claim filed Monday for an incident dated Sunday — but the attached statement shows a related transaction posted the previous Wednesday [1]. Could be an honest date error; could be a backdated claim. **Recommendation: request clarification, not denial.** Drafted a neutral message asking the member to confirm the incident date.",
             "c": ["bank_transactions"]},
            {"u": "Approve the clean nine and send the clarification.",
             "a": "Done. **Nine claims approved** and queued for payment — members get status notifications now [1]. The clarification request went out with a 5-day response window, and the two document requests include upload links. Queue is clear; next batch arrives at 1pm.",
             "c": ["bank_members"]},
        ],
    },
    "fsi_customer_sentiment_churn_demo.html": {
        "title": "FSI Sentiment & Churn",
        "vertical": "Financial Services",
        "tagline": "Early churn signals from balances, transactions, and support tone.",
        "persona": "David Osei, Head of Member Experience",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            {"u": "Which members show churn risk this month?",
             "a": "**7 members flagged, 3 high-priority** [1]:\n"
                  "- **MBR-2001:** payroll deposit stopped 6 weeks ago [2] — the classic leaving-signal.\n"
                  "- One member moved 80% of savings out over two months, no product complaints.\n"
                  "- One had two disputed transactions and a frustrated support call in 30 days.\n"
                  "The payroll-stop member has been with you 6 years — highest lifetime value at risk.",
             "c": ["bank_members", "bank_transactions"]},
            {"u": "What's the right intervention for the payroll-stop member?",
             "a": "**Not a retention offer — a check-in.** Payroll stops usually mean a job change; the account decision [1] hasn't been made yet. Recommended: personal call from her branch, ask how the transition is going, and mention direct-deposit switching takes one form. If she's already decided, ask what would have changed it — that's your churn data.",
             "c": ["bank_accounts"]},
            {"u": "Set up the outreach for all three.",
             "a": "Done:\n"
                  "- **Branch call task** for the payroll-stop member (assigned to the banker she's met) [1].\n"
                  "- **Savings-rate review** invitation for the mover.\n"
                  "- **Service-recovery call** plus dispute-fee refund for the frustrated member.\n"
                  "All three logged with follow-up dates; outcomes reported in two weeks.",
             "c": ["bank_members"]},
        ],
    },
    "fsi_financial_advisor_copilot_demo.html": {
        "title": "FSI Financial Advisor Copilot",
        "vertical": "Financial Services",
        "tagline": "Meeting prep, portfolio context, and follow-ups for advisors.",
        "persona": "Sarah Lindqvist, Financial Advisor",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            {"u": "Prep me for my 10am with Denise Calloway.",
             "a": "**Denise Calloway (MBR-2001)**, member since 2020 [1]:\n"
                  "- Checking healthy; savings up 12% this year [2] — a consistent saver.\n"
                  "- **Last meeting:** asked about education savings for her daughter.\n"
                  "- **Open item:** the 529 comparison you promised — attached, ready to walk through.\n"
                  "- **Life signal:** payroll deposits show a recent raise.\n"
                  "Agenda: 529 decision first; the raise is a natural opening for a retirement contribution.",
             "c": ["bank_members", "bank_accounts"]},
            {"u": "Summarize the 529 comparison in plain language.",
             "a": "Two solid options: the **state plan** gives her a tax deduction now and good-enough funds; the **national plan** has slightly better fund choices but no deduction. For her bracket the deduction wins unless she expects to move states. Plain recommendation: state plan, automatic monthly contribution sized to the raise [1].",
             "c": ["bank_accounts"]},
            {"u": "Log the meeting plan and set follow-ups.",
             "a": "**Logged.** After the meeting I'll capture decisions against this plan. Pre-set follow-ups: 529 enrollment check-in (2 weeks), contribution confirmation (next statement) [1], and an annual review placeholder. Compliance note attached — education-savings discussion, no securities recommendations made.",
             "c": ["bank_members"]},
        ],
    },
    "fsi_financial_insights_demo.html": {
        "title": "FSI Financial Insights",
        "vertical": "Financial Services",
        "tagline": "Member-facing spending insight that's specific, not generic.",
        "persona": "Member self-service, mobile app",
        "sources": ["bank_transactions", "bank_accounts"],
        "turns": [
            {"u": "Where did my money go last month?",
             "a": "**Your month at a glance** [1]:\n"
                  "- **Income:** payroll deposits as usual, plus one refund.\n"
                  "- **Biggest categories:** rent, groceries (up 8%), and subscriptions.\n"
                  "- **Noticed:** three subscriptions renewed within 4 days — about $47/month combined.\n"
                  "- **Good news:** you saved 11% of income, above your 3-month average [2].\n"
                  "Want the subscription list?",
             "c": ["bank_transactions", "bank_accounts"]},
            {"u": "Yes — which subscriptions, and which should I cancel?",
             "a": "The three renewals [1]:\n"
                  "| Subscription | Monthly |\n"
                  "| Streaming | $15.99 |\n"
                  "| Fitness app | $12.99 |\n"
                  "| Cloud storage | $17.99 |\n"
                  "Usage signal: the fitness app hasn't had a linked-card gym or store transaction in 4 months. I can't know what you value — but that's the one to look at. Canceling saves **$156/year**.",
             "c": ["bank_transactions"]},
            {"u": "Move that $13 a month into savings automatically.",
             "a": "Done — a **$13 monthly auto-transfer to savings** starts on your next payroll date [1]. Small but real: $156/year plus dividends. I'll flag it in next month's summary so you can watch the habit form.",
             "c": ["bank_accounts"]},
        ],
    },
    "fsi_fraud_detection_alert_demo.html": {
        "title": "FSI Fraud Detection & Alert",
        "vertical": "Financial Services",
        "tagline": "Suspicious activity caught, explained, and resolved without drama.",
        "persona": "Fraud Operations, real-time queue",
        "sources": ["bank_transactions", "bank_accounts"],
        "turns": [
            {"u": "Why did the system flag this card transaction?",
             "a": "**Three stacked signals, not one** [1]:\n"
                  "- Merchant category the member has never used, 900 miles from home.\n"
                  "- Amount **6x their average** card transaction.\n"
                  "- Second attempt 90 seconds after a decline.\n"
                  "Individually weak; together they cross the threshold. Card is **soft-held** pending member confirmation — nothing is declined permanently yet.",
             "c": ["bank_transactions"]},
            {"u": "The member confirmed it's fraud. Walk through the response.",
             "a": "Executing now:\n"
                  "1. **Card blocked**, replacement issued — arrives in 3 business days, digital card usable immediately.\n"
                  "2. **Provisional credit** posted for the disputed amount [1].\n"
                  "3. **Dispute case opened** with the network, evidence packet attached.\n"
                  "4. Recent transactions scanned — no other anomalies on this account.\n"
                  "The member gets a plain-language summary of all four steps.",
             "c": ["bank_accounts"]},
            {"u": "Any pattern across other members?",
             "a": "Yes — the **same merchant descriptor** hit two other members this week [1], both declined by the same rule. Pattern packaged and reported: merchant added to the watch list and the network notified. Your rule caught a small ring, not a one-off.",
             "c": ["bank_transactions"]},
        ],
    },
    "fsi_loan_origination_assistant_demo.html": {
        "title": "FSI Loan Origination Assistant",
        "vertical": "Financial Services",
        "tagline": "Applications completed, verified, and decision-ready in one pass.",
        "persona": "Kevin Marsh, Lending Officer",
        "sources": ["bank_members", "bank_accounts"],
        "turns": [
            {"u": "Review the auto loan application that just came in.",
             "a": "Application from a **4-year member, $24,000 auto loan** [1]:\n"
                  "- **Income:** verified from 12 months of payroll deposits — no paystub chase needed.\n"
                  "- **Debt-to-income:** 31%, inside guideline.\n"
                  "- **Banking behavior:** no overdrafts in 24 months, stable balances [2].\n"
                  "- **Missing:** the vehicle purchase agreement.\n"
                  "Everything else is decision-ready. Request the purchase agreement and this can close this week.",
             "c": ["bank_members", "bank_accounts"]},
            {"u": "What rate does she qualify for?",
             "a": "Based on tier-2 credit and the **relationship discount** (checking + direct deposit [1]), she qualifies for your posted rate **minus 0.25%**. That discount is the difference between you and the dealer's financing offer — lead with it. Monthly payment lands around $455 on a 60-month term.",
             "c": ["bank_accounts"]},
            {"u": "Send the offer and the document request together.",
             "a": "Sent — **one message, not two**: conditional approval at the relationship rate, a payment example, and a secure upload link for the purchase agreement. The application auto-advances the moment the document lands [1]. Average close time on this path: 2 days.",
             "c": ["bank_members"]},
        ],
    },
    "fsi_portfolio_rebalancing_demo.html": {
        "title": "FSI Portfolio Rebalancing",
        "vertical": "Financial Services",
        "tagline": "Drift detection and rebalancing proposals an advisor can defend.",
        "persona": "Rachel Yoon, Portfolio Manager",
        "sources": ["bank_accounts", "bank_members"],
        "turns": [
            {"u": "Which client portfolios have drifted past tolerance?",
             "a": "**12 of 240 portfolios exceed the 5% drift band** [1]:\n"
                  "- 8 drifted from equity outperformance — standard trim-and-redeploy.\n"
                  "- 3 drifted from a **concentrated position** appreciating — needs a client conversation, not just a trade.\n"
                  "- 1 is a cash buildup from an inheritance deposit — allocation conversation.\n"
                  "None require same-day action; all 12 have proposals drafted.",
             "c": ["bank_accounts"]},
            {"u": "Show me the concentrated-position case.",
             "a": "Client holds a single stock now at **19% of the portfolio** (policy cap: 10%) [1]. Complication: low cost basis, so a full trim triggers meaningful capital gains. **Proposal:** staged trim across two tax years, harvesting available losses against the first tranche, with a collar considered for downside protection meanwhile. Talking points drafted in plain language.",
             "c": ["bank_members"]},
            {"u": "Approve the 8 standard rebalances.",
             "a": "**Approved and queued** for execution at tomorrow's open. Trade rationale, before/after allocations, and cost estimates are attached to each client record [1] — audit-ready. The 3 concentrated cases and the cash-buildup client are on your call list with proposals attached.",
             "c": ["bank_accounts"]},
        ],
    },
    "fsi_regulatory_compliance_demo.html": {
        "title": "FSI Regulatory Compliance",
        "vertical": "Financial Services",
        "tagline": "Monitoring, evidence, and exam-ready answers without the scramble.",
        "persona": "Nina Petrova, Chief Compliance Officer",
        "sources": ["bank_transactions", "bank_members"],
        "turns": [
            {"u": "What needs my attention in this week's compliance review?",
             "a": "**Three items, one urgent:**\n"
                  "- **Urgent:** 2 currency transaction reports approach their filing deadline tomorrow — drafted, awaiting sign-off.\n"
                  "- **A structuring pattern:** one member made 4 deposits just under the reporting threshold in 10 days [1] — SAR evaluation recommended.\n"
                  "- **Routine:** monthly OFAC screening completed, zero matches, evidence archived.\n"
                  "Sign-offs first; they're time-boxed.",
             "c": ["bank_transactions"]},
            {"u": "Walk me through the structuring pattern before I decide.",
             "a": "Four cash deposits of **$9,200–$9,800 across three branches in 10 days** [1] — amounts, timing, and branch-hopping all consistent with structuring. Context that matters: the member owns a cash-heavy business but historically deposited weekly at one branch [2]. **The behavior change is the signal.** Recommendation: file the SAR; the narrative is drafted with the transaction table attached. Filing is protective either way.",
             "c": ["bank_transactions", "bank_members"]},
            {"u": "File it, and show me our exam readiness.",
             "a": "**SAR filed**, confirmation number logged. Exam readiness: all filings current, monitoring rules documented with change history, and every alert this quarter shows a decision trail [1] — including the ones we chose not to escalate, with reasons. That last part is what examiners actually test.",
             "c": ["bank_transactions"]},
        ],
    },
    "fsi_underwriting_support_demo.html": {
        "title": "FSI Underwriting Support",
        "vertical": "Financial Services",
        "tagline": "Files assembled, ratios computed, exceptions surfaced — underwriters decide.",
        "persona": "Tom Garrett, Senior Underwriter",
        "sources": ["bank_members", "bank_transactions"],
        "turns": [
            {"u": "Prepare the mortgage file that came in overnight.",
             "a": "**File assembled and verified** [1]:\n"
                  "- **Income:** two salaried borrowers, verified against deposit history [2] — matches stated within 2%.\n"
                  "- **DTI:** 36% front, 41% back — inside guideline, no compensating factors needed.\n"
                  "- **Assets:** down payment sourced and seasoned; one $8,000 deposit needs a letter of explanation.\n"
                  "- **Property:** appraisal ordered, due Friday.\n"
                  "One document request, then this file is decision-ready.",
             "c": ["bank_members", "bank_transactions"]},
            {"u": "What's the story on that $8,000 deposit?",
             "a": "It arrived 6 weeks ago from an account with a matching surname [1] — almost certainly a family gift. That's fine, but it needs the **gift letter and donor statement** to satisfy sourcing rules. Request drafted. Flag for you: if it were a loan, the DTI moves to 43% — still passing, but tighter. The letter settles it either way.",
             "c": ["bank_transactions"]},
            {"u": "Anything in the bank activity an automated score would miss?",
             "a": "Two things worth knowing [1]:\n"
                  "- A recurring monthly transfer out that looks like **informal rent-to-family** — not on the credit report but a real obligation.\n"
                  "- **Deposit consistency through a job change** last year — they never missed savings contributions.\n"
                  "One caution, one strength. Both noted in the file summary.",
             "c": ["bank_transactions"]},
        ],
    },
    "fsi_wealth_insights_generator_demo.html": {
        "title": "FSI Wealth Insights Generator",
        "vertical": "Financial Services",
        "tagline": "Client-ready portfolio narratives generated from real positions.",
        "persona": "Leah Armstrong, Wealth Advisor",
        "sources": ["bank_accounts", "bank_members"],
        "turns": [
            {"u": "Generate the quarterly insight letter for my top client.",
             "a": "**Draft ready.** The quarter in three points [1]:\n"
                  "- Portfolio up modestly, tracking the plan benchmark within half a percent — allocation working as designed.\n"
                  "- Cash from the business sale is now **14% of assets** — above target and the letter's main conversation starter.\n"
                  "- **Tax:** harvested losses from the spring rotation offset most realized gains.\n"
                  "Tone matches your previous letters; two paragraphs, then the numbers table.",
             "c": ["bank_accounts"]},
            {"u": "Make the cash point feel like an opportunity, not a scolding.",
             "a": "Revised: \"The proceeds from the sale give us a rare position of flexibility — 14% in cash while markets are choppy is a comfortable place to decide from, not a problem to fix. When we meet, I'd like to walk through three ways to put it to work at your pace, including keeping a larger reserve if that's what lets you sleep well.\" **Choice framing, no urgency pressure.**",
             "c": []},
            {"u": "Add a personal touch and send for my review.",
             "a": "Added a closing line referencing the daughter's graduation he mentioned last call (**from your meeting notes** [1], not assumed). Letter is in your drafts with the numbers table and disclosure block attached. Nothing sends without your sign-off.",
             "c": ["bank_members"]},
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
            {"u": "My order arrived damaged — the desk top has a crack across the corner.",
             "a": "I'm sorry — that shouldn't have made it out of the warehouse. Here's what I can do right now:\n"
                  "- **Replacement top** ships free, arrives in 3–4 business days, or\n"
                  "- **20% refund** if the crack is cosmetic and you'd rather keep it.\n"
                  "No need to return the damaged piece either way. Which works better? A photo helps me file the carrier claim, but it won't hold up your resolution.",
             "c": []},
            {"u": "Replacement please. Will someone install it?",
             "a": "Replacement ordered — **case CAS-260142 created** [1], confirmation on its way to your email. Installation: swapping the top takes about 15 minutes with the included tool, and I've attached the 4-step guide. If you'd rather not, I can schedule a technician visit for a flat $35 — most people find the swap easy, honestly.",
             "c": ["d365_cases_ui"]},
            {"u": "I'll do it myself. Thanks for making that painless.",
             "a": "Glad it was easy — that's the goal. Your replacement top **arrives Thursday** with tracking in your inbox, and case CAS-260142 stays open until you confirm it's sorted [1]. Reply to any of our emails if something's off. Enjoy the desk once it's whole again.",
             "c": ["d365_cases_ui"]},
        ],
    },
    "general_ask_hr_demo.html": {
        "title": "Ask HR",
        "vertical": "Cross-Industry",
        "tagline": "Policy answers and HR transactions in the flow of work.",
        "persona": "Employee self-service, Teams",
        "sources": ["hris_workers", "hris_time_off"],
        "turns": [
            {"u": "How much vacation do I have left, and can I take the first week of March off?",
             "a": "You have **9 vacation days remaining** this year [1].\n"
                  "March 2–6 looks workable: no team blackout dates, and only one teammate (of six) has overlapping time off [2]. Your manager Morgan Ellis typically approves within a day. Want me to submit the request?",
             "c": ["hris_workers", "hris_time_off"]},
            {"u": "Yes, submit it. Also — what's the policy if I need to extend by a day or two?",
             "a": "**Submitted — request TOR-1044**, 5 days, March 2–6, routed to Morgan [1].\n"
                  "**Extensions:** submit the extra days as a new request, even mid-trip. If you're out of balance, up to 2 days can go as unpaid with manager approval. No penalty for asking late, though earlier is kinder to the team calendar.",
             "c": ["hris_time_off"]},
            {"u": "What happens to unused days at year end?",
             "a": "You can **carry over up to 5 days**; they expire March 31. Anything beyond 5 is use-it-or-lose-it. With 4 days left after this request [1], you're under the cap — nothing at risk. I'll nudge you in November if you still have days on the table.",
             "c": ["hris_time_off"]},
        ],
    },
    "general_customer_360_demo.html": {
        "title": "Customer 360",
        "vertical": "Cross-Industry",
        "tagline": "Every system's view of one customer, stitched into a single brief.",
        "persona": "Account team, weekly review",
        "sources": ["d365_accounts", "sfdc_contacts"],
        "turns": [
            {"u": "Give me the full picture on Silver Elm Logistics.",
             "a": "**Silver Elm Logistics** — stitched from CRM, support, and finance [1]:\n"
                  "- **Commercial:** active customer, mid-market tier, renewal in 4 months.\n"
                  "- **Support:** 2 cases this quarter, both resolved inside SLA [2] — health is good.\n"
                  "- **Finance:** invoices current, no disputes.\n"
                  "- **Signal:** their ops director just changed — new stakeholder, relationship not yet built.\n"
                  "One risk, one action: meet the new ops director before renewal season.",
             "c": ["d365_accounts_ui", "d365_cases_ui"]},
            {"u": "What do we know about the new ops director?",
             "a": "Limited but useful [1]: promoted internally from the warehouse team, so she's lived with your product daily — an informed buyer, which cuts both ways. No direct contact history with your team yet. **Best introduction path:** your implementation engineer worked with her during rollout and is remembered well. Warm intro beats cold outreach here.",
             "c": ["sfdc_contacts"]},
            {"u": "Set up the renewal play.",
             "a": "Done:\n"
                  "- **Intro request** drafted for your implementation engineer.\n"
                  "- **Renewal opportunity** created at the 4-month horizon [1].\n"
                  "- **Health snapshot** pinned to the account so anyone touching Silver Elm sees the same picture.\n"
                  "Next review flags if the intro hasn't happened in 3 weeks.",
             "c": ["d365_opps"]},
        ],
    },
    "general_procurement_support_demo.html": {
        "title": "Procurement Support",
        "vertical": "Cross-Industry",
        "tagline": "PO status, supplier answers, and exception handling without the email chase.",
        "persona": "Procurement operations, daily standup",
        "sources": ["erp_pos", "erp_suppliers"],
        "turns": [
            {"u": "Which purchase orders need attention today?",
             "a": "Of **15 open POs**, three need action [1]:\n"
                  "- **PO-47012 (Granite Peak Manufacturing):** delivery due in 2 days, no shipping confirmation yet — chase now.\n"
                  "- One PO has a goods receipt posted but quantity **short by 12 units** [2] — decide: partial accept or claim.\n"
                  "- One invoice arrived **4% over PO price** — blocked for tolerance, awaiting your review.\n"
                  "The other 12 are on track.",
             "c": ["erp_pos", "erp_grn"]},
            {"u": "Chase Granite Peak and give me context for the call.",
             "a": "Status request sent through the supplier portal. Context [1]: **Granite Peak is NET30, precision machining**, historically reliable — 94% on-time over 12 months, and their two late deliveries were both flagged in advance. Silence is unusual for them, which suggests a portal miss rather than a real delay. If they confirm slippage, the cart-frame line is the one that gates your production schedule.",
             "c": ["erp_suppliers"]},
            {"u": "Resolve the price-variance invoice.",
             "a": "Reviewed: the 4% increase matches the supplier's **announced surcharge effective last month** — the PO was cut at the old price [1]. Options: accept with a note (the surcharge is contractual), or dispute and delay payment on a valid charge. **Recommended: accept**, and I've queued a price-list update so the next PO prices correctly. Block released pending your click.",
             "c": ["erp_pos"]},
        ],
    },
    "general_sales_coach_demo.html": {
        "title": "Sales Coach",
        "vertical": "Cross-Industry",
        "tagline": "Deal-specific coaching grounded in your own pipeline, not platitudes.",
        "persona": "Rep one-on-one prep",
        "sources": ["d365_opportunities", "d365_accounts"],
        "turns": [
            {"u": "Coach me on my Prairie Wind Energy deal before the demo tomorrow.",
             "a": "Where the deal actually stands [1]:\n"
                  "- **Strength:** the technical evaluator is engaged — 3 meetings, fast replies.\n"
                  "- **Gap:** no economic-buyer contact in 6 weeks of activity. That's the deal risk, not the demo.\n"
                  "- **Tomorrow's job:** use the demo to earn the exec intro, not to close.\n"
                  "One move: end by asking your evaluator, \"Who besides you needs to see this before a decision?\"",
             "c": ["d365_opps"]},
            {"u": "How do I handle it if they bring up our competitor's lower price?",
             "a": "Don't defend the price — **reframe the comparison**. \"You're right, their sticker is lower. Customers who switched to us from them cite two costs that didn't show on the quote: implementation overruns and per-seat add-ons in year two. Happy to walk through a 3-year comparison with your numbers.\" Then stop talking. If price is truly the only criterion, better to learn that tomorrow than in month three.",
             "c": []},
            {"u": "What should my close look like?",
             "a": "Three sentences, then silence: \"It sounds like this solves the monitoring gap your team flagged. What I'd suggest next is a 30-minute session with whoever owns the budget decision, where we show exactly this with your data. Who should that be?\" **You're closing for the intro** [1] — the deal close comes after.",
             "c": ["d365_accounts_ui"]},
        ],
    },
    "general_speech_to_crm_demo.html": {
        "title": "Speech to CRM",
        "vertical": "Cross-Industry",
        "tagline": "Talk through your meeting on the drive back — the CRM writes itself.",
        "persona": "Field seller, voice capture after a customer visit",
        "sources": ["d365_contacts", "d365_opportunities"],
        "turns": [
            {"u": "\"Just left Maple Thread Textiles. Met with their ops manager, they want the fleet proposal by Friday, budget's approved for Q3, and their plant manager Diane needs to sign off. Oh, and their old scanner contract ends in August.\"",
             "a": "**Captured and structured:**\n"
                  "- **Meeting logged:** Maple Thread Textiles, ops manager, today [1].\n"
                  "- **Task:** fleet proposal due Friday — assigned to you.\n"
                  "- **Opportunity updated:** budget approved, Q3 close timeframe [2].\n"
                  "- **New stakeholder:** Diane, plant manager, marked as approver.\n"
                  "- **Signal:** scanner contract expires August — logged as a competitive displacement flag.\n"
                  "Anything I misheard?",
             "c": ["d365_contacts_ui", "d365_opps"]},
            {"u": "\"Make the proposal task Thursday instead, and remind me to find Diane on LinkedIn tonight.\"",
             "a": "Updated: **proposal task moved to Thursday**, and a personal reminder set for 7pm tonight — \"Find Diane (plant manager, Maple Thread) on LinkedIn.\" Both changes synced to the opportunity record [1].",
             "c": ["d365_opps"]},
            {"u": "\"What's my day look like tomorrow?\"",
             "a": "Tomorrow: **two customer meetings** — morning demo at Blue Heron Stationery, afternoon check-in with Copper Kite Design [1]. One task due: the pricing follow-up you promised City of Alder Creek. Gap from 1–3pm; that's your window for the Maple Thread proposal if you want a head start on Thursday.",
             "c": ["d365_accounts_ui"]},
        ],
    },
    "general_voice_to_crm_demo.html": {
        "title": "Voice to CRM",
        "vertical": "Cross-Industry",
        "tagline": "Hands-free CRM: query, update, and log records by voice.",
        "persona": "Field seller, hands-free in transit",
        "sources": ["d365_accounts", "d365_opportunities"],
        "turns": [
            {"u": "\"What's my pipeline looking like this month?\"",
             "a": "Your month: **6 open opportunities** [1].\n"
                  "- 2 in Commit — Marigold Field Services and the Beacon Hill add-on.\n"
                  "- 3 mid-stage, 1 early.\n"
                  "- **Attention flag:** the Beacon Hill add-on has a proposal due tomorrow that isn't marked sent.\n"
                  "Want me to open that one?",
             "c": ["d365_opps"]},
            {"u": "\"Yes — push the Beacon Hill proposal date to Monday and note that their signer is traveling this week.\"",
             "a": "Done: **proposal due date moved to Monday**, and the note \"Signer traveling this week\" added to the Beacon Hill opportunity [1]. The Commit forecast keeps its close date — the slip is inside the buffer. You'll get a Monday-morning reminder.",
             "c": ["d365_opps"]},
            {"u": "\"Log a quick call note: spoke with Prairie Wind, they're happy, renewal conversation in September.\"",
             "a": "**Logged:** call activity on Prairie Wind Energy Cooperative [1] — positive sentiment, renewal conversation targeted for September. A September follow-up task is set so the renewal doesn't depend on memory. Anything else while you're driving?",
             "c": ["d365_accounts_ui"]},
        ],
    },
    "hr_ask_hr_demo.html": {
        "title": "Ask HR (HR Operations)",
        "vertical": "Human Resources",
        "tagline": "The HR team's view: caseload down, employees answered instantly.",
        "persona": "Maria Gonzalez, HR Business Partner",
        "sources": ["hris_workers", "hris_time_off"],
        "turns": [
            {"u": "What did the assistant handle for employees this week, and what needs me?",
             "a": "This week: **142 employee questions handled, 9 escalated** to you [1].\n"
                  "- **Self-served:** PTO balances, policy lookups, payslip questions, address changes.\n"
                  "- **Escalations:** 4 leave-of-absence consults, 3 manager coaching requests, 2 sensitive matters routed directly (no bot handling, per policy).\n"
                  "- **Pattern:** 18 questions about the new parental leave policy — the FAQ needs a clearer example.",
             "c": ["hris_workers"]},
            {"u": "Show me the time-off picture for Customer Service before I approve the March requests.",
             "a": "**Customer Service, March: 5 requests pending** [1].\n"
                  "- **TOR-1001** and two others don't overlap — safe approvals.\n"
                  "- Two requests overlap **March 9–11**, which puts the team below minimum coverage for two days [2].\n"
                  "- One requester has flexible dates per their note.\n"
                  "Suggested: approve three now, ask the flexible requester to shift two days, then all five can be honored.",
             "c": ["hris_time_off", "hris_departments"]},
            {"u": "Draft the message to the flexible requester.",
             "a": "Draft: \"Hi Jordan — your March time-off request [1] overlaps with a teammate's on the 9th–11th, which would leave the team short. You mentioned flexibility: if you can shift to start March 12, I can approve the full week today. If those exact dates matter, tell me and we'll figure it out — that's a real option too.\" Honest, choice-preserving, and it keeps trust in the process.",
             "c": ["hris_time_off"]},
        ],
    },
    "it_helpdesk_demo.html": {
        "title": "IT Helpdesk",
        "vertical": "IT Management",
        "tagline": "Diagnosis, fix, and ticket hygiene — before the user finishes their coffee.",
        "persona": "Employee, urgent pre-meeting issue",
        "sources": ["itsm_incidents"],
        "turns": [
            {"u": "Help me fix my laptop — it's running really slow and I have a meeting in 30 minutes.",
             "a": "Let's get you to that meeting. Quick diagnosis from your device telemetry:\n"
                  "- **Memory at 96%** — a browser with 40+ tabs and two conferencing apps running.\n"
                  "- Disk and CPU look healthy; this is a memory squeeze, not a hardware problem.\n"
                  "**Fastest fix (2 minutes):** close the idle conferencing app and restart the browser — it restores your tabs and typically frees 30% memory. Try that first?",
             "c": []},
            {"u": "Did it — much faster already. Why does this keep happening though?",
             "a": "Because your laptop has **8GB of RAM** and your workload has outgrown it. You've hit this three times this quarter — INC0010021, INC0010034, and today [1]. Two real fixes:\n"
                  "- A **RAM upgrade to 16GB** — your model supports it, ~2-day turnaround.\n"
                  "- Or a **refresh device** from the current catalog if you're due (you are, next month).\n"
                  "I'd wait for the refresh. Meanwhile, the browser-restart trick holds you over.",
             "c": ["itsm_incidents"]},
            {"u": "Book the refresh and close today's ticket.",
             "a": "Done:\n"
                  "- **Device refresh request submitted** for next month's cycle — you'll pick a model from the catalog link in your email.\n"
                  "- Today's incident is **resolved-with-workaround** and linked to the two prior tickets [1] so the pattern is visible to asset planning.\n"
                  "Enjoy the meeting — you've got 24 minutes to spare.",
             "c": ["itsm_incidents"]},
        ],
    },
}


# ---------------------------------------------------------------------------
# SVG glyphs (no emojis, no logo assets — inline vector shapes only)
# ---------------------------------------------------------------------------

GLYPH_SPARK = (
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
    '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/></svg>'
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
GLYPH_DB = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<ellipse cx="12" cy="5.5" rx="7.5" ry="2.8"/>'
    '<path d="M4.5 5.5v13c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8v-13"/>'
    '<path d="M4.5 12c0 1.5 3.4 2.8 7.5 2.8s7.5-1.3 7.5-2.8"/></svg>'
)
# rail + top bar icons
G_HOME = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11l8-7 8 7"/><path d="M6 9.5V20h12V9.5"/></svg>'
G_CHAT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5.5h16v11H9l-5 4z"/></svg>'
G_APPS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5" rx="1.4"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.4"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.4"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.4"/></svg>'
G_CAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="4" y="5.5" width="16" height="14" rx="2"/><path d="M4 10h16M8.5 3.5v3M15.5 3.5v3"/></svg>'
G_MORE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><circle cx="6" cy="12" r="1.6"/><circle cx="12" cy="12" r="1.6"/><circle cx="18" cy="12" r="1.6"/></svg>'
G_WAFFLE = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
            + "".join(f'<circle cx="{6 + c * 6}" cy="{6 + r * 6}" r="1.5"/>' for r in range(3) for c in range(3))
            + "</svg>")
G_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20.5 20.5L16 16"/></svg>'
G_SEND = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M3.4 20.4l17.4-8.4L3.4 3.6l-.01 6.53L15 12 3.39 13.87z"/></svg>'


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__ — M365 Copilot Demo</title>
<style>
:root {
  --bg: #faf9f8; --surface: #ffffff; --surface-2: #f5f4f3; --hover: #f3f2f1;
  --border: #edebe9; --border-strong: #d2d0ce;
  --text: #323130; --text-dim: #605e5c; --text-faint: #a19f9d;
  --accent: #0078d4; --accent-hover: #106ebe; --accent-pressed: #005a9e;
  --user-bubble: #e8ebfa; --user: #5b5fc7; --ok: #107c10; --warn: #d83b01;
  --shadow-2: 0 0.3px 0.9px rgba(0,0,0,.1), 0 1.6px 3.6px rgba(0,0,0,.13);
}
[data-theme="dark"] {
  --bg: #1b1a19; --surface: #252423; --surface-2: #2d2c2b; --hover: #323130;
  --border: #3b3a39; --border-strong: #484644;
  --text: #f3f2f1; --text-dim: #c8c6c4; --text-faint: #797775;
  --accent: #2899f5; --accent-hover: #3aa0f3; --accent-pressed: #6cb8f6;
  --user-bubble: #33344a; --user: #7f85f5; --ok: #92c353; --warn: #f1707b;
  --shadow-2: 0 0.3px 0.9px rgba(0,0,0,.32), 0 1.6px 3.6px rgba(0,0,0,.4);
}
* { margin:0; padding:0; box-sizing:border-box; }
html, body { max-width:100%; overflow-x:hidden; height:100%; }
body {
  font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.5;
  display: flex; flex-direction: column; height: 100vh;
  -webkit-font-smoothing: antialiased;
}
svg { width: 1em; height: 1em; display: inline-block; vertical-align: -0.12em; }
a { color: var(--accent); text-decoration: none; }
a:hover { color: var(--accent-hover); text-decoration: underline; }
button { font-family: inherit; }

/* ================= top app bar ================= */
.topbar {
  height: 48px; flex: 0 0 48px; display: flex; align-items: center; gap: 8px;
  background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 8px 0 4px;
  z-index: 20;
}
.tb-btn {
  width: 40px; height: 40px; border: none; background: none; color: var(--text-dim);
  border-radius: 4px; cursor: pointer; display: inline-flex; align-items: center;
  justify-content: center; font-size: 17px; flex: 0 0 auto;
}
.tb-btn:hover { background: var(--hover); color: var(--text); }
.tb-title { display: flex; align-items: center; gap: 8px; min-width: 0; }
.copilot-mark {
  width: 22px; height: 22px; border-radius: 4px; flex: 0 0 auto; position: relative;
  background: linear-gradient(135deg, #b4a0ff 0%, #ff7eb9 50%, #7ee7fc 100%);
}
.copilot-mark::before { content: ""; position: absolute; inset: 5px; background: #fff; opacity: .92; border-radius: 2px; }
.tb-title span { font-size: 14px; font-weight: 600; white-space: nowrap; }
.tb-search { flex: 1; max-width: 560px; margin: 0 auto; position: relative; min-width: 0; }
.tb-search .glyph { position: absolute; left: 10px; top: 50%; transform: translateY(-50%); color: var(--text-faint); font-size: 14px; display: inline-flex; }
.tb-search input {
  width: 100%; padding: 6px 10px 6px 32px; border: 1px solid var(--border-strong);
  border-radius: 4px; font-size: 13px; background: var(--surface-2); color: var(--text);
  font-family: inherit; outline: none;
}
.tb-right { margin-left: auto; display: flex; align-items: center; gap: 4px; }
.tb-avatar {
  width: 28px; height: 28px; border-radius: 50%; background: var(--user); color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600;
  flex: 0 0 auto; margin: 0 4px;
}
@media (max-width: 760px) { .tb-search { display: none; } .tb-title span { font-size: 13px; } }

/* ================= shell: rail + stage ================= */
.shell { flex: 1; display: flex; min-height: 0; }
.rail {
  width: 52px; flex: 0 0 52px; background: var(--surface); border-right: 1px solid var(--border);
  display: flex; flex-direction: column; align-items: center; padding: 8px 0; gap: 2px;
}
.rail-item {
  width: 44px; padding: 7px 0 5px; border: none; background: none; color: var(--text-dim);
  border-radius: 4px; cursor: pointer; display: flex; flex-direction: column; align-items: center;
  gap: 2px; font-size: 16px; position: relative;
}
.rail-item small { font-size: 9.5px; font-weight: 400; }
.rail-item:hover { background: var(--hover); color: var(--text); }
.rail-item.active { color: var(--accent); }
.rail-item.active::before {
  content: ""; position: absolute; left: -4px; top: 10px; bottom: 10px; width: 2.5px;
  background: var(--accent); border-radius: 2px;
}
@media (max-width: 760px) { .rail { display: none; } }

.stage { flex: 1; display: flex; flex-direction: column; min-width: 0; min-height: 0; }

/* pane header */
.pane-head {
  min-height: 48px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  padding: 6px 16px; background: var(--surface); border-bottom: 1px solid var(--border);
}
.back-link {
  display: inline-flex; align-items: center; gap: 5px; color: var(--text-dim);
  font-size: 12.5px; white-space: nowrap; border-radius: 4px; padding: 4px 6px;
}
.back-link:hover { color: var(--text); background: var(--hover); text-decoration: none; }
.pane-title { font-size: 14px; font-weight: 600; }
.agent-chip {
  display: inline-flex; align-items: center; gap: 6px; font-size: 12.5px; font-weight: 600;
  color: var(--accent); background: var(--hover); border-radius: 999px; padding: 3px 10px 3px 4px;
  white-space: nowrap; max-width: 100%; overflow: hidden; text-overflow: ellipsis;
}
.agent-chip .dot {
  width: 18px; height: 18px; border-radius: 5px; background: #0078d4; color: #fff;
  display: inline-flex; align-items: center; justify-content: center; font-size: 11px; flex: 0 0 auto;
}
.pane-controls { margin-left: auto; display: flex; gap: 8px; }
.ctl-btn {
  display: inline-flex; align-items: center; gap: 6px;
  background: var(--accent); color: #fff; border: 1px solid transparent; cursor: pointer;
  font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 4px;
}
.ctl-btn:hover { background: var(--accent-hover); }
.ctl-btn:active { background: var(--accent-pressed); }
.ctl-btn.secondary { background: var(--surface); color: var(--text); border-color: var(--border-strong); }
.ctl-btn.secondary:hover { background: var(--hover); }
.ctl-btn:disabled { opacity: .5; cursor: default; }

/* chat area */
.chat { flex: 1; overflow-y: auto; padding: 20px 16px 8px; }
.chat-inner { max-width: 760px; margin: 0 auto; display: flex; flex-direction: column; gap: 20px; }
.stage-note { color: var(--text-faint); font-size: 12.5px; text-align: center; padding: 24px 0 4px; }
.stage-note b { color: var(--text-dim); font-weight: 600; }
.message { animation: rise .25s ease both; min-width: 0; }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }

/* user turn: right-aligned bubble */
.message.user { display: flex; justify-content: flex-end; }
.user-bubble {
  max-width: 78%; background: var(--user-bubble); color: var(--text);
  padding: 10px 14px; border-radius: 8px 8px 2px 8px; font-size: 14px;
  overflow-wrap: break-word;
}
@media (max-width: 560px) { .user-bubble { max-width: 92%; } }

/* agent turn: attributed, full width */
.agent-head { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }
.agent-avatar {
  width: 28px; height: 28px; border-radius: 6px; background: #0078d4; color: #fff;
  display: flex; align-items: center; justify-content: center; font-size: 14px; flex: 0 0 auto;
}
.agent-name { font-size: 14px; font-weight: 600; }
.agent-tag {
  padding: 1.5px 8px; background: var(--hover); border-radius: 4px;
  font-size: 11.5px; color: var(--text-dim); white-space: nowrap;
}
.agent-body { margin-left: 36px; font-size: 14px; color: var(--text); min-width: 0; }
@media (max-width: 560px) { .agent-body { margin-left: 0; margin-top: 2px; } }
.agent-body p { margin: 0 0 8px; }
.agent-body p:last-child { margin-bottom: 0; }
.agent-body ul, .agent-body ol { margin: 0 0 8px 20px; }
.agent-body li { margin: 2px 0; }
.agent-body strong { font-weight: 600; }
.md-table-wrap { overflow-x: auto; margin: 0 0 8px; }
.agent-body table { border-collapse: collapse; font-size: 13px; min-width: 240px; }
.agent-body th, .agent-body td { border: 1px solid var(--border); padding: 5px 10px; text-align: left; }
.agent-body th { background: var(--surface-2); font-weight: 600; }
sup.cite { line-height: 0; }
sup.cite a {
  font-size: 10.5px; font-weight: 600; color: var(--accent);
  background: var(--hover); border-radius: 3px; padding: 0 4px; margin: 0 1px;
  text-decoration: none;
}
sup.cite a:hover { background: var(--accent); color: #fff; text-decoration: none; }
.typing { display: inline-flex; gap: 4px; padding: 4px 2px; }
.typing i { width: 6px; height: 6px; border-radius: 50%; background: var(--text-faint); animation: blink 1.1s infinite; }
.typing i:nth-child(2) { animation-delay: .18s; } .typing i:nth-child(3) { animation-delay: .36s; }
@keyframes blink { 0%,70%,100% { opacity: .25 } 30% { opacity: 1 } }

/* adaptive-card-style result card inside agent turn */
.acard {
  margin: 10px 0 2px; background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; box-shadow: var(--shadow-2); overflow: hidden; max-width: 560px;
}
.acard-head { display: flex; align-items: center; gap: 8px; padding: 10px 12px; border-bottom: 1px solid var(--border); }
.acard-head .glyph { color: var(--accent); display: inline-flex; font-size: 14px; }
.acard-title { font-size: 13px; font-weight: 600; }
.acard-count { margin-left: auto; font-size: 11.5px; font-weight: 600; color: var(--ok); background: var(--hover); padding: 2px 8px; border-radius: 4px; white-space: nowrap; }
.acard-count.err { color: var(--warn); }
.acard-note { padding: 10px 12px; font-size: 12.5px; color: var(--text-dim); }
.acard .tbl-wrap { overflow-x: auto; }
.acard table { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.acard th { text-align: left; padding: 7px 12px; background: var(--surface-2); color: var(--text); font-weight: 600; font-size: 11.5px; border-bottom: 1px solid var(--border); white-space: nowrap; }
.acard td { padding: 7px 12px; border-bottom: 1px solid var(--border); color: var(--text-dim); max-width: 170px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.acard tr:last-child td { border-bottom: none; }
.acard-src { padding: 7px 12px; font-size: 11px; color: var(--text-faint); border-top: 1px solid var(--border); }
.acard-src a { color: var(--text-faint); }
.acard-src a:hover { color: var(--accent); }

/* citation footer per reply */
.sources { margin: 10px 0 0; font-size: 12px; color: var(--text-dim); }
.sources .src-label { font-weight: 600; margin-bottom: 2px; }
.sources ol { margin: 0 0 0 18px; }
.sources li { margin: 1px 0; }
.sources a { color: var(--accent); }

/* suggested prompt pills */
.prompt-row { flex: 0 0 auto; padding: 8px 16px 0; }
.prompt-inner { max-width: 760px; margin: 0 auto; display: flex; gap: 8px; flex-wrap: wrap; }
.prompt-pill {
  border: 1px solid var(--border-strong); background: var(--surface); color: var(--text);
  font-size: 12.5px; padding: 6px 14px; border-radius: 999px; cursor: pointer;
  display: inline-flex; align-items: center; gap: 6px; max-width: 100%;
}
.prompt-pill .glyph { color: var(--accent); display: inline-flex; font-size: 12px; flex: 0 0 auto; }
.prompt-pill span.txt { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.prompt-pill:hover { background: var(--hover); border-color: var(--accent); }

/* input bar + disclaimer */
.input-container { flex: 0 0 auto; padding: 10px 16px 12px; }
.input-inner { max-width: 760px; margin: 0 auto; }
.input-wrapper { position: relative; }
.input-field {
  width: 100%; padding: 11px 44px 11px 14px;
  border: 1px solid var(--border-strong); border-radius: 8px;
  font-size: 14px; font-family: inherit; background: var(--surface); color: var(--text-faint);
}
.input-send {
  position: absolute; right: 6px; top: 50%; transform: translateY(-50%);
  width: 30px; height: 30px; border: none; background: none; border-radius: 4px;
  color: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 15px;
}
.ai-note { font-size: 11px; color: var(--text-faint); margin-top: 6px; text-align: center; }
</style>
</head>
<body>

<div class="topbar">
  <button class="tb-btn" title="App launcher (decorative)" aria-label="App launcher">__G_WAFFLE__</button>
  <div class="tb-title"><span class="copilot-mark" aria-hidden="true"></span><span>Microsoft 365 Copilot</span></div>
  <div class="tb-search">
    <span class="glyph">__G_SEARCH__</span>
    <input type="text" placeholder="Search" disabled aria-label="Search (decorative)">
  </div>
  <div class="tb-right">
    <button class="tb-btn" id="themeToggle" title="Toggle light/dark" aria-label="Toggle theme">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.4M12 19.1v2.4M2.5 12h2.4M19.1 12h2.4M5 5l1.7 1.7M17.3 17.3L19 19M19 5l-1.7 1.7M6.7 17.3L5 19"/></svg>
    </button>
    <div class="tb-avatar" title="Signed in (simulated): Aster Lane">AL</div>
  </div>
</div>

<div class="shell">
  <nav class="rail" aria-label="App rail (decorative)">
    <button class="rail-item" title="Home">__G_HOME__<small>Home</small></button>
    <button class="rail-item active" title="Chat">__G_CHAT__<small>Chat</small></button>
    <button class="rail-item" title="Apps">__G_APPS__<small>Apps</small></button>
    <button class="rail-item" title="Calendar">__G_CAL__<small>Calendar</small></button>
    <button class="rail-item" title="More">__G_MORE__<small>More</small></button>
  </nav>

  <main class="stage">
    <div class="pane-head">
      <a class="back-link" href="../../index.html">__GLYPH_BACK__ All templates</a>
      <span class="pane-title">Copilot</span>
      <span class="agent-chip"><span class="dot">__GLYPH_SPARK__</span>@__AGENT_NAME__</span>
      <div class="pane-controls">
        <button class="ctl-btn" id="playBtn">__GLYPH_PLAY__ Play demo</button>
        <button class="ctl-btn secondary" id="resetBtn" title="Restart">__GLYPH_RESET__</button>
      </div>
    </div>

    <div class="chat" id="chatScroll">
      <div class="chat-inner" id="chatBody">
        <div class="stage-note" id="stageNote"><b>__TITLE__</b> — __TAGLINE__<br>Scenario: __PERSONA__ &middot; Press Play, or pick a suggested prompt below.</div>
      </div>
    </div>

    <div class="prompt-row" aria-label="Suggested prompts">
      <div class="prompt-inner" id="promptRow"></div>
    </div>

    <div class="input-container">
      <div class="input-inner">
        <div class="input-wrapper">
          <input class="input-field" type="text" placeholder="Message Copilot (scripted demo — use Play or a suggested prompt)" disabled aria-label="Message input (disabled in demo)">
          <span class="input-send" aria-hidden="true">__G_SEND__</span>
        </div>
        <div class="ai-note">Simulated interface for demonstration — recreated with CSS only; not affiliated with or endorsed by Microsoft. AI-generated content over synthetic data (Aster Lane Office Systems simulated enterprise estate).</div>
      </div>
    </div>
  </main>
</div>

<script>
(function () {
  "use strict";
  /* ---------- theme (light-first Fluent; Fluent dark on toggle/OS) ---------- */
  var root = document.documentElement;
  var saved = null;
  try { saved = localStorage.getItem("aat-theme"); } catch (e) {}
  if (saved === "dark" || (saved === null && window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches)) {
    root.setAttribute("data-theme", "dark");
  }
  document.getElementById("themeToggle").addEventListener("click", function () {
    var dark = root.getAttribute("data-theme") === "dark";
    if (dark) { root.removeAttribute("data-theme"); } else { root.setAttribute("data-theme", "dark"); }
    try { localStorage.setItem("aat-theme", dark ? "light" : "dark"); } catch (e) {}
  });

  /* ---------- data ---------- */
  var TURNS = __TURNS_JSON__;          /* [{u, a, cites:[{label,url}], card}] */
  var SOURCES = __SOURCES_JSON__;
  var ID_LINKS = __ID_LINKS_JSON__;    /* [[regexSource, url], ...] */
  var AGENT_NAME = __AGENT_NAME_JSON__;
  var GLYPH_SPARK = __GLYPH_SPARK_JSON__;
  var GLYPH_DB = __GLYPH_DB_JSON__;

  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  };

  /* ---------- tiny markdown renderer: bold, bullets, ordered lists,
     compact tables, [n] citation markers, record-id autolinks ---------- */
  function inline(s, cites) {
    var h = esc(s);
    h = h.replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>");
    h = h.replace(/\\[(\\d)\\]/g, function (m, n) {
      var c = cites[Number(n) - 1];
      if (!c) return m;
      return '<sup class="cite"><a href="' + esc(c.url) + '" target="_blank" rel="noopener" title="' + esc(c.label) + '">' + n + "</a></sup>";
    });
    ID_LINKS.forEach(function (pair) {
      var re = new RegExp("(^|[^\\\\w-])(" + pair[0] + ")(?![\\\\w-])", "g");
      h = h.replace(re, function (m, pre, id) {
        return pre + '<a href="' + esc(pair[1]) + '" target="_blank" rel="noopener" title="Open in simulated source system">' + id + "</a>";
      });
    });
    return h;
  }

  function renderMd(text, cites) {
    var lines = text.split("\\n");
    var out = [], mode = null, buf = [];
    function flush() {
      if (!buf.length) { mode = null; return; }
      if (mode === "ul") out.push("<ul>" + buf.map(function (l) { return "<li>" + l + "</li>"; }).join("") + "</ul>");
      else if (mode === "ol") out.push("<ol>" + buf.map(function (l) { return "<li>" + l + "</li>"; }).join("") + "</ol>");
      else if (mode === "table") {
        var rows = buf.map(function (l) {
          return l.replace(/^\\|/, "").replace(/\\|$/, "").split("|").map(function (c) { return c.trim(); });
        });
        var t = '<div class="md-table-wrap"><table><thead><tr>' +
          rows[0].map(function (c) { return "<th>" + c + "</th>"; }).join("") + "</tr></thead><tbody>";
        rows.slice(1).forEach(function (r) {
          t += "<tr>" + r.map(function (c) { return "<td>" + c + "</td>"; }).join("") + "</tr>";
        });
        out.push(t + "</tbody></table></div>");
      } else out.push("<p>" + buf.join("<br>") + "</p>");
      buf = []; mode = null;
    }
    lines.forEach(function (raw) {
      var line = raw.trimEnd ? raw.trimEnd() : raw.replace(/\\s+$/, "");
      if (!line.trim()) { flush(); return; }
      if (/^- /.test(line)) {
        if (mode !== "ul") flush();
        mode = "ul"; buf.push(inline(line.slice(2), cites));
      } else if (/^\\d+\\. /.test(line)) {
        if (mode !== "ol") flush();
        mode = "ol"; buf.push(inline(line.replace(/^\\d+\\. /, ""), cites));
      } else if (/^\\|/.test(line)) {
        if (mode !== "table") flush();
        mode = "table"; buf.push(inline(line, cites));
      } else {
        if (mode !== "p") flush();
        mode = "p"; buf.push(inline(line, cites));
      }
    });
    flush();
    return out.join("");
  }

  /* ---------- live estate data (prefetched; rendered into per-turn cards) ---------- */
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
  var fetches = SOURCES.map(function (src) {
    return fetch(src.url).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  });

  function attachCard(container, si) {
    var src = SOURCES[si];
    if (!src) return;
    var card = document.createElement("div");
    card.className = "acard";
    card.innerHTML =
      '<div class="acard-head"><span class="glyph">' + GLYPH_DB + '</span>' +
      '<span class="acard-title">' + esc(src.system + " — " + src.label) + '</span>' +
      '<span class="acard-count">loading…</span></div>' +
      '<div class="acard-body"><div class="acard-note">Fetching live records…</div></div>' +
      '<div class="acard-src">Source: <a href="' + esc(src.url) + '" target="_blank" rel="noopener">' +
      esc(src.system) + ' · live sandbox</a></div>';
    container.appendChild(card);
    var countEl = card.querySelector(".acard-count");
    var bodyEl = card.querySelector(".acard-body");
    fetches[si].then(function (data) {
      var rows = rowsOf(src.shape, data);
      countEl.textContent = countOf(src.shape, data, rows) + " records";
      var h = '<div class="tbl-wrap"><table><thead><tr>';
      src.cols.forEach(function (c) { h += "<th>" + esc(c[0]) + "</th>"; });
      h += "</tr></thead><tbody>";
      rows.slice(0, 4).forEach(function (row) {
        h += "<tr>";
        src.cols.forEach(function (c) {
          var v = cell(row[c[1]]);
          h += '<td title="' + esc(v) + '">' + esc(v) + "</td>";
        });
        h += "</tr>";
      });
      bodyEl.innerHTML = h + "</tbody></table></div>";
    }).catch(function () {
      countEl.textContent = "offline";
      countEl.classList.add("err");
      bodyEl.innerHTML = '<div class="acard-note">Live data unavailable — offline or sandbox unreachable. ' +
        'The citations below still link to the public source URLs.</div>';
    });
  }

  /* ---------- conversation ---------- */
  var body = document.getElementById("chatBody");
  var scroller = document.getElementById("chatScroll");
  var note = document.getElementById("stageNote");
  var playBtn = document.getElementById("playBtn");
  var resetBtn = document.getElementById("resetBtn");
  var promptRow = document.getElementById("promptRow");
  var idx = 0, playing = false, timer = null;

  function scrollDown() { scroller.scrollTop = scroller.scrollHeight; }

  function userTurn(text) {
    var m = document.createElement("div");
    m.className = "message user";
    var b = document.createElement("div");
    b.className = "user-bubble";
    b.textContent = text;
    m.appendChild(b);
    body.appendChild(m);
    scrollDown();
  }

  function agentTurn() {
    var m = document.createElement("div");
    m.className = "message bot";
    m.innerHTML =
      '<div class="agent-head"><span class="agent-avatar">' + GLYPH_SPARK + '</span>' +
      '<span class="agent-name">' + esc(AGENT_NAME) + '</span>' +
      '<span class="agent-tag">AI generated</span></div>' +
      '<div class="agent-body"><span class="typing"><i></i><i></i><i></i></span></div>';
    body.appendChild(m);
    scrollDown();
    return m.querySelector(".agent-body");
  }

  function fillAgent(el, turn) {
    el.innerHTML = renderMd(turn.a, turn.cites || []);
    if (turn.card != null) attachCard(el, turn.card);
    var cites = turn.cites || [];
    if (cites.length) {
      var s = document.createElement("div");
      s.className = "sources";
      s.innerHTML = '<div class="src-label">Sources</div><ol>' + cites.map(function (c) {
        return '<li><a href="' + esc(c.url) + '" target="_blank" rel="noopener">' + esc(c.label) + " \\u2197</a></li>";
      }).join("") + "</ol>";
      el.appendChild(s);
    }
    scrollDown();
  }

  function clearNote() { if (note) { note.remove(); note = null; } }

  function renderPills() {
    promptRow.innerHTML = "";
    if (idx >= TURNS.length) return;
    /* Before playback: show all starters (Copilot-style). Mid-conversation:
       show just the next scripted prompt. Clicking a later starter
       fast-forwards through the turns before it. */
    var targets = idx === 0 ? TURNS.map(function (_, i) { return i; }) : [idx];
    targets.forEach(function (k) {
      if (k < idx) return;
      var pill = document.createElement("button");
      pill.className = "prompt-pill";
      pill.innerHTML = '<span class="glyph">' + GLYPH_SPARK + '</span><span class="txt">' + esc(TURNS[k].u) + "</span>";
      pill.addEventListener("click", function () { jumpTo(k); });
      promptRow.appendChild(pill);
    });
  }

  function jumpTo(k) {
    if (playing || k < idx || idx >= TURNS.length) return;
    clearNote();
    promptRow.innerHTML = "";
    while (idx < k) {           /* instant render of skipped turns */
      var t0 = TURNS[idx];
      userTurn(t0.u);
      fillAgent(agentTurn(), t0);
      idx += 1;
    }
    stepOnce();
  }

  function stepOnce() {
    var t = TURNS[idx];
    userTurn(t.u);
    var el = agentTurn();
    idx += 1;
    timer = setTimeout(function () {
      fillAgent(el, t);
      if (playing && idx < TURNS.length) { timer = setTimeout(stepOnce, 1500); }
      else {
        if (idx >= TURNS.length) { playing = false; playBtn.disabled = true; }
        renderPills();
      }
    }, 900);
  }

  playBtn.addEventListener("click", function () {
    if (playing || idx >= TURNS.length) return;
    clearNote();
    promptRow.innerHTML = "";
    playing = true;
    stepOnce();
  });
  resetBtn.addEventListener("click", function () {
    clearTimeout(timer); playing = false; idx = 0; playBtn.disabled = false;
    body.innerHTML = '<div class="stage-note" id="stageNote"><b>__TITLE__</b> \\u2014 __TAGLINE__<br>Scenario: __PERSONA__ \\u00b7 Press Play, or pick a suggested prompt below.</div>';
    note = document.getElementById("stageNote");
    renderPills();
  });

  renderPills();
})();
</script>
</body>
</html>
"""


def resolve_turns(spec):
    """Resolve cite keys and attach live-card indices to agent turns."""
    turns = []
    for i, t in enumerate(spec["turns"]):
        cites = [{"label": CITES[k][0], "url": CITES[k][1]} for k in t.get("c", [])]
        card = i if i < len(spec["sources"]) else None
        turns.append({"u": t["u"], "a": t["a"], "cites": cites, "card": card})
    return turns


def render(fname, spec):
    sources = [SOURCES[s] for s in spec["sources"]]
    agent_name = spec["title"] + " Agent"
    page = (
        TEMPLATE
        .replace("__TITLE__", html.escape(spec["title"]))
        .replace("__VERTICAL__", html.escape(spec["vertical"]))
        .replace("__TAGLINE__", html.escape(spec["tagline"]))
        .replace("__PERSONA__", html.escape(spec["persona"]))
        .replace("__AGENT_NAME__", html.escape(agent_name))
        .replace("__GLYPH_BACK__", GLYPH_BACK)
        .replace("__GLYPH_SPARK__", GLYPH_SPARK)
        .replace("__GLYPH_PLAY__", GLYPH_PLAY)
        .replace("__GLYPH_RESET__", GLYPH_RESET)
        .replace("__G_WAFFLE__", G_WAFFLE)
        .replace("__G_SEARCH__", G_SEARCH)
        .replace("__G_HOME__", G_HOME)
        .replace("__G_CHAT__", G_CHAT)
        .replace("__G_APPS__", G_APPS)
        .replace("__G_CAL__", G_CAL)
        .replace("__G_MORE__", G_MORE)
        .replace("__G_SEND__", G_SEND)
        .replace("__TURNS_JSON__", json.dumps(resolve_turns(spec)).replace("</", "<\\/"))
        .replace("__SOURCES_JSON__", json.dumps(
            [{"label": s["label"], "system": s["system"], "url": s["url"],
              "shape": s["shape"], "cols": s["cols"]} for s in sources]))
        .replace("__ID_LINKS_JSON__", json.dumps(ID_LINKS))
        .replace("__AGENT_NAME_JSON__", json.dumps(agent_name))
        .replace("__GLYPH_SPARK_JSON__", json.dumps(GLYPH_SPARK))
        .replace("__GLYPH_DB_JSON__", json.dumps(GLYPH_DB))
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
