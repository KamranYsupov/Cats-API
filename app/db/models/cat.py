from uuid import UUID
from typing import Sequence, Dict
from copy import copy

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base
from .breed import Breed
from app.schemas.breed import BreedSchema
from app.schemas.cat import CatSchema


class Cat(Base):
    name: Mapped[str] 
    color: Mapped[str] 
    age_months: Mapped[int] 
    description: Mapped[str] 
    breed_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            'breeds.id',
            ondelete='SET NULL'
        )
    )

    breed: Mapped[Breed] = relationship(
        back_populates='cats',
        lazy='joined'
    )
    
    def serialize(
        self, 
        schema_class,
        exclude_fields: Sequence[str | None] = [],
        model_dump: bool = False
    ) -> Dict:
        if 'breed' in exclude_fields:
            return super().serialize(
                schema_class,
                exclude_fields,
            )
            
        exclude_fields_breed = copy(exclude_fields)     
        exclude_fields_breed.append('breed')
        serialized_data = super().serialize(
            schema_class,
            exclude_fields_breed,
        )           
        if self.breed: 
            serialized_data['breed'] = BreedSchema(
                **self.breed.serialize(schema_class=BreedSchema)
            )
        schema = schema_class(**serialized_data)
        
        if model_dump:
            return schema.model_dump()
        
        return schema
                