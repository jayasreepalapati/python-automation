from datetime import date
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.uix.scrollview import ScrollView

from db.models import Habit, Streak
from services.habit_service import HabitService
from services.notify_service import NotifyService


class TodayScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "today"
        self.habit_service = HabitService()
        self.notify_service = NotifyService()
        self.dialog = None

    def on_enter(self):
        """Rebuild UI each time the screen is shown to reflect current state."""
        self.clear_widgets()
        self._build_ui()
        self._check_never_miss_twice()

    def _build_ui(self):
        app = self.manager.app if hasattr(self.manager, "app") else None
        habits = app.habits if app else []
        user = app.current_user if app else None

        root = MDBoxLayout(orientation="vertical", padding=[16, 24, 16, 16], spacing=16)

        root.add_widget(MDLabel(
            text=f"Today — {date.today().strftime('%A, %d %b')}",
            font_style="H6",
            size_hint_y=None,
            height=40
        ))

        if user:
            root.add_widget(MDLabel(
                text=user.identity_statement,
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_y=None,
                height=30
            ))

        scroll = ScrollView()
        habit_list = MDBoxLayout(
            orientation="vertical",
            spacing=12,
            size_hint_y=None,
            padding=[0, 8, 0, 8]
        )
        habit_list.bind(minimum_height=habit_list.setter("height"))

        for habit in habits:
            habit_list.add_widget(self._build_habit_card(habit))

        scroll.add_widget(habit_list)
        root.add_widget(scroll)

        progress_btn = MDFlatButton(
            text="View progress",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "progress")
        )
        root.add_widget(progress_btn)

        self.add_widget(root)

    def _build_habit_card(self, habit: Habit) -> MDCard:
        streak = self.habit_service.get_streak(habit)
        done = self.habit_service.checked_in_today(habit)

        card = MDCard(
            orientation="vertical",
            padding=[16, 12, 16, 12],
            spacing=8,
            size_hint_y=None,
            height=160,
            md_bg_color=(0.95, 0.97, 0.95, 1) if done else (1, 1, 1, 1)
        )

        top = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        top.add_widget(MDLabel(
            text=habit.title,
            font_style="Subtitle1",
            bold=True
        ))
        streak_label = MDLabel(
            text=f"{streak.current_streak} day streak",
            halign="right",
            theme_text_color="Secondary",
            font_style="Caption"
        )
        top.add_widget(streak_label)
        card.add_widget(top)

        card.add_widget(MDLabel(
            text=habit.cue,
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=24
        ))

        btn_row = MDBoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint_y=None,
            height=48
        )

        if done:
            btn_row.add_widget(MDLabel(
                text="Done for today",
                theme_text_color="Custom",
                text_color=(0.2, 0.7, 0.4, 1),
                font_style="Button"
            ))
        else:
            checkin_btn = MDRaisedButton(
                text="Check in",
                on_release=lambda x, h=habit: self._do_checkin(h, used_fallback=False)
            )
            fallback_btn = MDFlatButton(
                text="Just 2 mins",
                on_release=lambda x, h=habit: self._do_checkin(h, used_fallback=True)
            )
            btn_row.add_widget(checkin_btn)
            btn_row.add_widget(fallback_btn)

        card.add_widget(btn_row)
        return card

    def _do_checkin(self, habit: Habit, used_fallback: bool):
        self.habit_service.checkin(habit, used_fallback=used_fallback)
        self.on_enter()

    def _check_never_miss_twice(self):
        app = self.manager.app if hasattr(self.manager, "app") else None
        if not app:
            return
        for habit in app.habits:
            if self.habit_service.is_never_miss_twice(habit):
                self.notify_service.send_never_miss_twice(habit.title)
