from sqlalchemy.orm import Session, joinedload, selectinload
from typing import Optional, List
from src.models.modelsORM import *
from sqlalchemy import select, delete, insert, update, func
from src.models.modelsPD import TrackPD, TrackPDData, TrackCreate, TrackUpdate
from datetime import date



def get_track_by_id(db: Session, track_id: int) -> Optional[TrackPDData]:
    """Получить трек по ID со связанными данными"""
    with db() as session:
        track = session.scalar(
            select(Track)
            .options(
                joinedload(Track.author),
                joinedload(Track.album),
                joinedload(Track.genre)
            )
            .where(Track.id == track_id)
        )
        if not track:
            return None
        return TrackPDData.from_orm(track)


def create_track(db: Session, data: TrackCreate) -> TrackPD:
    with db() as session:
        track = Track(**data.model_dump())
        track.file_path = str(track.file_path)
        session.add(track)
        session.commit()
        session.refresh(track)
        return TrackPD.from_orm(track)

def create_track_2(db: Session, data: dict) -> Track:
    with db() as session:
        query = insert(Track).values(**data).returning(Track)
        print(query, "------->", type(query))
        result = session.execute(query).scalar_one()
        session.commit()
        return TrackPD.from_orm(result)

def delete_track_by_id(db: Session, track_id: int) -> None:
    with db() as session:
        if not session.get(Track, track_id):
            return False
        query = delete(Track).where(Track.id == track_id)
        session.execute(query)
        session.commit()
        return True

def get_list_tracks(
        db: Session,
        author_id: int = None,
        genre_id: int = None,
        limit: int = 100,
        offset: int = 0
) -> List[TrackPD]:

    with db() as session:
        query = select(Track)

        if author_id:
            query = query.where(Track.author_id == author_id)

        if genre_id:
            query = query.where(Track.genre_id == genre_id)

        tracks = session.execute(query.offset(offset).limit(limit)).scalars().all()

        return [TrackPD.from_orm(track) for track in tracks]


def update_data(db: Session, id_track: int, data: TrackUpdate) -> Optional[TrackPD]:
    with db() as session:
        data.file_path = str(data.file_path)
        query = update(Track).\
            where(Track.id == id_track).\
            values(**data.model_dump(exclude_unset=True)).\
            returning(Track)                                         # Проблема очевидная если у нас будут передаваться в словаре  ключи которых не существует  # упадет с ошибкой надо будет проверить через hasattr
        track = session.execute(query).scalar_one_or_none()
        session.commit()
        return TrackPD.model_validate(track)


def get_tracks_by_author(db: Session, author_id: int) -> List[TrackPD]:
    with db() as session:
        query = select(Track).where(Track.author_id == author_id).options(joinedload(Track.album))
        tracks = session.execute(query).scalars().all()
        return [TrackPD.model_validate(track) for track in tracks]

def get_by_album(db: Session, album_id: int) -> List[TrackPD]:
    with db() as session:
        query = select(Track)\
            .filter(Track.album_id == album_id)\
            .options(
                joinedload(Track.genre),
                joinedload(Track.author),
                joinedload(Track.album),
        )
        tracks = session.execute(query).unique().scalars().all()
        print(tracks)
    return [TrackPD.model_validate(t) for t in tracks]

def get_by_genre(db: Session, genre_id: int) -> List[TrackPD]:
    with db() as session:
        query = select(Track).where(Track.genre_id == genre_id)\
            .options(joinedload(Track.genre),
                     joinedload(Track.author),
            )
        tracks = session.execute(query).scalars().all()
        return [TrackPD.from_orm(t) for t in tracks]

# Методы для работы с датами и рейтингом
def get_released_after(db: Session, date: date) -> List[TrackPD]:
    with db() as session:
        query = select(Track).where(Track.release_date >= date).order_by(Track.release_date)
        tracks = session.execute(query).scalars().all()
        return [TrackPD.from_orm(t) for t in tracks]

def get_top_rated(db: Session, limit: int = 100) -> List[TrackPD]:
    with db() as session:
        tracks = session.query(Track) \
            .order_by(Track.rating.desc()) \
            .limit(limit) \
            .all()
    return [TrackPD.from_orm(t) for t in tracks]

# Поисковые методы
def search_by_title(db: Session, title_query: str) -> List[TrackPD]:
    """Поиск треков по названию"""
    with db() as session:
        tracks = session.query(Track) \
            .filter(func.lower(Track.title).contains(func.lower(title_query))) \
            .all()
    return [TrackPD.from_orm(t) for t in tracks]

# Агрегатные методы (возвращают примитивные типы)
def get_average_rating(db: Session) -> float:
    """Средний рейтинг всех треков"""
    return db().query(func.avg(Track.rating)).scalar() or 0.0

def get_total_duration(db: Session) -> int:
    """Общая продолжительность всех треков"""
    return db().query(func.sum(Track.duration)).scalar() or 0
