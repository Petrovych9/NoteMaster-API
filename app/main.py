from fastapi import FastAPI
from models.notes import Note

app = FastAPI(
    title='NoteMaster-API'
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/notes/")
async def create_note(note: Note):
    return note


@app.get("/notes/")
async def show_all_notes():
    notes = {}
    return notes
