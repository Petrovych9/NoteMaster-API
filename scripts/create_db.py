from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import DATABASE_URL
from app.models import Base


def main():
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine.connect())

    Base.metadata.create_all(bind=engine)

    return session


if __name__ == '__main__':
    main()
