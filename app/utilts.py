from hashlib import sha256

from app.config import SECRET_KEY


def get_pass_hash(password: str) -> str:
    result_hash = sha256(f'{SECRET_KEY}{password}'.encode('utf-8')).hexdigest()
    return str(result_hash)

