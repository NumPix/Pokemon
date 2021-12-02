import math as m
import json
from typing import Union

import numpy as np
import random as r

import time

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

data = json.loads(open('pokedata.json', 'r').read())

typeChart = {
    'Normal': {'Strength': [], 'Weakness': ['Rock', 'Steel'], 'NoEffect': ['Ghost']},
    'Fire': {'Strength': ['Grass', 'Steel', 'Ice', 'Bug'], 'Weakness': ['Fire', 'Water', 'Rock', 'Dragon'], 'NoEffect': []},
    'Water': {'Strength': ['Fire', 'Ground', 'Rock'], 'Weakness': ['Water', 'Grass', 'Dragon'], 'NoEffect': []},
    'Grass': {'Strength': ['Water', 'Ground', 'Rock'], 'Weakness': ['Fire', 'Grass', 'Dragon', 'Poison', 'Bug', 'Flying', 'Steel'], 'NoEffect': []},
    'Electric': {'Strength': ['Water', 'Flying'], 'Weakness': ['Electric', 'Grass', 'Dragon'], 'NoEffect': ['Ground']},
    'Ice': {'Strength': ['Grass', 'Ground', 'Flying', 'Dragon'], 'Weakness': ['Fire', 'Water', 'Ice', 'Steel'], 'NoEffect': []},
    'Fighting': {'Strength': ['Normal', 'Ice', 'Rock', 'Dark', 'Steel'], 'Weakness': ['Poison', 'Flying', 'Physical', 'Bug', 'Fairy'], 'NoEffect': ['Ghost']},
    'Poison': {'Strength': ['Grass', 'Fairy'], 'Weakness': ['Poison', 'Ground', 'Rock', 'Ghost'], 'NoEffect': ['Steel']},
    'Ground': {'Strength': ['Fire', 'Electric', 'Poison', 'Rock', 'Steel'], 'Weakness': ['Grass', 'Bug'], 'NoEffect': ['Flying']},
    'Flying': {'Strength': ['Grass', 'Fighting', 'Bug'], 'Weakness': ['Electric', 'Rock', 'Steel'], 'NoEffect': []},
    'Physic': {'Strength': ['Fighting', 'Poison'], 'Weakness': ['Physic', 'Steel'], 'NoEffect': ['Dark']},
    'Bug': {'Strength': ['Grass', 'Physic', 'Dark'], 'Weakness': ['Fire', 'Fighting', 'Poison', 'Flying', 'Ghost', 'Steel', 'Fairy'], 'NoEffect': []},
    'Rock': {'Strength': ['Fire', 'Ice', 'Flying', 'Bug'], 'Weakness': ['Fighting', 'Ground', 'Steel'], 'NoEffect': []},
    'Ghost': {'Strength': ['Physic', 'Ghost'], 'Weakness': ['Dark'], 'NoEffect': ['Normal']},
    'Dragon': {'Strength': ['Dragon'], 'Weakness': ['Steel'], 'NoEffect': ['Fairy']},
    'Dark': {'Strength': ['Physic', 'Ghost'], 'Weakness': ['Fighting', 'Dark', 'Fairy'], 'NoEffect': []},
    'Steel': {'Strength': ['Ice', 'Rock', 'Fairy'], 'Weakness': ['Fire', 'Water', 'Electric', 'Steel'], 'NoEffect': []},
    'Fairy': {'Strength': ['Fighting', 'Dragon', 'Dark'], 'Weakness': ['Poison', 'Steel'], 'NoEffect': []},
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

natureList = ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave',
              'Bold', 'Docile', 'Impish', 'Lax', 'Relaxed',
              'Modest', 'Mild', 'Bashful', 'Rash', 'Quiet',
              'Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy',
              'Timid', 'Hasty', 'Jolly', 'Naive', 'Serious']


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
            rand = r.randint(85, 100) / 100
            STAB = 1.5 if len(set(self.type) & set(user.type)) >= 1 else 1
            crit = r.randint(0, 64) == 1
            critical = 1.5 if crit else 1
            TypeMult = 1
            for type in target.type:
                if type in typeChart[self.type]['Strength']: TypeMult *= 2
                elif type in typeChart[self.type]['Weakness']: TypeMult /= 2
                elif type in typeChart[self.type]['NoEffect']:
                    print(color.YELLOW + 'its not effective' + color.END)
                    TypeMult = 0
                    break

            if TypeMult > 1: print(color.YELLOW + 'its very effective!' + color.END)
            elif TypeMult < 1: print(color.YELLOW + 'its not very effective' + color.END)

            damage = int((((2 * user.lvl / 5 + 2) * self.power * (user.stats[1] if self.category == 0 else user.stats[3]) / (target.stats[2] if self.category == 0 else target.stats[4]) / 50) + 2) * rand * STAB * critical * TypeMult)
            target.HP -= damage

            print(f'{data[target.id - 1]["name"]["english"]} get {damage} damage!')
            if crit:
                print(color.RED + 'A critical hit!' + color.END)
            if target.HP <= 0:
                target.HP = 0
                target.status = 'Fainted'
                print(color.RED + f'{data[target.id - 1]["name"]["english"]} fainted!' + color.END)

class pokemon:
    def __init__(self, name: str, moves: [str, str, str, str], gender: int, type: [str], id: int,
                 lvl: int, expType: int, item: str, status: str = ''):
        self.name = name
        self.gender = gender
        self.moves = moves
        self.pp = [move.pp for move in moves]
        self.nature = r.choice(natureList)
        self.natureStat = [1, 1, 1, 1, 1]

        self.natureStat[natureList.index(self.nature) % 5] -= 0.1
        self.natureStat[natureList.index(self.nature) // 5] += 0.1

        self.type = type
        """
        HP
        Attack
        Defence
        Sp.Attack
        Sp.Defence
        Speed
        """
        self.id = id
        self.lvl = lvl
        self.exp = [expFormulas[expType](lvl), expFormulas[expType](lvl + 1)]
        self.expType = expType
        self.item = item
        self.status = status

        self.iv = [r.randint(0, 31), r.randint(0, 31), r.randint(0, 31)]
        self.ev = [0, 0, 0, 0, 0, 0]

        self.baseStats = np.array(list(data[self.id - 1]['base'].values()))

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

    def attack(self, moveId, target):
        if self.pp[moveId] != 0:
            self.moves[moveId].use(self, target)
        self.pp[moveId] -= 1

def battle(YourTeam, FoesTeam, You, Foe):

    turn = False
    yNow = YourTeam[0]
    fNow = FoesTeam[0]
    print(f'{You} send out {yNow.name}!')
    print(f'{Foe} send out {fNow.name}!\n')
    yHpCol = [color.GREEN, color.END]
    fHpCol = [color.GREEN, color.END]
    """
    True - You
    False - Foe
    """

    def yAttack(fNow, yNow, yHpCol, fHpCol):
        print(f'{yNow.name} used {color.BOLD}{chMove.name}{color.END}!')
        yNow.attack(yNow.moves.index(chMove), fNow)
        if fNow.status == 'Fainted':
            try:
                fNow = r.choice(list(filter(lambda x: x.status != 'Fainted', FoesTeam)))
                print(f'{Foe} send out {fNow.name}!')
            except IndexError:
                pass

        if yNow.HP / yNow.stats[0] > 0.5:
            yHpCol = [color.GREEN, color.END]
        if yNow.HP / yNow.stats[0] <= 0.5:
            yHpCol = [color.YELLOW, color.END]
        if yNow.HP / yNow.stats[0] <= 0.25:
            yHpCol = [color.RED, color.END]

        if fNow.HP / fNow.stats[0] > 0.5:
            fHpCol = [color.GREEN, color.END]
        if fNow.HP / fNow.stats[0] <= 0.5:
            fHpCol = [color.YELLOW, color.END]
        if fNow.HP / fNow.stats[0] <= 0.25:
            fHpCol = [color.RED, color.END]

        print(
            f'\n{data[yNow.id - 1]["name"]["english"]} {yHpCol[0]}[{"█" * round(yNow.HP / yNow.stats[0] / 0.05) + "░" * (20 - round(yNow.HP / yNow.stats[0] / 0.05))}]{yHpCol[1]} {yNow.HP}/{yNow.stats[0]}')
        print(
            f'{data[fNow.id - 1]["name"]["english"]} {fHpCol[0]}[{"█" * round(fNow.HP / fNow.stats[0] / 0.05) + "░" * (20 - round(fNow.HP / fNow.stats[0] / 0.05))}]{fHpCol[1]} {fNow.HP}/{fNow.stats[0]}')
        print('\n==========================================\n')

        return fNow, yNow, yHpCol, fHpCol

    def fAttack(fNow, yNow, yHpCol, fHpCol):
        chMove = r.randint(0, len(fNow.moves) - 1)
        print(f'{fNow.name} used {color.BOLD}{fNow.moves[chMove].name}{color.END}!')
        fNow.attack(chMove, yNow)


        if yNow.HP / yNow.stats[0] > 0.5:
            yHpCol = [color.GREEN, color.END]
        if yNow.HP / yNow.stats[0] <= 0.5:
            yHpCol = [color.YELLOW, color.END]
        if yNow.HP / yNow.stats[0] <= 0.25:
            yHpCol = [color.RED, color.END]

        if fNow.HP / fNow.stats[0] > 0.5:
            fHpCol = [color.GREEN, color.END]
        if fNow.HP / fNow.stats[0] <= 0.5:
            fHpCol = [color.YELLOW, color.END]
        if fNow.HP / fNow.stats[0] <= 0.25:
            fHpCol = [color.RED, color.END]

        print(
            f'\n{data[yNow.id - 1]["name"]["english"]} {yHpCol[0]}[{"█" * round(yNow.HP / yNow.stats[0] / 0.05) + "░" * (20 - round(yNow.HP / yNow.stats[0] / 0.05))}]{yHpCol[1]} {yNow.HP}/{yNow.stats[0]}')
        print(
            f'{data[fNow.id - 1]["name"]["english"]} {fHpCol[0]}[{"█" * round(fNow.HP / fNow.stats[0] / 0.05) + "░" * (20 - round(fNow.HP / fNow.stats[0] / 0.05))}]{fHpCol[1]} {fNow.HP}/{fNow.stats[0]}')
        print('\n==========================================\n')

        return fNow, yNow, yHpCol, fHpCol

    print(f'{data[yNow.id - 1]["name"]["english"]} {yHpCol[0]}[{"█" * round(yNow.HP / yNow.stats[0] / 0.05) + "░" * (20 - round(yNow.HP / yNow.stats[0] / 0.05))}]{yHpCol[1]} {yNow.HP}/{yNow.stats[0]}')
    print(f'{data[fNow.id - 1]["name"]["english"]} {fHpCol[0]}[{"█" * round(fNow.HP / fNow.stats[0] / 0.05) + "░" * (20 - round(fNow.HP / fNow.stats[0] / 0.05))}]{fHpCol[1]} {fNow.HP}/{fNow.stats[0]}\n')

    while list(filter(lambda x: x.status != 'Fainted', YourTeam)) and list(filter(lambda x: x.status != 'Fainted', FoesTeam)):
        turn = not turn
        time.sleep(1)
        if turn:
            print(*list(map(lambda x: '•' + x.name + f" [{yNow.pp[yNow.moves.index(x)]}/{x.pp}]", yNow.moves)),
                  sep='\n',
                  end='\n\n')
            chMove = input().capitalize()
            while chMove not in list(map(lambda x: x.name, yNow.moves)):
                print(*list(map(lambda x: '•' + x.name + f" [{yNow.pp[yNow.moves.index(x)]}/{x.pp}]", yNow.moves)),
                      sep='\n')
                chMove = input().capitalize()
            chMove = list(filter(lambda x: x.name == chMove, yNow.moves))[0]
            tchMove = chMove
            if yNow.stats[5] >= fNow.stats[5]:
                fNow, yNow, yHpCol, fHpCol = yAttack(fNow, yNow, yHpCol, fHpCol)
            else:
                print('\n==========================================\n')
                fNow, yNow, yHpCol, fHpCol = fAttack(fNow, yNow, yHpCol, fHpCol)
                if yNow.status == 'Fainted':
                    try:
                        yNow = list(filter(lambda x: x.status != 'Fainted', YourTeam))[0]
                    except:
                        break
                    print(f'{You} send out {yNow.name}!')
                    turn = not turn
                    continue
                chMove = tchMove
                time.sleep(1)
                fNow, yNow, yHpCol, fHpCol = yAttack(fNow, yNow, yHpCol, fHpCol)
                turn = not turn
        else:
            fNow, yNow, yHpCol, fHpCol = fAttack(fNow, yNow, yHpCol, fHpCol)
            if yNow.status == 'Fainted':
                try:
                    yNow = list(filter(lambda x: x.status != 'Fainted', YourTeam))[0]
                except:
                    break
                print(f'{You} send out {yNow.name}!\n')
                continue

    if list(filter(lambda x: x.status != 'Fainted', YourTeam)):
        print('You Won!')
    else:
        print('You Lost!')