from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.spinner import MDSpinner
from kivy.clock import Clock
import threading

from db.models import User
from services.ai_service import AIService
from services.habit_service import HabitService


class OnboardingScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "onboarding"
        self.ai_service = AIService()
        self.habit_service = HabitService()
        self._build_ui()

    def _build_ui(self):
        layout = MDBoxLayout(
            orientation="vertical",
            padding=[32, 64, 32, 32],
            spacing=24
        )

        layout.add_widget(MDLabel(
            text="What habit do you want to build?",
            halign="center",
            font_style="H5",
            size_hint_y=None,
            height=60
        ))

        layout.add_widget(MDLabel(
            text="Describe your goal in plain English. We'll break it down for you.",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=40
        ))

        self.name_field = MDTextField(
            hint_text="Your name",
            size_hint_x=1,
            mode="rectangle"
        )
        layout.add_widget(self.name_field)

        self.goal_field = MDTextField(
            hint_text="e.g. I want to get fit and exercise regularly",
            multiline=True,
            size_hint_x=1,
            size_hint_y=None,
            height=120,
            mode="rectangle"
        )
        layout.add_widget(self.goal_field)

        self.remind_field = MDTextField(
            hint_text="Daily reminder time (HH:MM, e.g. 08:00)",
            size_hint_x=1,
            mode="rectangle"
        )
        layout.add_widget(self.remind_field)

        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=30
        )
        layout.add_widget(self.error_label)

        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(48, 48),
            pos_hint={"center_x": 0.5},
            active=False
        )
        layout.add_widget(self.spinner)

        self.submit_btn = MDRaisedButton(
            text="Build my habit plan",
            pos_hint={"center_x": 0.5},
            on_release=self.on_submit
        )
        layout.add_widget(self.submit_btn)

        self.add_widget(layout)

    def on_submit(self, *args):
        name = self.name_field.text.strip()
        goal = self.goal_field.text.strip()
        remind_time = self.remind_field.text.strip() or "08:00"

        if not name or not goal:
            self.error_label.text = "Please enter your name and goal."
            return

        self.error_label.text = ""
        self.submit_btn.disabled = True
        self.spinner.active = True

        threading.Thread(
            target=self._run_ai,
            args=(name, goal, remind_time),
            daemon=True
        ).start()

    def _run_ai(self, name: str, goal: str, remind_time: str):
        try:
            user = User.create(name=name, goal_raw=goal)
            plan = self.ai_service.breakdown_goal(goal)
            habits = self.habit_service.seed_from_plan(user, plan)
            Clock.schedule_once(
                lambda dt: self._on_success(user, habits, remind_time), 0
            )
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self._on_error(str(e)), 0
            )

    def _on_success(self, user, habits, remind_time):
        self.spinner.active = False
        self.submit_btn.disabled = False
        app = self.manager.app if hasattr(self.manager, "app") else None
        if app:
            app.current_user = user
            app.habits = habits
            app.remind_time = remind_time
        self.manager.current = "today"

    def _on_error(self, message: str):
        self.spinner.active = False
        self.submit_btn.disabled = False
        self.error_label.text = f"Something went wrong: {message}"
