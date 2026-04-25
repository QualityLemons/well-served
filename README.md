# Well-Served

**Milestone Project 3 — Level 5 Diploma in Web Software Engineering**

Well-Served is a Django-based facilitation platform designed to improve the dynamic of structured group activities inside organisations. It gives facilitators a bank of ready-made tools — warm-ups, reflection exercises, peer consultation formats, and more — that participants can complete individually or together in a live collaborative session. Responses are archived and exportable as Markdown and RTF documents.

---

## Table of Contents

1. [Purpose](#purpose)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Key Features](#key-features)
5. [Facilitation Tools](#facilitation-tools)
6. [Collaborative Sessions](#collaborative-sessions)
7. [Archive & Exports](#archive--exports)
8. [Data Models](#data-models)
9. [User Accounts](#user-accounts)
10. [Running Locally](#running-locally)
11. [Deployment](#deployment)
12. [Admin](#admin)
13. [Adding a New Tool](#adding-a-new-tool)
14. [Credits](#credits)

---

## Purpose

Organisations often struggle to create the conditions for honest, constructive dialogue. Well-Served provides a lightweight facilitation toolkit — grounded in Liberating Structures methodology — that any team can use to surface challenges, share hopes, and warm up to productive conversation. The platform removes the friction of paper-based activities by letting every participant log in, work through a structured prompt, and instantly see a combined result when the facilitator closes the session.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 6.0.4 |
| Database (dev) | SQLite (`db.sqlite3`) |
| Static files | WhiteNoise |
| Production server | Gunicorn |
| Hosting | Replit (development & production) |

---

## Project Structure

```
well-served/
├── config/                  Django project package
│   ├── settings/
│   │   ├── base.py          Shared settings (apps, middleware, auth, media)
│   │   └── local.py         Dev overrides (DEBUG=True, ALLOWED_HOSTS=['*'])
│   ├── urls.py              Root URL configuration
│   └── wsgi.py              WSGI entry point
│
├── accounts/                Custom user app (email-based auth)
│   ├── models.py            Custom User + UserManager
│   ├── forms.py             Registration / login forms
│   └── utils.py             log_action() helper (writes to AuditLog)
│
├── tools/                   Facilitation tool engine
│   ├── registry.py          TOOL_CATALOG — the single source of truth for every tool
│   ├── implementations.py   BaseTool subclasses (validate + process)
│   ├── forms.py             Django Form classes for each tool
│   ├── views.py             Solo draft flow + collaborative session flow
│   ├── urls.py              URL patterns (draft, autosave, submit, session CRUD)
│   └── utils.py             get_tool_metadata() with normalisation helper
│
├── archive/                 Submission records, sessions, audit log
│   ├── models.py            ToolSession, ToolInstance, AuditLog
│   ├── views.py             Archive dashboard + detail view
│   ├── views_downloads.py   Secure file download (solo + session exports)
│   └── urls.py
│
├── exporters/               File generation pipeline
│   ├── pipeline.py          run_export_pipeline() / run_session_export_pipeline()
│   ├── md_gen.py            Markdown generation (solo + combined session)
│   └── rtf_gen.py           RTF generation (solo + combined session)
│
├── templates/
│   ├── base.html            Site chrome (nav, messages, layout)
│   ├── accounts/            Login, registration, dashboard templates
│   ├── archive/             dashboard.html, detail.html
│   └── tools/
│       ├── catalog.html     Tool bank listing with Start solo / Start session
│       ├── draft_editor.html  Solo drafting interface
│       ├── session_open.html  Live collaborative session page
│       ├── session_closed.html Combined results + download links
│       ├── info_box.html    What / How / Why / agreements panel (included by editors)
│       └── _timer.html      Reusable countdown timer widget (sync-capable)
│
├── static/                  CSS, JS, images
├── media/                   Generated MD and RTF export files
├── manage.py
└── requirements.txt
```

---

## Key Features

### Solo tool use
Any logged-in user can pick a tool from the catalog, work through the form at their own pace, save a draft as many times as they like, then submit when ready. Submission runs the tool's processing logic and stores the result as an archived record with downloadable MD and RTF files.

### Collaborative sessions
A facilitator creates a **session** for any tool, which generates a unique shareable link. Participants open the link (login required), fill in their own copy of the form, and save as many times as they like. The facilitator sees a live participant list — including who has saved a response — that updates every four seconds without a page refresh. When everyone is done, the facilitator clicks **Close session and reveal results**, which:

- Locks all responses.
- Runs each participant's data through the tool's processing logic.
- Generates a combined Markdown and RTF export.
- Reveals a unified results page — showing every participant's response labelled with their email — to anyone with the session link.

### Archive dashboard
Every user's `/archive/dashboard/` shows:

- **Solo submissions** — a paginated table of their individually submitted records with a View link.
- **Sessions I'm part of** — every session they host or have joined, with role (Host / Participant), status (Open / Closed), and a direct link back to the session page.

### Timer widget
Tools can opt-in to a countdown timer (configurable per tool in seconds). The timer:

- Displays MM:SS, turns amber at ≤ 10 seconds, red at zero.
- Provides Start / Pause / Reset controls.
- Shows a phase progress bar that fills as time elapses.
- In collaborative sessions, syncs state in real time across all participants via the polling endpoint — including pause state and late joiners.
- Announces phase changes, milestone countdowns (at 60 s, 30 s, 10 s), and pause/resume events to screen reader users via an `aria-live` region.
- Displays a visible "Paused" badge so participants know a pause is intentional.

### What / How / Why info panel
Every tool page shows a structured instruction panel:

- **What** — the physical or group setup.
- **How** — step-by-step instructions.
- **Why** — the facilitation rationale.
- **Agreements** — per-tool ground rules (e.g. Conversation Café's six dialogue norms), rendered as a numbered list where defined.
- A **Load example data** button that pre-fills the form with sample responses.

### Tool catalog
The catalog page shows every tool as a card with its title, a short **tagline**, and two call-to-action buttons: Start solo and Start session.

---

## Facilitation Tools

22 tools are currently registered across two categories.

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
| Create | Host | Clicks **Start session** on a tool card → session created, shareable URL generated |
| Share | Host | Copies the URL and sends to participants |
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
| `host` | FK to User — the facilitator who created the session |
| `tool_slug` | Which tool this session runs |
| `tool_version` | Version string at time of creation |
| `status` | `open` or `closed` |
| `created_at` / `closed_at` | Timestamps |
| `md_file` / `rtf_file` | Combined export files (populated on close) |

### `ToolInstance`
One per user per session (or one per solo submission).

| Field | Description |
|---|---|
| `user` | FK to User |
| `session` | FK to ToolSession (null for solo submissions) |
| `tool_slug` / `tool_version` | Tool identity |
| `status` | `draft` → `archived` on submit / session close |
| `payload_input` | Raw form data (JSON) |
| `payload_output` | Processed result (JSON) |
| `md_file` / `rtf_file` | Per-instance export files (solo only) |
| `submitted_at` | Set when status transitions to `archived` |

A `UniqueConstraint` on `(session, user)` prevents a participant from having more than one response per session.

### `AuditLog`
Records login events, tool submissions, and file downloads with IP address and timestamp.

---

## User Accounts

Authentication is email-based (no username). The custom `User` model uses `email` as `USERNAME_FIELD`.

| URL | Purpose |
|---|---|
| `/accounts/login/` | Log in |
| `/accounts/register/` | Create an account |
| `/accounts/logout/` | Log out |
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

**Environment:** The project reads settings from `config.settings.local` by default (`DJANGO_SETTINGS_MODULE` is set in `manage.py`). No `.env` file is required for local development.

---

## Deployment

The project is configured for Replit Autoscale deployment using Gunicorn:

```
gunicorn --bind=0.0.0.0:5000 --reuse-port config.wsgi:application
```

`python manage.py migrate` runs as a build step before the server starts.

Static files are served by WhiteNoise (configured in `base.py` middleware).

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
    'category': 'My Category',
    'what': 'Physical setup description.',
    'how': 'Step-by-step instructions.',
    'why': 'Facilitation rationale.',
    'agreements': ['Ground rule one.', 'Ground rule two.'],  # optional
    'example_input': {'field_name': 'example value'},
    'display_fields': ['field_name', 'word_count'],
    'timer_seconds': 300,  # optional
},
```

No URL changes, migrations, or template changes are needed — the catalog, draft editor, and session pages pick up new tools automatically.

---

## Admin

The Django admin at `/admin/` provides full CRUD for:

- `ToolSession` — view and manage collaborative sessions.
- `ToolInstance` — view individual submissions.
- `AuditLog` — read-only activity trail.
- `User` — manage accounts and permissions.

Default superuser credentials (development only):
- Email: `admin@example.com`
- Password: `admin12345`

---

## Credits

Built as Milestone Project 3 for the Level 5 Diploma in Web Software Engineering.

Facilitation methodology draws on **Liberating Structures** — a collection of microstructures that supports including and unleashing everyone in a group.
