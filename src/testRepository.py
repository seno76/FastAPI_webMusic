from datetime import datetime
from src.repository.userRepository import (
    get_user_by_id_core,
    get_user_by_id_orm,
)

from src.repository.trackRepository import (
    create_track_2

)


from src.bd.database import sync_engine, session_factory

res = get_user_by_id_core(sync_engine, 3)
print(res)
print(type(res))
for i in res:
    for j in i:
        print(j, type(j))

res = get_user_by_id_orm(session_factory, 3)

print(res)


# res = get_users_is_active(session_factory)
#
#
# res = get_user_by_username(session_factory, "metal_head")
#
# res = get_user_by_email(session_factory, "jazz.lover@example.com")



# user = select(User).where(User.id == 1)
# print("------------->", user)
#
# res = set_user_status(session_factory, 133, False)
#
# print("----------->", res)

# print(get_count_users(session_factory, False))
#
# print(create_user(session_factory, {
#             "username": "hhhhhhhhhhhhhhh",
#             "email": "hhhhhhhhhh@example.com",
#             "password_hash": hashlib.sha256(b"Music123!").hexdigest(),
#             "is_active": False
#         },))

# delete_user_by_id(session_factory, 16)


# print(get_plalylist_by_user_id(session_factory, 1))

# print(create_new_author(session_factory, {
#                 "id_user": 9,  # Связь с пользователем music_lover
#                 "bio": "Профессиональный композитор и аранжировщик с 10-летним опытом. Специализация: поп-музыка и саундтреки.",
#                 "count_tracks": 23
#             },))

# delete_aythor_by_id(session_factory, 6)

# print(get_all_authors(session_factory))
#
#
# print(get_track_by_id(session_factory, 3))


# print("Создан --------->", create_track(session_factory, {"author_id": 2,
#                 "album_id": 3,
#                 "genre_id": 2,
#                 "title": "Neon Lights",
#                 "duration": 184,
#                 "file_path": "/music/rock/neon_lights.mp3",
#                 "is_explicit": True,
#                 "release_date": datetime(2018, 11, 21),
#                 "created_at": datetime(2018, 10, 1),
#                 "rating": 4.6}))
#
#
print("Создан --------->", create_track_2(session_factory, {"author_id": 2,
                "album_id": 3,
                "genre_id": 2,
                "title": "Neon Lights",
                "duration": 184,
                "file_path": "/music/rock/neon_lights.mp3",
                "is_explicit": True,
                "release_date": datetime(2018, 11, 21),
                "created_at": datetime(2018, 10, 1),
                "rating": 4.6}))

# delete_track_by_id(session_factory, 38)
# delete_track_by_id(session_factory, 39)

# print(len(get_list_tracks(session_factory, limit=5, author_id=1)))
#
# print(update_data(session_factory, 3, {"title": "jkhdvkhkjdshvjkhvdsjk"}))


# print(get_tracks_by_author(session_factory, 2)[0])
#
# print(get_by_album(session_factory, 2)[0].user_preferences)

# print(get_by_genre(session_factory, 2))


# for data in get_released_after(session_factory, datetime(2022, 2, 23)):
#     print(data.author)