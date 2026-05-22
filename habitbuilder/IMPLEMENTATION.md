# Habit Builder — Phase 1 Implementation Design

*Atomic Habits app — Phase 1: Core loop*

---

## Overview

Habit Builder takes a personal goal stated in plain language and uses AI to break it down into
micro-habits on Day 1. All subsequent user journeys — check-ins, streaks, reminders, and progress
tracking — run entirely offline using local Python logic and a SQLite database. No external service
dependencies beyond the Anthropic SDK.

---

## Guiding Principles

- **AI is used once** — on Day 1 during onboarding only. The AI output seeds the database and all
  further journeys are powered by local logic.
- **Self-contained** — no cloud services, no accounts, no internet required after onboarding.
- **Lean stack** — pure Python end-to-end: UI, logic, data, and notifications all in one language.
- **Offline-first** — the app works fully without an internet connection after the initial goal
  breakdown.

---

## Mobile Framework

### Recommended: Kivy + KivyMD

Pure Python cross-platform framework for iOS, Android, and Desktop. KivyMD provides Material
Design UI components. Chosen because the entire codebase — UI, logic, and data — stays in Python
with no language switching.

**Key packages:**
- `kivy` — cross-platform UI framework
- `kivymd` — Material Design components for Kivy
- `buildozer` — packaging and deployment to Android and iOS

### Alternatives Considered

| Framework | Approach | Trade-off |
|---|---|---|
| BeeWare (Toga) | Python → native platform UI | Truly native look, but younger ecosystem and fewer widgets |
| Flutter + Python backend | Dart UI + Python FastAPI | Best UI quality, but requires learning Dart for the frontend layer |

---

## AI Usage — Day 1 Only

The Claude API is called exactly once per goal during onboarding. It takes the user's plain-text
goal and returns a structured habit plan which is persisted to SQLite. From this point the app
runs with no further API calls.

### What the AI generates on Day 1

- 3 micro-habits derived from the goal
- A 2-minute fallback version for each habit (for hard days)
- An implementation intention / cue for each habit ("after I do X, I will Y")
- An identity statement ("I am someone who…")

### What the AI does NOT power

| User journey | Powered by |
|---|---|
| Daily check-in (tap to log) | Local Python + SQLite write |
| Streak calculation | Python date arithmetic on checkins table |
| Never-miss-twice detection | Python comparing last_checkin to today's date |
| Reminders and notifications | `plyer` + `schedule` library (local, free) |
| Progress view | SQLite query rendered in Kivy UI |
| 2-minute fallback display | Stored in habits table from Day 1 AI output |

---

## Technology Stack

| Layer | Tool | Cost |
|---|---|---|
| Mobile UI | Kivy + KivyMD | Free / open source |
| Database | SQLite + peewee ORM | Free / built-in to Python |
| Notifications | plyer | Free / open source |
| Job scheduling | schedule | Free / open source |
| Data validation | pydantic | Free / open source |
| AI — onboarding only | Anthropic SDK | Pay-per-use API (one call per goal) |

### Note on notifications

`plyer` wraps each platform's native notification system (Android notification API, iOS local
notifications, OS notification centre on desktop). It is entirely free and open source — no server,
no account, no paid service. It fires notifications directly from the app process on the device.

Limitation: `plyer` handles local notifications scheduled from within the app. Background
notifications when the app is closed require a push service (e.g. Firebase). This is acceptable
for Phase 1 and can be revisited in Phase 2.

---

## SQLite Schema

### Table: users

| Column | Type | Note |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Display name |
| goal_raw | TEXT | Plain-text goal as entered by user |
| identity_statement | TEXT | "I am someone who…" — AI generated |
| created_at | DATETIME | Onboarding timestamp |

### Table: habits

| Column | Type | Note |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| user_id | INTEGER FK | → users.id |
| title | TEXT | AI-generated habit label |
| two_min_version | TEXT | 2-minute fallback micro-habit |
| cue | TEXT | Implementation intention ("after X, I will Y") |
| sort_order | INTEGER | Display ordering in Today view |

### Table: checkins

| Column | Type | Note |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| habit_id | INTEGER FK | → habits.id |
| checked_at | DATE | Date of check-in (one per day per habit) |
| used_fallback | BOOLEAN | True if the 2-minute rule was used |
| note | TEXT | Optional quick journal entry |

### Table: streaks

| Column | Type | Note |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| habit_id | INTEGER FK | → habits.id |
| current_streak | INTEGER | Current consecutive days |
| longest_streak | INTEGER | Personal best streak |
| last_checkin | DATE | Used for never-miss-twice detection |

---

## Project Structure

```
habitbuilder/
├── main.py                  # App entry point
├── habitbuilder.kv          # Kivy UI layout definitions
├── db/
│   ├── models.py            # peewee ORM model classes
│   └── database.py          # SQLite initialisation and migrations
├── services/
│   ├── ai_service.py        # Claude API call — onboarding only
│   ├── habit_service.py     # Streak calculation and check-in logic
│   └── notify_service.py    # Reminder scheduling via plyer + schedule
├── screens/
│   ├── onboarding.py        # Goal intake screen (triggers AI call)
│   ├── today.py             # Daily check-in view
│   └── progress.py          # Streak and progress view
└── habitbuilder.db          # SQLite database file (auto-created on first run)
```

---

## Key Screens — Phase 1

### 1. Onboarding screen
- User enters their goal in plain English
- App calls Claude API (one-time) and shows a loading state
- AI response is parsed and written to `habits` table
- User confirms their identity statement
- User sets their preferred daily reminder time

### 2. Today view
- Lists all habits with a one-tap check-off button
- Shows current streak count per habit
- Surfaces the 2-minute fallback if the user taps "this feels hard today"
- Optional quick note field per check-in
- Never-miss-twice banner shown if yesterday was missed

### 3. Progress view
- Streak count (current and personal best) per habit
- Simple calendar heatmap of check-in history
- Identity statement displayed as a motivational anchor

---

## Core Logic — Streak Calculation

```python
from datetime import date, timedelta

def update_streak(habit_id: int):
    streak = Streak.get(Streak.habit_id == habit_id)
    today = date.today()
    yesterday = today - timedelta(days=1)

    if streak.last_checkin == yesterday:
        # Continuing streak
        streak.current_streak += 1
    elif streak.last_checkin == today:
        # Already checked in today — no change
        return
    else:
        # Streak broken — reset
        streak.current_streak = 1

    streak.last_checkin = today
    streak.longest_streak = max(streak.longest_streak, streak.current_streak)
    streak.save()
```

---

## Core Logic — AI Service (Day 1)

```python
import anthropic
import json

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are a habit coach applying the Atomic Habits framework.
Given a user's goal, return ONLY a valid JSON object with this structure:
{
  "identity_statement": "I am someone who...",
  "habits": [
    {
      "title": "Short habit label",
      "two_min_version": "2-minute fallback version",
      "cue": "After I [existing habit], I will [new habit]"
    }
  ]
}
Return exactly 3 habits. No preamble, no markdown, only the JSON object."""

def breakdown_goal(goal: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"My goal: {goal}"}]
    )
    return json.loads(response.content[0].text)
```

---

## Phase 1 Build Order

1. Set up project structure and virtual environment
2. Define peewee ORM models and SQLite initialisation
3. Build AI service and test goal breakdown
4. Build onboarding screen — goal input → AI call → DB seed
5. Build Today view — habit list, check-in, streak display
6. Build streak and never-miss-twice logic
7. Build notification scheduling with plyer
8. Build Progress view — heatmap and streak stats
9. Package with buildozer for Android

---

## Out of Scope for Phase 1

The following are planned for Phase 2 and Phase 3:

- Weekly AI review and reflection
- Habit stacking engine
- Temptation bundling suggestions
- Background push notifications (requires Firebase)
- Identity score trend over time
- Multi-habit management beyond the initial 3
- Environment design tips

---

*Implementation design produced with Claude — Anthropic*
