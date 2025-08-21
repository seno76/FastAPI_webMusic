from src.bd.database import session_factory, sync_engine
from src.models.modelsPD import *
from datetime import datetime
from src.repository.playlistRepository import (
    create_playlist,
    delete_playlist,

)


# print(create_playlist(session_factory, {
#     "id_user": 2,  # rock_fanatic
#     "title": "Rock Legends",
#     "count_tracks": 15,
#     "cover_url": "https://example.com/covers/playlists/rock_legends.jpg",
#     "all_time": 3682,  # ~61 минута
#     "created_at": datetime(2023, 4, 15)
# },))


print(delete_playlist(session_factory, 11))
