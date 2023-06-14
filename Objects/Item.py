import os
from dotenv import load_dotenv

from Objects.color import color
from Data.data import *

load_dotenv(".env")

TURN_SEPARATOR = os.getenv("TURN_SEPARATOR")


class Item:
    def __init__(self, name, type: str, id: int):
        self.name = name
        self.type = type
        """
        Pokeballs
        HP/PP restore
        Status restore
        Battle items
        """
        self.id = id

    def heal(self, target):
        target.HP += healing_amount[self.name]
        if target.HP >= target.stats[0]:
            print(f'\n{target.name}s HP maxed out!')
            target.HP = target.stats[0]
        else:
            print(f'\n{target.name} recovered {healing_amount[self.name]} HP!')

    def use(self, target=None, moveId=None):
        if self.type == 'HP/PP restore':
            if self.name in healing:
                self.heal(target)
            if self.name == "Full restore":
                print(f'\n{target.name} fully restored')
                target.HP = target.stats[0]
                target.status = ''
            elif self.name == "Elixir":
                max_pp = [move.pp for move in target.moves]
                for mv in range(4):
                    target.pp[mv] += 10
                    if target.pp[mv] > max_pp[mv]:
                        target.pp[mv] = max_pp[mv]
                if target.pp == [move.pp for move in target.moves]:
                    print(f'\n{target.name}s pp were fully restored')
                else:
                    print(f'\n{target.name}s pp were restored')
            elif self.name == "Max Elixir":
                target.pp = [move.pp for move in target.moves]
                print(f'\n{target.name}s pp were fully restored')
            elif self.name == "Ether":
                target.pp[moveId] += 10
                if target.pp[moveId] > target.moves[moveId].pp:
                    target.pp[moveId] = target.moves[moveId].pp
                    print(f'\n{target.name}s {color.BOLD}{target.moves[moveId].name}{color.END} pp were fully restored')
                else:
                    print(f'\n{target.name}s {target.moves[moveId].name} pp were restored')
            elif self.name == "Max Ether":
                target.pp[moveId] = target.moves[moveId].pp
                print(f'\n{target.name}s {color.BOLD}{target.moves[moveId].name}{color.END} pp were fully restored')
        elif self.type == "Status restore":
            if self.name == 'Revive':
                target.status = ''
                target.HP = target.stats[0] // 2
                print(f'\n{target.name} was revived')
            elif self.name == 'Max revive':
                target.status = ''
                target.HP = target.stats[0]
                print(f'\n{target.name} was revived')
            elif self.name == 'Revival herb':
                target.status = ''
                target.HP = target.stats[0]
                print(f'\n{target.name} was revived')
            elif self.name in ['Full heal', 'Full restore', 'Ice heal', 'Pumkin berry', 'Aspear berry', 'Lava cookie',
                               'Heal powder', 'Lum berry', 'Burn heal', 'Rawst berry', 'Paralyze heal', 'Cheri berry']:
                print(f'\n{target.name} is no more {target.status.lower()}')
                target.status = ''

        elif self.type == 2:
            pass
        elif self.type == "Battle items":
            pass
        else:
            return
        print(f"\n{TURN_SEPARATOR}\n")
