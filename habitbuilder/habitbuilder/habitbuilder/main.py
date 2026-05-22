from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from db.database import init_db, close_db
from screens.onboarding import OnboardingScreen
from screens.today import TodayScreen
from screens.progress import ProgressScreen


class HabitBuilderApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None
        self.habits = []
        self.remind_time = "08:00"

    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.theme_style = "Light"

        init_db("habitbuilder.db")

        sm = ScreenManager()
        sm.app = self

        sm.add_widget(OnboardingScreen())
        sm.add_widget(TodayScreen())
        sm.add_widget(ProgressScreen())

        return sm

    def on_stop(self):
        close_db()


if __name__ == "__main__":
    HabitBuilderApp().run()
