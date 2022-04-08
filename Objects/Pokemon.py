from Objects.Item import Item
from Objects.color import color
from Data.data import *
import json
import numpy as np
import random as r

expTypes = json.loads(open("Data/Json/expType.json", 'r').read())


class Pokemon:
    def __init__(self, name: str, moves: [str, str, str, str], gender: int, id: int,
                 lvl: int = 1, item: Item = None, status: str = ''):
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
        self.expType = ['Erratic','Fast','Medium Fast','Medium Slow','Slow','Fluctuating'].index(expTypes[str(self.id)])
        self.exp = [expFormulas[self.expType](lvl), expFormulas[self.expType](lvl + 1)]
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

    def expGain(self, num: int, prt: bool = True):
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

            self.expGain(num - tempExp, prt)
            if temp < self.lvl and prt:
                print(color.BOLD + f'{self.name} grew to lvl {self.lvl}!' + color.END)
                print(
                    '\nHP: \t\t+{0} -> {6}\nAttack: \t+{1} -> {7}\nDefence: \t+{2} -> {8}\nSp.Attack: \t+{3} -> {9}\nSp.Defence: +{4} -> {10}\nSpeed: \t\t+{5} -> {11}'.format(
                        *deltaStats, *self.stats))

    def expCalc(self, target, pokemonUsed) -> int:
        return int(1.5 * target.lvl * int(baseXp[data[target.id - 1]['name']['english']]) / 5 / pokemonUsed * (
                    ((2 * target.lvl + 10) / (target.lvl + self.lvl + 10)) ** 2.5))

    def attack(self, moveId, target):
        if self.pp[moveId] != 0:
            self.moves[moveId].use(self, target)
        self.pp[moveId] -= 1

    def changeStats(self, statId, value):
        self.stats[statId] += value

    def getStatus(self, status):
        if 'Fire' in self.type and status == 'Burned':
            return
        if 'Ice' in self.type and status == 'Frozen':
            return
        if 'Electric' in self.type and status == 'Paralyzed':
            return
        if 'Steel' in self.type and status == 'Poisoned':
            return
        if self.status == '':
            self.status = status
            if self.status in ['Poisoned', 'Burned', 'Paralyzed']:
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} is {self.status}!\n" + color.END)
                if self.status == 'Paralyzed':
                    self.stats[5] *= 0.5
            if self.status == 'Frozen':
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} is frozen solid!\n" + color.END)
            if self.status == 'Sleeping':
                print(color.BOLD + f"\n{data[self.id - 1]['name']['english']} felt asleep!\n" + color.END)