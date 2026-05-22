from datetime import date, timedelta
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

from services.habit_service import HabitService


class HeatmapCell(Widget):
    """A single day cell in the check-in heatmap."""

    def __init__(self, filled: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (14, 14)
        self.filled = filled
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.filled:
                Color(0.18, 0.62, 0.44, 1)
            else:
                Color(0.88, 0.88, 0.88, 0.4)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[3])


class ProgressScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "progress"
        self.habit_service = HabitService()

    def on_enter(self):
        self.clear_widgets()
        self._build_ui()

    def _build_ui(self):
        app = self.manager.app if hasattr(self.manager, "app") else None
        habits = app.habits if app else []
        user = app.current_user if app else None

        root = MDBoxLayout(orientation="vertical", padding=[16, 24, 16, 16], spacing=16)

        root.add_widget(MDLabel(
            text="Progress",
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
        content = MDBoxLayout(
            orientation="vertical",
            spacing=16,
            size_hint_y=None,
            padding=[0, 8, 0, 8]
        )
        content.bind(minimum_height=content.setter("height"))

        for habit in habits:
            content.add_widget(self._build_habit_progress(habit))

        scroll.add_widget(content)
        root.add_widget(scroll)

        back_btn = MDFlatButton(
            text="Back to today",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: setattr(self.manager, "current", "today")
        )
        root.add_widget(back_btn)
        self.add_widget(root)

    def _build_habit_progress(self, habit) -> MDCard:
        streak = self.habit_service.get_streak(habit)
        checkin_dates = self.habit_service.get_checkins_for_habit(habit, days=66)
        checkin_set = set(checkin_dates)

        card = MDCard(
            orientation="vertical",
            padding=[16, 16, 16, 16],
            spacing=12,
            size_hint_y=None,
            height=200
        )

        card.add_widget(MDLabel(
            text=habit.title,
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=32
        ))

        stat_row = MDBoxLayout(
            orientation="horizontal",
            spacing=16,
            size_hint_y=None,
            height=48
        )
        stat_row.add_widget(self._stat(str(streak.current_streak), "current streak"))
        stat_row.add_widget(self._stat(str(streak.longest_streak), "best streak"))
        stat_row.add_widget(self._stat(str(len(checkin_dates)), "total days"))
        card.add_widget(stat_row)

        card.add_widget(MDLabel(
            text="Last 66 days",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height=20
        ))

        heatmap = self._build_heatmap(checkin_set)
        card.add_widget(heatmap)

        return card

    def _stat(self, value: str, label: str) -> MDBoxLayout:
        box = MDBoxLayout(orientation="vertical", spacing=2)
        box.add_widget(MDLabel(
            text=value,
            font_style="H6",
            halign="center",
            size_hint_y=None,
            height=32
        ))
        box.add_widget(MDLabel(
            text=label,
            font_style="Caption",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=None,
            height=20
        ))
        return box

    def _build_heatmap(self, checkin_set: set) -> GridLayout:
        grid = GridLayout(
            cols=11,
            spacing=3,
            size_hint_y=None,
            height=48
        )
        today = date.today()
        for i in range(66):
            d = today - timedelta(days=65 - i)
            grid.add_widget(HeatmapCell(filled=(d in checkin_set)))
        return grid
