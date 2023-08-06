from typing import Union
import json
import sys
import os
from colorama import Fore, Style
from whist_score.models.Player import Player
from whist_score.models.RoundTypes import (
    BaseMiserieClass,
    Abondance,
    VragenEnMeegaan,
    Solo,
    GroteMiserie,
    KleineMiserie,
    GroteMiserieOpTafel,
    Troel,
    Piccolo,
)

from whist_score.constants import (
    KLEINE_MISERIE,
    KLEINE_SOLO_SLIM,
    GROTE_MISERIE,
    PICCOLO,
    GROTE_MISERIE_OP_TAFEL,
    GROTE_SOLO_SLIM,
    VRAGEN_EN_MEEGAAN,
    TROEL,
    SOLO,
    ABONDANCE,
    SAVE_FOLDER,
    CONFIG_FOLDER,
    GAME_TYPES_FILE_NAME,
)
from whist_score.utils import read_json


# Get the path to the config file
game_types_config_file_path = os.path.join(CONFIG_FOLDER, GAME_TYPES_FILE_NAME)


class Game:
    def __init__(
        self,
        current_round: int = 1,
        players: list = [None, None, None, None],
        scoresheet: list = [],
        current_game_id: Union[None, int] = None,
    ):
        self.current_round = current_round
        self.players = players
        self.scoresheet = scoresheet
        self.current_game_id = current_game_id

    def display_points(self):
        print()
        print("\t|" + "\t|".join([player.name for player in self.players]))
        print("\t|" + "\t|".join(["-----"] * len(self.players)))
        for i, record in enumerate(self.scoresheet):
            print(f"{i+1}\t|{record[0]}\t|{record[1]}\t|{record[2]}\t|{record[3]}")
        print()

    def add_record_to_scoresheet(self) -> None:
        self.scoresheet.append(
            (
                self.players[0].score,
                self.players[1].score,
                self.players[2].score,
                self.players[3].score,
            )
        )

    def remove_record_from_scoresheet(self) -> None:
        del self.scoresheet[-1]

    def update_record(self, record_id: int, new_values: list) -> None:
        for index, item in enumerate(new_values):
            if type(item) == int:
                self.scoresheet[record_id][index] = new_values[index]

    def menu(self):
        while True:
            print()
            print(f"({Fore.BLUE}N{Style.RESET_ALL})ext round")
            print(f"({Fore.BLUE}S{Style.RESET_ALL})ave game")
            print(f"({Fore.BLUE}D{Style.RESET_ALL})isplay scoresheet")
            print(f"({Fore.BLUE}R{Style.RESET_ALL})emove last record from scoresheet")
            print(f"({Fore.BLUE}M{Style.RESET_ALL})odify score")
            print(f"({Fore.BLUE}Q{Style.RESET_ALL})uit")
            answer = input("Choose your next action: ").strip()
            if answer in ("N", "n"):
                break
            elif answer in ("S", "s"):
                self.save()
            elif answer in ("Q", "q"):
                self.exit()
            elif answer in ("D", "d"):
                self.display_points()
            elif answer in ("R", "r"):
                self.remove_record()
            elif answer in ("M", "m"):
                if len(self.scoresheet) == 0:
                    print(
                        f"{Fore.RED}No score record(s) available to modify.{Style.RESET_ALL}"
                    )
                    continue
                self.modify_scoresheet()
            else:
                continue

    def exit(self):
        while True:
            quitting = input("Are you sure you wish to exit? (y/N): ").strip()
            if quitting in ("N", "n", ""):
                break
            elif quitting in ("Y", "y"):
                sys.exit(0)
            else:
                continue

    def remove_record(self):
        while True:
            removing = input(
                "Are you sure you wish to delete the last record from the scoresheet? (y/N): "
            ).strip()
            if removing in ("N", "n", ""):
                break
            elif removing in ("Y", "y"):
                try:
                    self.remove_record_from_scoresheet()
                except IndexError:
                    print(
                        f"{Fore.RED}Unable to remove last record from scoresheet: the scorelist seems to be empty.{Style.RESET_ALL}"
                    )
                except Exception as e:
                    print(
                        f"{Fore.RED}An error occurred while trying to remove last record from scoresheet: {e}{Style.RESET_ALL}"
                    )
                self.display_points()
            else:
                continue

    def modify_scoresheet(self):
        while True:
            self.display_points()
            removing = input(
                "Please select the record to modify (q to quit modifying): "
            ).strip()
            try:
                if removing in ("Q", "q"):
                    return
                if int(removing) not in range(1, len(self.scoresheet) + 1):
                    raise ValueError()
                break
            except ValueError:
                print(f"{Fore.RED}Please select a valid number.{Style.RESET_ALL}")
                continue
            except Exception as e:
                print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
                continue
        while True:
            new_values = input(
                "Please give new points for this record, all seperated by a space. If you do not want to change a specific value, put x instead of the new value: "
            ).strip()
            try:
                new_values = new_values.split()
                for index, item in enumerate(new_values):
                    try:
                        new_values[index] = int(item)
                    except ValueError:
                        new_values[index] = "x"
                    except Exception as e:
                        print(
                            f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}"
                        )
                        continue
                if len(new_values) != 4:
                    raise ValueError()
                self.update_record(record_id=int(removing) - 1, new_values=new_values)
                print(f"{Fore.GREEN}Successfully updated record.{Style.RESET_ALL}")
                self.display_points()
                break
            except ValueError:
                print(f"{Fore.RED}Please insert 4 valid numbers.{Style.RESET_ALL}")
                continue
            except Exception as e:
                print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
                continue

    def save(self):
        payload = {
            "current_round": self.current_round,
            "scoresheet": self.scoresheet,
            "players": [player.name for player in self.players],
        }
        while True:
            answer = input("Give a name for the file (leave empty to cancel): ").strip()
            if answer == "":
                print(
                    f"{Fore.RED}You provided an empty value. Game not saved.{Style.RESET_ALL}"
                )
                break
            try:
                with open(f"{SAVE_FOLDER}{answer}.json", "w") as f:
                    json.dump(payload, f, indent=2)
                print(
                    f"{Fore.GREEN}Successfully saved to {SAVE_FOLDER}{answer}.json{Style.RESET_ALL}"
                )
                break
            except Exception as e:
                print(e.__repr__())
                continue

    def new_game(self):
        while True:
            players = input(
                "Please insert the names of the 4 players, all separated by a space:\n"
            )
            try:
                players = players.split()
                if len(players) != 4:
                    raise ValueError("There must be exactly 4 player names.")
                break
            except Exception as e:
                print(
                    f"{Fore.RED}Error while fetching players: {e} Please try again.{Style.RESET_ALL}"
                )
                players = None
        players = [Player(name=player_name) for player_name in players]
        print()
        for i, player in enumerate(players):
            print(f"Player {i+1}: {player.name}")
        print()
        self.players = players
        self.new_round()

    def load_game(self):
        while True:
            json_files = [
                pos_json
                for pos_json in os.listdir(SAVE_FOLDER)
                if pos_json.endswith(".json")
            ]
            print()
            for index, name in enumerate(json_files):
                print(f"({Fore.BLUE}{index}{Style.RESET_ALL})\t{name}")
            answer = input("Please select a game to load: ").strip()
            try:
                try:
                    answer = int(answer)
                except Exception:
                    raise TypeError("Please provide a valid number.")
                if answer not in range(len(json_files)):
                    raise ValueError("Please select a valid number.")
                with open(f"{SAVE_FOLDER}{json_files[answer]}", "r") as f:
                    payload = json.load(f)
                break
            except Exception as e:
                print()
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                print()
                continue
        players = []
        for index, item in enumerate(payload["players"]):
            players.append(Player(name=item, score=payload["scoresheet"][-1][index]))
        self.current_round = payload["current_round"]
        self.scoresheet = payload["scoresheet"]
        self.players = players
        self.new_round()

    def new_round(self):
        while True:
            self.display_points()
            self.menu()

            print(f"{Fore.GREEN}Starting new round...{Style.RESET_ALL}")
            current_game_type = choose_game_type()
            current_game = choose_players(
                game=self, current_game_type=current_game_type
            )
            if not current_game:
                continue

            if issubclass(type(current_game), BaseMiserieClass):
                current_game.complete()
                current_game.assign_points()
            else:
                while True:
                    answer = input("How many tricks were achieved? ").strip()
                    try:
                        answer = int(answer)
                        if answer not in range(0, 14):
                            continue
                        break
                    except ValueError:
                        print(f"{Fore.RED}Please provide a number.{Style.RESET_ALL}")
                    except Exception:
                        continue
                current_game.assign_points(tricks_achieved=answer)
            self.add_record_to_scoresheet()
            self.current_round += 1


def choose_game_type() -> dict:
    print("-" * 30)
    game_types = read_json(game_types_config_file_path)
    for index, item in enumerate(game_types):
        print(f"({Fore.BLUE}{index}{Style.RESET_ALL})\t{item['name']}")
    print("-" * 30)
    while True:
        game_number = input("Select new game: ").strip()
        try:
            game_number = int(game_number)
        except ValueError:
            print(f"{Fore.RED}Please provide a number.{Style.RESET_ALL}")
        except Exception as e:
            print(
                f"{Fore.RED}An error occurred while parsing the input: {e}{Style.RESET_ALL}"
            )
            continue
        if game_number in range(len(game_types)):
            valid = False
            while True:
                validity = input(
                    f"Chosen game: {Fore.BLUE}{game_types[game_number]['name']}{Style.RESET_ALL}. Is this correct? (Y/n): "
                ).strip()
                if validity in ("Y", "y", ""):
                    valid = True
                    break
                elif validity in ("N", "n"):
                    valid = False
                    break
                else:
                    continue
            if valid:
                break
            else:
                continue
        else:
            print(f"{Fore.RED}Please insert a valid number.{Style.RESET_ALL}")
            continue
    return game_types[game_number]


def choose_players(game: Game, current_game_type: dict) -> Union[None, object]:
    while True:
        players = input(
            f"""
({Fore.BLUE}1{Style.RESET_ALL})\t{game.players[0].name}
({Fore.BLUE}2{Style.RESET_ALL})\t{game.players[1].name}
({Fore.BLUE}3{Style.RESET_ALL})\t{game.players[2].name}
({Fore.BLUE}4{Style.RESET_ALL})\t{game.players[3].name}\n
({Fore.BLUE}q{Style.RESET_ALL})\tQuit new round\n
Who is playing {Fore.BLUE}{current_game_type['name']}{Style.RESET_ALL}? If more players, please separate with a space: """
        ).strip()
        if players in ("Q", "q"):
            return
        try:
            playing_players = players.split()
            for index, player in enumerate(playing_players):
                playing_players[index] = game.players[int(player) - 1]
            other_players = [x for x in game.players if x not in playing_players]
        except ValueError:
            print(
                f"{Fore.RED}Please provide one or more valid numbers, separated by a space if necessary.{Style.RESET_ALL}"
            )
            continue
        except Exception as e:
            print(f"{Fore.RED}An unexpected exception occurred: {e}{Style.RESET_ALL}")
            continue
        try:
            if ABONDANCE in current_game_type["name"]:
                current_game = Abondance(
                    number_of_tricks=current_game_type["number_of_tricks"],
                    playing_players=playing_players,
                    other_players=other_players,
                )
            elif current_game_type["name"] == KLEINE_SOLO_SLIM:
                current_game = Abondance(
                    number_of_tricks=current_game_type["number_of_tricks"],
                    playing_players=playing_players,
                    other_players=other_players,
                )
            elif current_game_type["name"] == GROTE_SOLO_SLIM:
                current_game = Abondance(
                    number_of_tricks=current_game_type["number_of_tricks"],
                    playing_players=playing_players,
                    other_players=other_players,
                )
            elif VRAGEN_EN_MEEGAAN in current_game_type["name"]:
                current_game = VragenEnMeegaan(
                    number_of_tricks=current_game_type["number_of_tricks"],
                    playing_players=playing_players,
                    other_players=other_players,
                )
            elif current_game_type["name"] == TROEL:
                while True:
                    answer = input("Did you keep the current trump? (Y/n): ").strip()
                    if answer in ("Y", "y", ""):
                        number_of_tricks = current_game_type["number_of_tricks"][
                            "trump_kept"
                        ]
                        current_game = Troel(
                            number_of_tricks=number_of_tricks,
                            playing_players=playing_players,
                            other_players=other_players,
                            trump_changed=False,
                        )
                        break
                    elif answer in ("N", "n"):
                        number_of_tricks = current_game_type["number_of_tricks"][
                            "trump_changed"
                        ]
                        current_game = Troel(
                            number_of_tricks=number_of_tricks,
                            playing_players=playing_players,
                            other_players=other_players,
                            trump_changed=True,
                        )
                        break
            elif SOLO in current_game_type["name"]:
                current_game = Solo(
                    number_of_tricks=current_game_type["number_of_tricks"],
                    playing_players=playing_players,
                    other_players=other_players,
                )
            elif current_game_type["name"] == KLEINE_MISERIE:
                current_game = KleineMiserie(
                    playing_players=playing_players, other_players=other_players
                )
            elif current_game_type["name"] == GROTE_MISERIE:
                current_game = GroteMiserie(
                    playing_players=playing_players, other_players=other_players
                )
            elif current_game_type["name"] == PICCOLO:
                current_game = Piccolo(
                    playing_players=playing_players, other_players=other_players
                )
            elif current_game_type["name"] == GROTE_MISERIE_OP_TAFEL:
                current_game = GroteMiserieOpTafel(
                    playing_players=playing_players, other_players=other_players
                )
            break
        except ValueError as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An exception occurred: {e}{Style.RESET_ALL}")
    return current_game
