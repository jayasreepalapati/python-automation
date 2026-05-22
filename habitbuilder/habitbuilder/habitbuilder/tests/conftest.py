import pytest
from peewee import SqliteDatabase
from db.models import db, User, Habit, CheckIn, Streak

TABLES = [User, Habit, CheckIn, Streak]


@pytest.fixture(autouse=True)
def test_db():
    """
    Use a fast in-memory SQLite database for every test.
    Tables are created fresh and dropped after each test.
    """
    test_database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
    db.initialize(test_database)

    with test_database:
        test_database.create_tables(TABLES)
        yield test_database
        test_database.drop_tables(TABLES)


@pytest.fixture
def user():
    return User.create(
        name="Test User",
        goal_raw="I want to exercise every day",
        identity_statement="I am someone who exercises daily"
    )


@pytest.fixture
def habit(user):
    h = Habit.create(
        user=user,
        title="Go for a 30-minute run",
        two_min_version="Put on running shoes",
        cue="After I wake up, I will go for a run",
        sort_order=0
    )
    Streak.create(habit=h, current_streak=0, longest_streak=0, last_checkin=None)
    return h
