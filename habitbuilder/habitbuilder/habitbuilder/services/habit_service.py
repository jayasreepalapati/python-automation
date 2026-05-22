from datetime import date, timedelta
from db.models import User, Habit, CheckIn, Streak
from services.ai_service import AIService, HabitPlan


class HabitService:

    def seed_from_plan(self, user: User, plan: HabitPlan) -> list[Habit]:
        """
        Persist AI-generated habit plan to the database.
        Called once after onboarding. Creates habits and initialises streaks.
        """
        user.identity_statement = plan.identity_statement
        user.save()

        habits = []
        for i, h in enumerate(plan.habits):
            habit = Habit.create(
                user=user,
                title=h["title"],
                two_min_version=h["two_min_version"],
                cue=h["cue"],
                sort_order=i
            )
            Streak.create(
                habit=habit,
                current_streak=0,
                longest_streak=0,
                last_checkin=None
            )
            habits.append(habit)

        return habits

    def checkin(self, habit: Habit, used_fallback: bool = False, note: str = "") -> CheckIn:
        """
        Record a check-in for today. Idempotent — calling twice on the same day
        returns the existing check-in without creating a duplicate.
        """
        today = date.today()
        existing = (CheckIn
                    .select()
                    .where(CheckIn.habit == habit, CheckIn.checked_at == today)
                    .first())
        if existing:
            return existing

        checkin = CheckIn.create(
            habit=habit,
            checked_at=today,
            used_fallback=used_fallback,
            note=note
        )
        self._update_streak(habit)
        return checkin

    def _update_streak(self, habit: Habit) -> None:
        """Recalculate and persist streak after a check-in."""
        streak = Streak.get(Streak.habit == habit)
        today = date.today()
        yesterday = today - timedelta(days=1)

        if streak.last_checkin == today:
            return
        elif streak.last_checkin == yesterday:
            streak.current_streak += 1
        else:
            streak.current_streak = 1

        streak.last_checkin = today
        streak.longest_streak = max(streak.longest_streak, streak.current_streak)
        streak.save()

    def get_streak(self, habit: Habit) -> Streak:
        return Streak.get(Streak.habit == habit)

    def is_never_miss_twice(self, habit: Habit) -> bool:
        """
        Returns True if yesterday was missed and today has not been checked in yet.
        Used to surface the never-miss-twice nudge on the Today view.
        """
        streak = Streak.get(Streak.habit == habit)
        today = date.today()
        yesterday = today - timedelta(days=1)

        already_checked_today = (CheckIn
                                 .select()
                                 .where(CheckIn.habit == habit, CheckIn.checked_at == today)
                                 .exists())

        if already_checked_today:
            return False

        return streak.last_checkin is not None and streak.last_checkin < yesterday

    def get_checkins_for_habit(self, habit: Habit, days: int = 66) -> list[date]:
        """
        Return a list of dates on which the habit was checked in,
        going back `days` days. Used for the progress heatmap.
        """
        cutoff = date.today() - timedelta(days=days)
        rows = (CheckIn
                .select(CheckIn.checked_at)
                .where(CheckIn.habit == habit, CheckIn.checked_at >= cutoff)
                .order_by(CheckIn.checked_at))
        return [row.checked_at for row in rows]

    def get_habits_for_user(self, user: User) -> list[Habit]:
        return list(Habit.select().where(Habit.user == user).order_by(Habit.sort_order))

    def checked_in_today(self, habit: Habit) -> bool:
        return (CheckIn
                .select()
                .where(CheckIn.habit == habit, CheckIn.checked_at == date.today())
                .exists())
