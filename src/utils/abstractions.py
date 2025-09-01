from abc import ABC, abstractmethod

from pydantic import BaseModel
from src.bd.database import session_factory
from sqlalchemy import select, insert


class AbstractRepository(ABC):
    
    @abstractmethod
    def find_all():
        raise NotImplementedError
    
    @abstractmethod
    def find_by_id():
        raise NotImplementedError
    
    @abstractmethod
    def create_new():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    
    model = None
    
    def find_all(self, ):
        with session_factory() as session:
            stmt = select(self.model)
            result = session.execute(stmt).scalars().all()
            return result
    
    def find_by_id(self):
        ...
    
    def create_new(self, data: dict):
        with session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            result = session.execute(stmt)
            session.commit()
            return result.scalar_one()