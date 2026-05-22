# Habit Builder — App Design Plan
*Powered by the Atomic Habits framework by James Clear*

---

## Overview

Habit Builder takes a personal goal stated in plain language and uses AI to break it down into micro-habits, smart reminders, and a structured 66-day plan — applying James Clear's four laws of behaviour change at every step.

---

## The Four Laws — App Pillars

### Law 1 — Make it obvious
- Goal intake in plain English
- Habit stacking suggestions ("after I do X, I will Y")
- Implementation intentions ("when X happens, I will do Y")

### Law 2 — Make it attractive
- Temptation bundling (pair a habit you need with something you enjoy)
- Identity reframing: "I am someone who…"
- Motivational context tied to the user's stated goal

### Law 3 — Make it easy
- 2-minute rule breakdown (every habit reduced to a 2-minute version)
- Friction reduction tips
- Environment design prompts

### Law 4 — Make it satisfying
- Streak tracking with never-miss-twice rule
- Progress visualisation (habit heatmap)
- Identity score that grows as habits compound

---

## Core Features

| Feature | Description |
|---|---|
| AI goal breakdown | Claude takes any goal and returns micro-habits, habit stacks, and a 66-day plan |
| Daily check-in | One-tap habit logging with streak counter and never-miss-twice nudge |
| Progress & streaks | GitHub-style habit heatmap, streak count, and identity score |
| Smart reminders | Context-aware notifications tied to implementation intentions |
| Weekly review | AI-generated reflection on patterns, friction, and suggested adjustments |
| Identity builder | Tracks "votes" for the new identity; reframes each check-in as proof of who you're becoming |

---

## Key Screens

### 1. Onboarding / Goal setup
- Enter your goal in plain English
- Choose your starting identity statement ("I am someone who…")
- Set implementation intention (when / where / how)
- Pick cue, routine, reward
- AI generates 3 micro-habits to start with

### 2. Today view
- Habit list with one-tap check-off
- Current streak + identity progress
- Friction reduction tip of the day
- 2-minute fallback if the habit feels hard
- Quick journal: what went well?

### 3. Weekly review
- Heatmap of the last 7 days
- AI insight on patterns and friction points
- Suggested habit adjustments
- Identity score trend
- Option to evolve the habit as it becomes automatic

---

## Build Phases

### Phase 1 — MVP (Core loop)
- Goal intake + AI breakdown
- Daily check-in + streak counter
- Push notifications
- Basic progress view

### Phase 2 — Sustain (Retention layer)
- Weekly AI review
- Never-miss-twice alerts
- Identity tracker
- Habit heatmap

### Phase 3 — Deepen (Compound growth)
- Habit stacking engine
- Temptation bundling
- Multi-habit management
- Environment design tips

---

## AI Architecture (Claude API)

Each core feature is powered by a Claude API call:

| Feature | Prompt input | Output |
|---|---|---|
| Goal breakdown | User's goal in plain text | Micro-habits, habit stack, 66-day curve, friction warnings |
| Weekly review | 7-day check-in history | Pattern analysis, what's working, adjustments |
| Friction analysis | Missed days + user notes | Root cause, friction reduction suggestions |
| Identity framing | Goal + completed habits | Identity statement, "votes cast" count |

---

## Key Design Decisions

- **Today view must be frictionless** — one tap to log. Any more friction and users drop off.
- **2-minute rule fallback** should be surfaced prominently on the Today view.
- **Identity framing is the differentiator** — every check-in should reinforce who the user is becoming, not just log a task completed.
- **66-day curve** — research supports 66 days to automaticity (not the popular but incorrect "21 days").
- **Never-miss-twice** is a hard rule enforced by the app, not just a suggestion.

---

## Tech Stack Suggestion

| Layer | Recommendation |
|---|---|
| Frontend | React Native (iOS + Android from one codebase) |
| Backend | Node.js + Express or Next.js API routes |
| Database | Supabase (Postgres + auth + realtime) |
| AI | Anthropic Claude API (claude-sonnet-4-20250514) |
| Notifications | Expo Push Notifications or OneSignal |
| Analytics | PostHog (open source, self-hostable) |

---

*Design document generated with Claude — Anthropic*
