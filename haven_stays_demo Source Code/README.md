# Haven Stays — Luxury Vacation Rental Concierge

**Date:** 2026-07-06 · **POC:** AdaL Cloud examples

## TL;DR

An **impressive, real-looking company website** ("Haven Stays", a luxury vacation
rental concierge platform) with a **floating chat button in the bottom-right
corner** — exactly like a real production site's support/booking widget. Clicking
it opens a chat window where **Haven**, an AI concierge, helps visitors find and
book luxury vacation rentals. Every factual step (property search, availability
check, price quote with live discounts, lead capture) runs through **custom
tools**, and the widget renders each as a **live tool card** — so the audience
literally sees the agent *doing bookings*, not just chatting.

This is a polished, production-ready SaaS clone of Wander.com, built on
**AdaL Cloud**, fronted by a tiny **backend-for-frontend (BFF) proxy** that holds
the AdaL Cloud credential server-side.

## Why a proxy (and not "just a static page")

AdaL Cloud's API requires a per-user Clerk **JWT** on every request
(`Authorization: Bearer <token>`). A public storefront must **never** embed that
token in client HTML — it would be world-readable. So the demo ships a minimal
**BFF proxy** (`proxy/server.py`, ~180 lines of FastAPI) that:

1. Holds the JWT **server-side** (from `ADAL_JWT` env or a gitignored
   `proxy/.adal_jwt` file).
2. **Auto-creates the agent** on startup from `agent/agent.py` (reusing it by
   name on restart) — no manual setup step.
3. Serves the static storefront (`site/`) and proxies the only two browser calls
   — `POST /api/session` and `POST /api/chat/{id}` — to AdaL Cloud, injecting the
   Bearer token and forwarding the SSE stream verbatim.

The browser talks **only** to this proxy's `/api/*`. It never sees the token, the
upstream base URL, or even the agent id. This is the same pattern you'd use to
keep any provider key (OpenAI, Stripe) out of client code.

## What this demonstrates

- Creating a **custom agent** (system prompt + custom Python tools) via the API.
- Instantiating a **session** and streaming a **turn** over SSE.
- Rendering rich streaming events (assistant text + **tool cards**) in a real UI.
- A production-safe **credential-proxy** pattern any company site can copy.
- **Guardrails**: system prompt discipline, JWT proxy pattern, deterministic tools,
  and scoped widget behavior.

## Layout

```
haven_stays_demo/
  README.md              # this spec
  run_local.sh           # run the proxy locally (http://127.0.0.1:8500/)
  deploy_aws.sh          # build -> ECR -> App Runner (public HTTPS URL)
  agent/
    agent.py             # name + system_prompt + agent_config() (the /v1/agents body)
    tools.py             # the CUSTOM_TOOLS source (readable copy of what's embedded)
  proxy/
    server.py            # BFF: holds the JWT, auto-creates the agent, proxies /api/*
    Dockerfile           # container image (bundles proxy + site + agent)
    requirements.txt     # fastapi, uvicorn, httpx
    .gitignore           # ignores .adal_jwt (never commit the token)
    .adal_jwt            # (you create this) the Clerk JWT — gitignored
  site/
    index.html           # the Haven Stays storefront + floating chat widget
    about/careers/contact/legal.html, 404.html
    assets/              # photorealistic property/lifestyle images (nano-banana-2)
    robots.txt, sitemap.xml, site.webmanifest
```

The storefront (`site/index.html`) goes well beyond a demo harness: a full
booking funnel (property grid → quick-view modal with image gallery → check
dates that hands off to the concierge), plus destination stories, reviews, FAQ,
guarantee strip, newsletter, cookie consent, proactive chat nudge,
back-to-top, and full SEO/a11y/PWA layers (JSON-LD, OG/Twitter meta, skip
link, focus states). No blocking `alert()` dialogs anywhere.

## Running it locally

```bash
cd haven_stays_demo

# Provide the AdaL Cloud JWT one of two ways (never commit it):
export ADAL_JWT="eyJ..."          # env var, OR
echo "eyJ..." > proxy/.adal_jwt   # gitignored file

./run_local.sh                    # serves http://127.0.0.1:8500/
```

Open `http://127.0.0.1:8500/`, click the chat button, and talk to Haven.

## Deploying to AWS

`deploy_aws.sh` builds the proxy image, pushes it to ECR, and creates/updates an
**App Runner** service with a public HTTPS URL. The JWT is passed as a runtime
env var (never baked into the image):

```bash
cd haven_stays_demo
ADAL_JWT="eyJ..." ./deploy_aws.sh          # prints the live https:// URL
```

Env knobs (all optional):

| Var | Default | Meaning |
|---|---|---|
| `ADAL_JWT` | — (required) | Clerk session JWT the demo runs under. |
| `ADAL_BASE_URL` | `https://cloud.adal.sylph.ai` | Upstream AdaL Cloud API base. |
| `ADAL_MODEL` | `google-gemini-3-flash-preview` | Per-session model. |
| `PORT` / `HOST` | `8500` / `127.0.0.1` | Where the proxy listens. |

### Widget behavior

- **First open** lazily creates a session (`POST /api/session`) and greets the
  user; subsequent opens reuse the same session id (kept in `sessionStorage`).
- **Sending a message** streams the response via `POST /api/chat/{id}` (SSE),
  rendering assistant text as it arrives and **each tool call as a live card**:
  `tool.started` shows the tool name with an icon.
- **Auto-provision**: the first turn auto-provisions the worker (shows a
  connecting state), so no explicit provision/poll is needed.
- Graceful states: connecting, streaming, session-reaped retry, error.

## The agent

**Name:** `Haven Concierge v1`

**System prompt (summary):** Haven, senior concierge for a luxury vacation rental
platform. Consultative, warm, never pushy. MUST use tools for all facts (never
invent property details, prices, availability, or IDs). Ask 1–2 clarifying
questions (budget, location, amenities, dates, party size), recommend at most
2–3 curated homes, always `build_quote` before quoting a price and state the
savings, be honest about availability, and `capture_lead` only when the traveler
shows booking intent.

**Custom tools (`CUSTOM_TOOLS`):**

| Tool | Purpose |
|---|---|
| `search_properties(location, budget, amenities)` | Find luxury homes by region/destination, nightly budget, and required amenities. |
| `check_availability(property_id, dates)` | Check availability for a property on given dates. |
| `build_quote(property_id, nights, loyalty_member)` | Price a stay: 10% weekly discount for 7+ nights, +5% for loyalty. Returns nightly rate, totals, savings. |
| `capture_lead(name, email, property_id)` | Place a hold on a property + save contact for follow-up. Call on booking intent. |

**Design choice — deterministic, self-contained tools:** the property catalog is
an in-memory dict and pricing is pure logic, so every tool call succeeds live (no
external API to fail mid-demo). Rates and discounts live in `build_quote`, not the
prompt, so the agent physically cannot hallucinate a price — every number on
screen came from a tool result. Swap `_CATALOG` for a real HTTP call later if
desired.

## Guardrails

1. **System prompt discipline** — the agent is instructed to always use tools for
   facts, never invent property details, limit recommendations to 2–3 curated
   homes, ask clarifying questions, and capture leads only on intent.
2. **JWT proxy pattern** — the Clerk JWT never reaches the browser; it lives
   server-side in the BFF proxy.
3. **Deterministic tools** — pricing and availability are pure logic, so the
   agent cannot hallucinate; every number on screen came from a tool result.
4. **Scoped widget behavior** — the chat widget only talks to the proxy's
   `/api/*` endpoints; it never sees the token, agent ID, or upstream URL.

## Demo script (shows every tool)

1. Visitor: *"I'm looking for an oceanfront villa in Hawaii under $1300/night."*
   → `search_properties("hawaii", 1300, ["oceanfront"])` → recommends
   **Cliffside Oasis, Maui**.
2. *"Is it available July 15-22? I'm a loyalty member."*
   → `check_availability("HVN-MAUI-01", "2026-07-15 to 2026-07-22")` +
   `build_quote("HVN-MAUI-01", 7, loyalty_member=True)` → shows the **10% weekly
   discount** and **5% loyalty savings** live.
3. *"I'll take it — can you hold it for me? I'm Jane, jane@example.com."*
   → `capture_lead("Jane", "jane@example.com", "HVN-MAUI-01")` → held + next steps.

Each step renders as a tool card in the widget — the "wow": the agent visibly
*doing bookings*, not just chatting.

## Future work

- Persist conversation across page reloads (session id already in sessionStorage).
- Swap the in-memory catalog for a live inventory endpoint.
- A scoped, publishable **embed token** (narrow session-create + chat scope) so a
  pure static page can call AdaL Cloud directly without the BFF proxy.
