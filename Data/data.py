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

natureList = ["Hardy", "Lonely", "Adamant", "Naughty", "Brave",
              "Bold", "Docile", "Impish", "Lax", "Relaxed",
              "Modest", "Mild", "Bashful", "Rash", "Quiet",
              "Calm", "Gentle", "Careful", "Quirky", "Sassy",
              "Timid", "Hasty", "Jolly", "Naive", "Serious"]

healing = ['Potion', 'Super potion', 'Hyper potion', 'Max potion', 'Fresh water', 'Soda pop', 'Lemonade', 'Moomoo milk', 'Full restore']
pprest = ['Ether', 'Max ether', 'Elixir', 'Max elixir']
frozenHeal = ['Full heal', 'Full restore', 'Ice heal', 'Pumkin berry', 'Aspear berry', 'Lava cookie', 'Heal powder', 'Lum berry']
burnHeal = ['Burn heal', 'Rawst berry', 'Full heal', 'Lava cookie', 'Full restore', 'Heal powder', 'Lum berry']
paralysisHeal = ['Paralyze heal', 'Cheri berry', 'Full heal', 'Lava cookie','Full restore', 'Heal powder', 'Lum berry']
poisonHeal = ['Antidote', 'Pecha berry', 'Full heal', 'Lava cookie','Full restore', 'Heal powder', 'Lum berry']