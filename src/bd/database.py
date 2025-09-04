from settingsBD import settings_bd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

sync_engine = create_engine(
    url=settings_bd.get_db_url,
    echo=False,
)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    ...
