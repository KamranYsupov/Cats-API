from uuid import UUID

from pydantic import BaseModel
from typing import List, Optional


class BreedBaseSchema(BaseModel): 
    name: str

class BreedCreateSchema(BreedBaseSchema):
    pass

class BreedSchema(BreedBaseSchema):
    id: UUID 
