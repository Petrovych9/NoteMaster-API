from pytest import fixture

from app.db import Base, DatabaseSessionManager


@fixture(scope='session', autouse=True)
def setup_db():
    bind = DatabaseSessionManager(test=True).test_engine
    Base.metadata.drop_all(bind=bind)
    Base.metadata.create_all(bind=bind)
    yield
    Base.metadata.drop_all(bind=bind)


