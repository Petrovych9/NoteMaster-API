from fastapi import status, APIRouter

from app.urls import BasicUrls


base_router = APIRouter(
        prefix='',
        tags=['base'],
    )

@base_router.get(BasicUrls.ROOT.value, name='root')
def root():
    return status.HTTP_200_OK, 'http://127.0.0.1:8000/docs'
