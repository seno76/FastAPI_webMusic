from src.models.modelsPD import *
from src.bd.database import session_factory, sync_engine
from datetime import datetime
from src.repository.albumRepository import (
    get_album_by_id,
    create_album,
    delete_album_by_id,
    get_albums_by_genre,

)

# print(get_album_by_id(session_factory, 2))


# print(create_album(session_factory, {
#     "genre_id": 1,
#     "title": "Midnight Memories",
#     "cover_url": "https://example.com/covers/pop2.jpg",
#     "release_date": datetime(2020, 7, 8),
#     "created_at": datetime(2020, 6, 20),
#     "rating": 4.2
# },))

# print(delete_album_by_id(session_factory, 2))

print(get_albums_by_genre(session_factory, 2))






