from Battle import *
from Data.attacks import *
from Data.items import *


def main():
    Items = [(Potion, 4), (Superpotion, 10), (Maxpotion, 2), (Revive, 5), (Maxrevive, 1), (Fullheal, 5), (Xattack2, 3),
             (Xdefense2, 2), (Elixir, 2), (Ether, 1)]

    Bag = {
        'hp/pp restore': dict(list(filter(lambda x: x[0].type == "HP/PP restore", Items))),
        'status restore': dict(list(filter(lambda x: x[0].type == "Status restore", Items))),
        'poke balls': dict(list(filter(lambda x: x[0].type == "Pokeballs", Items))),
        'battle items': dict(list(filter(lambda x: x[0].type == "Battle items", Items)))
    }

    # Team 1 pokemon
    YourTeam = [
        Pokemon("Gabby", [Bite, DragonBreath, Bulldoze, AerialAce], 1, 444, 1, 4),
        Pokemon("Vivi", [BugBite, DrainingKiss, Psybeam, Hurricane], 0, 666, 1, 2),
        Pokemon("Trump", [Crunch, IcePunch, IronTail, ThunderFang], 1, 735, 1, 2),
        Pokemon("Misty", [AncientPower, MudSlap, TriAttack, HiddenPower], 0, 175, 1, 1),
        Pokemon("Kyolya", [Flamethrower, Inferno, LavaPlume, IronTail], 1, 156, 1, 3),
        Pokemon("Clie", [DoubleEdge, GrassKnot, GyroBall, RockTomb], 1, 344, 1, 2),
    ]

    # Team 2 pokemon
    FoesTeam = [
        Pokemon("Doggy", [DarkPulse, HeatWave, ThunderFang, RockSmash], 1, 228, 1, 4),
        Pokemon("Rein", [Bulldoze, MudSlap, MegaKick, Magnitude], 1, 750, 1, 2),
        Pokemon("Lei", [BodySlam, AncientPower, IronTail, WaterPulse], 1, 305, 1, 4),
        Pokemon("Amogus", [EnergyBall, HiddenPower, Astonish, Bide], 1, 590, 1, 2),
        Pokemon("Creepie", [Earthquake, Spikes, Swift, GyroBall], 1, 204, 1, 2),
        Pokemon("Samuro", [Blizzard, HydroPump, IceBeam, AirSlash], 1, 503, 1, 3),
    ]

    for i in range(6):
        YourTeam[i].expGain(r.randint(200000, 250000), False)
        FoesTeam[i].expGain(r.randint(200000, 250000), False)

    r.shuffle(YourTeam)
    r.shuffle(FoesTeam)

    battle(YourTeam, FoesTeam, "Shiro", "Izuna", Bag)


if __name__ == '__main__':
    main()
