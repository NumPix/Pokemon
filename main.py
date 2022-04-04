from Battle import *
from Data.attacks import *
from Data.items import *

def main():

    Items = [(Potion, 4), (Superpotion, 10), (Maxpotion, 2), (Revive, 5), (Maxrevive, 1), (Fullheal, 5), (Xattack2, 3), (Xdefense2, 2), (Elixir, 2), (Ether, 1)]


    Bag = {
        'hp/pp restore': dict(list(filter(lambda x: x[0].type == "HP/PP restore", Items))),
        'status restore': dict(list(filter(lambda x: x[0].type == "Status restore", Items))),
        'poke balls': dict(list(filter(lambda x: x[0].type == "Pokeballs", Items))),
        'battle items': dict(list(filter(lambda x: x[0].type == "Battle items", Items)))
    }


    #Team 1 pokemon
    Seismitoad = Pokemon("Seismy", [HydroPump, EarthPower, SludgeWave, FocusBlast], 1, 537, 1, 3, Lifeorb)
    Haxorus = Pokemon("Axy", [SwordsDance, Outrage, Earthquake, Taunt], 1, 612, 1, 4, Lumberry)
    Shuckle = Pokemon("Shulcky", [StickyWeb, StealthRock, Encore, Toxic], 1, 213, 1, 3, Mentalherb)
    Emboar = Pokemon("Amber", [FlareBlitz, Superpower, WildCharge, HeadSmash], 1, 500, 1, 3, Lifeorb)
    Pangoro = Pokemon("Pandy", [Superpower, KnockOff, GunkShot, PartingShot], 1, 675, 1, 2, Choiceband)
    Klefki = Pokemon("Keyaru", [Reflect, LightScreen, FairyLock, FoulPlay], 1, 707, 1, 1, Lightclay)

    #Team 2 pokemon

    Froslass = Pokemon("Frozzy", [Taunt, Spikes, DestinyBond, IceBeam], 0, 478, 1, 2, Focussash)
    Cresselia = Pokemon("Crya", [Moonlight, Psychic, SkillSwap, Toxic], 0, 488, 1, 4, Leftovers)
    Sylveon = Pokemon("Sylph", [HyperVoice, Psyshock, HiddenPower, BatonPass], 0, 700, 1, 2, Choicespecs)
    Tyrantrum = Pokemon("Tyrie", [HeadSmash, Outrage, Earthquake, Superpower], 1, 697, 1, 2, Choicescarf)
    Kyurem = Pokemon("Kiara", [Substitute, IceBeam, FusionBolt, Roost], 1, 646, 1, 4, Leftovers)
    Bronzong = Pokemon("Brazz", [GyroBall, Earthquake, StealthRock, HiddenPower], 1, 437, 1, 2, Leftovers)

    YourTeam = [Seismitoad, Haxorus, Shuckle, Emboar, Pangoro, Klefki]
    FoesTeam = [Froslass, Cresselia, Sylveon, Tyrantrum, Kyurem, Bronzong]

    for i in range(6):
        YourTeam[i].expGain(r.randint(1000, 10000), False)
        FoesTeam[i].expGain(r.randint(1000, 10000), False)

    r.shuffle(YourTeam)
    r.shuffle(FoesTeam)

    battle(YourTeam, FoesTeam, "Shiro", "Izuna", Bag)

if __name__ == '__main__':
    main()
