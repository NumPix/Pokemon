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
            for type in target.type:
                if type in typeChart[self.type]["Strength"]:
                    TypeMult *= 2
                elif type in typeChart[self.type]["Weakness"]:
                    TypeMult /= 2
                elif type in typeChart[self.type]["NoEffect"]:
                    print(color.YELLOW + "its not effective" + color.END)
                    TypeMult = 0
                    break

            if TypeMult > 1:
                print(color.YELLOW + "its very effective!" + color.END)
            elif TypeMult < 1 and TypeMult != 0:
                print(color.YELLOW + "its not very effective" + color.END)

            damage = hit * int((((2 * user.lvl / 5 + 2) * self.power * (
                user.stats[1] if self.category == 0 else user.stats[3]) / (
                                     target.stats[2] if self.category == 0 else target.stats[
                                         4]) / 50) + 2) * rand * STAB * critical * TypeMult)
            target.HP -= damage

            print(f"{data[target.id - 1]['name']['english']} got {damage} damage!")
            if crit:
                print(color.RED + "A critical hit!" + color.END)
            if target.HP <= 0:
                target.HP = 0
                target.status = "Fainted"
                print(color.RED + f"{data[target.id - 1]['name']['english']} fainted!" + color.END)
