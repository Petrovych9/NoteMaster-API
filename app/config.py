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

    user_postgres: str = Field('USER_POSTGRES', env='USER_POSTGRES')
    pass_postgres: str = Field('PASS_POSTGRES', env='PASS_POSTGRES')
    host_postgres: str = Field('HOST_POSTGRES', env='HOST_POSTGRES')


class JwtToken(BaseSettings):
    private_cert: str = str((Path(__file__).parent.parent / 'certs' / 'jwt-private.pem').read_text())
    public_cert: str = str((Path(__file__).parent.parent / 'certs' / 'jwt-public.pem').read_text())
    algo: str = 'RS256'             # pyjwt docs for public and private keys
    life_time_sec: int = 360
    long_life_time_sec: int = 3600
    type: str = 'Bearer'


class UrlsBase(BaseSettings):
    api_version_prefix: str = '/v1'

    users_prefix: str = '/users'
    notes_prefix: str = '/notes'
    note_category_prefix: str = '/category'


class UserEndpoints(UrlsBase):
    login: str = '/login'
    refresh_token: str = '/refresh_token'
    user1: str = '/user'

    def get_url(self, endpoint: str):
        return f"{self.api_version_prefix + self.users_prefix + endpoint}"


class BaseEndpoints(UrlsBase):
    root: str = '/'

    def get_url(self, endpoint: str):
        return f"{self.api_version_prefix + endpoint}"


class NoteEndpoints(UrlsBase):
    create: str = '/create'
    update: str = '/update'
    delete: str = '/delete'
    get: str = '/get'

    def get_url(self, endpoint: str):
        return f"{self.api_version_prefix + self.notes_prefix + endpoint}"


class NoteCategoryEndpoints(UrlsBase):
    create: str = '/create'
    update: str = '/update'
    delete: str = '/delete'

    def get_url(self, endpoint: str):
        return f"{self.api_version_prefix + self.notes_prefix +self.note_category_prefix + endpoint}"


class Urls(UrlsBase):
    base_endpoints: BaseEndpoints = BaseEndpoints()
    users_endpoints: UserEndpoints = UserEndpoints()
    notes_endpoints: NoteEndpoints = NoteEndpoints()
    notes_category: NoteCategoryEndpoints = NoteCategoryEndpoints()


class Settings(BaseSettings):
    app_name: str = 'NoteMaster-API'
    db: Database = Database()

    # db_url: str = f'sqlite:///{os.path.join(db.absolute_root_dir, db.db_name)}'
    db_url: str = f'postgresql://{db.user_postgres}:{db.pass_postgres}@{db.host_postgres}/{db.db_name}'
    test_db_url: str = f"sqlite:///{os.path.join(db.absolute_root_dir, db.test_db_name)}"

    urls: Urls = Urls()

    jwt: JwtToken = JwtToken()


@lru_cache
def get_settings():
    return Settings()
