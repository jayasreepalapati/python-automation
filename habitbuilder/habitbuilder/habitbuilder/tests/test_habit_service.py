import pytest
from datetime import date, timedelta
from unittest.mock import patch

from db.models import CheckIn, Streak
from services.habit_service import HabitService
from services.ai_service import HabitPlan


class TestHabitServiceCheckin:

    def setup_method(self):
        self.service = HabitService()

    def test_checkin_creates_record(self, habit):
        ci = self.service.checkin(habit)
        assert ci.id is not None
        assert ci.checked_at == date.today()

    def test_checkin_idempotent(self, habit):
        ci1 = self.service.checkin(habit)
        ci2 = self.service.checkin(habit)
        assert ci1.id == ci2.id
        assert CheckIn.select().where(CheckIn.habit == habit).count() == 1

    def test_checkin_with_fallback(self, habit):
        ci = self.service.checkin(habit, used_fallback=True)
        assert ci.used_fallback is True

    def test_checked_in_today_true(self, habit):
        self.service.checkin(habit)
        assert self.service.checked_in_today(habit) is True

    def test_checked_in_today_false(self, habit):
        assert self.service.checked_in_today(habit) is False


class TestStreakLogic:

    def setup_method(self):
        self.service = HabitService()

    def test_first_checkin_streak_is_one(self, habit):
        self.service.checkin(habit)
        streak = self.service.get_streak(habit)
        assert streak.current_streak == 1

    def test_consecutive_days_increases_streak(self, habit):
        yesterday = date.today() - timedelta(days=1)
        CheckIn.create(habit=habit, checked_at=yesterday)
        streak = Streak.get(Streak.habit == habit)
        streak.current_streak = 1
        streak.last_checkin = yesterday
        streak.save()

        self.service.checkin(habit)
        updated = self.service.get_streak(habit)
        assert updated.current_streak == 2

    def test_missed_day_resets_streak(self, habit):
        two_days_ago = date.today() - timedelta(days=2)
        streak = Streak.get(Streak.habit == habit)
        streak.current_streak = 5
        streak.longest_streak = 5
        streak.last_checkin = two_days_ago
        streak.save()

        self.service.checkin(habit)
        updated = self.service.get_streak(habit)
        assert updated.current_streak == 1

    def test_longest_streak_updates(self, habit):
        yesterday = date.today() - timedelta(days=1)
        streak = Streak.get(Streak.habit == habit)
        streak.current_streak = 9
        streak.longest_streak = 9
        streak.last_checkin = yesterday
        streak.save()

        self.service.checkin(habit)
        updated = self.service.get_streak(habit)
        assert updated.current_streak == 10
        assert updated.longest_streak == 10

    def test_longest_streak_not_reduced(self, habit):
        streak = Streak.get(Streak.habit == habit)
        streak.current_streak = 0
        streak.longest_streak = 20
        streak.last_checkin = date.today() - timedelta(days=5)
        streak.save()

        self.service.checkin(habit)
        updated = self.service.get_streak(habit)
        assert updated.longest_streak == 20

    def test_checkin_today_twice_no_double_increment(self, habit):
        self.service.checkin(habit)
        self.service.checkin(habit)
        streak = self.service.get_streak(habit)
        assert streak.current_streak == 1


class TestNeverMissTwice:

    def setup_method(self):
        self.service = HabitService()

    def test_never_miss_twice_triggered(self, habit):
        two_days_ago = date.today() - timedelta(days=2)
        streak = Streak.get(Streak.habit == habit)
        streak.last_checkin = two_days_ago
        streak.save()
        assert self.service.is_never_miss_twice(habit) is True

    def test_never_miss_twice_not_triggered_if_checked_today(self, habit):
        self.service.checkin(habit)
        assert self.service.is_never_miss_twice(habit) is False

    def test_never_miss_twice_not_triggered_if_checked_yesterday(self, habit):
        yesterday = date.today() - timedelta(days=1)
        streak = Streak.get(Streak.habit == habit)
        streak.last_checkin = yesterday
        streak.save()
        assert self.service.is_never_miss_twice(habit) is False

    def test_never_miss_twice_not_triggered_if_no_history(self, habit):
        assert self.service.is_never_miss_twice(habit) is False


class TestSeedFromPlan:

    def setup_method(self):
        self.service = HabitService()

    def test_seed_creates_habits(self, user):
        plan = HabitPlan(
            identity_statement="I am someone who moves daily",
            habits=[
                {"title": "Morning walk", "two_min_version": "Walk to door",
                 "cue": "After I wake up, I will walk"},
                {"title": "Evening stretch", "two_min_version": "One stretch",
                 "cue": "After dinner, I will stretch"},
                {"title": "Drink water", "two_min_version": "One glass",
                 "cue": "After each meal, I will drink water"},
            ]
        )
        habits = self.service.seed_from_plan(user, plan)
        assert len(habits) == 3
        user.refresh()
        assert user.identity_statement == "I am someone who moves daily"

    def test_seed_creates_streaks(self, user):
        plan = HabitPlan(
            identity_statement="I am someone who reads",
            habits=[
                {"title": "Read 10 pages", "two_min_version": "Read 1 page",
                 "cue": "After coffee, I will read"}
            ]
        )
        habits = self.service.seed_from_plan(user, plan)
        streak = Streak.get(Streak.habit == habits[0])
        assert streak.current_streak == 0
        assert streak.last_checkin is None


class TestGetCheckinsForHabit:

    def setup_method(self):
        self.service = HabitService()

    def test_returns_last_n_days(self, habit):
        today = date.today()
        for i in range(5):
            CheckIn.create(habit=habit, checked_at=today - timedelta(days=i))

        checkins = self.service.get_checkins_for_habit(habit, days=66)
        assert len(checkins) == 5

    def test_excludes_old_checkins(self, habit):
        old_date = date.today() - timedelta(days=100)
        CheckIn.create(habit=habit, checked_at=old_date)
        checkins = self.service.get_checkins_for_habit(habit, days=66)
        assert len(checkins) == 0
