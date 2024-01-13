import os
from pathlib import Path
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseSettings):
    dir_path: str = os.path.dirname(os.path.realpath(__file__))
    absolute_root_dir: str = '/home/petrovych/space/github/NoteMaster-API'

    model_config = SettingsConfigDict(env_file=os.path.join(dir_path, '../.env'))

    db_name: str = Field('DB_NAME', env='DB_NAME')
    test_db_name: str = Field('TEST_DB_NAME', env='TEST_DB_NAME')
    secret_key: str = Field('SECRET_KEY', env='SECRET_KEY')


class JwtToken(BaseSettings):
    private_cert: str = str((Path(__file__).parent.parent / 'certs' / 'jwt-private.pem').read_text())
    public_cert: str = str((Path(__file__).parent.parent / 'certs' / 'jwt-public.pem').read_text())
    algo: str = 'RS256'             # pyjwt docs for public and private keys
    life_time_sec: int = 360
    type: str = 'Bearer'


class BaseEndpoints(BaseSettings):
    root: str = '/'


class UserEndpoints(BaseSettings):
    login: str = '/login'
    user1: str = '/user'


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

    db_url: str = f'sqlite:///{os.path.join(db.absolute_root_dir, db.db_name)}'
    test_db_url: str = f"sqlite:///{os.path.join(db.absolute_root_dir, db.test_db_name)}"

    urls: Urls = Urls()

    jwt: JwtToken = JwtToken()


@lru_cache
def get_settings():
    return Settings()
