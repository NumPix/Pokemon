import json
import math as m

data = json.loads(open("Data/Json/pokedata.json", "r").read())
baseXp = json.loads(open("Data/Json/baseXp.json", "r").read())
itemsData = json.loads(open("Data/Json/items.json", "r").read())

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

healing_amount = {
    'Potion': 20,
    'Super potion': 50,
    'Hyper potion': 200,
    'Max potion': 1000,
    'Fresh water': 30,
    'Soda pop': 50,
    'Lemonade': 70,
    'Moomoo milk': 100,
    'Full restore': 1000
}

natureList = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
              "Bold", "Docile", "Impish", "Lax", "Relaxed",
              "Modest", "Mild", "Bashful", "Rash", "Quiet",
              "Calm", "Gentle", "Careful", "Quirky", "Sassy",
              "Timid", "Hasty", "Jolly", "Naive", "Serious"]

healing = ['Potion', 'Super potion', 'Hyper potion', 'Max potion', 'Fresh water', 'Soda pop', 'Lemonade', 'Moomoo milk', 'Full restore']
pp_restore = ['Ether', 'Max ether', 'Elixir', 'Max elixir']
frozen_heal = ['Full heal', 'Full restore', 'Ice heal', 'Pumkin berry', 'Aspear berry', 'Lava cookie', 'Heal powder', 'Lum berry']
burn_heal = ['Burn heal', 'Rawst berry', 'Full heal', 'Lava cookie', 'Full restore', 'Heal powder', 'Lum berry']
paralysis_heal = ['Paralyze heal', 'Cheri berry', 'Full heal', 'Lava cookie', 'Full restore', 'Heal powder', 'Lum berry']
poison_heal = ['Antidote', 'Pecha berry', 'Full heal', 'Lava cookie', 'Full restore', 'Heal powder', 'Lum berry']

poison_inflict_chances = {
    "Cross poison": [1, 9],     # 10%
    "Poison tail": [1, 9],      # 10%
    "Sludge wave": [1, 9],      # 10%
    "Gunk shot": [3, 7],        # 30%
    "Poison jab": [3, 7],       # 30%
    "Poison sting": [3, 7],     # 30%
    "Sludge bomb": [3, 7],      # 30%
    "Sludge": [3, 7],           # 30%
    "Shell side arm": [2, 8],   # 20%
    "Smog": [4, 6]              # 40%
}

paralysis_inflict_chances = {
    "Nuzzle": [1, 0],           # 100%
    "Zap cannon": [255, 1],     # ~99.6% (255/256)
    "Body slam": [3, 7],        # 30%
    "Bounce": [3, 7],           # 30%
    "Discharge": [3, 7],        # 30%
    "Dragon breath": [3, 7],    # 30%
    "Force palm": [3, 7],       # 30%
    "Freeze shock": [3, 7],     # 30%
    "Lick": [3, 7],             # 30%
    "Spark": [3, 7],            # 30%
    "Thunder": [3, 7],          # 30%
    "Bolt strike": [2, 8],      # 20%
    "Thunderbolt": [1, 9],      # 10%
    "Shadow bolt": [1, 9],      # 10%
    "Thunder fang": [1, 9],     # 10%
    "Thunder punch": [1, 9],    # 10%
    "Thunder shock": [1, 9]     # 10%
}

burn_inflict_chances = {
    "Inferno": [1, 0],          # 100%
    "Lava plume": [3, 7],       # 30%
    "Scald": [3, 7],            # 30%
    "Steam eruption": [3, 7],   # 30%
    "Searing shot": [3, 7],     # 30%
    "Blue flare": [2, 8],       # 20%
    "Blaze kick": [1, 9],       # 10%
    "Ember": [1, 9],            # 10%
    "Fire blast": [1, 9],       # 10%
    "Fire fang": [1, 9],        # 10%
    "Fire punch": [1, 9],       # 10%
    "Flame wheel": [1, 9],      # 10%
    "Flamethrower": [1, 9],     # 10%
    "Flare blitz": [1, 9],      # 10%
    "Heat wave": [1, 9],        # 10%
    "Pyro ball": [1, 9],        # 10%
}