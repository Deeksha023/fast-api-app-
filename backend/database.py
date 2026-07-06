from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Deeksha%402005@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def ensure_users_schema():
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("users")}
    with engine.begin() as connection:
        if "username" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN username VARCHAR(255)"))
        if "hashed_password" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR(255)"))
        if "role" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'Candidate'"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()