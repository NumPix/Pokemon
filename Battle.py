import random as rd
import time
import os
from dotenv import load_dotenv

from Objects.Pokemon import Pokemon
from Objects.color import color
from Objects.Move import Move
from Data.data import *

load_dotenv(".env")

SECTION_SEPARATOR = os.getenv("SECTION_SEPARATOR")
TURN_SEPARATOR = os.getenv("TURN_SEPARATOR")
DELAY_TIME = float(os.getenv("DELAY_TIME"))


def delay():
    time.sleep(DELAY_TIME)


def print_hp(target: Pokemon):

    hp_col = []

    if target.HP / target.stats[0] > 0.5:
        hp_col = [color.GREEN, color.END]
    if target.HP / target.stats[0] <= 0.5:
        hp_col = [color.YELLOW, color.END]
    if target.HP / target.stats[0] <= 0.25:
        hp_col = [color.RED, color.END]

    gender = color.BOLD + color.BLUE + "♂" + color.END if target.gender == 1 \
        else color.BOLD + color.FAIRY + "♀" + color.END

    status = ''
    if target.status == 'Fainted':
        status = '|' + color.RED + target.status + color.END + '|'
    elif target.status == 'Paralyzed':
        status = '|' + color.YELLOW + target.status + color.END + '|'
    elif target.status in ['Poisoned', 'BPoisoned']:
        status = '|' + color.PURPLE + 'Poisoned' + color.END + '|'
    elif target.status == 'Sleeping':
        status = '|' + color.BOLD + target.status + color.END + '|'
    elif target.status == 'Frozen':
        status = '|' + color.BLUE + target.status + color.END + '|'
    elif target.status == 'Burned':
        status = '|' + color.RED + target.status + color.END + '|'

    hp = f"{data[target.id - 1]['name']['english']} {gender} "

    while len(hp) < 27:
        hp += ' '

    hp += (3 - len(str(target.lvl))) * ' '

    hp_filling = '█' * round(target.HP / target.stats[0] / .05) + '░' * (20 - round(target.HP / target.stats[0] / .05))

    print(f"{hp}lv{target.lvl} {hp_col[0]}[{hp_filling}]{hp_col[1]} {target.HP}/{target.stats[0]}\t{status}")


def print_game_status(your_team, foes_team, y_now, f_now):
    print('\n' + '● ' * len(list(filter(lambda x: x.status != 'Fainted', your_team))) + '○ ' * (
            6 - len(list(filter(lambda x: x.status != 'Fainted', your_team)))))
    print_hp(y_now)
    print_hp(f_now)
    print('● ' * len(list(filter(lambda x: x.status != 'Fainted', foes_team))) + '○ ' * (
            6 - len(list(filter(lambda x: x.status != 'Fainted', foes_team)))))


def print_move(target: Pokemon, move: Move):
    if target.pp[target.moves.index(move)] / move.pp >= 0.5:
        move_col = [color.END, color.END]
    elif target.pp[target.moves.index(move)] / move.pp >= 0.25:
        move_col = [color.YELLOW, color.END]
    else:
        move_col = [color.RED, color.END]

    type_col = [color.__dict__[move.type.upper()], color.END]

    move_str = move_col[0] + "•" + move.name + f" [{target.pp[target.moves.index(move)]}/{move.pp}]" + move_col[1]
    while len(move_str) < 35:
        move_str += ' '

    print(move_str + type_col[0] + f'|{move.type}|' + type_col[1])


def print_frozen(frozen: bool, target: Pokemon, game_data):
    # game_data: your_team, foes_team, y_now, f_now, turn, d_u
    if frozen:
        print(color.BOLD + f"{data[target.id - 1]['name']['english']} is frozen solid!" + color.END)
        print_game_status(*game_data[:4])
        print(f"\n{TURN_SEPARATOR}\n")
        return game_data[3], game_data[2], game_data[4], game_data[5]
    else:
        target.status = ''
        print(color.BOLD + f"{data[game_data[3].id - 1]['name']['english']} thawed out!")


def print_paralyzed(paralyzed: bool, target: Pokemon, game_data):
    # game_data: your_team, foes_team, y_now, f_now, turn, d_u
    if not paralyzed:
        print(color.BOLD + f"{data[target.id - 1]['name']['english']} is paralyzed! It can't move!" + color.END)
        print_game_status(*game_data[:4])
        print(f"\n{TURN_SEPARATOR}\n")
        return game_data[3], game_data[2], game_data[4], game_data[5]


def print_exp_gain(d_u, f_now):
    for poke in filter(lambda x: x.status != 'Fainted', d_u):
        print(f'\n{SECTION_SEPARATOR}')
        print(f'{poke.name} got {poke.expCalc(f_now, len(d_u))} xp!')
        poke.expGain(poke.expCalc(f_now, len(d_u)))
        print(f'{SECTION_SEPARATOR}\n')
        delay()


def battle(your_team, foes_team, you, foe, items: dict):

    y_temp_stats = list(map(lambda x: x.stats, your_team))
    f_temp_stats = list(map(lambda x: x.stats, foes_team))

    # weather = '' (Not implemented yet)

    turn = False

    """
    True - You
    False - Foe
    """

    y_now = your_team[0]
    f_now = foes_team[0]
    print(f"{you} send out {y_now.name}!")
    print(f"{foe} send out {f_now.name}!\n")
    d_u = {y_now}

    def y_check_faint():
        if not list(filter(lambda x: x.status != 'Fainted', your_team)):
            raise Exception("You Lost")
        print('------------------------------------------')
        for i in range(len(your_team)):
            print(f'({i}) ', end='')
            print_hp(your_team[i])
        print('------------------------------------------\n')
        print(color.BOLD + 'Choose your next Pokemon!\n' + color.END)
        ch_poke = input().strip()
        while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
            print('------------------------------------------')
            for i in range(len(your_team)):
                print(f'({i}) ', end='')
                print_hp(your_team[i])
            print('------------------------------------------\n')
            ch_poke = input().strip()
        y_now = your_team[int(ch_poke)]
        return y_now

    def y_attack(f_now, y_now, turn, d_u):

        if y_now.status == 'Frozen':
            frozen: bool = rd.choices([True, False], [8, 2])[0] and not ch_move.name in [
                "Fusion flare", "Flame wheel", "Sacred fire", "Flare blitz", "scald", "Steam eruption"]
            print_frozen(frozen, y_now, [your_team, foes_team, y_now, f_now, turn, d_u])

        if y_now.status == 'Paralyzed':
            paralyzed = rd.choices([True, False], [3, 1])[0]
            print_paralyzed(paralyzed, y_now, [your_team, foes_team, y_now, f_now, turn, d_u])

        print(f"{y_now.name} used {color.BOLD}{ch_move.name}{color.END}!")

        y_now.attack(y_now.moves.index(ch_move), f_now)
        if f_now.status == "Fainted":
            delay()

            print_exp_gain(d_u, f_now)

            d_u = {y_now}

            try:
                f_now = rd.choice(list(filter(lambda x: x.status != "Fainted", foes_team)))

                print(color.BOLD + f"{foe} is going to send out {data[f_now.id - 1]['name']['english']}!" + color.END)
                print("Do you want to switch pokemon (y/N)?")

                switch = False
                ch = input().lower().strip()

                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input().strip()

                if ch in ['n', 'no', '']: pass
                else:
                    switch = True
                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}')

                    ch_poke = input().strip()
                    back = False

                    while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                            your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
                        if ch_poke == '':
                            back = True
                            break

                        print(f'{SECTION_SEPARATOR}')

                        for i in range(len(your_team)):
                            print(f'({i}) ', end='')
                            print_hp(your_team[i])
                        print(f'{SECTION_SEPARATOR}\n')

                        ch_poke = input().strip()

                    if not back:
                        y_now = your_team[int(ch_poke)]
                        d_u = {y_now}
                    else:
                        switch = False

                print(f"{foe} send out {f_now.name}!")

                if switch:
                    print(f"{you} send out {y_now.name}!")

                turn = False
            except IndexError:
                pass

        print_game_status(your_team, foes_team, y_now, f_now)
        print(f"\n{TURN_SEPARATOR}\n")

        delay()
        return f_now, y_now, turn, d_u

    def fAttack(f_now, y_now, turn, d_u):
        ch_move = rd.randint(0, len(f_now.moves) - 1)

        if f_now.status == 'Burned':
            burn_dmg = f_now.stats[0] // 8

            print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} is hurt by its burn" + color.END)

            f_now.HP -= burn_dmg

            if f_now.HP <= 0:
                f_now.status = 'Fainted'

                print(color.RED + f"{data[f_now.id - 1]['name']['english']} fainted!" + color.END)
        if f_now.status == 'Poisoned':
            poison_dmg = f_now.stats[0] // 8

            print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} is hurt by poison!" + color.END)

            f_now.HP -= poison_dmg

            if f_now.HP <= 0:
                f_now.status = 'Fainted'

                print(color.RED + f"{data[f_now.id - 1]['name']['english']} fainted!" + color.END)
        if f_now.status == 'Frozen':
            if f_now.moves[ch_move].name in ["Fusion flare", "Flame wheel", "Sacred fire", "Flare blitz", "scald", "Steam eruption"]:
                f_now.status = ''
                print(color.BOLD + f"{data[f_now.id - 1]['name']['english']} thawed out!")
            else:
                frozen: bool = rd.choices([True, False], [8, 2])[0]
                print_frozen(frozen, f_now, [your_team, foes_team, y_now, f_now, turn, d_u])

        if f_now.status == 'Paralyzed':

            paralyzed = rd.choices([True, False], [3, 1])[0]
            print_paralyzed(paralyzed, f_now, [your_team, foes_team, y_now, f_now, turn, d_u])

        if f_now.status == "Fainted":
            delay()

            print_exp_gain(d_u, f_now)

            d_u = {y_now}
            try:
                f_now = rd.choice(list(filter(lambda x: x.status != "Fainted", foes_team)))

                print(
                    color.BOLD + f"{foe} is going to send out {data[f_now.id - 1]['name']['english']}!" + color.END)
                print("Do you want to switch pokemon (y/N)?")

                switch = False
                ch = input().lower().strip()

                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input().strip()

                if ch in ['n', 'no', '']:
                    pass
                else:
                    switch = True

                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_poke = input().strip()
                    back = False

                    while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or \
                            your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)):
                        if ch_poke == '':
                            back = True
                            break

                        print(f'{SECTION_SEPARATOR}')

                        for i in range(len(your_team)):
                            print(f'({i}) ', end='')
                            print_hp(your_team[i])

                        print(f'{SECTION_SEPARATOR}\n')

                        ch_poke = input().strip()

                    if not back:
                        y_now = your_team[int(ch_poke)]
                    else:
                        switch = False

                print(f"{foe} send out {f_now.name}!")

                if switch:
                    print(f"{you} send out {y_now.name}!")
                return f_now, y_now, turn, d_u

            except IndexError:
                pass

            print(f"\n{TURN_SEPARATOR}\n")
            print_game_status(your_team, foes_team, y_now, f_now)

            return f_now, y_now, turn, d_u

        print(f"{f_now.name} used {color.BOLD}{f_now.moves[ch_move].name}{color.END}!")

        f_now.attack(ch_move, y_now)

        print_game_status(your_team, foes_team, y_now, f_now)
        print(f"\n{TURN_SEPARATOR}\n")

        delay()

        return f_now, y_now, turn, d_u

    print_game_status(your_team, foes_team, y_now, f_now)
    print(f"\n{TURN_SEPARATOR}\n")

    while list(filter(lambda x: x.status != "Fainted", your_team)) and list(filter(lambda x: x.status != "Fainted", foes_team)):
        turn = not turn
        if turn:
            if y_now.status == 'Burned':
                burn_dmg = f_now.stats[0] // 8

                print(color.BOLD + f"{data[y_now.id - 1]['name']['english']} is hurt by its burn!" + color.END)

                y_now.HP -= burn_dmg

                if y_now.HP <= 0:
                    y_now.Hp = 0
                    y_now.status = 'Fainted'

                    print(color.RED + f"{data[y_now.id - 1]['name']['english']} fainted!" + color.END)

                    y_check_faint()
            if y_now.status == 'Poisoned':
                poison_dmg = f_now.stats[0] // 8

                print(color.BOLD + f"{data[y_now.id - 1]['name']['english']} is hurt by poison!" + color.END)

                y_now.HP -= poison_dmg
                if y_now.HP <= 0:
                    y_now.Hp = 0
                    y_now.status = 'Fainted'
                    print(color.RED + f"{data[y_now.id - 1]['name']['english']} fainted!" + color.END)
                    y_check_faint()

            print(*["(0) •Attack", "(1) •Pokemon", "(2) •Bag"], sep = "\n", end="\n\n")

            turn_option = input().strip()

            while turn_option not in ["0", "1", "2"]:
                print(*["(0) •Attack", "(1) •Pokemon", "(2) •Bag"], sep="\n", end="\n\n")
                turn_option = input().strip()

            if turn_option == "0":
                print(f'{SECTION_SEPARATOR}')

                for i in range(len(y_now.moves)):
                    print(f'({i}) ', end=' ')
                    print_move(y_now, y_now.moves[i])

                print(f'{SECTION_SEPARATOR}\n')

                ch_move = input().strip()
                back = False

                while not ch_move.isdigit() or int(ch_move) not in [i for i in range(len(y_now.moves))] or y_now.moves[int(ch_move)] \
                        not in list(filter(lambda x: y_now.pp[y_now.moves.index(x)] > 0, y_now.moves)):
                    if ch_move == '':
                        back = True
                        break

                    print(f'{SECTION_SEPARATOR}')

                    for i in range(4):
                        print(f'({i}) ', end=' ')
                        print_move(y_now, y_now.moves[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_move = input().strip()
                if back:
                    turn = False
                    continue

                ch_move = y_now.moves[int(ch_move)]
                tch_move = ch_move

                if y_now.stats[5] >= f_now.stats[5]:
                    f_now, y_now, turn, d_u = y_attack(f_now, y_now, turn, d_u)
                    if not turn:
                        continue
                else:
                    print(f"\n{TURN_SEPARATOR}\n")

                    f_now, y_now, turn, d_u = fAttack(f_now, y_now, turn, d_u)

                    if y_now.status == "Fainted":
                        try:
                            y_now = y_check_faint()
                        except:
                            break
                        d_u.add(y_now)

                        print(f"\n{you} send out {y_now.name}!")

                        turn = False
                        continue

                    ch_move = tch_move
                    delay()
                    f_now, y_now, turn, d_u = y_attack(f_now, y_now, turn, d_u)

                    if not turn:
                        continue
                    turn = not turn

            elif turn_option == "1":

                print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                print(f'{SECTION_SEPARATOR}')

                for i in range(len(your_team)):
                    print(f'({i}) ', end='')
                    print_hp(your_team[i])

                print(f'{SECTION_SEPARATOR}\n')

                ch_poke = input().strip()
                back = False

                while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))] or\
                        your_team[int(ch_poke)] not in list(filter(lambda x: x.status != 'Fainted', your_team)) or your_team[int(ch_poke)] == y_now:
                    if ch_poke == '':
                        back = True
                        break

                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_poke = input().strip()
                if back:
                    turn = False
                    continue

                y_now = your_team[int(ch_poke)]
                d_u.add(y_now)

                print(f'{you} send out {y_now.name}!')

            elif turn_option == "2":
                print()
                for i in range(len(items)):
                    print(f"({i}) •{list(items.keys())[i]}")
                print()

                back = False
                ch_cat = input().strip()

                while not ch_cat.isdigit() or int(ch_cat) not in [i for i in range(len(items))]:
                    if ch_cat == '':
                        back = True
                        break

                    print()
                    for i in range(len(items)):
                        print(f"({i}) •{list(items.keys())[i]}")
                    print()

                    ch_cat = input().strip()
                if back:
                    turn = False
                    continue

                ch_cat = list(items.keys())[int(ch_cat)]

                print(f'{SECTION_SEPARATOR}')

                for i in range(len(items[ch_cat])):
                    it = list(items[ch_cat].keys())[i]
                    temp = f'({i}) {it.name}'

                    while len(temp) < 24:
                        temp += ' '

                    print(f'{temp}[{items[ch_cat][it]}]')
                print(f'{SECTION_SEPARATOR}')

                ch_item = input().strip()

                if ch_item == '':
                    back = True
                while ch_item not in [str(i) for i in range(len(items[ch_cat]))]:
                    if ch_item == '':
                        back = True
                        break

                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(items[ch_cat])):
                        it = list(items[ch_cat].keys())[i]
                        print(f'({i}) {it.name}\t[{items[ch_cat][it]}]')

                    print(f'{SECTION_SEPARATOR}')

                    ch_item = input().strip()
                if back:
                    turn = False
                    continue
                if ch_cat == "pokeballs":
                    list(items[ch_cat].keys())[int(ch_item)].use()
                else:
                    ch_item = list(items[ch_cat].keys())[int(ch_item)]

                    print('\n' + color.BOLD + f'use {ch_item.name} on which pokemon?' + color.END + '\n')
                    print(f'{SECTION_SEPARATOR}')

                    for i in range(len(your_team)):
                        print(f'({i}) ', end='')
                        print_hp(your_team[i])

                    print(f'{SECTION_SEPARATOR}\n')

                    ch_poke = input().strip()
                    back = False

                    while not ch_poke.isdigit() or int(ch_poke) not in [i for i in range(len(your_team))]:
                        if ch_poke == '':
                            back = True
                            break

                        print(f'{SECTION_SEPARATOR}')
                        for i in range(len(your_team)):
                            print(f'({i}) ', end='')
                            print_hp(your_team[i])
                        print(f'{SECTION_SEPARATOR}\n')

                        ch_poke = input().strip()
                    if back:
                        turn = False
                        continue

                    ch_poke = your_team[int(ch_poke)]

                    if ch_item.name in healing:
                        if (ch_poke.HP == ch_poke.stats[0] and ch_item.name in healing) or ch_poke.status == 'Fainted':
                            print('\nThere is no effect\n')
                            turn = False
                            continue
                        else:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)
                    elif ch_item.name in pp_restore:
                        if ch_item.name in ['Elixir', 'Max elixir']:
                            if ch_poke.pp == [move.pp for move in ch_poke.moves]:
                                print('\nThere is no effect\n')
                                turn = False
                                continue
                            else:
                                ch_item.use(target=ch_poke)
                                items[ch_cat][ch_item] -= 1

                                if items[ch_cat][ch_item] == 0:
                                    items[ch_cat].pop(ch_item)
                        elif ch_item.name in ['Ether', 'Max ether']:
                            print('\n' + color.BOLD + f'which move pp should be restored?' + color.END + '\n')
                            print(f'{SECTION_SEPARATOR}')

                            for i in range(4):
                                print(f'({i}) ', end=' ')
                                print_move(ch_poke, ch_poke.moves[i])

                            print(f'{SECTION_SEPARATOR}\n')

                            ch_move = input().strip()
                            back = False

                            while not ch_move.isdigit() or int(ch_move) not in [i for i in range(len(y_now.moves))]:
                                if ch_move == '':
                                    back = True
                                    break

                                print(f'{SECTION_SEPARATOR}')

                                for i in range(4):
                                    print(f'({i}) ', end=' ')
                                    print_move(y_now, y_now.moves[i])
                                print(f'{SECTION_SEPARATOR}\n')

                                ch_move = input().strip()
                            if back:
                                turn = False
                                continue
                            if ch_poke.moves[int(ch_move)].pp == ch_poke.pp[int(ch_move)]:
                                print('\nThere is no effect\n')
                                turn = False
                                continue
                            else:
                                ch_item.use(ch_poke, int(ch_move))
                                items[ch_cat][ch_item] -= 1

                                if items[ch_cat][ch_item] == 0:
                                    items[ch_cat].pop(ch_item)
                    elif ch_item.name in map(lambda x: x.name, items["status restore"].keys()):
                        if ch_poke.status == '':
                            print("\nThere is no effect\n")
                            turn = False
                            continue
                        elif ch_poke.status == 'Fainted' and ch_item.name in ['Revive', 'Max revive', 'Revival herb']:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)
                        elif ch_poke.status == 'Frozen' and ch_item.name in frozen_heal:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)

                        elif ch_poke.status == 'Burned' and ch_item.name in burn_heal:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)

                        elif ch_poke.status == 'Paralyzed' and ch_item.name in paralysis_heal:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)

                        elif ch_poke.status in ['Poisoned', 'BPoisoned'] and ch_item.name in poison_heal:
                            ch_item.use(target=ch_poke)
                            items[ch_cat][ch_item] -= 1

                            if items[ch_cat][ch_item] == 0:
                                items[ch_cat].pop(ch_item)

        else:
            f_now, y_now, turn, d_u = fAttack(f_now, y_now, turn, d_u)
            if y_now.status == "Fainted":
                try:
                    y_now = y_check_faint()
                except:
                    break
                d_u.add(y_now)

                print(f"\n{you} send out {y_now.name}!\n")
                print(f"\n{TURN_SEPARATOR}")
                print_game_status(your_team, foes_team, y_now, f_now)

                turn = False
                continue

    if list(filter(lambda x: x.status != "Fainted", your_team)):
        print("You Won!")
    else:
        print("You Lost!")

    for i in range(len(your_team)):
        your_team[i].stats = y_temp_stats[i]
    for i in range(len(foes_team)):
        foes_team[i].stats = f_temp_stats[i]