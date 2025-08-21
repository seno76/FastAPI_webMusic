from hashlib import sha256
from src.bd.database import session_factory
from src.repository.userRepository import (
    get_user_by_id_orm,
    get_count_users,
    get_users_is_active,
    get_user_by_username,
    get_user_by_email,
    set_user_status,
    create_user,
    delete_user_by_id,
    get_plalylist_by_user_id,


)

# print(get_user_by_id_orm(session_factory, 2).userPreference)
# print(get_count_users(session_factory, True))
# print(get_users_is_active(session_factory))
# print(get_user_by_username(session_factory, 'jazz_enthusiast'))
# print(get_user_by_email(session_factory, 'metal.fan@example.com'))
# print(set_user_status(session_factory, 2, False))

new_user = {
    "username": "hhhhhhhhhhhhhhh",
    "email": "hhhhhhhhhh@example.com",
    "password_hash": sha256(b"Music123!").hexdigest(),
    "is_active": False
}

# print(create_user(session_factory, new_user))



# print(delete_user_by_id(session_factory, 10))


print(get_plalylist_by_user_id(session_factory, 2))
