from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql:///test_db", echo=True)
SessionMaker = sessionmaker(engine)


def get_db_session():
    return SessionMaker()
