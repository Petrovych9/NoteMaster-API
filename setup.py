from setuptools import setup

setup(
    name='note-master-api',
    version='0.0.1',
    author='Petrovych9',
    author_email='bohdan.work@urk.net',
    description='NoteMaster-API',
    install_requires=[
        'fastapi==0.103.1',
        'uvicorn==0.23.2',
        'starlette==0.27.0',
        'pydantic==2.3.0'
    ],
    scripts=['app/main.py']
)
