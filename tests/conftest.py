from pytest import fixture

from app.db import Base, get_test_engine


@fixture(scope='session', autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=get_test_engine())
    Base.metadata.create_all(bind=get_test_engine())
    yield
    Base.metadata.drop_all(bind=get_test_engine())


