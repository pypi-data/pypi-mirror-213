from typing import Union


class Player:
    def __init__(
        self, name: str, succeeded_round: bool = False, score: Union[None, int] = 0
    ) -> None:
        self.name = name
        self.succeeded_round = succeeded_round
        self.score = score

    def __str__(self) -> str:
        return f"Player object with name {self.name}"

    def __repr__(self) -> str:
        return f"Player object with name {self.name}"

    def add_to_score(self, score: int) -> None:
        self.score += score
