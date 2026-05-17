# KwaCart

**Milestone Project 3 — Level 5 Diploma in Web Software Engineering**

KwaCart is a Django-based facilitation platform built around **Liberating Structures** — 23 participatory methods that help groups do their best thinking together. It gives facilitators a bank of ready-made tools — warm-ups, reflection exercises, peer consultation formats, and more — that participants can complete individually or together in a live collaborative session. Responses are archived and exportable as Markdown and RTF documents.

---

## Table of Contents

1. [Purpose](#purpose)
2. [Tech Stack](#tech-stack)
3. [User Stories](#user-stories)
4. [Agile Methodology](#agile-methodology)
5. [UX Design](#ux-design)
6. [Project Structure](#project-structure)
7. [Public Pages (no account required)](#public-pages-no-account-required)
8. [Key Features](#key-features)
9. [Facilitation Tools](#facilitation-tools)
10. [Collaborative Sessions](#collaborative-sessions)
11. [Archive & Exports](#archive--exports)
12. [Data Models](#data-models)
13. [User Accounts](#user-accounts)
14. [Running Locally](#running-locally)
15. [Deployment](#deployment)
16. [Security](#security)
17. [Admin](#admin)
18. [Adding a New Tool](#adding-a-new-tool)
19. [Validation](#validation)
20. [Testing](#testing)
21. [Credits](#credits)

---

## Purpose

Organisations often struggle to create the conditions for honest, constructive dialogue. KwaCart provides a lightweight facilitation toolkit — grounded in Liberating Structures methodology — that any team can use to surface challenges, share hopes, and warm up to productive conversation. The platform removes the friction of paper-based activities by letting every participant log in, work through a structured prompt, and instantly see a combined result when the facilitator closes the session.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 6.0.4 |
| Database (dev) | SQLite (`db.sqlite3`) |
| Static files | WhiteNoise 6.6 |
| Production server | Gunicorn 25.x |
| Hosting | Replit (development & production) |

---

## User Stories

| # | As a… | I want to… | So that… |
|---|---|---|---|
| 1 | Visitor | browse the landing page without logging in | I can understand what the platform offers before committing to an account |
| 2 | Visitor | use a free tool (Min Specs or 15% Solutions) without an account | I can experience the platform's value before signing up |
| 3 | Visitor | join the waiting list with my email | I am notified when the platform opens more widely |
| 4 | Visitor | submit a feature request | I can influence the product roadmap |
| 5 | New user | register for an account with my email and a password | I can save my work and participate in sessions |
| 6 | Returning user | log in to my account | I can access my archive and join live sessions |
| 7 | Logged-in user | browse the full tool catalog | I can choose the right facilitation tool for my situation |
| 8 | Logged-in user | draft a tool response at my own pace, with autosave | I can refine my thinking without losing progress |
| 9 | Logged-in user | submit a solo draft and receive a downloadable Markdown and RTF export | I have a portable record of my thinking |
| 10 | Facilitator (host) | start a collaborative session for any tool | I can run a real-time group activity |
| 11 | Facilitator | share a session link with signed-in participants | Colleagues who already have accounts can join immediately |
| 12 | Facilitator | display a guest QR code that participants scan to join without an account | I can include participants who haven't registered, such as external guests or workshop attendees |
| 13 | Guest participant | scan a QR code, enter only my name, and fill in a session form | I can contribute to a live session without creating an account |
| 14 | Facilitator | see participant names (including guests) update in real time as people join | I can gauge readiness before starting |
| 15 | Facilitator | start, pause, and reset a countdown timer that all participants see in sync | I can time-box each phase of the activity |
| 16 | Facilitator | close the session when everyone has responded | All contributions are locked and a combined export is generated automatically |
| 17 | Participant (signed-in or guest) | be redirected automatically when the host closes the session | I see the combined results without needing to refresh |
| 18 | Logged-in user | view my archive of solo submissions and sessions | I can revisit and reflect on past work |
| 19 | Logged-in user | download Markdown and RTF exports for any archived record | I can share outputs or store them outside the platform |
| 20 | Staff user | view the waiting-list table in the archive dashboard | I can manage the rollout and follow up with prospective users |
| 21 | CEO | run structured dialogue sessions across teams and levels of my organisation using a shared facilitation tool | I can break down communication barriers, surface what people actually think, and replace top-down messaging with genuine two-way conversation |
| 22 | Middle manager | deploy a live session tool so that everyone involved in a stalled project can contribute their perspective in real time and see each other's responses immediately when the session closes | the process feels transparent and trustworthy, and the team can move forward together based on evidence rather than assumption |
| 23 | Youth worker | guide a group of young people through a series of facilitation tools, saving every session's responses to a growing archive | the group builds a real record of their collective thinking while also developing practical skills in scribing, facilitation, and working with structured data |

---

## Agile Methodology

The project was planned and delivered using an Agile approach across five one-week sprints. A GitHub Project board tracked every user story through four columns — **Backlog → In Progress → In Review → Done** — providing a continuous, visible record of progress.

### GitHub Project board

The board is linked to the repository and uses GitHub Issues as cards. Each issue corresponds to a user story by number (e.g. Issue #8 maps to US-08 in the table above). Labels on each issue show its MoSCoW priority and the sprint it was scheduled in. Commit messages reference the closing issue number (`Closes #N`) so that merging a branch automatically moves the card to Done.

### MoSCoW prioritisation

All 23 user stories were prioritised at the start of the project. The categories below reflect the decisions made in Sprint 1 planning.

| Priority | User stories | Rationale |
|---|---|---|
| **Must Have** | US 1, 5, 6, 7, 8, 9, 10, 16, 18 | Without these the application has no usable core: public landing, authentication, solo tool drafting and submission, session creation and closure, and the archive. |
| **Should Have** | US 2, 11, 12, 13, 14, 15, 17, 19 | Guest QR access, the timer, real-time participant status, and auto-redirect on session close significantly improve the live facilitation experience but the platform can function without them. |
| **Could Have** | US 3, 4, 20, 21, 22, 23 | Waiting list, feature requests, and the staff dashboard are useful for managing the rollout but are not part of the core facilitation workflow. The CEO, manager, and youth-worker personas (US 21–23) describe future deployment contexts that informed design decisions without requiring dedicated features. |
| **Won't Have (this release)** | — | No features were formally deferred to a later release; all Must and Should stories were completed within the five sprints. |

### Sprint log

Each sprint had a defined goal, a set of user stories pulled from the backlog, and a review at the end before the next sprint was planned.

| Sprint | Goal | User stories delivered |
|---|---|---|
| **1 — Foundation** | Working Django project with email authentication, landing page, and public nav | US 1, 5, 6 |
| **2 — Solo tool flow** | Tool catalog, draft editor with autosave, submit endpoint, Markdown/RTF/HTML export, archive dashboard | US 7, 8, 9, 18, 19 |
| **3 — Collaborative sessions** | Session creation, signed-in participant joining, real-time status polling, timer, session close and combined export | US 10, 11, 14, 15, 16, 17 |
| **4 — Guest access and public engagement** | Guest join via QR / UUID token (no account required), free try-it pages, waiting list, feature request, staff waiting-list view | US 2, 3, 4, 12, 13, 20 |
| **5 — Hardening and deployment** | Custom error pages, full validation pass (W3C/JSHint/flake8), security audit, Heroku deployment configuration, README completion | US 21, 22, 23 (context-driven design review); all earlier stories re-tested |

### Iterative development in practice

The sprint structure meant that each increment was a working, deployable application:

- After Sprint 1 a visitor could reach the landing page and create an account.
- After Sprint 2 a logged-in user could draft, submit, and download solo tool output.
- After Sprint 3 a facilitator could run a full live session with authenticated colleagues.
- After Sprint 4 any participant — with or without an account — could join via QR code, and members of the public could engage through the waiting list.
- After Sprint 5 the application was production-ready on Heroku with hardened security settings and complete documentation.

Sprint reviews identified several scope adjustments. The drawing canvas was initially a Could Have but was promoted to Should Have during Sprint 2 when it became clear the Min Specs tool required freeform input. The HTML export format was added during Sprint 4 review after user testing showed that Markdown and RTF alone were insufficient for participants who wanted to paste output directly into a browser-viewable file.

---

## UX Design

### Design goals

The overriding goal was to minimise friction at every step. Facilitation tools are used in workshops and meetings where participants are time-pressed and sometimes unfamiliar with digital tools. The UI therefore prioritises clarity over visual richness: generous whitespace, a single-column form layout, labels above fields (never placeholder-only), and a limited palette applied consistently.

### Information architecture

The site is divided into two clear zones:

- **Public** — landing page, about, two free try-it tools, waiting list, feature request, login, register. Visitors can experience the platform's value before committing to an account.
- **Authenticated** — tool catalog, draft editor, collaborative sessions, archive dashboard, downloads. Everything that stores or retrieves personal data sits behind login.

This boundary was a deliberate design decision: making the free tools genuinely free (no sign-up wall) reduces the barrier to a first-use experience, which is the primary conversion moment for a platform like this.

Within the authenticated zone a further privilege layer exists: only the session host can close a session; only staff users see the waiting-list table. These role distinctions are surfaced visibly in the UI (the Close Session button only appears to the host; the waiting-list panel is hidden from regular users) so the access model is legible without reading documentation.

### Colour palette rationale

Six colours were chosen and assigned specific semantic roles so the palette carries meaning rather than just decoration:

| Colour | Hex | Semantic role | Reasoning |
|---|---|---|---|
| Purple | `#5D3A9B` | Primary brand, buttons, links | Associated with creativity and facilitation; distinctive without being aggressive |
| Teal | `#40B0A6` | Success states, result borders, open sessions | Calm, positive — signals that something has worked or is live |
| Gold | `#E1BE6A` | "Free" badges, count labels, CTA highlight | Draws attention without urgency; works alongside purple without clashing |
| Orange | `#E66100` | Step numbers, running-timer button | Conveys active/in-progress state without the alarm connotations of red |
| Yellow | `#FEFE62` | "Already on list" duplicate notice | High contrast on light backgrounds; distinct from the success teal |
| Pink | `#D35FB7` | Accent use | Completes the palette; used sparingly to avoid diluting meaning |

All colour choices were checked for WCAG AA contrast (≥ 4.5:1) against their backgrounds during development.

### Navigation and form design decisions

- **Single-column forms** — all tool forms use a single-column layout so the reading order is linear and keyboard navigation is predictable. This also avoids the ambiguity of multi-column grid forms on narrow screens.
- **Server-side validation with inline errors** — form errors are rendered next to the offending field and linked via `aria-describedby` (wired by `aria_wiring.js`) so screen readers announce the error when the field is focused. Client-side validation (e.g. `required` attributes) is used only as a first-pass convenience, never as the sole guard.
- **Autosave on keystroke** — the draft editor saves two seconds after the user stops typing rather than requiring an explicit save action. This removes the cognitive load of remembering to save, which matters in workshop settings where a facilitator may close a laptop lid without warning.
- **QR code for guest access** — the QR code was chosen specifically to eliminate the friction of typing a URL on a mobile device during a live session. Scanning a code is a single gesture; copying a URL and opening a browser takes five to eight steps on most phones.
- **Timer server-sync** — rather than each participant's browser running its own clock (which drifts), the timer state is stored server-side and polled every four seconds. All participants and the host see the same remaining time regardless of when they joined the session.
- **Post/Redirect/Get on all forms** — every form POST that mutates state (submitting a response, signing up to the waiting list, submitting a feature request, running a free try-it tool) redirects to a GET after success. This means pressing the browser back button and then forward never triggers a "Confirm Form Resubmission" dialog and never creates a duplicate record.

### Page designs (implemented UI)

The screenshots below show the implemented design for each key page.

---

### Landing Page
The public homepage — introduces the platform, links to free tools, registration, and the waiting list.

![Landing page](docs/screenshots/landing.jpg)

---

### About Page
Explains Liberating Structures, the 23 tools, and the project background.

![About page](docs/screenshots/about.jpg)

---

### Register
New account creation — email address and password. Redirects to login on success.

![Register page](docs/screenshots/register.jpg)

---

### Log In
Email-based login. Redirects authenticated users directly to the tool catalog.

![Login page](docs/screenshots/login.jpg)

---

### Free Tool — Min Specs
Try Min Specs without an account. Includes a 5-minute countdown timer, structured form, and instant output.

![Min Specs free try](docs/screenshots/tool-min-specs.jpg)

---

### Free Tool — 15% Solutions
Try 15% Solutions without an account. Same timer and structured output experience.

![15% Solutions free try](docs/screenshots/tool-15-percent.jpg)

---

### Waiting List Signup
Visitors can register their interest before accounts open publicly.

![Waiting list](docs/screenshots/waiting-list.jpg)

---

### Feature Request
Visitors and users can submit ideas for new tools or platform improvements.

![Feature request](docs/screenshots/feature-request.jpg)

---

### Guest Join
Participants who scan the QR code land here. They enter only their name — no account needed — and go straight to the session form.

![Guest join](docs/screenshots/guest-join.jpg)

---

### Page Access Map

| Colour | Meaning |
|---|---|
| Public (no login) | Landing, About, Free Tools, Waiting List, Feature Request, Login, Register |
| Login required | Tool Catalog, Draft Editor, Session pages, Archive Dashboard, Archive Detail, Downloads |
| Staff / Admin only | Waiting list table in dashboard, Django Admin (`/admin/`) |

---

## Project Structure

```
KwaCart/
├── config/
│   ├── settings/
│   │   ├── base.py          Shared settings
│   │   ├── local.py         Dev overrides (DEBUG=True, ALLOWED_HOSTS from REPLIT_DOMAINS)
│   │   └── production.py    Production settings (Gunicorn, WhiteNoise, SECURE_PROXY_SSL_HEADER)
│   ├── urls.py              Root URL config — home, about, waiting-list, feature-request, accounts, tools, archive
│   └── wsgi.py
│
├── accounts/                Email-based auth
│   ├── models.py            Custom User + UserManager (validate_password enforced)
│   ├── forms.py             Registration / login forms
│   └── utils.py             log_action() helper (writes to AuditLog)
│
├── tools/                   Facilitation tool engine
│   ├── registry.py          TOOL_CATALOG — single source of truth for all 23 tools
│   ├── implementations.py   BaseTool subclasses (validate + process)
│   ├── forms.py             Django Form classes for each tool
│   ├── views.py             Solo draft + collaborative session + free try-it flows
│   ├── urls.py              URL patterns
│   └── utils.py             get_tool_metadata() + SHA-256 canvas file handling
│
├── archive/                 Sessions, submissions, waiting list, feature requests
│   ├── models.py            ToolSession, ToolInstance, AuditLog, WaitingListEntry, FeatureRequest
│   ├── admin.py             Admin registrations for all archive models
│   ├── views.py             Archive dashboard + detail + waiting list signup + feature request
│   ├── views_downloads.py   Secure file download (solo + session exports)
│   ├── urls.py
│   ├── urls_waiting_list.py  Public waiting-list routes
│   └── urls_feature_request.py  Public feature-request routes
│
├── exporters/
│   ├── pipeline.py          run_export_pipeline() / run_session_export_pipeline()
│   ├── md_gen.py            Markdown generation (solo + combined)
│   └── rtf_gen.py           RTF generation (solo + combined)
│
├── templates/
│   ├── base.html            Site chrome (nav, messages, .sr-only utility)
│   ├── landing.html         Public homepage — no login required
│   ├── about.html           About page
│   ├── accounts/            Login, registration templates
│   ├── archive/
│   │   ├── dashboard.html              Personal archive + waiting-list section (staff only)
│   │   ├── detail.html
│   │   ├── waiting_list_signup.html    Public signup
│   │   └── feature_request.html        Public feature request form
│   └── tools/
│       ├── catalog.html          Tool bank
│       ├── tool_try.html         Free try-it page (no login, countdown timer)
│       ├── draft_editor.html     Solo drafting interface
│       ├── session_open.html     Live collaborative session (QR code share)
│       ├── session_closed.html   Combined results + download links
│       ├── info_box.html         What / How / Why / agreements panel
│       ├── _timer.html           Countdown timer (server-sync, aria-live, offline detection)
│       └── _drawing_canvas.html  Drawing canvas with accessibility announcements
│
├── media/drawings/          Canvas PNG files (SHA-256 content-based filenames)
├── static/
├── manage.py
└── requirements.txt
```

---

## Public Pages (no account required)

| URL | Description |
|---|---|
| `/` | Landing page — introduces the platform, links to free tools and waiting list |
| `/about/` | About page — explains Liberating Structures, the 23 tools, and the project |
| `/tools/min-specs/try/` | Free try-it page for Min Specs |
| `/tools/15-percent-solutions/try/` | Free try-it page for 15% Solutions |
| `/waiting-list/` | Waiting-list signup (email + optional name) |
| `/request-a-feature/` | Feature request form (name, email, title, description) |
| `/accounts/login/` | Log in |

### Free try-it pages
Both free tools include the full form and result output, a **5-minute countdown timer** with Start / Pause / Reset controls, a progress bar, and screen-reader-friendly milestone announcements. A "Join the waiting list" nudge is shown instead of a "Create account" call-to-action.

### Waiting list
Visitors can sign up at `/waiting-list/`. Duplicate email addresses are handled gracefully. Staff users see the full waiting-list table in the archive dashboard.

### Feature requests
Visitors and users can submit a feature idea at `/request-a-feature/`. Submissions are stored in the `FeatureRequest` model and are visible to staff only via the Django admin. The form collects name, email, a short title, and a description.

---

## Key Features

### Colour palette
The interface uses a 6-colour palette:

| Colour | Hex | Role |
|---|---|---|
| Purple | `#5D3A9B` | Primary brand, buttons, links |
| Teal | `#40B0A6` | Success states, result borders, open-session indicators |
| Gold | `#E1BE6A` | "Free" badges, count labels, CTA band highlight button |
| Orange | `#E66100` | Step numbers, running-timer button |
| Yellow | `#FEFE62` | "Already on list" duplicate-notice border |
| Pink | `#D35FB7` | Accent use |

### Solo tool use
Any logged-in user can pick a tool from the catalog, draft at their own pace (autosave on every keystroke), and submit when ready. Submission processes the response and stores downloadable Markdown and RTF files.

### Collaborative sessions
A facilitator creates a **session** for any tool. Participants join via a shared URL or **QR code** displayed on the session page. Every four seconds, the page polls for participant list updates, timer state, and session-closed redirects. When the facilitator closes the session, all responses are processed and a combined export is generated.

#### Guest QR code access (no account needed)
The session page shows two share options:

- **Signed-in link** — for participants who already have an account.
- **Guest QR code** — a separate link (and scannable QR code) that lets anyone join without creating an account. Scanning the code takes the participant to a name-entry page; after entering their name they go straight to the form. The host sees all participants — including guests — listed by name in real time.

Guest responses are saved alongside signed-in responses and appear in the combined results when the session closes. Guests see a prompt to create an account at the end if they'd like to keep a personal archive in future.

### Drawing canvas
Tools with `show_canvas: True` in the registry include a freehand drawing canvas. Drawings are saved as PNG files in `media/drawings/` using SHA-256 content-based filenames. The file path (not the data URL) is stored in `payload_input`. The canvas includes keyboard and screen-reader accessibility support with ARIA live announcements for every toolbar action.

### Archive dashboard
`/archive/dashboard/` shows solo submissions, sessions the user hosts or has joined (with role and status), and a waiting-list table (staff users only).

### Timer widget
Tools can opt in to a countdown timer. The timer:

- MM:SS display, turns amber at ≤ 10 s, red at zero.
- Start / Pause / Reset controls with a phase progress bar.
- **Server sync** — all participants see the same remaining time via the poll endpoint.
- **Late-join** — screen readers hear an approximate time-remaining message on first sync.
- **Milestone announcements** at 5 min, 2 min, 1 min, 30 s, and 10 s.
- **Phase-transition announcements** — each phase change fires exactly one ARIA live announcement.
- **Pause badge** — visible "Paused" indicator; host-only amber reminder if paused for over 5 minutes (configurable threshold via `pause_reminder_threshold_sec`).
- **Long-pause teardown** — the amber reminder clears immediately when the host resumes.
- **Reconnection toast** — banner appears after a connectivity outage clears.
- **Offline detection** — stale badge shown immediately on `window.offline` event, not just on poll failure.
- **Reset announcement fix** — reset from paused announces "Timer reset", not "Timer resumed".

### What / How / Why info panel
Every tool page includes a structured instruction panel with **What**, **How**, **Why**, and optional **Agreements**. A **Load example data** button pre-fills the form.

### Tool catalog
Each tool card shows its title, a short tagline, and **Start solo** / **Start session** buttons.

---

## Facilitation Tools

23 tools are currently registered across two categories.

### Low-Risk Warm-ups

| Tool | Tagline |
|---|---|
| I am and I like | A quick energiser — go around the circle, share your name and something you love. |

### Facilitation

| Tool | Tagline |
|---|---|
| 1-2-4-All | Turn any question into group insight — alone, then pairs, then fours, then everyone. |
| 15% Solutions | What can you start doing right now, with the freedom and resources you already have? |
| 25/10 Crowd Sourcing | Surface your group's boldest ideas in 30 minutes with cards and a countdown from 25. |
| Appreciative Interviews | Uncover what's already working by sharing stories of peak success. |
| Conversation Café | Calm group dialogue on a hard question — a talking object and four structured rounds. |
| Discovery & Action Dialogue | Seven questions that surface hidden solutions already working in your group. |
| Drawing Together | A silent, simultaneous visual exercise using five universal shapes. |
| Five Structural Elements | Get into pairs, share challenges and expectations, build new connections fast. |
| Helping Heuristics | Practise four ways of helping in 15 minutes and discover your default pattern. |
| Idea Generation | A minute of individual reflection, then share with the group. |
| Improv Prototyping | Act out the problem, spot what works, and rebuild a better version on the spot. |
| Impromptu Networking | Meet three people, share your challenge, walk away with fresh ideas. |
| Min Specs | Strip your rules down to the bone. What absolutely must stay? |
| Nine Whys | Ask "why?" nine times and find out what actually drives you. |
| Shift & Share | Ditch the long presentations. Rotate through rapid-fire innovation stations instead. |
| TRIZ | List everything that would guarantee failure — then stop doing those things. |
| Troika Consulting | Three people, three turns, back turned. Straight-talking peer advice in 30 minutes. |
| User Experience Fishbowl | Insiders share the unfiltered story. The room listens, then asks. |
| What, So What, Now What? | Debrief any shared experience in three stages — facts first, then meaning, then action. |
| Wicked Questions | Name the contradictions your group is navigating — and make them visible. |
| Wise Crowds | 15 minutes of focused peer advice on a real challenge, with the client's back turned. |
| Wise Crowds (Large Group) | Scale peer consultation to a full room — one client, primary team, satellite groups. |

---

## Collaborative Sessions

| Step | Who | What happens |
|---|---|---|
| Create | Host | Clicks **Start session** on a tool card → session created, shareable URL and QR code generated |
| Share | Host | Copies the URL or displays the QR code for participants to scan |
| Join | Participant | Opens URL, logs in if not already, sees the form |
| Respond | Everyone | Fills in the form, clicks **Save my response** (editable until session closes) |
| Monitor | Host | Sees participant list update live; a green tick appears next to anyone who has saved |
| Close | Host only | Clicks **Close session and reveal results** → all responses locked, exports generated |
| View | Everyone | Combined results page shows all contributions; host and participants can download MD/RTF |

**Access control:**

- Only logged-in users can join.
- Only the host can close a session.
- Downloads are restricted to the host and participants; anyone else gets a 404.
- The status polling endpoint returns 403 to non-participants.

---

## Archive & Exports

### Solo submissions
On submit, the pipeline generates two files per record:

- `archives/md/<date>_<slug>_<id>.md`
- `archives/rtf/<date>_<slug>_<id>.rtf`

Files are downloadable from the archive detail page.

### Combined session exports
When a session is closed, the pipeline generates two combined files:

- `archives/md/<date>_<slug>_session_<uuid>.md`
- `archives/rtf/<date>_<slug>_session_<uuid>.rtf`

Each file lists every participant's processed output in sequence. Download links appear at the top of the closed-session page.

---

## Data Models

### `ToolSession`
| Field | Description |
|---|---|
| `id` | UUID primary key (used in shareable URLs) |
| `host` | FK → User — the facilitator who created the session |
| `tool_slug` | Which tool this session runs |
| `tool_version` | Version string at time of creation |
| `status` | `open` or `closed` |
| `created_at` / `closed_at` | Timestamps |
| `timer_started_at` | DateTimeField — when the timer was last started |
| `timer_paused_at` | DateTimeField — when the timer was paused (null if running or never paused) |
| `timer_elapsed_before_pause` | FloatField — seconds elapsed before the current pause |
| `pause_reminder_threshold_sec` | IntegerField — minutes of inactivity before the host sees a pause reminder (default 5 min) |
| `md_file` / `rtf_file` | Combined export files (populated on close) |

### `ToolInstance`
One per user per session (or one per solo submission).

| Field | Description |
|---|---|
| `user` | FK → User |
| `session` | FK → ToolSession (null for solo) |
| `tool_slug` / `tool_version` | Tool identity |
| `status` | `draft` → `archived` on submit / session close |
| `payload_input` | Raw form data (JSON); drawing tools store canvas file path, not data URL |
| `payload_output` | Processed result (JSON) |
| `md_file` / `rtf_file` | Per-instance export files (solo only) |
| `submitted_at` | Set when status transitions to `archived` |

A `UniqueConstraint` on `(session, user)` prevents a participant from having more than one response per session.

### `WaitingListEntry`
| Field | Description |
|---|---|
| `email` | Unique email address |
| `name` | Optional display name |
| `signed_up_at` | Auto timestamp |

### `FeatureRequest`
| Field | Description |
|---|---|
| `name` | Submitter's name |
| `email` | Submitter's email |
| `title` | Short feature title (max 300 chars) |
| `description` | Full description (free text) |
| `submitted_at` | Auto timestamp |

Visible to staff only via Django admin. No user account required to submit.

### `AuditLog`
Records login events, tool submissions, and file downloads with IP address and timestamp.

---

## User Accounts

Authentication is email-based (no username). The custom `User` model uses `email` as `USERNAME_FIELD`. Django's built-in password validators are enforced at the model layer via `validate_password()`.

| URL | Purpose |
|---|---|
| `/accounts/login/` | Log in |
| `/accounts/register/` | Create an account |
| `/accounts/logout/` | Log out (redirects to login) |
| `/archive/dashboard/` | Personal archive + session list |
| `/tools/` | Tool catalog |

---

## Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply migrations
python manage.py migrate

# 3. Create a superuser
python manage.py createsuperuser

# 4. Start the development server
python manage.py runserver 0.0.0.0:5000
```

The app will be available at `http://localhost:5000`.

**Environment:** The project reads settings from `config.settings.local` by default (`DJANGO_SETTINGS_MODULE` is set in `manage.py`). No `.env` file is required for local development — `ALLOWED_HOSTS` falls back to `localhost` / `127.0.0.1` when the `REPLIT_DOMAINS` environment variable is absent.

---

## Deployment

### Heroku

The project is fully configured for Heroku deployment. The files Heroku requires are already in the repository:

| File | Purpose |
|---|---|
| `Procfile` | Declares the `web` process (Gunicorn) and the `release` process (runs `migrate` on every deploy) |
| `runtime.txt` | Pins the Python version to `python-3.12.12` |
| `requirements.txt` | All dependencies with exact version pins |
| `config/settings/production.py` | Production settings — reads all secrets from environment variables |

**Step-by-step deployment**

1. Create a new Heroku app from the [Heroku dashboard](https://dashboard.heroku.com/) or with the CLI:
   ```
   heroku create your-app-name
   ```

2. Add the Heroku Postgres add-on (this automatically sets `DATABASE_URL`):
   ```
   heroku addons:create heroku-postgresql:essential-0
   ```

3. Set the required config vars (replace the placeholder values):
   ```
   heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
   heroku config:set SECRET_KEY='<a long random string — never reuse the dev key>'
   heroku config:set ALLOWED_HOSTS='your-app-name.herokuapp.com'
   heroku config:set CSRF_TRUSTED_ORIGINS='https://your-app-name.herokuapp.com'
   ```

4. Push the code to Heroku:
   ```
   git push heroku main
   ```
   Heroku will automatically:
   - Install dependencies from `requirements.txt`
   - Run `python manage.py collectstatic --noinput` (WhiteNoise serves the result)
   - Run `python manage.py migrate --noinput` (the `release` process in `Procfile`)
   - Start Gunicorn via the `web` process

5. Create a superuser so you can access `/admin/`:
   ```
   heroku run python manage.py createsuperuser
   ```

**Required config vars summary**

| Variable | Value |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `SECRET_KEY` | A strong random string (50+ characters) |
| `ALLOWED_HOSTS` | `your-app-name.herokuapp.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app-name.herokuapp.com` |
| `DATABASE_URL` | Set automatically by the Heroku Postgres add-on |

**How the production settings work on Heroku**

- `DATABASE_URL` is detected by `production.py` and passed to `dj-database-url`, switching the database from SQLite to Heroku Postgres automatically
- `SECURE_PROXY_SSL_HEADER` is already set so Django trusts Heroku's SSL termination
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are `True`, so cookies are HTTPS-only
- WhiteNoise (`CompressedManifestStaticFilesStorage`) serves and compresses static files without a separate CDN

---

### Replit

The project also runs on Replit with `config.settings.local` (set in `manage.py`). Static files are served by WhiteNoise and the dev server runs on port 5000:

```
gunicorn --bind=0.0.0.0:5000 --reuse-port config.wsgi:application
```

`python manage.py migrate` and `python manage.py collectstatic` run as build steps before the server starts. SSL termination is handled by the Replit proxy; `SECURE_PROXY_SSL_HEADER` is set correctly in `production.py` for when `config.settings.production` is active there.

---

## Configuration and dependencies

### Dependencies (`requirements.txt`)

All runtime and development dependencies are listed in `requirements.txt` with exact version pins, so the environment is fully reproducible and it is clear which version of each package is in use:

| Package | Pinned version | Purpose |
|---|---|---|
| `django` | 6.0.4 | Web framework |
| `django-environ` | 0.13.0 | Environment variable helpers |
| `gunicorn` | 25.3.0 | Production WSGI server |
| `whitenoise` | 6.6.0 | Static file serving |
| `psycopg2-binary` | 2.9.12 | PostgreSQL driver (used when `DATABASE_URL` is set) |
| `dj-database-url` | 3.1.2 | Parses `DATABASE_URL` into Django's `DATABASES` dict |
| `playwright` | 1.58.0 | Browser automation (end-to-end test runner) |
| `pytest-django` | 4.12.0 | Django integration for pytest |
| `pytest-playwright` | 0.7.2 | Playwright integration for pytest |

Every dependency update is committed to the repository so there is a clear record of when and why versions changed.

### Data store configuration

The database is configured in **one place only** — `DATABASES` in `config/settings/base.py` (lines 87–92). No other settings file defines `DATABASES` unconditionally:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To switch database backends in any environment, set a single `DATABASE_URL` environment variable (e.g. `postgres://user:pass@host/dbname`). `config/settings/production.py` detects this variable at startup and calls `dj_database_url.config()` to override the block; when the variable is absent, the SQLite default is used unchanged. No other code needs to change.

**The database file is not accessible to end users.** `db.sqlite3` is a file on the server filesystem — it is not mounted under any URL, not referenced by any view, and is listed in `.gitignore` so it is never committed to the repository. In production, WhiteNoise serves only from `STATIC_ROOT` (compiled assets); the `MEDIA_URL` route added by `django.conf.urls.static.static()` is a no-op when `DEBUG=False`, so uploaded files are also not auto-served. All data access goes through Django's ORM.

---

## Security

### 1 — Secrets and environment variables

All sensitive values are read from environment variables at runtime and are **never hard-coded in the source tree**:

| Secret | Where it lives | How it is read |
|---|---|---|
| `SECRET_KEY` | Replit environment secret | `os.environ.get('SECRET_KEY', '')` in `config/settings/production.py`; a deliberately broken-looking dev-only fallback is used in `base.py` so it can never be mistaken for a real key |
| `ALLOWED_HOSTS` | `ALLOWED_HOSTS` env var (production) | Parsed from a comma-separated string in `config/settings/production.py` |
| `CSRF_TRUSTED_ORIGINS` | `CSRF_TRUSTED_ORIGINS` env var | Same pattern — exact domain list, never a wildcard |

The following files are listed in `.gitignore` and are **never committed to the repository**:

| Entry | What it covers |
|---|---|
| `.env` | Any local environment file |
| `db.sqlite3` | Development database (contains all user data) |
| `media/` | User-uploaded and generated export files |
| `staticfiles/` | Build output from `collectstatic` |
| `*.log` | Server and application logs |
| `local_settings.py` | Any developer-local settings override |

### 2 — Login protection

Every route that accesses or modifies user data is guarded before the view body runs:

| Mechanism | Applied to |
|---|---|
| `@login_required` decorator | `tool_catalog`, `draft_editor`, `autosave_endpoint`, `submit_tool`, `session_create`, `session_detail`, `session_close`, `session_status`, `timer_start`, `timer_pause`, `timer_reset`, `session_set_pause_reminder`, `archive_record_delete`, `secure_download`, `secure_session_download` |
| `LoginRequiredMixin` on CBVs | `ArchiveDashboardView`, `ArchiveDetailView` |
| `redirect_authenticated_user = True` | `UserLoginView` — already-logged-in users are redirected away from the login page |

Public routes (landing page, about, free try-it tools, waiting list, feature request, login, register) carry no login requirement by design. Guest session participants authenticate via a URL-embedded `guest_token` UUID rather than a Django account; the `session_status` poll endpoint validates the `guest_instance_id` stored in the browser session and returns `403` if it is absent or invalid.

### 3 — Ownership and object-level permissions

Authenticated users can only access and modify their own data. Every view that retrieves a user-owned object passes `user=request.user` (or `host=request.user`) directly to `get_object_or_404`, so a crafted URL that substitutes another user's primary key receives a `404` — not a `403`, which would confirm the record exists:

| View | Ownership guard |
|---|---|
| `draft_editor` | `get_object_or_404(ToolInstance, id=instance_id, user=request.user, status='draft', session__isnull=True)` |
| `submit_tool` | Same constraint — also enforces `session__isnull=True` so session contributions cannot be submitted via the solo endpoint |
| `ArchiveDetailView` | `get_queryset()` returns `ToolInstance.objects.filter(user=self.request.user)` |
| `archive_record_delete` | `get_object_or_404(ToolInstance, pk=pk, user=request.user)` |
| `secure_download` | `get_object_or_404(ToolInstance, id=instance_id, user=request.user)` |
| `secure_session_download` | `Q(host=request.user) \| Q(instances__user=request.user)` — host or participant only |
| `session_close`, `timer_start/pause/reset`, `session_set_pause_reminder` | `get_object_or_404(ToolSession, id=session_id, host=request.user)` — host only |
| `session_status` poll | Explicit `is_host or is_participant` check → `403` for non-participants |

**Staff-only content:** the waiting-list table in the archive dashboard is rendered only when `user.is_staff` is `True`; the Django admin (`/admin/`) requires `is_staff` via Django's built-in admin authentication.

**Download file-type whitelist:** `views_downloads.py` validates `file_type` against `VALID_FILE_TYPES = {'md', 'rtf', 'html'}` before calling `getattr(instance, f'{file_type}_file')`, preventing arbitrary attribute access via a crafted URL.

**Additional hardening measures**

| Measure | Detail |
|---|---|
| CSRF protection | Django's `CsrfViewMiddleware` is active; all state-changing POST forms include `{% csrf_token %}` |
| Password validation | `validate_password()` called in `UserManager.create_user()` before `set_password()` |
| Secure cookies (production) | `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True` |
| HSTS (production) | `SECURE_HSTS_SECONDS = 31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`, `SECURE_HSTS_PRELOAD = True` |
| Gunicorn | Pinned to ≥ 23.0.0 (addresses HTTP request-smuggling CVEs in 21.x) |
| Canvas file hashing | SHA-256 content-addressable PNG filenames prevent path traversal in `media/drawings/` |
| Audit log | Login events, tool submissions, and file downloads are recorded with IP address and timestamp in `AuditLog` |

---

## Admin

The Django admin at `/admin/` provides full CRUD for:

- `ToolSession` — view and manage collaborative sessions.
- `ToolInstance` — view individual submissions.
- `AuditLog` — read-only activity trail.
- `WaitingListEntry` — view and export waiting-list signups.
- `FeatureRequest` — view submitted feature ideas (staff only).
- `User` — manage accounts and permissions.

Default superuser credentials (development only):
- Email: `admin@example.com`
- Password: `admin12345`

---

## Adding a New Tool

1. **Create a form** in `tools/forms.py` — one `forms.Form` subclass with the fields you need.

2. **Create an implementation** in `tools/implementations.py` — subclass `BaseTool`, implement `validate()` and `process()`. `process()` must return a dict.

3. **Register the tool** in `tools/registry.py` — add an entry to `TOOL_CATALOG`:

```python
'my-tool-slug': {
    'class': 'tools.implementations.MyTool',
    'form_class': 'tools.forms.MyToolForm',
    'title': 'My Tool',
    'tagline': 'One punchy sentence shown on the catalog card.',
    'category': 'Facilitation',
    'what': 'Physical setup description.',
    'how': 'Step-by-step instructions.',
    'why': 'Facilitation rationale.',
    'agreements': ['Ground rule one.'],   # optional
    'example_input': {'field': 'value'},  # optional — powers Load example data
    'display_fields': ['field', 'word_count'],
    'timer_seconds': 300,                 # optional — session countdown timer
    'try_timer_seconds': 60,              # optional — solo try-it page timer
    'try_timer_label': 'Reflect alone',   # optional — label shown on try-it timer
    'show_canvas': False,                 # optional — enable freehand drawing canvas
},
```

No URL changes, migrations, or template changes are needed — the catalog, draft editor, and session pages pick up new tools automatically. To expose a tool on a public free try-it page, add its slug to `FREE_TOOL_SLUGS` in `tools/views.py`.

---

## Validation

All HTML, CSS, JavaScript, and Python source code has been validated and is free of errors.

---

### HTML — W3C Nu Html Checker

Every public page was checked against the [W3C Nu Html Checker](https://validator.w3.org/nu/). All pages return **"Document checking completed. No errors or warnings to show."**

| Page | URL checked | Result |
|---|---|---|
| Landing | `/` | No errors |
| About | `/about/` | No errors |
| Log in | `/accounts/login/` | No errors |
| Register | `/accounts/signup/` | No errors |

**Landing page** — the only HTML issue found during development was an `<h4>` step heading that immediately followed an `<h2>`, skipping heading level 3. This was corrected by changing all four step headings (`Pick a tool`, `Start a session`, `Work through the phases`, `Review the archive`) from `<h4>` to `<h3>`, and the matching CSS selector `.step h4` was updated to `.step h3`.

**Landing page (no errors):**

![W3C HTML validation — landing page](docs/validation/html_landing.png)

**About page (no errors):**

![W3C HTML validation — about page](docs/validation/html_about.png)

**Register page (no errors):**

![W3C HTML validation — register page](docs/validation/html_signup.png)

---

### CSS — W3C Jigsaw CSS Validator

The shared stylesheet `static/css/base.css` was validated against the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) at **CSS level 3 + SVG**. Result: **"Congratulations! No Error Found."**

![W3C CSS validation — base.css](docs/validation/css_base.png)

---

### JavaScript — JSHint

All 11 JavaScript files in `static/js/` were checked using **JSHint 2.13.6** with the configuration below. The result is **0 errors** across all files.

```json
{
  "browser": true,
  "esversion": 11,
  "globals": { "getCookie": true, "QRCode": true }
}
```

Files checked (all pass with 0 errors):

| File | Notes |
|---|---|
| `autosave.js` | — |
| `canvas_tool.js` | — |
| `drawing_canvas.js` | — |
| `qr_display.js` | — |
| `session_control.js` | — |
| `session_poll.js` | `laxbreak: true` for multi-line ternaries |
| `timer.js` | `/* jshint esversion:11, laxbreak:true, shadow:true, -W082, -W058 */` inline directive |
| `tool_try_timer.js` | `laxbreak: true` for multi-line ternaries |
| `waiting_list.js` | — |
| `feature_request.js` | — |
| `signup.js` | — |

![JSHint validator](docs/validation/js_jshint.png)

---

### Python — PEP 8 (flake8)

All Python source files were linted with **flake8** at `--max-line-length=119`. The result is **0 errors** across the full codebase.

Command run:

```bash
python -m flake8 accounts/ archive/ tools/ exporters/ config/ \
    --max-line-length=119 --exclude=__pycache__,migrations --count
```

Output:

```
0
```

Issues resolved during this pass:

| Category | File(s) | Fix applied |
|---|---|---|
| `F401` unused imports | `accounts/forms.py`, `tools/interface.py`, `archive/views.py` | Removed unused imports |
| `E302` expected 2 blank lines | `accounts/signals.py`, `tools/utils.py` | Added missing blank lines |
| `W605` invalid escape sequence | `exporters/rtf_gen.py` | Changed string literals to raw strings (`r"..."`) |
| `E501` line too long | `tools/implementations.py`, `tools/registry.py`, `tools/urls.py` | Rewrapped lines within 119-char limit |
| `F405` may be from star import | `config/settings/production.py` | Added `# noqa: F401,F403` where star import is intentional |

---

## Testing

All user-facing flows were tested manually against the running application with `DEBUG=False` to replicate production behaviour. Tests were carried out in Chrome (desktop) and Firefox (desktop). The tables below are grouped by feature area.

### 1 — Public pages

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Landing page loads | Navigate to `/` | Page renders with hero section, tool previews, and nav links for About, Login, Sign up | As expected | Pass |
| About page loads | Navigate to `/about/` | About page renders with product description and call-to-action links | As expected | Pass |
| Waiting list signup — valid | Navigate to `/waiting-list/`; enter valid email; submit | Success message shown; entry recorded in database | As expected | Pass |
| Waiting list signup — duplicate email | Submit the same email a second time | Form rejects the duplicate with a validation error | As expected | Pass |
| Waiting list signup — blank email | Submit form with empty email field | Form validation error; no submission | As expected | Pass |
| Feature request — valid | Navigate to `/request-a-feature/`; fill in subject and body; submit | Success message shown; request recorded | As expected | Pass |
| Feature request — blank subject | Submit form with empty subject | Form validation error; no submission | As expected | Pass |
| Free try-it — Min Specs | Navigate to `/tools/min-specs/try/`; fill in the prompt fields; submit | Results displayed on page without requiring login | As expected | Pass |
| Free try-it — 15% Solutions | Navigate to `/tools/15-solutions/try/`; fill in the prompt fields; submit | Results displayed on page without requiring login | As expected | Pass |
| Nav links resolve (public) | Click KwaCart logo, About, Login, Sign up in top nav | Each link navigates to the correct page without a 404 | As expected | Pass |

---

### 2 — Registration

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Successful registration | Navigate to `/accounts/signup/`; enter a new email and matching passwords; submit | Account created; user redirected to the tool catalog | As expected | Pass |
| Duplicate email | Attempt signup with an email that already exists | Form shows a validation error; no second account created | As expected | Pass |
| Passwords do not match | Enter two different passwords; submit | Form shows a validation error | As expected | Pass |
| Password too short | Enter a password shorter than 8 characters; submit | Django's built-in validators reject it with an explanation | As expected | Pass |
| Invalid email format | Enter a string without `@`; submit | Form validation error | As expected | Pass |

---

### 3 — Login and logout

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Successful login | Navigate to `/accounts/login/`; enter valid credentials; submit | User redirected to tool catalog; nav shows email and Logout button | As expected | Pass |
| Wrong password | Submit with a correct email but wrong password | Error message shown; user not authenticated | As expected | Pass |
| Unknown email | Submit with an email that has no account | Error message shown; user not authenticated | As expected | Pass |
| Logout | Click the Logout button in the nav | User session cleared; redirected to login page; nav reverts to public state | As expected | Pass |
| Access protected page while logged out | Navigate to `/tools/` without a session | Redirected to `/accounts/login/?next=/tools/` | As expected | Pass |
| Login redirect | Follow redirect from a protected page; log in | After login, user returned to the originally requested URL | As expected | Pass |

---

### 4 — Solo tool — draft creation and autosave

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Tool catalog loads | Log in; navigate to `/tools/` | Catalog page lists all available facilitation tools | As expected | Pass |
| Open draft editor | Click a tool; click "Start solo" | Draft editor page loads with the tool's prompt fields | As expected | Pass |
| Autosave on input | Begin typing in a prompt field; wait 2–3 seconds | Status indicator changes to "Saved" without a manual save action | As expected | Pass |
| Autosave persists on reload | Reload the draft editor after autosave | Previously entered text is pre-populated in the fields | As expected | Pass |
| Manual save button | Click the Save button explicitly | "Draft saved." success message appears | As expected | Pass |
| Resume existing draft | Navigate away; return to the tool's draft URL | Draft content is restored from the last save | As expected | Pass |

---

### 5 — Solo tool — submit and archive

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Submit completed draft | Fill in all required fields; click Submit | "Tool execution successful. Files generated." message shown; redirected to archive detail | As expected | Pass |
| Submit incomplete draft | Clear a required field; click Submit | Validation error shown; no archive entry created | As expected | Pass |
| Archive entry created | After successful submission, view `/archive/dashboard/` | New entry appears in the archive list with timestamp and tool name | As expected | Pass |
| Cannot submit another user's draft | Attempt to load a draft URL belonging to a different account | 403 response returned | As expected | Pass |

---

### 6 — Collaborative session — host flow

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Create session | From a tool page, click "Start a live session" | Session created; host sees the session room with a QR code and shareable guest link | As expected | Pass |
| QR code displayed | On the session page, view the QR code panel | QR code is visible and encodes the guest join URL | As expected | Pass |
| Copy guest link | Click the copy-link button next to the guest URL | URL copied to clipboard (button changes state to confirm) | As expected | Pass |
| Timer start | Click the Start timer button in the session room | Countdown begins and is visible to the host | As expected | Pass |
| Timer reset | Click Reset timer | Timer returns to the configured duration | As expected | Pass |
| Pause reminder | Timer reaches zero | Pause reminder notification displayed | As expected | Pass |
| Close session | Click "Close session" | "Session closed. Combined results are now visible." message; session status updated; combined export available in archive | As expected | Pass |
| Cannot close another user's session | Attempt to POST to `/tools/session/<id>/close/` with a different logged-in account | 403 returned; session not closed | As expected | Pass |

---

### 7 — Collaborative session — participant and guest flow

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Authenticated participant joins | Log in as a second account; open the session detail URL | Session room loads; participant's prompt fields are displayed | As expected | Pass |
| Participant submits response | Fill in the prompt fields; click Submit | "Your response was saved." message shown | As expected | Pass |
| Guest joins via QR / link (no account) | Open the guest join URL in a browser with no session | Guest join page loads; guest prompted to enter name/email and fill in prompts | As expected | Pass |
| Guest response saved | Guest fills in prompts and submits | "Your response was saved." confirmation; no account required | As expected | Pass |
| Guest cannot join a closed session | Attempt to open guest URL after host has closed the session | Page informs guest the session is no longer accepting responses | As expected | Pass |
| Session status polling | Participant page auto-polls session status | Host-initiated close is detected and participant's view updates without a manual reload | As expected | Pass |

---

### 8 — Archive dashboard and detail

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Archive dashboard loads | Log in; navigate to `/archive/dashboard/` | Lists all solo and session archive entries belonging to the logged-in user only | As expected | Pass |
| Solo entry detail | Click a solo archive entry | Detail page shows the submission content and download links | As expected | Pass |
| Session entry detail | Click a session archive entry | Detail page shows combined responses from host, participants, and guests | As expected | Pass |
| Cross-user isolation | Log in as a second account; navigate to `/archive/detail/<id>/` using an ID owned by account one | 403 returned; content not visible | As expected | Pass |
| Unauthenticated access | Navigate to `/archive/dashboard/` without a session | Redirected to login page | As expected | Pass |

---

### 9 — Archive delete

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Delete own record | From archive detail, click Delete; confirm | "Record deleted successfully." message; entry removed from dashboard | As expected | Pass |
| Delete another user's record | POST to `/archive/delete/<id>/` with an ID owned by a different account | 403 returned; record not deleted | As expected | Pass |

---

### 10 — Downloads

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| Solo Markdown download | From archive detail, click the Markdown download link | `.md` file downloads with the tool output formatted in Markdown | As expected | Pass |
| Solo RTF download | Click the RTF download link | `.rtf` file downloads and opens correctly in a word processor | As expected | Pass |
| Solo HTML download | Click the HTML download link | `.html` file downloads with styled output | As expected | Pass |
| Session combined Markdown download | From a closed session's detail page, click the combined Markdown download | Single `.md` file containing all participant responses downloads | As expected | Pass |
| Session combined RTF download | Click the combined RTF download | Combined `.rtf` file downloads | As expected | Pass |
| Download another user's file | Attempt to access `/archive/download/<id>/md/` using an ID owned by another account | 403 returned; no file served | As expected | Pass |
| Download from closed session — other user | Attempt to access `/archive/session-download/<uuid>/md/` for a session not hosted by the current user | 403 returned | As expected | Pass |

---

### 11 — Access control and redirects

| Feature | Test steps | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|
| 404 custom page | Navigate to a URL that does not exist (e.g. `/does-not-exist/`) with `DEBUG=False` | Custom 404 template renders with "Page not found" and navigation buttons | As expected | Pass |
| 403 custom page | Trigger a permission-denied response (e.g. accessing another user's archive record) | Custom 403 template renders with "Access denied" | As expected | Pass |
| Admin restricted to staff | Navigate to `/admin/` as a non-staff authenticated user | Redirected to admin login; access not granted | As expected | Pass |
| Admin accessible to superuser | Log in as a superuser; navigate to `/admin/` | Django admin interface loads | As expected | Pass |
| Draft editor requires login | Navigate to `/tools/<slug>/draft/` without a session | Redirected to `/accounts/login/?next=…` | As expected | Pass |
| Session detail requires login | Navigate to `/tools/session/<uuid>/` without a session | Redirected to login page | As expected | Pass |
| Autosave endpoint rejects unauthenticated POST | POST to `/tools/<slug>/autosave/` without a session | 302 redirect to login returned; draft not saved | As expected | Pass |

---

## Credits

### Project

Built as Milestone Project 3 for the Level 5 Diploma in Web Software Engineering.

### Facilitation methodology

Liberating Structures — created by Henri Lipmanowicz and Keith McCandless — a collection of microstructures that support including and unleashing everyone in a group. See [liberatingstructures.com](https://www.liberatingstructures.com). Tool names, descriptions, phases, and facilitation guidance throughout the platform are drawn from this methodology.

### Python / Django ecosystem (installed via `requirements.txt`)

| Package | Licence | Purpose |
|---|---|---|
| [Django](https://www.djangoproject.com) | BSD-3-Clause | Web framework — ORM, views, forms, auth, admin |
| [WhiteNoise](https://whitenoise.readthedocs.io) | MIT | Static file serving in production |
| [Gunicorn](https://gunicorn.org) | MIT | WSGI HTTP server |
| [django-environ](https://django-environ.readthedocs.io) | MIT | Environment-variable configuration |
| [dj-database-url](https://github.com/jazzband/dj-database-url) | BSD-2-Clause | Database URL parsing |
| [psycopg2-binary](https://www.psycopg.org) | LGPL-3.0 | PostgreSQL adapter (production database) |
| [Playwright](https://playwright.dev/python/) | Apache-2.0 | Browser automation used in the test suite |
| [pytest-django](https://pytest-django.readthedocs.io) | BSD-3-Clause | Django integration for pytest |
| [pytest-playwright](https://github.com/microsoft/playwright-pytest) | Apache-2.0 | Playwright integration for pytest |

### JavaScript libraries (vendored — not installed via a package manager)

| Library | Licence | File | Purpose |
|---|---|---|---|
| [qrcode.js](https://github.com/davidshimjs/qrcodejs) by davidshimjs | MIT | `static/js/libraries/qrcode.min.js` | Client-side QR code generation for the guest-join link on the session page |

The file is included verbatim from the upstream release. An attribution comment has been added at the top of the file.

### Learner-written code

All code **not** listed above was written by the project author. This includes:

- All Python source files: `accounts/`, `archive/`, `tools/`, `exporters/`, `config/`
- All JavaScript files in `static/js/` except the vendored library above
- All CSS files in `static/css/`
- All HTML templates in `templates/`
- All migration files in `*/migrations/`
