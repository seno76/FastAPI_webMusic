from src.repository.authorRepository import (
    get_author_by_id,
    get_all_authors,
    create_new_author,
    get_by_user_id,
    get_all_authors,
    update_author,
)
from src.bd.database import session_factory, sync_engine


# print(get_author_by_id(session_factory, 1))

# print(create_new_author(session_factory, {
#     "id_user": 9,
#     "bio": "Профессиональный композитор и аранжировщик с 10-летним опытом. Специализация: поп-музыка и саундтреки.",
#     "count_tracks": 23
# },))

# print(get_by_user_id(session_factory, 9))


# print(get_all_authors(session_factory))
# print(update_author(session_factory, 5, {"bio" : "МОе бля био про меня же дохуя можно сказать"}))
