import math as m
import json
from typing import Union

import numpy as np
import random as r

import time

class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

data = json.loads(open("pokedata.json", "r").read())
baseXp = json.loads(open("baseXp.json", "r").read())

typeChart = {
    "Normal": {"Strength": [], "Weakness": ["Rock", "Steel"], "NoEffect": ["Ghost"]},
    "Fire": {"Strength": ["Grass", "Steel", "Ice", "Bug"], "Weakness": ["Fire", "Water", "Rock", "Dragon"], "NoEffect": []},
    "Water": {"Strength": ["Fire", "Ground", "Rock"], "Weakness": ["Water", "Grass", "Dragon"], "NoEffect": []},
    "Grass": {"Strength": ["Water", "Ground", "Rock"], "Weakness": ["Fire", "Grass", "Dragon", "Poison", "Bug", "Flying", "Steel"], "NoEffect": []},
    "Electric": {"Strength": ["Water", "Flying"], "Weakness": ["Electric", "Grass", "Dragon"], "NoEffect": ["Ground"]},
    "Ice": {"Strength": ["Grass", "Ground", "Flying", "Dragon"], "Weakness": ["Fire", "Water", "Ice", "Steel"], "NoEffect": []},
    "Fighting": {"Strength": ["Normal", "Ice", "Rock", "Dark", "Steel"], "Weakness": ["Poison", "Flying", "Physical", "Bug", "Fairy"], "NoEffect": ["Ghost"]},
    "Poison": {"Strength": ["Grass", "Fairy"], "Weakness": ["Poison", "Ground", "Rock", "Ghost"], "NoEffect": ["Steel"]},
    "Ground": {"Strength": ["Fire", "Electric", "Poison", "Rock", "Steel"], "Weakness": ["Grass", "Bug"], "NoEffect": ["Flying"]},
    "Flying": {"Strength": ["Grass", "Fighting", "Bug"], "Weakness": ["Electric", "Rock", "Steel"], "NoEffect": []},
    "Psychic": {"Strength": ["Fighting", "Poison"], "Weakness": ["Psychic", "Steel"], "NoEffect": ["Dark"]},
    "Bug": {"Strength": ["Grass", "Psychic", "Dark"], "Weakness": ["Fire", "Fighting", "Poison", "Flying", "Ghost", "Steel", "Fairy"], "NoEffect": []},
    "Rock": {"Strength": ["Fire", "Ice", "Flying", "Bug"], "Weakness": ["Fighting", "Ground", "Steel"], "NoEffect": []},
    "Ghost": {"Strength": ["Psychic", "Ghost"], "Weakness": ["Dark"], "NoEffect": ["Normal"]},
    "Dragon": {"Strength": ["Dragon"], "Weakness": ["Steel"], "NoEffect": ["Fairy"]},
    "Dark": {"Strength": ["Psychic", "Ghost"], "Weakness": ["Fighting", "Dark", "Fairy"], "NoEffect": []},
    "Steel": {"Strength": ["Ice", "Rock", "Fairy"], "Weakness": ["Fire", "Water", "Electric", "Steel"], "NoEffect": []},
    "Fairy": {"Strength": ["Fighting", "Dragon", "Dark"], "Weakness": ["Poison", "Steel"], "NoEffect": []},
}

expFormulas = [
    lambda n: (n ** 3) * (100 - n) // 50 if n < 50
    else (n ** 3) * (150 - n) // 100 if n < 68
    else (n ** 3) * m.floor((1911 - 10 * n) / 3) // 500 if n < 98
    else (n ** 3) * (160 - n) // 100,

    lambda n: 4 * (n ** 3) // 5,

    lambda n: n ** 3,

    lambda n: round(6 / 5 * (n ** 3) - 15 * (n ** 2) + 100 * n - 140),

    lambda n: 5 * (n ** 3) // 4,

    lambda n: round((n ** 3) * ((m.floor((n + 1) / 3) + 24) / 50)) if n < 15
    else (n ** 3) * (n + 14) // 50 if n < 36
    else (n ** 3) * (m.floor(n / 2) + 32) // 50
]

# Exp Gain Type indexes
"""
0 - Erratic
1 - Fast
2 - Medium Fast
3 - Medium Slow
4 - Slow
5 - Fluctuating
"""

natureList = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
              "Bold", "Docile", "Impish", "Lax", "Relaxed",
              "Modest", "Mild", "Bashful", "Rash", "Quiet",
              "Calm", "Gentle", "Careful", "Quirky", "Sassy",
              "Timid", "Hasty", "Jolly", "Naive", "Serious"]


class move:
    def __init__(self, name: str, type: [str], category: int, pp: int, power: Union[int, None], accuracy: Union[float, None], times=1):
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
                if type in typeChart[self.type]["Strength"]: TypeMult *= 2
                elif type in typeChart[self.type]["Weakness"]: TypeMult /= 2
                elif type in typeChart[self.type]["NoEffect"]:
                    print(color.YELLOW + "its not effective" + color.END)
                    TypeMult = 0
                    break

            if TypeMult > 1: print(color.YELLOW + "its very effective!" + color.END)
            elif TypeMult < 1 and TypeMult != 0: print(color.YELLOW + "its not very effective" + color.END)

            damage = hit * int((((2 * user.lvl / 5 + 2) * self.power * (user.stats[1] if self.category == 0 else user.stats[3]) / (target.stats[2] if self.category == 0 else target.stats[4]) / 50) + 2) * rand * STAB * critical * TypeMult)
            target.HP -= damage

            print(f"{data[target.id - 1]['name']['english']} got {damage} damage!")
            if crit:
                print(color.RED + "A critical hit!" + color.END)
            if target.HP <= 0:
                target.HP = 0
                target.status = "Fainted"
                print(color.RED + f"{data[target.id - 1]['name']['english']} fainted!" + color.END)

class pokemon:
    def __init__(self, name: str, moves: [str, str, str, str], gender: int, id: int,
                 lvl: int, expType: int, item: str, status: str = ""):
        self.name = name
        self.gender = gender
        self.moves = moves
        self.pp = [move.pp for move in moves]
        self.nature = r.choice(natureList)
        self.natureStat = [1, 1, 1, 1, 1]

        self.natureStat[natureList.index(self.nature) % 5] -= 0.1
        self.natureStat[natureList.index(self.nature) // 5] += 0.1

        """
        HP
        Attack
        Defence
        Sp.Attack
        Sp.Defence
        Speed
        """
        self.id = id

        self.type = data[id - 1]['type']

        self.lvl = lvl
        self.exp = [expFormulas[expType](lvl), expFormulas[expType](lvl + 1)]
        self.expType = expType
        self.item = item
        self.status = status

        self.iv = [r.randint(0, 31), r.randint(0, 31), r.randint(0, 31)]
        self.ev = [0, 0, 0, 0, 0, 0]

        self.baseStats = np.array(list(data[self.id - 1]["base"].values()))

        self.stats = np.array([m.floor(
            0.01 * (2 * self.baseStats[0] + self.iv[0] + m.floor(0.25 * self.ev[0])) * self.lvl) + self.lvl + 5,

                               m.floor((
                                               0.01 * ((2 * self.baseStats[1] + self.iv[1] + m.floor(
                                           0.25 * self.ev[1])) * self.lvl) + 5) * self.natureStat[0]),

                               m.floor((
                                               0.01 * ((2 * self.baseStats[2] + self.iv[1] + m.floor(
                                           0.25 * self.ev[2])) * self.lvl) + 5) * self.natureStat[1]),

                               m.floor((
                                               0.01 * ((2 * self.baseStats[3] + self.iv[1] + m.floor(
                                           0.25 * self.ev[3])) * self.lvl) + 5) * self.natureStat[2]),

                               m.floor((
                                               0.01 * ((2 * self.baseStats[4] + self.iv[2] + m.floor(
                                           0.25 * self.ev[4])) * self.lvl) + 5) * self.natureStat[3]),

                               m.floor((
                                               0.01 * ((2 * self.baseStats[5] + self.iv[1] + m.floor(
                                           0.25 * self.ev[5])) * self.lvl) + 5) * self.natureStat[4]),
                               ])
        self.HP = self.stats[0]


    def expGain(self, num: int):
        temp = self.lvl
        if num < self.exp[1] - self.exp[0]:
            self.exp[0] += num
        else:
            tempExp = self.exp[1] - self.exp[0]
            self.lvl += 1
            self.exp = [expFormulas[self.expType](self.lvl), expFormulas[self.expType](self.lvl + 1)]
            tempStats = self.stats.copy()
            self.stats = np.array([m.floor(
                0.01 * (2 * self.baseStats[0] + self.iv[0] + m.floor(0.25 * self.ev[0])) * self.lvl) + self.lvl + 5,

                          m.floor((
                                          0.01 * ((2 * self.baseStats[1] + self.iv[1] + m.floor(
                                      0.25 * self.ev[1])) * self.lvl) + 5) * self.natureStat[0]),

                          m.floor((
                                          0.01 * ((2 * self.baseStats[2] + self.iv[1] + m.floor(
                                      0.25 * self.ev[2])) * self.lvl) + 5) * self.natureStat[1]),

                          m.floor((
                                          0.01 * ((2 * self.baseStats[3] + self.iv[1] + m.floor(
                                      0.25 * self.ev[3])) * self.lvl) + 5) * self.natureStat[2]),

                          m.floor((
                                          0.01 * ((2 * self.baseStats[4] + self.iv[2] + m.floor(
                                      0.25 * self.ev[4])) * self.lvl) + 5) * self.natureStat[3]),

                          m.floor((
                                          0.01 * ((2 * self.baseStats[5] + self.iv[1] + m.floor(
                                      0.25 * self.ev[5])) * self.lvl) + 5) * self.natureStat[4]),
                          ])

            deltaStats = self.stats - tempStats

            self.HP += deltaStats[0]

            self.expGain(num - tempExp)
            if temp < self.lvl:
                print(color.BOLD + f'{self.name} grew to lvl {self.lvl}!' + color.END)
                print('\nHP: \t\t+{0} -> {6}\nAttack: \t+{1} -> {7}\nDefence: \t+{2} -> {8}\nSp.Attack: \t+{3} -> {9}\nSp.Defence: +{4} -> {10}\nSpeed: \t\t+{5} -> {11}'.format(*deltaStats, *self.stats))

    def expCalc(self, target, pokemonUsed) -> int:
        return int(1.5 * target.lvl * int(baseXp[data[target.id]['name']['english']]) / 5 / pokemonUsed * (((2 * target.lvl + 10) / (target.lvl + self.lvl + 10)) ** 2.5))

    def attack(self, moveId, target):
        if self.pp[moveId] != 0:
            self.moves[moveId].use(self, target)
        self.pp[moveId] -= 1

def printHP(target: pokemon):
    if target.HP / target.stats[0] > 0.5:
        HpCol = [color.GREEN, color.END]
    if target.HP / target.stats[0] <= 0.5:
        HpCol = [color.YELLOW, color.END]
    if target.HP / target.stats[0] <= 0.25:
        HpCol = [color.RED, color.END]
    print(f"{data[target.id - 1]['name']['english']} {target.lvl} lv. {HpCol[0]}[{'█' * round(target.HP / target.stats[0] / 0.05) + '░' * (20 - round(target.HP / target.stats[0] / 0.05))}]{HpCol[1]} {target.HP}/{target.stats[0]}")

def printMove(target: pokemon, Move: move):
    if target.pp[target.moves.index(Move)] / Move.pp >= 0.5:
        moveCol = [color.END, color.END]
    elif target.pp[target.moves.index(Move)] / Move.pp >= 0.25:
        moveCol = [color.YELLOW, color.END]
    else:
        moveCol = [color.RED, color.END]

    print(moveCol[0] + "•" + Move.name + f" [{target.pp[target.moves.index(Move)]}/{Move.pp}]" + moveCol[1])



def battle(YourTeam, FoesTeam, You, Foe):

    yTempStats = list(map(lambda x: x.stats, YourTeam))
    fTempStats = list(map(lambda x: x.stats, FoesTeam))

    turn = False
    yNow = YourTeam[0]
    fNow = FoesTeam[0]
    print(f"{You} send out {yNow.name}!")
    print(f"{Foe} send out {fNow.name}!\n")
    """
    True - You
    False - Foe
    """
    dU = {yNow}

    def yCheckFaint():
        time.sleep(1)
        print('------------------------------------------')
        for poke in YourTeam: printHP(poke)
        print('------------------------------------------\n')
        print(color.BOLD + 'Choose your next Pokemon!\n' + color.END)
        chPoke = input().capitalize()
        while chPoke not in list(
                map(lambda x: data[x.id - 1]['name']['english'], filter(lambda x: x.status != 'Fainted', YourTeam))):
            print('------------------------------------------')
            for poke in YourTeam: printHP(poke)
            print('------------------------------------------\n')
            chPoke = input().capitalize()
        chPoke = YourTeam.index(list(filter(lambda x: data[x.id - 1]['name']['english'] == chPoke, YourTeam))[0])
        yNow = YourTeam[chPoke]
        return yNow

    def yAttack(fNow, yNow, turn, dU):
        print(f"{yNow.name} used {color.BOLD}{chMove.name}{color.END}!")
        yNow.attack(yNow.moves.index(chMove), fNow)
        if fNow.status == "Fainted":
            time.sleep(1)
            for poke in filter(lambda x: x.status != 'Fainted', dU):
                print('\n------------------------------------------')
                print(f'{poke.name} got {poke.expCalc(poke, len(dU))} xp!')
                poke.expGain(poke.expCalc(poke, len(dU)))
                print('------------------------------------------\n')
                time.sleep(1)
            dU = {yNow}
            try:
                fNow = r.choice(list(filter(lambda x: x.status != "Fainted", FoesTeam)))

                print(color.BOLD + f"{Foe} is going to send out {data[fNow.id - 1]['name']['english']}!" + color.END)
                print("Do you want to switch pokemon (Y/n)?")
                switch = False
                ch = input().lower()
                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input()
                if ch in ['n', 'no', '']: pass
                else:
                    switch = True
                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print('------------------------------------------')
                    for poke in YourTeam: printHP(poke)
                    print('------------------------------------------\n')
                    chPoke = input().capitalize()
                    back = False
                    while chPoke not in list(map(lambda x: data[x.id - 1]['name']['english'],
                                                 filter(lambda x: x.status != 'Fainted', YourTeam))):
                        if chPoke == '':
                            back = True
                            break
                        print('------------------------------------------')
                        for poke in YourTeam: printHP(poke)
                        print('------------------------------------------\n')
                        chPoke = input().capitalize()
                    if not back:
                        chPoke = YourTeam.index(
                            list(filter(lambda x: data[x.id - 1]['name']['english'] == chPoke, YourTeam))[0])
                        yNow = YourTeam[chPoke]
                    else:
                        switch = False

                print(f"{Foe} send out {fNow.name}!")
                if switch:
                    print(f"{You} send out {yNow.name}!")
                turn = False
            except IndexError:
                pass

        print('\n' + '● ' * len(list(filter(lambda x: x.status != 'Fainted',YourTeam))) + '○ '* (6 - len(list(filter(lambda x: x.status != 'Fainted',YourTeam)))))
        printHP(yNow)
        printHP(fNow)
        print('● ' * len(list(filter(lambda x: x.status != 'Fainted',FoesTeam))) + '○ '* (6 - len(list(filter(lambda x: x.status != 'Fainted',FoesTeam)))))
        print("\n==========================================\n")

        return fNow, yNow, turn, dU

    def fAttack(fNow, yNow, turn):
        chMove = r.randint(0, len(fNow.moves) - 1)
        print(f"{fNow.name} used {color.BOLD}{fNow.moves[chMove].name}{color.END}!")
        fNow.attack(chMove, yNow)

        print('\n' + '● ' * len(list(filter(lambda x: x.status != 'Fainted', YourTeam))) + '○ ' * (
                    6 - len(list(filter(lambda x: x.status != 'Fainted', YourTeam)))))
        printHP(yNow)
        printHP(fNow)
        print('● ' * len(list(filter(lambda x: x.status != 'Fainted', FoesTeam))) + '○ ' * (
                    6 - len(list(filter(lambda x: x.status != 'Fainted', FoesTeam)))))
        print("\n==========================================\n")

        return fNow, yNow, turn

    print('\n' + '● ' * len(list(filter(lambda x: x.status != 'Fainted', YourTeam))) + '○ ' * (
                6 - len(list(filter(lambda x: x.status != 'Fainted', YourTeam)))))
    printHP(yNow)
    printHP(fNow)
    print('● ' * len(list(filter(lambda x: x.status != 'Fainted', FoesTeam))) + '○ ' * (
                6 - len(list(filter(lambda x: x.status != 'Fainted', FoesTeam)))))
    print("\n==========================================\n")

    while list(filter(lambda x: x.status != "Fainted", YourTeam)) and list(filter(lambda x: x.status != "Fainted", FoesTeam)):
        turn = not turn
        if turn:
            print(*["•Attack", "•Pokemon"], sep = "\n", end="\n\n")
            opt = input().capitalize()
            while opt not in ["Attack", "Pokemon"]:
                print(*["•Attack", "•Pokemon"], sep="\n", end="\n\n")
                opt = input().capitalize()
            if opt == "Attack":
                print('------------------------------------------')
                for mv in yNow.moves: printMove(yNow, mv)
                print('------------------------------------------\n')
                chMove = input().capitalize()
                back = False
                while chMove not in list(map(lambda x: x.name, filter(lambda x: yNow.pp[yNow.moves.index(x)] > 0, yNow.moves))):
                    if chMove == '':
                        back = True
                        break
                    for mv in yNow.moves: printMove(yNow, mv)
                    chMove = input().capitalize()
                if back:
                    turn = False
                    continue
                chMove = list(filter(lambda x: x.name == chMove, yNow.moves))[0]
                tchMove = chMove
                if yNow.stats[5] >= fNow.stats[5]:
                    fNow, yNow, turn, dU = yAttack(fNow, yNow, turn, dU)
                    if not turn:
                        continue
                else:
                    print("\n==========================================\n")
                    fNow, yNow, turn = fAttack(fNow, yNow, turn)
                    if yNow.status == "Fainted":
                        try:
                            yNow = yCheckFaint()
                        except:
                            break
                        dU.add(yNow)
                        print(f"\n{You} send out {yNow.name}!")
                        turn = False
                        continue
                    chMove = tchMove
                    time.sleep(1)
                    fNow, yNow, turn, dU = yAttack(fNow, yNow, turn, dU)
                    if not turn:
                        continue
                    turn = not turn
            elif opt == "Pokemon":
                print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                print('------------------------------------------')
                for poke in YourTeam: printHP(poke)
                print('------------------------------------------\n')
                chPoke = input().capitalize()
                back = False
                while chPoke not in list(map(lambda x: data[x.id - 1]['name']['english'], filter(lambda x: x.status != 'Fainted', YourTeam))):
                    if chPoke == '':
                        back = True
                        break
                    print('------------------------------------------')
                    for poke in YourTeam: printHP(poke)
                    print('------------------------------------------\n')
                    chPoke = input().capitalize()
                if back:
                    turn = False
                    continue
                chPoke = YourTeam.index(
                    list(filter(lambda x: data[x.id - 1]['name']['english'] == chPoke, YourTeam))[0])
                yNow = YourTeam[chPoke]
                print(f'{You} send out {yNow.name}!')
        else:
            fNow, yNow, turn = fAttack(fNow, yNow, turn)
            if yNow.status == "Fainted":
                try:
                    yNow = yCheckFaint()
                except:
                    break
                dU.add(yNow)
                print(f"\n{You} send out {yNow.name}!\n")
                turn = False
                continue

    if list(filter(lambda x: x.status != "Fainted", YourTeam)):
        print("You Won!")
    else:
        print("You Lost!")

    for i in range(len(YourTeam)):
        YourTeam[i].stats = yTempStats[i]
    for i in range(len(FoesTeam)):
        FoesTeam[i].stats = fTempStats[i]