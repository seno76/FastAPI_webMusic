from fastapi import FastAPI
from enum import Enum
from src.repository.authorRepository import get_all_authors
from src.bd.database import session_factory, sync_engine
from src.api.userServise import router as user_router
from src.api.authorService import router as author_router
from src.api.albumService import router as album_router
from src.api.genreService import router as genre_router
from src.api.trackService import router as track_router
from src.api.playlistService import router as playlist_router
from src.api.userPreferenceService import router as preference_router


app = FastAPI()
class mydata(str, Enum):
    one = "1"
    two = "2"
    tree = "3"

@app.get("/a")
def get_authors():
    return {"m":"hello"}

@app.get("/foo/{data:path}")
async def foo(data: mydata):
    return {"data": data}


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