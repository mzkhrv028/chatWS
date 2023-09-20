from dataclasses import dataclass


@dataclass
class User:
    id: str
    name: str

    def __str__(self) -> str:
        return f"User with id = {self.id}, name = {self.name}"