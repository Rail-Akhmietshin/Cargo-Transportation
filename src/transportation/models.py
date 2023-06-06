from sqlalchemy import Integer, Float, Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import metadata, Base


class Location(Base):
    __tablename__ = "app_transportation_location"
    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[str] = mapped_column(String, nullable=False)
    zip_code: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)


class Cargo(Base):
    __tablename__ = "app_transportation_cargo"
    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pick_up: Mapped[int] = mapped_column(ForeignKey(Location.id))
    delivery: Mapped[int] = mapped_column(ForeignKey(Location.id))
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(Text)


class Car(Base):
    __tablename__ = "app_transportation_car"
    metadata = metadata

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    unique_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    current_location: Mapped[int] = mapped_column(ForeignKey(Location.id))
    load_capacity: Mapped[int] = mapped_column(Integer)

