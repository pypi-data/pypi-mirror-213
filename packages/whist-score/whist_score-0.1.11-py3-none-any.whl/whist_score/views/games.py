from whist_score.models.Player import Player
from whist_score.models.Game import Game
from colorama import Fore, Style


def new_game(players: str):
    while True:
        if not players:
            players = input(
                "Please insert the names of the 4 players, separated by a space:\n"
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
    game = Game(players=players)
    game.new_round()


def load_game():
    game = Game()
    game.load_game()
