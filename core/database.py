from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core import envConfig

engine = create_engine(envConfig.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
