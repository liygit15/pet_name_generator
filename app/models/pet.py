from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from ..db import db

class Pet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None]
    animal_type: Mapped[str]
    personality: Mapped[str]
    color: Mapped[str]

    def to_dict(self):
        pet_dict = {
            "id" : self.id,
            "animal": self.animal_type,
            "personality": self.personality,
            "coloration": self.color
        }
        if self.name:
            pet_dict["name"] = self.name
        
        return pet_dict


    @classmethod
    def from_dict(cls, data_dict):
        new_pet = cls(
            name = data_dict["name"],
            animal_type = data_dict["animal"],
            personality = data_dict["personality"],
            color = data_dict["coloration"]
        )

        return new_pet