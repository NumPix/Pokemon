from Battle import *
from Data.attacks import *
from Data.items import *


def main():
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
        YourTeam[i].expGain(r.randint(200000, 250000), False)

    for i in range(len(FoesTeam)):
        FoesTeam[i].expGain(r.randint(200000, 250000), False)

    battle(YourTeam, FoesTeam, "Shiro", "Izuna", Bag)


if __name__ == '__main__':
    main()
