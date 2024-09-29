from uuid import UUID
from typing import Optional

from pydantic import BaseModel

from .breed import BreedSchema


class CatBaseSchema(BaseModel):
    name: str
    color: str
    age_months: int
    description: str
    

class CatCreateSchema(CatBaseSchema):
    breed_id: UUID | str


class CatUpdateSchema(CatBaseSchema):
    breed_id: UUID | str


class CatSchema(CatBaseSchema):
    id: UUID
    breed: Optional[BreedSchema] = None
