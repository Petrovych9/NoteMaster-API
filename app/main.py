from fastapi import FastAPI

app = FastAPI(
    title='NoteMaster-API'
)


@app.get('/home')
async def home():
    return 'Home page'


