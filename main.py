from Mechanics import *
from attacks import *

Venusaur = pokemon("Bulby", [RazorLeaf, LeafBlade, PetalDance, EnergyBall], 1, ["Grass", "Poison"], 3, 60, 3, "")
Pikachu = pokemon("Pikie", [Thunderbolt, Thunder, IronTail, QuickAttack], 1, ["Electric"], 25, 65, 2, "")
Charizard = pokemon("Charry", [Ember, FireFang, AerialAce, Earthquake], 1, ["Fire", "Flying"], 6, 55, 3, "")
Vaporion = pokemon("Vapy", [WaterGun, HydroPump, Surf, QuickAttack], 0, ["Water"], 134, 65, 2, "")

Pikachu.expGain(12500)

YourTeam = [Pikachu, Venusaur]
FoesTeam = [Charizard, Vaporion]

battle(YourTeam, FoesTeam, "Shiro", "Izuna")


