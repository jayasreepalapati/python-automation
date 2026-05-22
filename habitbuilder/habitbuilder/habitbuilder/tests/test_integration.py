"""
Integration tests — exercise the full user journey end-to-end
using an in-memory SQLite database and a mocked AI service.
No real API calls are made.
"""
import json
import pytest
from datetime import date, timedelta
from unittest.mock import MagicMock

from db.models import User, Habit, CheckIn, Streak
from services.ai_service import AIService, HabitPlan
from services.habit_service import HabitService


MOCK_PLAN = HabitPlan(
    identity_statement="I am someone who moves every day",
    habits=[
        {"title": "Morning run",
         "two_min_version": "Step outside for fresh air",
         "cue": "After I wake up, I will go for a run"},
        {"title": "Evening stretch",
         "two_min_version": "Do one stretch",
         "cue": "After dinner, I will stretch"},
        {"title": "Log workout",
         "two_min_version": "Write one word",
         "cue": "After exercise, I will log it"},
    ]
)


def make_ai_service_mock():
    service = AIService.__new__(AIService)
    service.breakdown_goal = MagicMock(return_value=MOCK_PLAN)
    return service


class TestOnboardingJourney:
    """Day 1 — user enters goal, AI breaks it down, data is seeded."""

    def setup_method(self):
        self.ai = make_ai_service_mock()
        self.habit_svc = HabitService()

    def test_full_onboarding_creates_user(self):
        user = User.create(name="Jayasree", goal_raw="I want to exercise daily")
        plan = self.ai.breakdown_goal(user.goal_raw)
        self.habit_svc.seed_from_plan(user, plan)

        assert User.select().count() == 1
        user.refresh()
        assert user.identity_statement == "I am someone who moves every day"

    def test_full_onboarding_creates_three_habits(self):
        user = User.create(name="Jayasree", goal_raw="I want to exercise daily")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)

        assert len(habits) == 3
        assert Habit.select().where(Habit.user == user).count() == 3

    def test_full_onboarding_creates_streaks(self):
        user = User.create(name="Jayasree", goal_raw="I want to exercise daily")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)

        for habit in habits:
            streak = Streak.get(Streak.habit == habit)
            assert streak.current_streak == 0
            assert streak.last_checkin is None

    def test_ai_called_exactly_once(self):
        user = User.create(name="Jayasree", goal_raw="I want to exercise daily")
        plan = self.ai.breakdown_goal(user.goal_raw)
        self.habit_svc.seed_from_plan(user, plan)

        assert self.ai.breakdown_goal.call_count == 1


class TestDailyCheckinJourney:
    """Day N — user opens app, checks in habits, streaks update."""

    def setup_method(self):
        self.habit_svc = HabitService()
        self.ai = make_ai_service_mock()

    def _onboard(self) -> tuple:
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)
        return user, habits

    def test_checkin_all_habits(self):
        user, habits = self._onboard()
        for habit in habits:
            self.habit_svc.checkin(habit)

        total = CheckIn.select().count()
        assert total == 3

    def test_streak_increments_per_habit(self):
        user, habits = self._onboard()
        for habit in habits:
            self.habit_svc.checkin(habit)

        for habit in habits:
            streak = self.habit_svc.get_streak(habit)
            assert streak.current_streak == 1

    def test_partial_checkin_correct_streaks(self):
        user, habits = self._onboard()
        self.habit_svc.checkin(habits[0])

        assert self.habit_svc.get_streak(habits[0]).current_streak == 1
        assert self.habit_svc.get_streak(habits[1]).current_streak == 0

    def test_fallback_checkin_still_counts(self):
        user, habits = self._onboard()
        self.habit_svc.checkin(habits[0], used_fallback=True)

        streak = self.habit_svc.get_streak(habits[0])
        assert streak.current_streak == 1


class TestStreakJourney:
    """Multi-day streak building and break scenarios."""

    def setup_method(self):
        self.habit_svc = HabitService()
        self.ai = make_ai_service_mock()

    def _onboard_one_habit(self):
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)
        return habits[0]

    def _simulate_checkin_on(self, habit, d: date):
        """Directly insert a check-in on a specific date and update streak."""
        CheckIn.create(habit=habit, checked_at=d)
        streak = Streak.get(Streak.habit == habit)
        yesterday = d - timedelta(days=1)
        if streak.last_checkin == yesterday:
            streak.current_streak += 1
        else:
            streak.current_streak = 1
        streak.last_checkin = d
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.save()

    def test_seven_day_streak(self):
        habit = self._onboard_one_habit()
        today = date.today()
        for i in range(6, 0, -1):
            self._simulate_checkin_on(habit, today - timedelta(days=i))
        self.habit_svc.checkin(habit)
        assert self.habit_svc.get_streak(habit).current_streak == 7

    def test_streak_breaks_then_rebuilds(self):
        habit = self._onboard_one_habit()
        today = date.today()
        for i in range(3, 1, -1):
            self._simulate_checkin_on(habit, today - timedelta(days=i))

        self.habit_svc.checkin(habit)
        assert self.habit_svc.get_streak(habit).current_streak == 1

    def test_longest_streak_preserved_after_break(self):
        habit = self._onboard_one_habit()
        streak = Streak.get(Streak.habit == habit)
        streak.longest_streak = 14
        streak.current_streak = 0
        streak.last_checkin = date.today() - timedelta(days=5)
        streak.save()

        self.habit_svc.checkin(habit)
        assert self.habit_svc.get_streak(habit).longest_streak == 14


class TestNeverMissTwiceJourney:

    def setup_method(self):
        self.habit_svc = HabitService()
        self.ai = make_ai_service_mock()

    def test_nudge_shown_after_missed_day(self):
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)
        habit = habits[0]

        streak = Streak.get(Streak.habit == habit)
        streak.last_checkin = date.today() - timedelta(days=2)
        streak.save()

        assert self.habit_svc.is_never_miss_twice(habit) is True

    def test_nudge_clears_after_checkin(self):
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)
        habit = habits[0]

        streak = Streak.get(Streak.habit == habit)
        streak.last_checkin = date.today() - timedelta(days=2)
        streak.save()

        self.habit_svc.checkin(habit)
        assert self.habit_svc.is_never_miss_twice(habit) is False


class TestProgressJourney:

    def setup_method(self):
        self.habit_svc = HabitService()
        self.ai = make_ai_service_mock()

    def test_heatmap_returns_correct_dates(self):
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        habits = self.habit_svc.seed_from_plan(user, plan)
        habit = habits[0]

        today = date.today()
        for i in range(5):
            CheckIn.create(habit=habit, checked_at=today - timedelta(days=i))

        checkins = self.habit_svc.get_checkins_for_habit(habit, days=66)
        assert len(checkins) == 5
        assert today in checkins

    def test_get_habits_for_user_ordered(self):
        user = User.create(name="Jayasree", goal_raw="Get fit")
        plan = self.ai.breakdown_goal(user.goal_raw)
        self.habit_svc.seed_from_plan(user, plan)

        habits = self.habit_svc.get_habits_for_user(user)
        assert [h.sort_order for h in habits] == [0, 1, 2]
