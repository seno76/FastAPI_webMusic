from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.modelsORM import *
from sqlalchemy import select, update, delete
from src.models.modelsPD import GenrePDData, GenrePD, GenreBase, GenreCreate

def get_all_genres(db: Session, offset: int = 0, limit: int = 10) -> List[GenrePD]: # Нужно будет посмотреть типы потому что тут я возвращаю один тип (юолее полный а в сервисе GenreBase)
    with db() as session:
        genres = session.scalars(select(Genre).limit(limit).offset(offset)).all()
        return [GenrePD.model_validate(genre) for genre in genres]

def get_genre_by_id(db: Session, genre_id: int) -> Optional[GenrePDData]:
    with db() as session:
        genre = session.scalar(select(Genre).where(Genre.id == genre_id))
        if not genre:
            return None
        return GenrePDData.model_validate(genre)

def create_new_genre(db: Session, data: GenreCreate) -> GenrePD:
    with db() as session:
        genre = Genre(**data.model_dump())
        session.add(genre)
        session.commit()
        session.refresh(genre)
        return GenrePD.model_validate(genre)

def delete_genre(db: Session, genre_id: int) -> bool:
    with db() as session:
        if not session.get(Genre, genre_id):
            return False
        query = delete(Genre).where(Genre.id == genre_id)
        session.execute(query)
        session.commit()
        return True