from src.bd.database import session_factory, sync_engine
from src.models.modelsPD import *
from src.repository.genreRepository import (
    get_all_genres,
    get_genre_by_id,
)

# print(get_all_genres(session_factory))
print(get_genre_by_id(session_factory, 3))



