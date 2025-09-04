from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.modelsORM import *
from sqlalchemy import select, update, delete
from src.schemas.genre import GenrePDData, GenrePD, GenreCreate
from src.utils.abstractions import SQLAlchemyRepository
from src.bd.database import session_factory


class GenreRepository(SQLAlchemyRepository):

    model = Genre

    def get_all_genres(
        self, offset: int = 0, limit: int = 10
    ) -> List[
        GenrePD
    ]:  # Нужно будет посмотреть типы потому что тут я возвращаю один тип (юолее полный а в сервисе GenreBase)
        with session_factory() as session:
            genres = session.scalars(
                select(self.model).limit(limit).offset(offset)
            ).all()
            return [GenrePD.model_validate(genre) for genre in genres]

    def get_genre_by_id(self, genre_id: int) -> Optional[GenrePDData]:
        with session_factory() as session:
            genre = session.scalar(select(self.model).where(self.model.id == genre_id))
            if not genre:
                return None
            return GenrePDData.model_validate(genre)

    def create_new_genre(self, data: GenreCreate) -> GenrePD:
        with session_factory() as session:
            genre = self.model(**data.model_dump())
            session.add(genre)
            session.commit()
            session.refresh(genre)
            return GenrePD.model_validate(genre)

    def delete_genre(self, genre_id: int) -> bool:
        with session_factory() as session:
            if not session.get(self.model, genre_id):
                return False
            query = delete(self.model).where(self.model.id == genre_id)
            session.execute(query)
            session.commit()
            return True
