import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Postgres за замовчуванням; можна перевизначити, напр.:
#   DATABASE_URL=sqlite:///hw7.db
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:hw7secret@localhost:5432/hw7",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
