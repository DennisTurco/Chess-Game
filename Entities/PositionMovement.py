from typing import Optional
from Entities.Posxy import Posxy

class PositionMovement:
    initial_position: Optional[Posxy]
    final_position: Optional[Posxy]

    def __init__(self, initial_position: Optional[Posxy] = None, final_position: Optional[Posxy] = None):
        self.initial_position = initial_position
        self.final_position = final_position

    def __str__(self) -> str:
        return f"[[{self.initial_position.x if self.initial_position else 'None'}, " \
               f"{self.initial_position.y if self.initial_position else 'None'}], " \
               f"[{self.final_position.x if self.final_position else 'None'}, " \
               f"{self.final_position.y if self.final_position else 'None'}]]"