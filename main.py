from fastapi import FastAPI, HTTPException, Depends, Response, Body
from enum import Enum
from typing import Annotated
from src.api.userServise import router as user_router
from src.api.authorService import router as author_router
from src.api.albumService import router as album_router
from src.api.genreService import router as genre_router
from src.api.trackService import router as track_router
from src.api.playlistService import router as playlist_router
from src.api.userPreferenceService import router as preference_router
from src.api.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)



@app.get("/")
def get_authors():
    return {"message":"Hello World!!!"}

# @app.get("/{item}")
# async def get_item(item: float):
#     return {"ok": item}

app.include_router(user_router)
app.include_router(author_router)
app.include_router(album_router)
app.include_router(genre_router)
app.include_router(track_router)
app.include_router(playlist_router)
app.include_router(preference_router)
app.include_router(login_router)