from dataclasses import dataclass


@dataclass
class Event:
    kind: str
    payload: dict

    def __str__(self) -> str:
        return f"Event <{self.kind}> with payload = {self.payload}"