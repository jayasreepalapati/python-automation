import os
from peewee import SqliteDatabase
from db.models import db, User, Habit, CheckIn, Streak

TABLES = [User, Habit, CheckIn, Streak]


def init_db(db_path: str = "habitbuilder.db") -> None:
    """Initialise the SQLite database and create tables if they don't exist."""
    db.init(db_path, pragmas={
        "journal_mode": "wal",
        "foreign_keys": 1,
        "cache_size": -1024 * 64,
    })
    db.connect(reuse_if_open=True)
    db.create_tables(TABLES, safe=True)


def close_db() -> None:
    """Close the database connection if open."""
    if not db.is_closed():
        db.close()


def get_db() -> SqliteDatabase:
    """Return the active database instance."""
    return db
