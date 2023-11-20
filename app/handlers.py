import uuid

from fastapi import APIRouter, Body, Depends        # todo what is it

from app.forms import UserLoginForm
from app.models import connect_db, User, AuthToken

from utilts import get_pass_hash

auth_router = APIRouter()  # todo what is it


@auth_router.post('/login', name='user: login')
def login(
        user_form: UserLoginForm = Body(..., embed=True),
        db=Depends(connect_db)
):
    user = db.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_pass_hash(user_form.password) != user.password:
        return 500

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    db.add(auth_token)
    db.commit()
    return {"status": 'OK'}
