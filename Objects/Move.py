from typing import Union
import random as rd

import Data.data
from Data.data import *
from Objects.color import color


class Move:
    def __init__(self, name: str, type: [str], category: int, pp: int, power: Union[int, None],
                 accuracy: Union[float, None], times=1):
        self.name = name
        self.type = type
        self.category = category
        """
        0: Physical
        1: Special
        2: Status
        """
        self.pp = pp
        self.power = power
        self.accuracy = accuracy
        self.times = times

    def use(self, user, target):
        if self.category != 2 and self.power is not None:

            try:
                hit = rd.choices(population=[1, 0], weights=[self.accuracy, 1 - self.accuracy])[0]
            except:
                hit = 1

            if hit == 0:
                print(f"{data[target.id - 1]['name']['english']} avoided the attack!")
                return

            rand = rd.randint(85, 100) / 100
            stab = 1.5 if len(set(self.type) & set(user.type)) >= 1 else 1
            crit = rd.randint(0, 16) == 1
            critical = 1.5 if crit else 1
            type_mult = 1
            burned = 0.5 if user.status == 'Burned' and self.category == 0 else 1
            for type in target.type:
                if type in typeChart[self.type]["Strength"]:
                    type_mult *= 2
                elif type in typeChart[self.type]["Weakness"]:
                    type_mult /= 2
                elif type in typeChart[self.type]["NoEffect"]:
                    print(color.YELLOW + "its not effective" + color.END)
                    type_mult = 0
                    break

            # Type strengths exceptions:
            if self.name == "Freeze-dry" and "Water" in [target.type]:
                type_mult *= 2

            # End of exceptions

            if type_mult > 1:
                print(color.YELLOW + "its very effective!" + color.END)
            elif type_mult < 1 and type_mult != 0:
                print(color.YELLOW + "its not very effective" + color.END)

            damage = hit * int((((2 * user.lvl / 5 + 2) * self.power * ((
                user.stats[1] if self.category == 0 else user.stats[3]) / (
                                     target.stats[2] if self.category == 0 else target.stats[
                                         4])) / 50) + 2) * rand * stab * critical * type_mult * burned)
            target.HP -= damage

            print(f"{data[target.id - 1]['name']['english']} got {damage} damage!")
            if crit:
                print(color.RED + "A critical hit!" + color.END)

            # Status dealing

            if self.name == "Tri Attack":
                if rd.choices([1, 0], [1, 4])[0]:
                    status = rd.choices(["Frozen", "Paralyzed", "Burned"], [1, 1, 1])[0]
                    target.status = status

            if self.name in Data.data.poison_inflict_chances and hit:
                if rd.choices([1, 0], Data.data.poison_inflict_chances[self.name])[0]:
                    target.getStatus("Poisoned")

            if self.name in Data.data.paralysis_inflict_chances and hit and "Electric" not in target.type:
                if rd.choices([1, 0], Data.data.paralysis_inflict_chances[self.name])[0]:
                    target.getStatus("Paralyzed")

            if self.name in Data.data.burn_inflict_chances and hit and "Fire" not in target.type:
                if rd.choices([1, 0], Data.data.paralysis_inflict_chances[self.name])[0]:
                    target.getStatus("Burned")

            if self.name in ["Ice beam", "Blizzard", "Freeze-dry", "Freezing glare", "Ice fang", "Ice punch", "Powder snow", "Shadow chill"] and hit:
                if rd.choices([1, 0], [1, 9])[0]:
                    target.getStatus("Frozen")

            if target.status == 'Frozen' and (self.type == 'Fire' or self.name == 'Scald' or self.name == 'Steam erruption'):
                print(color.BOLD + f"{data[target.id - 1]['name']['english']} thawed out!")
                target.status = ''

            # End of status dealing

            if target.HP <= 0:
                target.HP = 0
                target.status = "Fainted"
                print(color.RED + f"{data[target.id - 1]['name']['english']} fainted!" + color.END)

