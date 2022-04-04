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

    def use(self, target=None, moveId=None):
        if self.type == "HP/PP restore":
            if self.name == "Potion":
                healed = 20
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Super potion":
                healed = 50
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Hyper potion":
                healed = 200
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Max potion":
                print(f'\n{target.name}s HP maxed out!')
                target.HP = target.stats[0]
            elif self.name == "Super potion":
                healed = 50
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Fresh water":
                healed = 30
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Soda pop":
                healed = 50
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Lemonade":
                healed = 70
                target.HP += healed
                if target.HP >= target.stats[0]:
                    print(f'\n{target.name}s HP maxed out!')
                    target.HP = target.stats[0]
                else:
                    print(f'\n{target.name} recovered {healed} HP!')
            elif self.name == "Full restore":
                print(f'\n{target.name}s HP maxed out!')
                target.HP = target.stats[0]
                target.status = ''
            elif self.name == "Elixir":
                maxpp = [move.pp for move in target.moves]
                for mv in range(4):
                    target.pp[mv] += 10
                    if target.pp[mv] > maxpp[mv]:
                        target.pp[mv] = maxpp[mv]
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
                    print(f'\n{target.name}s {target.moves[moveId].name} pp were fully restored')
                else:
                    print(f'\n{target.name}s {target.moves[moveId].name} pp were restored')
            elif self.name == "Max Ether":
                target.pp[moveId] = target.moves[moveId].pp
                print(f'\n{target.name}s {target.moves[moveId].name} pp were fully restored')
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
        elif self.type == 2:
            pass
        elif self.type == 3:
            pass
        else:
            return
        print("\n==========================================\n")
