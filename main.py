from Mechanics import *
from attacks import *

#Team 1 pokemon
Seismitoad = pokemon("Seismy", [HydroPump, EarthPower, SludgeWave, FocusBlast], 1, 537, 70, 3, "Life Orb")
Haxorus = pokemon("Axy", [SwordsDance, Outrage, Earthquake, Taunt], 1, 612, 70, 4, "Lum Berry")
Shuckle = pokemon("Shulcky", [StickyWeb, StealthRock, Encore, Toxic], 1, 213, 70, 3, "Mental Herb")
Emboar = pokemon("Amber", [FlareBlitz, Superpower, WildCharge, HeadSmash], 1, 500, 70, 3, "Life Orb")
Pangoro = pokemon("Pandy", [Superpower, KnockOff, GunkShot, PartingShot], 1, 675, 70, 2, "Choice Band")
Klefki = pokemon("Keyaru", [Reflect, LightScreen, FairyLock, FoulPlay], 1, 707, 70, 1, "Light Clay")

#Team 2 pokemon

Froslass = pokemon("Frozzy", [Taunt, Spikes, DestinyBond, IceBeam], 0, 478, 70, 2, "Focus Sash")
Cresselia = pokemon("Crya", [Moonlight, Psychic, SkillSwap, Toxic], 0, 488, 70, 4, "Leftover")
Sylveon = pokemon("Sylph", [HyperVoice, Psyshock, HiddenPower, BatonPass], 0, 700, 70, 2, "Choice Specs")
Tyrantrum = pokemon("Tyrie", [HeadSmash, Outrage, Earthquake, Superpower], 1, 697, 70, 2, "Choice Scarf")
Kyurem = pokemon("Kiara", [Substitute, IceBeam, FusionBolt, Roost], 1, 646, 70, 4, "Leftovers")
Bronzong = pokemon("Brazz", [GyroBall, Earthquake, StealthRock, HiddenPower], 1, 437, 70, 2, "Leftovers")

YourTeam = [Seismitoad, Haxorus, Shuckle, Emboar, Pangoro, Klefki]
FoesTeam = [Froslass, Cresselia, Sylveon, Tyrantrum, Kyurem, Bronzong]
r.shuffle(YourTeam)
r.shuffle(FoesTeam)

battle(YourTeam, FoesTeam, "Shiro", "Izuna")


