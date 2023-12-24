import os
from starlette.config import Config     # todo what is it
from starlette.datastructures import CommaSeparatedStrings, Secret     # todo what is it
from pydantic_settings import BaseSettings, SettingsConfigDict

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

DATABASE_URL = f"sqlite:///{root_dir}" + config('DB_NAME', cast=str)
DATABASE_URL_TEST = f"sqlite:///{root_dir}" + config('TEST_DB_NAME', cast=str)

SECRET_KEY = config('SECRET_KEY', cast=Secret)


class Settings(BaseSettings):
    app_name: str = 'NoteMaster-API'
    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

