from typing import Union
from Data.data import *
import random as r
from Objects.color import color


class Move:
    def __init__(self, name: str, type: [str], category: int, pp: int, power: Union[int, None],
                 accuracy: Union[float, None], times=1):
        self.name = name
        self.type = type
        self.category = category
        """
        0: Physical
        1: status
        2: Status
        """
        self.pp = pp
        self.power = power
        self.accuracy = accuracy
        self.times = times

    def use(self, user, target):
        if self.category != 2 and self.power != None:

            try:
                hit = r.choices(population=[1, 0], weights=[self.accuracy, 1 - self.accuracy])[0]
            except:
                hit = 1

            if hit == 0:
                print(f"{data[target.id - 1]['name']['english']} avoided the attack!")
                return

            rand = r.randint(85, 100) / 100
            STAB = 1.5 if len(set(self.type) & set(user.type)) >= 1 else 1
            crit = r.randint(0, 16) == 1
            critical = 1.5 if crit else 1
            TypeMult = 1
            burned = 0.5 if user.status == 'Burned' else 1
            for type in target.type:
                if type in typeChart[self.type]["Strength"]:
                    TypeMult *= 2
                elif type in typeChart[self.type]["Weakness"]:
                    TypeMult /= 2
                elif type in typeChart[self.type]["NoEffect"]:
                    print(color.YELLOW + "its not effective" + color.END)
                    TypeMult = 0
                    break

            # Type strengths exceptions:
            if self.name == "Freeze-dry" and "Water" in [target.type]:
                TypeMult *= 2

            # End of exceptions

            if TypeMult > 1:
                print(color.YELLOW + "its very effective!" + color.END)
            elif TypeMult < 1 and TypeMult != 0:
                print(color.YELLOW + "its not very effective" + color.END)

            damage = hit * int((((2 * user.lvl / 5 + 2) * self.power * ((
                user.stats[1] if self.category == 0 else user.stats[3]) / (
                                     target.stats[2] if self.category == 0 else target.stats[
                                         4])) / 50) + 2) * rand * STAB * critical * TypeMult * burned)
            target.HP -= damage

            print(f"{data[target.id - 1]['name']['english']} got {damage} damage!")
            if crit:
                print(color.RED + "A critical hit!" + color.END)

            # Status dealing

            if self.name == "Tri Attack":
                if r.choices([1, 0], [1, 4])[0]:
                    status = r.choices(["Frozen", "Paralyzed", "Burned"], [1,1,1])[0]
                    target.status = status

            if self.name in ["Cross poison", "Gunk shot", "Poison gas", "Poison jab", "Poison powder", "Poison sting",
                             "Poison tail", "Shell side arm", "Sludge", "Sludge bomb", "Sludge wave", "Smog", "Toxic thread",
                             "Toxic"] and hit:
                if self.name in ["Poison gas", "Poison powder", "Toxic thread", "Toxic"]:
                    if self.name != 'Poison powder' or 'Grass' not in target.type:
                        target.getStatus("Poisoned")
                elif self.name in ["Cross poison", "Poison tail", "Sludge wave"]:
                    if r.choices([1, 0], [1, 9])[0]:
                        target.getStatus("Poisoned")
                elif self.name in ["Gunk shot", "Poison jab", "Poison sting", "Sludge bomb"]:
                    if r.choices([1, 0], [3, 7])[0]:
                        target.getStatus("Poisoned")
                elif self.name in ["Shell side arm"]:
                    if r.choices([1, 0], [2, 8])[0]:
                        target.getStatus("Poisoned")
                elif self.name in ["Smog"]:
                    if r.choices([1, 0], [4, 6])[0]:
                        target.getStatus("Poisoned")
                elif self.name in ["Toxic"]:
                    if r.choices([1, 0], [1, 1])[0]:
                        target.getStatus("Poisoned")


            if self.name in ["Body slam", "Bolt strike", "Bounce", "Buzzy buzz", "Discharge", "Dragon breath", "Force palm",
                             "Freeze shock", "Glare", "Lick", "Nuzzle", "Shadow bolt", "Spark", "Splishy splash", "Stun spore",
                             "Thunder", "Thunder fang", "Thunder punch", "Thunder shock", "Thunder wave", "Thunderbolt",
                             "Volt tackle", "Zap cannon"] and hit:
                if self.name in ["Buzzy buzz", "Glare", "Nuzzle", "Stun spore", "Thunder wave", "Zap cannon"]:
                    if self.name != 'Stun spore' or 'Grass' not in target.type:
                        target.getStatus("Paralyzed")
                elif self.name in ["Body slam", "Bounce", "Discharge", "Dragon breath", "Force palm", "Freeze shock",
                                   "Lick", "Spark", "Splishy splash", "Thunder"]:
                    if r.choices([1, 0], [3, 7])[0]:
                        target.getStatus("Paralyzed")
                elif self.name in ["Bolt strike"]:
                    if r.choices([1, 0], [1, 4])[0]:
                        target.getStatus("Paralyzed")
                elif self.name in ["Shadow bolt", "Thunder fang", "Thunder punch", "Thunder shock", "Thunderbolt"]:
                    if r.choices([1, 0], [1, 9])[0]:
                        target.getStatus("Paralyzed")

            if self.name in ["Blaze kick", "Blue flare", "Ember", "Fire blast",
                             "Fire fang", "Fire punch", "Flame wheel", "Flamethrower", "Flare blitz", "Heat wave",
                             "Ice burn", "Inferno", "Lava plume", "Pyro ball", "Sacred fire", "Scald", "Scorching sands",
                             "Searing shot", "Shadow fire", "Sizzly slide", "Steam eruption", "Will-o-wisp"] and hit:
                if self.name in ["Inferno", "Sizzly slide", "Will-o-wisp"]:
                    target.getStatus("Burned")
                elif self.name in ["Blaze kick", "Ember", "Fire blast",
                             "Fire fang", "Fire punch", "Flame wheel", "Flamethrower", "Flare blitz", "Heat wave",
                             "Pyro ball", "Shadow fire"]:
                    if r.choices([1, 0], [1, 9])[0]:
                        target.getStatus("Burned")
                elif self.name in ["Blue flare"]:
                    if r.choices([1, 0], [1, 4])[0]:
                        target.getStatus("Burned")
                elif self.name in ["Lava plume", "Scald", "Scorching sands", "Searing shot", "Steam eruption"]:
                    if r.choices([1, 0], [3, 7])[0]:
                        target.getStatus("Burned")
                elif self.name in ["Sacred fire"]:
                    if r.choices([1, 0], [1, 1])[0]:
                        target.getStatus("Burned")

            if self.name in ["Ice beam", "Blizzard", "Freeze-dry", "Freezing glare", "Ice fang", "Ice punch", "Powder snow", "Shadow chill"] and hit:
                if r.choices([1, 0], [1, 9])[0]:
                    target.getStatus("Frozen")

            if target.status == 'Frozen' and (self.type == 'Fire' or self.name == 'Scald' or self.name == 'Steam erruption'):
                print(color.BOLD + f"{data[target.id - 1]['name']['english']} thawed out!")
                target.status = ''

            # End of status dealing

            if target.HP <= 0:
                target.HP = 0
                target.status = "Fainted"
                print(color.RED + f"{data[target.id - 1]['name']['english']} fainted!" + color.END)

