from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from typing import List
from src.api.userRouting import router as user_router
from src.api.authorRouting import router as author_router
from src.api.albumRouting import router as album_router
from src.api.genreRouting import router as genre_router
from src.api.trackRouting import router as track_router
from src.api.playlistRouting import router as playlist_router
from src.api.userPreferenceService import router as preference_router
from src.api.login import router as login_router
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)


@app.get("/")
def get_authors():
    return {"message":"Hello World!!!"}


@app.post("/file")
async def upload_file(uploadFile: UploadFile):
    file = uploadFile.file
    filename = uploadFile.filename
    with open(filename, "wb") as f:
        f.write(file.read())


def iterfile(filename: str):
    file_size = os.path.getsize(filename)
    print(f"Starting stream of {file_size} bytes")

    with open(filename, "rb") as f:
        bytes_sent = 0
        while chunk := f.read(1024 * 1024):
            bytes_sent += len(chunk)
            print(
                f"Sent {bytes_sent}/{file_size} bytes ({bytes_sent / file_size * 100:.1f}%)"
            )
            yield chunk

    print("Stream completed")


@app.get("/files/streaming/{filename}")
async def stream_file_simple(filename: str):
    file_path = filename

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename,
        content_disposition_type="inline",  # Для воспроизведения в браузере
    )


@app.post("/files")
async def upload_files(uploadFile: List[UploadFile]):
    for upload_file in uploadFile:
        file = upload_file.file
        filename = upload_file.filename
        with open(filename, "wb") as f:
            f.write(file.read())


@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)


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
