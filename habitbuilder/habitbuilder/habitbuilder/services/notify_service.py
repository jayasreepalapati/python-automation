import threading
import schedule
import time
from plyer import notification


class NotifyService:

    def __init__(self):
        self._thread: threading.Thread | None = None
        self._running = False

    def schedule_daily_reminder(self, remind_time: str, habits: list) -> None:
        """
        Schedule a daily local notification at a given time (HH:MM format).
        Runs in a background thread. Does not require any external service.
        """
        schedule.clear("habit-reminder")

        schedule.every().day.at(remind_time).do(
            self._send_reminder, habits=habits
        ).tag("habit-reminder")

        self._start_scheduler()

    def _send_reminder(self, habits: list) -> None:
        incomplete = [h.title for h in habits if not self._is_checked_today(h)]
        if not incomplete:
            return

        count = len(incomplete)
        message = f"{count} habit{'s' if count > 1 else ''} left for today"

        notification.notify(
            title="Habit Builder",
            message=message,
            app_name="Habit Builder",
            timeout=10
        )

    def _is_checked_today(self, habit) -> bool:
        from datetime import date
        from db.models import CheckIn
        return (CheckIn
                .select()
                .where(CheckIn.habit == habit,
                       CheckIn.checked_at == date.today())
                .exists())

    def _start_scheduler(self) -> None:
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def _run_loop(self) -> None:
        while self._running:
            schedule.run_pending()
            time.sleep(30)

    def stop(self) -> None:
        self._running = False
        schedule.clear("habit-reminder")

    def send_never_miss_twice(self, habit_title: str) -> None:
        """
        Fire an immediate nudge when the never-miss-twice rule is triggered.
        Called from the Today view on app open.
        """
        notification.notify(
            title="Don't break the chain",
            message=f"You missed yesterday — do just 2 minutes of '{habit_title}' today.",
            app_name="Habit Builder",
            timeout=12
        )
