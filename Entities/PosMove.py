from typing import Optional
from Entities.Pos import Pos

class PosMove:
    initial_position: Optional[Pos]
    final_position: Optional[Pos]

    def __init__(self, initial_position: Optional[Pos] = None, final_position: Optional[Pos] = None):
        self.initial_position = initial_position
        self.final_position = final_position

    def __str__(self) -> str:
        return f"[[{self.initial_position.x if self.initial_position else 'None'}, " \
               f"{self.initial_position.y if self.initial_position else 'None'}], " \
               f"[{self.final_position.x if self.final_position else 'None'}, " \
               f"{self.final_position.y if self.final_position else 'None'}]]"

    def reset(self):
        self.initial_position = None
        self.final_position = None
