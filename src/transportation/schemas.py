from pydantic import BaseModel, Field


class CargoCreate(BaseModel):
    pick_up: int
    delivery: int
    weight: float = Field(ge=1.0, le=1000.0)
    description: str


class CarUpdate(BaseModel):
    id: int
    zip_code: int


class CargoUpdate(BaseModel):
    id: int
    weight: float
    description: str


class CargosFilter(BaseModel):
    weight: float = None
    distance: int = None
