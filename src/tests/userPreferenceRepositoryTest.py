from src.bd.database import session_factory, sync_engine
from src.models.modelsPD import *
from src.repository.userPreferenceRepository import (
    create_user_preference,
    delete_user_preference,
    get_preferences_by_user,
    get_track_preferences,
    get_album_preferences,
    update_preference,
    get_most_preferred_tracks,
    get_most_preferred_albums
)

# print(create_user_preference(session_factory, {
#     "id_user": 3,
#     "id_track": 7,  # Smooth Operator
#     "id_album": 4  # Smooth Jazz Collection
# },))

# print(delete_user_preference(session_factory, 2))

# print(get_preferences_by_user(session_factory, 2))

# print(get_track_preferences(session_factory, 3))

# print(get_album_preferences(session_factory, 5))

# print(update_preference(session_factory, 3, {"id_album": 3}))

# print(get_most_preferred_tracks(session_factory))

print(get_most_preferred_albums(session_factory, 3))
