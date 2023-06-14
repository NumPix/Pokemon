import random

from Objects.color import color
from Battle import *
from Data.attacks import *
from Data.items import *


def new_game():
    print(color.BOLD + "Chose a starter pokemon:" + color.END)

    list_of_starters = [
        "Bulbasaur",
        "Charmander",
        "Squirtle",
        "Chikorita",
        "Cindaquil",
        "Totodile",
        "Treecko",
        "Torchik",
        "Mudkip",
        "Turtwig",
        "Chimchar",
        "Piplup",
        "Snivy",
        "Tepig",
        "Oshawott",
        "Chespin",
        "Fennekin",
        "Froakie",
    ]

    print(*[f"({poke[0]}) {poke[1]}" for poke in enumerate(list_of_starters)], sep="\n", end="\n\n")

    ch_poke = input().strip()

    while ch_poke not in range(18):
        print(*[f"({poke[0]}) {poke[1]}" for poke in enumerate(list_of_starters)], sep="\n", end="\n\n")
        ch_poke = input().strip()

    print(color.BOLD + "Good! Let your own adventure begin!" + color.END + "\n")

    return ch_poke


def main():
    print(color.BOLD + "Welcome to Pokemon Battles!\n" + color.END)
    print(*["(0) •New Game", "(1) •Continue", "(2) •Exit"], sep="\n", end="\n\n")

    menu_option = input().strip()

    while menu_option not in ["0", "1", "2"]:
        print(*["(0) •New Game", "(1) •Continue", "(2) •Exit"], sep="\n", end="\n\n")
        menu_option = input().strip()

    if menu_option == "0":
        starter_poke = new_game()


"""def main():
    with open("config.json") as cnf:
        config = json.load(cnf)

    Items = list(map(lambda x: (globals()[x[0]], x[1]), config["Items"].items()))

    Bag = {
        'hp/pp restore': dict(list(filter(lambda x: x[0].type == "HP/PP restore", Items))),
        'status restore': dict(list(filter(lambda x: x[0].type == "Status restore", Items))),
        'poke balls': dict(list(filter(lambda x: x[0].type == "Pokeballs", Items))),
        'battle items': dict(list(filter(lambda x: x[0].type == "Battle items", Items)))
    }

    YourTeam = list(
        map(lambda x: Pokemon(x["name"], list(map((lambda y: globals()[y]), x["attacks"])), x["gender"], x["id"]),
            config["YourTeam"]))

    FoesTeam = list(
        map(lambda x: Pokemon(x["name"], list(map((lambda y: globals()[y]), x["attacks"])), x["gender"], x["id"]),
            config["FoesTeam"]))

    for i in range(len(YourTeam)):
        YourTeam[i].expGain(random.randint(200000, 300000), False)

    for i in range(len(FoesTeam)):
        FoesTeam[i].expGain(random.randint(200000, 300000), False)

    battle(YourTeam, FoesTeam, "Izuna", "Glacie", Bag)
"""

if __name__ == '__main__':
    main()
