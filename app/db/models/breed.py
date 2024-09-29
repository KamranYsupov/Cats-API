from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base


class Breed(Base):    
    name: Mapped[str] = mapped_column(String, unique=True, index=True)

    cats: Mapped[list['Cat']] = relationship(
        back_populates='breed',
        lazy='selectin',
    )