import hashlib
from datetime import datetime
from src.bd.database import session_factory, Base, sync_engine
from src.models.modelsORM import *
from src.models.modelsPD import TypeItem
import random

def create_db():
    Base.metadata.create_all(bind=sync_engine)


def del_db():
    Base.metadata.drop_all(bind=sync_engine)


def insert_data_for_users():
    with session_factory() as session:
        users = [
        {
            "username": "music_lover",
            "email": "music.lover@example.com",
            "password_hash": hashlib.sha256(b"Music123!").hexdigest(),
            "is_active": False
        },
        {
            "username": "rock_fanatic",
            "email": "rock.fan@example.com",
            "password_hash": hashlib.sha256(b"RockOn456").hexdigest(),
            "is_active": True
        },
        {
            "username": "jazz_enthusiast",
            "email": "jazz.lover@example.com",
            "password_hash": hashlib.sha256(b"Jazz789$").hexdigest(),
            "is_active": False
        },
        {
            "username": "pop_queen",
            "email": "pop.queen@example.com",
            "password_hash": hashlib.sha256(b"PopStar!1").hexdigest(),
            "is_active": True
        },
        {
            "username": "classical_master",
            "email": "classical.fan@example.com",
            "password_hash": hashlib.sha256(b"Beethoven2").hexdigest(),
            "is_active": True
        },
        {
            "username": "hiphop_head",
            "email": "hiphop.fan@example.com",
            "password_hash": hashlib.sha256(b"HipHop#3").hexdigest(),
            "is_active": False
        },
        {
            "username": "electronic_dreamer",
            "email": "edm.lover@example.com",
            "password_hash": hashlib.sha256(b"EDM456%").hexdigest(),
            "is_active": False
        },
        {
            "username": "indie_spirit",
            "email": "indie.music@example.com",
            "password_hash": hashlib.sha256(b"Indie789^").hexdigest(),
            "is_active": True
        },
        {
            "username": "blues_traveler",
            "email": "blues.fan@example.com",
            "password_hash": hashlib.sha256(b"Blues123&").hexdigest(),
            "is_active": True
        },
        {
            "username": "metal_head",
            "email": "metal.fan@example.com",
            "password_hash": hashlib.sha256(b"Metal456*").hexdigest(),
            "is_active": True
        },
        {
            "username": "folk_singer",
            "email": "folk.music@example.com",
            "password_hash": hashlib.sha256(b"Folk789(").hexdigest(),
            "is_active": False
        },
        {
            "username": "reggae_soul",
            "email": "reggae.lover@example.com",
            "password_hash": hashlib.sha256(b"Reggae1)").hexdigest(),
            "is_active": True
        },
        {
            "username": "country_road",
            "email": "country.music@example.com",
            "password_hash": hashlib.sha256(b"Country2_").hexdigest(),
            "is_active": True
        },
        {
            "username": "disco_king",
            "email": "disco.fan@example.com",
            "password_hash": hashlib.sha256(b"Disco345=").hexdigest(),
            "is_active": False
        },
        {
            "username": "punk_rocker",
            "email": "punk.music@example.com",
            "password_hash": hashlib.sha256(b"Punk789+").hexdigest(),
            "is_active": True
        }
    ]
        for user in users:
            session.add(User(**user))
        session.commit()


def insert_data_for_author():
    with session_factory() as session:
        authors = [
            {
                "id_user": 1,  # Связь с пользователем music_lover
                "bio": "Профессиональный композитор и аранжировщик с 10-летним опытом. Специализация: поп-музыка и саундтреки.",
                "count_tracks": 23
            },
            {
                "id_user": 2,  # Связь с пользователем rock_fanatic
                "bio": "Лидер рок-группы 'Громовые Коты'. Автор более 50 песен в жанрах хард-рок и альтернативный рок.",
                "count_tracks": 52
            },
            {
                "id_user": 3,  # Связь с пользователем jazz_enthusiast
                "bio": "Джазовый саксофонист, выступавший на международных фестивалях. Преподаватель джазовой импровизации.",
                "count_tracks": 17
            },
            {
                "id_user": 4,  # Связь с пользователем pop_queen
                "bio": "Поп-исполнительница, известная под псевдонимом 'StarGirl'. Две песни в топ-100 Billboard.",
                "count_tracks": 34
            },
            {
                "id_user": 5,  # Связь с пользователем classical_master
                "bio": "Концертирующий пианист, лауреат международных конкурсов. Специализируется на классических обработках.",
                "count_tracks": 28
            }
        ]
        for author in authors:
            session.add(Author(**author))
        session.commit()


def insert_data_for_tracks():
    with session_factory() as session:
        tracks = [
            {
                "author_id": 1,
                "album_id": 1,
                "genre_id": 1,
                "title": "Electric Love",
                "duration": 213,
                "file_path": "/music/pop/electic_love.mp3",
                "is_explicit": False,
                "release_date": datetime(2022, 3, 15),
                "created_at": datetime(2022, 3, 10),
                "rating": 4.5
            },
            {
                "author_id": 1,
                "album_id": 1,
                "genre_id": 1,
                "title": "Midnight Dance",
                "duration": 198,
                "file_path": "/music/pop/midnight_dance.mp3",
                "is_explicit": False,
                "release_date": datetime(2022, 3, 15),
                "created_at": datetime(2022, 3, 10),
                "rating": 4.3
            },

            # Рок-треки
            {
                "author_id": 2,
                "album_id": 3,
                "genre_id": 2,
                "title": "Thunder Road",
                "duration": 256,
                "file_path": "/music/rock/thunder_road.mp3",
                "is_explicit": False,
                "release_date": datetime(2018, 11, 21),
                "created_at": datetime(2018, 10, 1),
                "rating": 4.8
            },
            {
                "author_id": 2,
                "album_id": 3,
                "genre_id": 2,
                "title": "Neon Lights",
                "duration": 184,
                "file_path": "/music/rock/neon_lights.mp3",
                "is_explicit": True,
                "release_date": datetime(2018, 11, 21),
                "created_at": datetime(2018, 10, 1),
                "rating": 4.6
            },

            # Хип-хоп
            {
                "author_id": 5,
                "album_id": 5,
                "genre_id": 3,
                "title": "Urban King",
                "duration": 221,
                "file_path": "/music/hiphop/urban_king.mp3",
                "is_explicit": True,
                "release_date": datetime(2021, 9, 30),
                "created_at": datetime(2021, 8, 10),
                "rating": 4.7
            },

            # Электроника
            {
                "author_id": 5,
                "album_id": 6,
                "genre_id": 4,
                "title": "Digital Dreams",
                "duration": 312,
                "file_path": "/music/electronic/digital_dreams.mp3",
                "is_explicit": False,
                "release_date": datetime(2019, 2, 14),
                "created_at": datetime(2019, 1, 5),
                "rating": 4.3
            },

            # Джаз
            {
                "author_id": 3,
                "album_id": 7,
                "genre_id": 6,
                "title": "Smooth Operator",
                "duration": 278,
                "file_path": "/music/jazz/smooth_operator.mp3",
                "is_explicit": False,
                "release_date": datetime(2017, 8, 17),
                "created_at": datetime(2017, 7, 20),
                "rating": 4.9
            },

            # Классика
            {
                "author_id": 5,
                "album_id": 8,
                "genre_id": 7,
                "title": "Moonlight Sonata (Remastered)",
                "duration": 425,
                "file_path": "/music/classical/moonlight_sonata.mp3",
                "is_explicit": False,
                "release_date": datetime(2016, 4, 5),
                "created_at": datetime(2016, 3, 1),
                "rating": 5.0
            },

            # Метал
            {
                "author_id": 5,
                "album_id": 9,
                "genre_id": 9,
                "title": "Steel Hammer",
                "duration": 198,
                "file_path": "/music/metal/steel_hammer.mp3",
                "is_explicit": True,
                "release_date": datetime(2023, 1, 10),
                "created_at": datetime(2022, 12, 1),
                "rating": 4.6
            },

            # Инди
            {
                "author_id": 2,
                "album_id": 10,
                "genre_id": 15,
                "title": "Whispering Wind",
                "duration": 234,
                "file_path": "/music/indie/whispering_wind.mp3",
                "is_explicit": False,
                "release_date": datetime(2021, 6, 18),
                "created_at": datetime(2021, 5, 20),
                "rating": 4.4
            },

            # Треки без альбома
            {
                "author_id": 4,
                "album_id": None,
                "genre_id": 1,
                "title": "Lonely Star",
                "duration": 201,
                "file_path": "/music/pop/lonely_star.mp3",
                "is_explicit": False,
                "release_date": datetime(2023, 5, 12),
                "created_at": datetime(2023, 4, 15),
                "rating": 4.2
            },
            {
                "author_id": 3,
                "album_id": None,
                "genre_id": 11,
                "title": "Blues Traveler",
                "duration": 267,
                "file_path": "/music/blues/blues_traveler.mp3",
                "is_explicit": False,
                "release_date": datetime(2022, 10, 8),
                "created_at": datetime(2022, 9, 1),
                "rating": 4.5
            },

            # Разные варианты explicit
            {
                "author_id": 4,
                "album_id": 5,
                "genre_id": 3,
                "title": "Street Life (Clean Version)",
                "duration": 189,
                "file_path": "/music/hiphop/street_life_clean.mp3",
                "is_explicit": False,
                "release_date": datetime(2021, 9, 30),
                "created_at": datetime(2021, 8, 10),
                "rating": 4.0
            },
            {
                "author_id": 1,
                "album_id": 5,
                "genre_id": 3,
                "title": "Street Life (Explicit)",
                "duration": 192,
                "file_path": "/music/hiphop/street_life_explicit.mp3",
                "is_explicit": True,
                "release_date": datetime(2021, 9, 30),
                "created_at": datetime(2021, 8, 10),
                "rating": 4.2
            },

            # Разные длительности
            {
                "author_id": 2,
                "album_id": 6,
                "genre_id": 4,
                "title": "Digital Sunrise (Extended Mix)",
                "duration": 482,
                "file_path": "/music/electronic/digital_sunrise_extended.mp3",
                "is_explicit": False,
                "release_date": datetime(2019, 2, 14),
                "created_at": datetime(2019, 1, 5),
                "rating": 4.7
            },
            {
                "author_id": 3,
                "album_id": 7,
                "genre_id": 6,
                "title": "Jazz Improvisation #7",
                "duration": 634,
                "file_path": "/music/jazz/improvisation_7.mp3",
                "is_explicit": False,
                "release_date": datetime(2017, 8, 17),
                "created_at": datetime(2017, 7, 20),
                "rating": 4.8
            },

            # Разные рейтинги
            {
                "author_id": 2,
                "album_id": 4,
                "genre_id": 2,
                "title": "Guitar Solo",
                "duration": 156,
                "file_path": "/music/rock/guitar_solo.mp3",
                "is_explicit": False,
                "release_date": datetime(2015, 5, 3),
                "created_at": datetime(2015, 4, 15),
                "rating": 3.9
            },
            {
                "author_id": 5,
                "album_id": 8,
                "genre_id": 7,
                "title": "Classical Moment",
                "duration": 187,
                "file_path": "/music/classical/classical_moment.mp3",
                "is_explicit": False,
                "release_date": datetime(2016, 4, 5),
                "created_at": datetime(2016, 3, 1),
                "rating": 4.1
            },

            # Сборник
            {
                "author_id": 1,
                "album_id": 11,
                "genre_id": 1,
                "title": "Best of Pop 2023",
                "duration": 218,
                "file_path": "/music/compilations/best_pop_2023.mp3",
                "is_explicit": False,
                "release_date": datetime(2023, 12, 1),
                "created_at": datetime(2023, 11, 15),
                "rating": 4.6
            },
            {
                "author_id": 2,
                "album_id": 11,
                "genre_id": 2,
                "title": "Rock Anthem",
                "duration": 245,
                "file_path": "/music/compilations/rock_anthem.mp3",
                "is_explicit": True,
                "release_date": datetime(2023, 12, 1),
                "created_at": datetime(2023, 11, 15),
                "rating": 4.7
            }
        ]
        for track in tracks:
            session.add(Track(**track))
        session.commit()


def insert_data_for_album():
    with session_factory() as session:
        albums = [
            # Поп-альбомы
            {
                "genre_id": 1,  # Pop
                "title": "Electric Dreams",
                "cover_url": "https://example.com/covers/pop1.jpg",
                "release_date": datetime(2022, 3, 15),
                "created_at": datetime(2022, 3, 10),
                "rating": 4.5
            },
            {
                "genre_id": 1,
                "title": "Midnight Memories",
                "cover_url": "https://example.com/covers/pop2.jpg",
                "release_date": datetime(2020, 7, 8),
                "created_at": datetime(2020, 6, 20),
                "rating": 4.2
            },

            # Рок-альбомы
            {
                "genre_id": 2,  # Rock
                "title": "Thunderstruck",
                "cover_url": "https://example.com/covers/rock1.jpg",
                "release_date": datetime(2018, 11, 21),
                "created_at": datetime(2018, 10, 1),
                "rating": 4.8
            },
            {
                "genre_id": 2,
                "title": "Neon Nights",
                "cover_url": "https://example.com/covers/rock2.jpg",
                "release_date": datetime(2015, 5, 3),
                "created_at": datetime(2015, 4, 15),
                "rating": 4.0
            },

            # Хип-хоп
            {
                "genre_id": 3,  # Hip-Hop
                "title": "Urban Legends",
                "cover_url": "https://example.com/covers/hiphop1.jpg",
                "release_date": datetime(2021, 9, 30),
                "created_at": datetime(2021, 8, 10),
                "rating": 4.7
            },

            # Электроника
            {
                "genre_id": 4,  # Electronic
                "title": "Digital Sunrise",
                "cover_url": "https://example.com/covers/electronic1.jpg",
                "release_date": datetime(2019, 2, 14),
                "created_at": datetime(2019, 1, 5),
                "rating": 4.3
            },

            # Джаз
            {
                "genre_id": 6,  # Jazz
                "title": "Smooth Jazz Collection",
                "cover_url": "https://example.com/covers/jazz1.jpg",
                "release_date": datetime(2017, 8, 17),
                "created_at": datetime(2017, 7, 20),
                "rating": 4.9
            },

            # Классика
            {
                "genre_id": 7,  # Classical
                "title": "Moonlight Sonata",
                "cover_url": "https://example.com/covers/classical1.jpg",
                "release_date": datetime(2016, 4, 5),
                "created_at": datetime(2016, 3, 1),
                "rating": 5.0
            },

            # Метал
            {
                "genre_id": 9,  # Metal
                "title": "Steel Warriors",
                "cover_url": "https://example.com/covers/metal1.jpg",
                "release_date": datetime(2023, 1, 10),
                "created_at": datetime(2022, 12, 1),
                "rating": 4.6
            },

            # Инди
            {
                "genre_id": 15,  # Indie
                "title": "Whispers in the Dark",
                "cover_url": "https://example.com/covers/indie1.jpg",
                "release_date": datetime(2021, 6, 18),
                "created_at": datetime(2021, 5, 20),
                "rating": 4.4
            },

            # Сборник
            {
                "genre_id": None,  # Без жанра
                "title": "Best Hits 2020-2023",
                "cover_url": "https://example.com/covers/compilation1.jpg",
                "release_date": datetime(2023, 12, 1),
                "created_at": datetime(2023, 11, 15),
                "rating": 4.7
            }
        ]
        for album in albums:
            session.add(Album(**album))
        session.commit()


def insert_data_for_genre():
    with session_factory() as session:
        genres = [
            {"name": "Pop", "description": "Коммерчески успешная музыка с акцентом на мелодии и запоминающиеся тексты"},
            {"name": "Rock", "description": "Гитаро-ориентированная музыка с сильным ритмом"},
            {"name": "Hip-Hop/Rap", "description": "Ритмичная музыка с речитативом и битами"},
            {"name": "Electronic", "description": "Музыка, созданная с использованием электронных инструментов и технологий"},
            {"name": "R&B/Soul", "description": "Музыка, сочетающая элементы ритм-энд-блюза, соула и поп-музыки"},
            {"name": "Jazz", "description": "Импровизационная музыка с синкопированными ритмами"},
            {"name": "Classical", "description": "Традиционная академическая музыка"},
            {"name": "Country", "description": "Народная музыка с корнями в сельской местности США"},
            {"name": "Metal", "description": "Агрессивная гитарная музыка с мощными ударными"},
            {"name": "Reggae", "description": "Ямайская музыка с акцентом на синкопированные ритмы"},
            {"name": "Blues", "description": "Музыка, основанная на блюзовых аккордовых прогрессиях"},
            {"name": "Folk", "description": "Традиционная музыка, передаваемая из поколения в поколение"},
            {"name": "Disco", "description": "Танцевальная музыка с пульсирующим ритмом"},
            {"name": "Punk", "description": "Агрессивная, протестная музыка с простыми мелодиями"},
            {"name": "Indie", "description": "Альтернативная музыка независимых исполнителей"},
            {"name": "Techno", "description": "Электронная танцевальная музыка с повторяющимися битами"},
            {"name": "House", "description": "Электронная музыка с ритмом 4/4 и басовыми ударами"},
            {"name": "Trap", "description": "Поджанр хип-хопа с акцентом на басы и синтезаторы"},
            {"name": "K-Pop", "description": "Корейская поп-музыка с яркими аранжировками"},
            {"name": "Latin", "description": "Музыка латиноамериканского происхождения"}
        ]
        for genre in genres:
            session.add(Genre(**genre))
        session.commit()


def insert_data_for_playList():
    with session_factory() as session:
        playlists = [
            {
                "id_user": 1,  # music_lover
                "title": "Pop Hits 2023",
                "count_tracks": 12,
                "cover_url": "https://example.com/covers/playlists/pop_hits.jpg",
                "all_time": 2543,  # ~42 минуты
                "created_at": datetime(2023, 5, 10)
            },

            # Рок-коллекция
            {
                "id_user": 2,  # rock_fanatic
                "title": "Rock Legends",
                "count_tracks": 15,
                "cover_url": "https://example.com/covers/playlists/rock_legends.jpg",
                "all_time": 3682,  # ~61 минута
                "created_at": datetime(2023, 4, 15)
            },

            # Джазовый вечер
            {
                "id_user": 3,  # jazz_enthusiast
                "title": "Smooth Jazz Evening",
                "count_tracks": 8,
                "cover_url": "https://example.com/covers/playlists/jazz_evening.jpg",
                "all_time": 5432,  # ~90 минут
                "created_at": datetime(2023, 6, 1)
            },

            # Тренировочный плейлист
            {
                "id_user": 4,  # pop_queen
                "title": "Workout Motivation",
                "count_tracks": 20,
                "cover_url": "https://example.com/covers/playlists/workout.jpg",
                "all_time": 4821,  # ~80 минут
                "created_at": datetime(2023, 3, 20)
            },

            # Классика для работы
            {
                "id_user": 5,  # classical_master
                "title": "Focus & Productivity",
                "count_tracks": 10,
                "cover_url": "https://example.com/covers/playlists/classical_focus.jpg",
                "all_time": 7234,  # ~2 часа
                "created_at": datetime(2023, 2, 5)
            },

            # Хип-хоп микстейп
            {
                "id_user": 6,  # hiphop_head
                "title": "Urban Vibes",
                "count_tracks": 18,
                "cover_url": "https://example.com/covers/playlists/urban_vibes.jpg",
                "all_time": 4215,  # ~70 минут
                "created_at": datetime(2023, 7, 12)
            },

            # Электронная энергия
            {
                "id_user": 7,  # electronic_dreamer
                "title": "EDM Energy Boost",
                "count_tracks": 15,
                "cover_url": "https://example.com/covers/playlists/edm_energy.jpg",
                "all_time": 6123,  # ~1 час 42 минуты
                "created_at": datetime(2023, 1, 30)
            },

            # Романтический вечер
            {
                "id_user": 8,  # indie_spirit
                "title": "Romantic Mood",
                "count_tracks": 12,
                "cover_url": "https://example.com/covers/playlists/romantic.jpg",
                "all_time": 3821,  # ~63 минуты
                "created_at": datetime(2023, 6, 25)
            },

            # Дорожный плейлист
            {
                "id_user": 9,  # blues_traveler
                "title": "Road Trip Mix",
                "count_tracks": 25,
                "cover_url": "https://example.com/covers/playlists/road_trip.jpg",
                "all_time": 8923,  # ~2 часа 29 минут
                "created_at": datetime(2023, 5, 5)
            },

            # Метал для настроения
            {
                "id_user": 10,  # metal_head
                "title": "Metal Power Hour",
                "count_tracks": 10,
                "cover_url": "https://example.com/covers/playlists/metal_power.jpg",
                "all_time": 3600,  # ровно 1 час
                "created_at": datetime(2023, 4, 1)
            }
        ]
        for playlist in playlists:
            session.add(PlayList(**playlist))
        session.commit()


def insert_data_for_playlist_tracks():
    with session_factory() as session:
        playlist_tracks_data = [
            # Pop Hits 2023 (playlist_id=1)
            {"playlist_id": 1, "track_id": 1, "order": 1},  # Electric Love
            {"playlist_id": 1, "track_id": 2, "order": 2},  # Midnight Dance
            {"playlist_id": 1, "track_id": 11, "order": 3},  # Lonely Star

            # Rock Legends (playlist_id=2)
            {"playlist_id": 2, "track_id": 3, "order": 1},  # Thunder Road
            {"playlist_id": 2, "track_id": 4, "order": 2},  # Neon Lights
            {"playlist_id": 2, "track_id": 17, "order": 3},  # Guitar Solo

            # Smooth Jazz Evening (playlist_id=3)
            {"playlist_id": 3, "track_id": 7, "order": 1},  # Smooth Operator
            {"playlist_id": 3, "track_id": 16, "order": 2},  # Jazz Improvisation #7

            # Workout Motivation (playlist_id=4)
            {"playlist_id": 4, "track_id": 6, "order": 1},  # Digital Dreams
            {"playlist_id": 4, "track_id": 15, "order": 2},  # Digital Sunrise (Extended)
            {"playlist_id": 4, "track_id": 20, "order": 3},  # Rock Anthem

            # Focus & Productivity (playlist_id=5)
            {"playlist_id": 5, "track_id": 8, "order": 1},  # Moonlight Sonata
            {"playlist_id": 5, "track_id": 18, "order": 2},  # Classical Moment

            # Urban Vibes (playlist_id=6)
            {"playlist_id": 6, "track_id": 5, "order": 1},  # Urban King
            {"playlist_id": 6, "track_id": 13, "order": 2},  # Street Life (Clean)
            {"playlist_id": 6, "track_id": 14, "order": 3},  # Street Life (Explicit)

            # EDM Energy Boost (playlist_id=7)
            {"playlist_id": 7, "track_id": 6, "order": 1},  # Digital Dreams
            {"playlist_id": 7, "track_id": 15, "order": 2},  # Digital Sunrise (Extended)

            # Romantic Mood (playlist_id=8)
            {"playlist_id": 8, "track_id": 1, "order": 1},  # Electric Love
            {"playlist_id": 8, "track_id": 7, "order": 2},  # Smooth Operator
            {"playlist_id": 8, "track_id": 10, "order": 3},  # Whispering Wind

            # Road Trip Mix (playlist_id=9)
            {"playlist_id": 9, "track_id": 3, "order": 1},  # Thunder Road
            {"playlist_id": 9, "track_id": 5, "order": 2},  # Urban King
            {"playlist_id": 9, "track_id": 12, "order": 3},  # Blues Traveler

            # Metal Power Hour (playlist_id=10)
            {"playlist_id": 10, "track_id": 9, "order": 1},  # Steel Hammer
            {"playlist_id": 10, "track_id": 20, "order": 2}  # Rock Anthem
        ]
        for playlist_track in playlist_tracks_data:
            session.add((PlaylistTrack(**playlist_track)))
        session.commit()


def insert_data_for_userPreference():
    with session_factory() as session:
        # Очищаем таблицы (опционально, если нужно перезаписать данные)
        # session.execute("DELETE FROM user_track_preferences")
        # session.execute("DELETE FROM user_album_preferences")
        # session.execute("DELETE FROM user_preferences")
        # session.commit()

        # Данные для вставки
        sample_combinations = [
            {"user_id": 3, "preference_type": "ALBUM", "album_id": 5},
            {"user_id": 3, "preference_type": "TRACK", "track_id": 12},
            {"user_id": 4, "preference_type": "TRACK", "track_id": 18},
            {"user_id": 5, "preference_type": "ALBUM", "album_id": 8},
            {"user_id": 6, "preference_type": "TRACK", "track_id": 40},
            {"user_id": 7, "preference_type": "ALBUM", "album_id": 3},
            {"user_id": 8, "preference_type": "TRACK", "track_id": 1},
            {"user_id": 9, "preference_type": "ALBUM", "album_id": 11},
            {"user_id": 10, "preference_type": "TRACK", "track_id": 15},
            {"user_id": 11, "preference_type": "ALBUM", "album_id": 6},
            {"user_id": 12, "preference_type": "TRACK", "track_id": 43},
            {"user_id": 13, "preference_type": "ALBUM", "album_id": 9},
            {"user_id": 14, "preference_type": "TRACK", "track_id": 19},
            {"user_id": 15, "preference_type": "ALBUM", "album_id": 10},
            {"user_id": 2, "preference_type": "TRACK", "track_id": 5},
            {"user_id": 18, "preference_type": "ALBUM", "album_id": 12},
            {"user_id": 1, "preference_type": "TRACK", "track_id": 48}
        ]

        for item in sample_combinations:
            # Создаем основную запись предпочтения
            user_pref = UserPreference(
                user_id=item["user_id"],
                preference_type=item["preference_type"]
            )
            session.add(user_pref)
            session.flush()  # Получаем ID созданной записи

            # Создаем соответствующую запись в зависимой таблице
            if item["preference_type"] == "TRACK":
                track_pref = UserTrackPreference(
                    id=user_pref.id,
                    track_id=item["track_id"]
                )
                session.add(track_pref)
            else:
                album_pref = UserAlbumPreference(
                    id=user_pref.id,
                    album_id=item["album_id"]
                )
                session.add(album_pref)

        session.commit()
        print(f"Успешно добавлено {len(sample_combinations)} записей предпочтений")



def full_in_the_data():
    # insert_data_for_genre()  # <--------- Заполнение таблицы жанров
    # insert_data_for_users()  # <--------- Заполнение таблицы пользователей
    # insert_data_for_author()  # <-------- Заполнение таблицы авторов
    # insert_data_for_album() # <---------- Заполнение таблицы альбомов
    # insert_data_for_tracks() # <--------- Заполнение таблицы треков
    # insert_data_for_playList() # <------- Заполнение таблицы плейлистов
    insert_data_for_userPreference() # <- Заполнение таюлицы предпочтений пользователя
    # insert_data_for_playlist_tracks() # < Заполнение таюлицы связи


if __name__ == "__main__":

    # create_db() # Создание бд
    # del_db() # Удаление БД
    full_in_the_data() # Наполнение данными бд