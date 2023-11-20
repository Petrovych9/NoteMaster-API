from fastapi import APIRouter, Body, Depends

from .database import connect_db

auth_router = APIRouter()  # todo what is it


@auth_router.post('/login', name='user: login')
def login():
    return {"status": 'OK'}
