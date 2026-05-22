import pytest
from datetime import date
from db.models import User, Habit, CheckIn, Streak


class TestUserModel:

    def test_create_user(self, user):
        assert user.id is not None
        assert user.name == "Test User"
        assert user.goal_raw == "I want to exercise every day"

    def test_user_defaults(self):
        u = User.create(name="Jane", goal_raw="Read more books")
        assert u.identity_statement == ""
        assert u.created_at is not None

    def test_user_count(self, user):
        assert User.select().count() == 1


class TestHabitModel:

    def test_create_habit(self, habit, user):
        assert habit.id is not None
        assert habit.title == "Go for a 30-minute run"
        assert habit.user_id == user.id

    def test_habit_has_two_min_version(self, habit):
        assert habit.two_min_version == "Put on running shoes"

    def test_habit_has_cue(self, habit):
        assert "After I wake up" in habit.cue

    def test_multiple_habits_per_user(self, user):
        for i in range(3):
            Habit.create(
                user=user,
                title=f"Habit {i}",
                two_min_version="2 min",
                cue="cue",
                sort_order=i
            )
        assert Habit.select().where(Habit.user == user).count() == 3

    def test_habit_sort_order(self, user):
        for i in [2, 0, 1]:
            Habit.create(user=user, title=f"H{i}", two_min_version="x",
                         cue="c", sort_order=i)
        habits = list(Habit.select().where(Habit.user == user).order_by(Habit.sort_order))
        assert [h.sort_order for h in habits] == [0, 1, 2]


class TestCheckInModel:

    def test_create_checkin(self, habit):
        ci = CheckIn.create(habit=habit, checked_at=date.today())
        assert ci.id is not None
        assert ci.checked_at == date.today()
        assert ci.used_fallback is False

    def test_checkin_with_fallback(self, habit):
        ci = CheckIn.create(habit=habit, checked_at=date.today(), used_fallback=True)
        assert ci.used_fallback is True

    def test_checkin_with_note(self, habit):
        ci = CheckIn.create(habit=habit, checked_at=date.today(), note="Felt great!")
        assert ci.note == "Felt great!"

    def test_duplicate_checkin_raises(self, habit):
        CheckIn.create(habit=habit, checked_at=date.today())
        with pytest.raises(Exception):
            CheckIn.create(habit=habit, checked_at=date.today())


class TestStreakModel:

    def test_streak_created_with_zeros(self, habit):
        streak = Streak.get(Streak.habit == habit)
        assert streak.current_streak == 0
        assert streak.longest_streak == 0
        assert streak.last_checkin is None

    def test_streak_update(self, habit):
        streak = Streak.get(Streak.habit == habit)
        streak.current_streak = 5
        streak.longest_streak = 10
        streak.last_checkin = date.today()
        streak.save()

        refreshed = Streak.get(Streak.habit == habit)
        assert refreshed.current_streak == 5
        assert refreshed.longest_streak == 10
