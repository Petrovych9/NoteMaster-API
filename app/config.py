import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseSettings):
    dir_path: str = os.path.dirname(os.path.realpath(__file__))
    root_dir: str = '..'

    model_config = SettingsConfigDict(env_file=f'.env', env_file_encoding='utf-8')

    db_name: str = Field('DB_NAME', env='DB_NAME')
    test_db_name: str = Field('TEST_DB_NAME', env='TEST_DB_NAME')
    secret_key: str = Field('SECRET_KEY', env='SECRET_KEY')


class BaseEndpoints(BaseSettings):
    root: str = '/'


class UserEndpoints(BaseSettings):
    login: str = '/login'
    user: str = '/user123'


class NoteEndpoints(BaseSettings):
    pass


class Urls(BaseSettings):
    api_version_prefix: str = '/v1'
    base_endpoints: BaseEndpoints = BaseEndpoints()

    users_prefix: str = '/users'
    users_endpoints: UserEndpoints = UserEndpoints()

    notes_prefix: str = '/notes'
    notes_endpoints: NoteEndpoints = NoteEndpoints()


class Settings(BaseSettings):
    app_name: str = 'NoteMaster-API'
    db: Database = Database()

    db_url: str = f"sqlite:///{db.db_name}"
    test_db_url: str = f"sqlite:///{db.test_db_name}"

    urls: Urls = Urls()


@lru_cache
def get_settings():
    return Settings()
