from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from src.bd.database import Base
import enum


class TypeItem(enum.Enum):
    TRACK = "TRACK"
    ALBUM = "ALBUM"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    author = relationship("Author", back_populates="user", uselist=False)
    playlists = relationship("PlayList", back_populates="user", cascade="all, delete-orphan")

    track_preferences = relationship("UserTrackPreference", back_populates="user", cascade="all, delete-orphan")
    album_preferences = relationship("UserAlbumPreference", back_populates="user", cascade="all, delete-orphan")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    bio = Column(String(1000))
    count_tracks = Column(Integer)
    is_deleted = Column(Boolean, default=False)

    user = relationship("User", back_populates="author", uselist=False)
    tracks = relationship("Track", back_populates="author")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="SET NULL"), nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200))
    duration = Column(Integer)
    file_path = Column(String(200))
    is_explicit = Column(Boolean)
    release_date = Column(DateTime)
    created_at = Column(DateTime)
    rating = Column(Float)

    author = relationship("Author", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
    genre = relationship("Genre", back_populates="tracks")
    playlist = relationship("PlayList", secondary="playlist_tracks", back_populates="tracks")
    user_preferences = relationship("UserTrackPreference", back_populates="track")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(200))
    cover_url = Column(String(200))
    release_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=True)
    rating = Column(Float)

    tracks = relationship("Track", back_populates="album")
    genre = relationship("Genre", back_populates="albums")
    user_preferences = relationship("UserAlbumPreference", back_populates="album")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    name = Column(String(50))
    description = Column(String(200))
    is_delete = Column(Boolean, default=False)

    tracks = relationship("Track", back_populates="genre")
    albums = relationship("Album", back_populates="genre")


class PlaylistTrack(Base):
    __tablename__ = 'playlist_tracks'

    playlist_id = Column(Integer, ForeignKey('playlists.id', ondelete="CASCADE"), primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id', ondelete="CASCADE"), primary_key=True)
    order = Column(Integer)  # Порядок трека в плейлисте
    added_at = Column(DateTime, default=func.now())


class PlayList(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(100))
    cover_url = Column(String(200))
    all_time = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    # updated_at можно добавить

    user = relationship("User", back_populates="playlists")
    tracks = relationship("Track", secondary="playlist_tracks", back_populates="playlist")


class UserTrackPreference(Base):
    __tablename__ = "user_track_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="track_preferences")
    track = relationship("Track", back_populates="user_preferences")


class UserAlbumPreference(Base):
    __tablename__ = "user_album_preferences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="album_preferences")
    album = relationship("Album", back_populates="user_preferences")


print(Base.metadata.tables)

__all__ = [
    "User",
    "Author",
    "Track",
    "Album",
    "Genre",
    "PlayList",
    "PlaylistTrack",
    "UserTrackPreference",
    "UserAlbumPreference",
    "TypeItem",
]
