from hashlib import sha256

from app.config import get_settings


def get_pass_hash(password: str) -> str:
    result_hash = sha256(f'{get_settings().db.secret_key}{password}'.encode('utf-8')).hexdigest()
    return str(result_hash)

