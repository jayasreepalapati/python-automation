from datetime import date, datetime
from peewee import (
    Model, SqliteDatabase,
    AutoField, IntegerField, TextField,
    DateField, DateTimeField, BooleanField,
    ForeignKeyField
)

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField()
    name = TextField()
    goal_raw = TextField()
    identity_statement = TextField(default="")
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = "users"


class Habit(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="habits", on_delete="CASCADE")
    title = TextField()
    two_min_version = TextField()
    cue = TextField()
    sort_order = IntegerField(default=0)

    class Meta:
        table_name = "habits"


class CheckIn(BaseModel):
    id = AutoField()
    habit = ForeignKeyField(Habit, backref="checkins", on_delete="CASCADE")
    checked_at = DateField(default=date.today)
    used_fallback = BooleanField(default=False)
    note = TextField(default="")

    class Meta:
        table_name = "checkins"
        indexes = (
            (("habit_id", "checked_at"), True),
        )


class Streak(BaseModel):
    id = AutoField()
    habit = ForeignKeyField(Habit, backref="streak", on_delete="CASCADE")
    current_streak = IntegerField(default=0)
    longest_streak = IntegerField(default=0)
    last_checkin = DateField(null=True)

    class Meta:
        table_name = "streaks"
