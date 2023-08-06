import click
from whist_score.views.games import new_game, load_game
from colorama import Fore, Style


@click.command()
@click.option("--players", help="Names of the 4 players, seperated by a space")
def main(players=None):
    while True:
        choice = input(
            f"({Fore.BLUE}N{Style.RESET_ALL})ew game | ({Fore.BLUE}L{Style.RESET_ALL})oad game | ({Fore.BLUE}S{Style.RESET_ALL})ettings\n"
        ).strip()
        if choice in ("N", "n"):
            new_game(players=players)
            break
        elif choice in ("L", "l"):
            load_game()
            break
        elif choice in ("S", "s"):
            settings()
            break
        else:
            print("Please provide a valid option.")


def settings():
    pass


if __name__ == "__main__":
    main()
