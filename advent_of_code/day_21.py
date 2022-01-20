"""
Day 21 Modules
"""

from dataclasses import dataclass, field


@dataclass
class DeterministicDie:
    face: int = field(default=0)
    roll_count: int = field(default=0)

    def roll(self) -> int:
        self.face = self.face + 1 if self.face + 1 <= 100 else 1
        self.roll_count = self.roll_count + 1
        return self.face


@dataclass(eq=True, unsafe_hash=True)
class Player:
    position: int
    score: int = field(default=0)

    def move(self, spaces: int) -> int:
        spaces = spaces % 10
        self.position = (
            self.position + spaces
            if self.position + spaces <= 10
            else self.position + spaces - 10
        )
        self.score = self.score + self.position
        return self.score

    def won_game(self, max_score: int = 1000) -> bool:
        return self.score >= max_score
