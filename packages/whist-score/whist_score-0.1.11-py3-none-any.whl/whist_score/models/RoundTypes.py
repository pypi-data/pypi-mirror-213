from whist_score.constants import (
    # SOLO_POINT_SYSTEM,
    # MISERIE_POINT_SYSTEM,
    # ABONDANCE_POINT_SYSTEM,
    # VRAGEN_EN_MEEGAAN_POINT_SYSTEM,
    # TROEL_POINT_SYSTEM,
    CONFIG_FOLDER,
    SOLO_POINT_SYSTEM_FILE_NAME,
    ABONDANCE_POINT_SYSTEM_FILE_NAME,
    TROEL_POINT_SYSTEM_FILE_NAME,
    VRAGEN_EN_MEEGAAN_POINT_SYSTEM_FILE_NAME,
    MISERIE_POINT_SYSTEM_FILE_NAME,
)
from whist_score.utils import read_json
from colorama import Fore, Style
import os

# Get the path to the config file
solo_point_system_config_file_path = os.path.join(
    CONFIG_FOLDER, SOLO_POINT_SYSTEM_FILE_NAME
)
vragen_en_meegaan_point_system_config_file_path = os.path.join(
    CONFIG_FOLDER, VRAGEN_EN_MEEGAAN_POINT_SYSTEM_FILE_NAME
)
troel_point_system_config_file_path = os.path.join(
    CONFIG_FOLDER, TROEL_POINT_SYSTEM_FILE_NAME
)
miserie_point_system_config_file_path = os.path.join(
    CONFIG_FOLDER, MISERIE_POINT_SYSTEM_FILE_NAME
)
abondance_point_system_config_file_path = os.path.join(
    CONFIG_FOLDER, ABONDANCE_POINT_SYSTEM_FILE_NAME
)


class BaseRoundClass:
    def __init__(self, playing_players: list = [], other_players: list = []):
        self.playing_players = playing_players
        self.other_players = other_players

    def complete(self):
        for player in self.playing_players:
            player.has_succeeded = False
        while True:
            succeeded = input("Did all the player(s) succeed? (Y/n): ").strip()
            if succeeded in ("Y", "y", ""):
                for player in self.playing_players:
                    player.has_succeeded = True
                break
            elif succeeded in ("N", "n"):
                pass
            else:
                continue
            answer = input("Did some players succeed? (Y/n): ")
            if answer in ("Y", "y", ""):
                self.choose_succeeded_players()
                break
            elif answer in ("N", "n"):
                break
            else:
                continue

    def choose_succeeded_players(self):
        while True:
            for index, player in enumerate(self.playing_players):
                print(f"({Fore.BLUE}{index}{Style.RESET_ALL})\t{player.name}")
            answer = input(
                "Please choose the players that succeeded. Separate with a space if needed (q to quit to previous question): "
            )
            try:
                answer = answer.split()
                if answer == ["q"] or answer == ["Q"]:
                    break
                for item in answer:
                    if int(item) not in range(len(self.playing_players)):
                        continue
                break
            except Exception:
                continue
        if answer != ["q"] and answer != ["Q"]:
            for item in answer:
                self.playing_players[int(item)].has_succeeded = True

    def assign_points(self, tricks_achieved: int, point_system: dict) -> None:
        for player in self.playing_players:
            player.add_to_score(
                point_system[str(self.number_of_tricks)]["player"][str(tricks_achieved)]
            )
        for player in self.other_players:
            player.add_to_score(
                point_system[str(self.number_of_tricks)]["other_players"][
                    str(tricks_achieved)
                ]
            )


class Abondance(BaseRoundClass):
    def __init__(
        self,
        number_of_tricks: int,
        playing_players: list = [],
        other_players: list = [],
    ) -> None:
        self.number_of_tricks = number_of_tricks
        if len(playing_players) != 1:
            raise ValueError(
                "There can only be exactly 1 playing player in a game of Abondance."
            )
        if len(other_players) != 3:
            raise ValueError("The number of opposing players must be 3.")
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, tricks_achieved: int):
        super().assign_points(
            tricks_achieved=tricks_achieved,
            point_system=read_json(abondance_point_system_config_file_path),
        )


class VragenEnMeegaan(BaseRoundClass):
    def __init__(
        self,
        number_of_tricks: int,
        playing_players: list = [],
        other_players: list = [],
    ) -> None:
        self.number_of_tricks = number_of_tricks
        if len(playing_players) != 2:
            raise ValueError(
                "There can only be exactly 2 players in a game of vragen en meegaan."
            )
        if len(playing_players) != 2:
            raise ValueError("The number of opposing players must be 2.")
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, tricks_achieved: int) -> None:
        super().assign_points(
            tricks_achieved=tricks_achieved,
            point_system=read_json(vragen_en_meegaan_point_system_config_file_path),
        )


class Troel(VragenEnMeegaan):
    def __init__(
        self,
        number_of_tricks: int,
        playing_players: list = [],
        other_players: list = [],
        trump_changed=False,
    ) -> None:
        super().__init__(
            number_of_tricks=number_of_tricks,
            playing_players=playing_players,
            other_players=other_players,
        )
        self.trump_changed = trump_changed

    def assign_points(
        self,
        tricks_achieved: int,
        point_system: dict = read_json(troel_point_system_config_file_path),
    ) -> None:
        if self.trump_changed:
            for player in self.playing_players:
                player.add_to_score(
                    point_system["player"]["trump_changed"][str(tricks_achieved)]
                )
            for player in self.other_players:
                player.add_to_score(
                    point_system["other_players"]["trump_changed"][str(tricks_achieved)]
                )
        elif not self.trump_changed:
            for player in self.playing_players:
                player.add_to_score(
                    point_system["player"]["trump_kept"][str(tricks_achieved)]
                )
            for player in self.other_players:
                player.add_to_score(
                    point_system["other_players"]["trump_kept"][str(tricks_achieved)]
                )


class Solo(BaseRoundClass):
    def __init__(
        self,
        number_of_tricks: int,
        playing_players: list = [],
        other_players: list = [],
    ) -> None:
        self.number_of_tricks = number_of_tricks
        if len(playing_players) != 1:
            raise ValueError(
                "There can only be exactly 1 playing player in a game of Solo."
            )
        if len(other_players) != 3:
            raise ValueError(
                "The number of opposing players must be 3 in a game of Solo."
            )
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, tricks_achieved: int) -> None:
        super().assign_points(
            tricks_achieved=tricks_achieved,
            point_system=read_json(solo_point_system_config_file_path),
        )


class BaseMiserieClass(BaseRoundClass):
    def __init__(self, playing_players: list = [], other_players: list = []) -> None:
        self.number_of_tricks = 0
        if len(playing_players) <= 0 or len(playing_players) > 4:
            raise ValueError("Please select 1 to 4 players.")
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, point_system: str) -> None:
        number_of_failed_players = [
            player.has_succeeded for player in self.playing_players
        ].count(False)
        base_point_system = read_json(miserie_point_system_config_file_path)
        for player in self.playing_players:
            player.add_to_score(
                base_point_system[point_system]["punten_geslaagd"]
            ) if player.has_succeeded else player.add_to_score(
                base_point_system[point_system]["punten_niet_geslaagd"]
            )
        if number_of_failed_players == 1:
            for player in self.other_players:
                player.add_to_score(
                    base_point_system[point_system]["punten_anderen_niet_geslaagd"]["1"]
                )
        elif number_of_failed_players == 2:
            for player in self.other_players:
                player.add_to_score(
                    base_point_system[point_system]["punten_anderen_niet_geslaagd"]["2"]
                )
        elif number_of_failed_players == 3:
            for player in self.other_players:
                player.add_to_score(
                    base_point_system[point_system]["punten_anderen_niet_geslaagd"]["3"]
                )


class KleineMiserie(BaseMiserieClass):
    def __init__(self, playing_players: list = [], other_players: list = []) -> None:
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, point_system="kleine_miserie"):
        super().assign_points(
            point_system=point_system,
        )


class Piccolo(BaseMiserieClass):
    def __init__(self, playing_players: list = [], other_players: list = []) -> None:
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, point_system="piccolo"):
        super().assign_points(
            point_system=point_system,
        )


class GroteMiserie(BaseMiserieClass):
    def __init__(self, playing_players: list = [], other_players: list = []) -> None:
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, point_system="grote_miserie"):
        super().assign_points(
            point_system=point_system,
        )


class GroteMiserieOpTafel(BaseMiserieClass):
    def __init__(self, playing_players: list = [], other_players: list = []) -> None:
        super().__init__(playing_players=playing_players, other_players=other_players)

    def assign_points(self, point_system="grote_miserie_op_tafel"):
        super().assign_points(
            point_system=point_system,
        )
