from fastapi import status, APIRouter

from app.config import get_settings


base_router = APIRouter(
        prefix='',
        tags=['base'],
    )


@base_router.get(get_settings().urls.base_endpoints.root, name='root')
def root():
    return status.HTTP_200_OK, 'http://127.0.0.1:8000/docs'
