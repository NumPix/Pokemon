from Objects.Pokemon import Pokemon
from Objects.color import color
from Objects.Move import Move
import random as r
import time
from Data.data import *

def printHP(target: Pokemon):

    HpCol = []

    if target.HP / target.stats[0] > 0.5:
        HpCol = [color.GREEN, color.END]
    if target.HP / target.stats[0] <= 0.5:
        HpCol = [color.YELLOW, color.END]
    if target.HP / target.stats[0] <= 0.25:
        HpCol = [color.RED, color.END]

    status = ''
    if target.status == 'Fainted':
        status = '|' + color.RED + target.status + color.END + '|'
    elif target.status == 'Paralyzed':
        status = '|' + color.YELLOW + target.status + color.END + '|'
    elif target.status == 'Poisoned':
        status = '|' + color.PURPLE + target.status + color.END + '|'
    elif target.status == 'Sleeping':
        status = '|' + color.BOLD + target.status + color.END + '|'
    elif target.status == 'Frozen':
        status = '|' + color.BLUE + target.status + color.END + '|'
    elif target.status == 'Burned':
        status = '|' + color.RED + target.status + color.END + '|'

    print(f"{data[target.id - 1]['name']['english']} {target.lvl} lv. {HpCol[0]}[{'█' * round(target.HP / target.stats[0] / 0.05) + '░' * (20 - round(target.HP / target.stats[0] / 0.05))}]{HpCol[1]} {target.HP}/{target.stats[0]} {status}")

def printMove(target: Pokemon, Move: Move):
    if target.pp[target.moves.index(Move)] / Move.pp >= 0.5:
        moveCol = [color.END, color.END]
    elif target.pp[target.moves.index(Move)] / Move.pp >= 0.25:
        moveCol = [color.YELLOW, color.END]
    else:
        moveCol = [color.RED, color.END]

    print(moveCol[0] + "•" + Move.name + f" [{target.pp[target.moves.index(Move)]}/{Move.pp}]" + moveCol[1])

def battle(YourTeam, FoesTeam, You, Foe, Items: dict):

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
            print(*["•Attack", "•Pokemon", "•Bag"], sep = "\n", end="\n\n")
            opt = input().capitalize()
            while opt not in ["Attack", "Pokemon", "Bag"]:
                print(*["•Attack", "•Pokemon", "•Bag"], sep="\n", end="\n\n")
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
                dU.add(yNow)
                print(f'{You} send out {yNow.name}!')

            elif opt == "Bag":
                print()
                for elem in Items: print("•" + elem)
                print()
                back = False
                chCat = input().lower()
                while chCat not in Items:
                    if chCat == '':
                        back = True
                        break
                    print()
                    for elem in Items: print("•" + elem)
                    print()
                    chCat = input().lower()
                if back:
                    turn = False
                    continue

                print('------------------------------------------')
                for it in Items[chCat]: print(f'{it.name}\t({Items[chCat][it]})')
                print('------------------------------------------')
                chIt = input().capitalize()
                if chIt == '':
                    back = True
                while chIt not in list(map(lambda x: x.name, Items[chCat].keys())):
                    if chIt == '':
                        back = True
                        break
                    print('------------------------------------------')
                    for it in Items[chCat]: print(f'{it.name}\t({Items[chCat][it]})')
                    print('------------------------------------------')
                    chIt = input().capitalize()
                if back:
                    turn = False
                    continue
                if chCat == "pokeballs":
                    list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0].use()
                else:
                    print()
                    print(color.BOLD + f'use {chIt} on which pokemon?' + color.END)
                    print()
                    print('------------------------------------------')
                    for poke in YourTeam: printHP(poke)
                    print('------------------------------------------\n')
                    chPoke = input().capitalize()
                    back = False
                    while chPoke not in list(map(lambda x: data[x.id - 1]['name']['english'], YourTeam)):
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
                    chPoke = YourTeam[YourTeam.index(list(filter(lambda x: data[x.id - 1]['name']['english'] == chPoke, YourTeam))[0])]
                    if chIt in healing:
                        if chPoke.HP == chPoke.stats[0] and chIt in healing:
                            print('\nThere is no effect\n')
                            turn = False
                            continue
                        else:
                            list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0].use(target=chPoke)
                            Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] -= 1
                            if Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] == 0:
                                Items[chCat].pop(list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0])
                    elif chIt in pprest:
                        if chIt in ['Elixir', 'Max elixir'] and chPoke.pp == [move.pp for move in chPoke.moves]:
                            print('\nThere is no effect\n')
                            turn = False
                            continue
                        elif chIt in ['Elixir', 'Max elixir'] and chPoke.pp != [move.pp for move in chPoke.moves]:
                            list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0].use(target=chPoke)
                            Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] -= 1
                            if Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] == 0:
                                Items[chCat].pop(list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0])
                        elif chIt in ['Ether', 'Max ether']:
                            print()
                            print(color.BOLD + f'which move pp should be restored?' + color.END)
                            print()
                            print('------------------------------------------')
                            for mv in chPoke.moves: printMove(chPoke, mv)
                            print('------------------------------------------\n')
                            chMove = input().capitalize()
                            back = False
                            while chMove not in list(map(lambda x: x.name, chPoke.moves)):
                                if chMove == '':
                                    back = True
                                    break
                                for mv in chPoke.moves: printMove(chPoke, mv)
                                chMove = input().capitalize()
                            if back:
                                turn = False
                                continue
                            chMove = chPoke.moves.index(list(filter(lambda x: x.name == chMove, chPoke.moves))[0])
                            if chPoke.moves[chMove].pp == chPoke.pp[chMove]:
                                print('\nThere is no effect\n')
                                turn = False
                                continue
                            else:
                                list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0].use(target=chPoke, moveId=chMove)
                                Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] -= 1
                                if Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] == 0:
                                    Items[chCat].pop(list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0])
                    elif chIt in map(lambda x: x.name, Items["status restore"].keys()):
                        if chPoke.status == '':
                            print("There is no effect")
                            continue
                        elif chPoke.status == 'Fainted' and chIt in ['Revive', 'Max revive', 'Revival herb']:
                            list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0].use(target=chPoke)
                            Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] -= 1
                            if Items[chCat][list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0]] == 0:
                                Items[chCat].pop(list(filter(lambda x: x.name == chIt, Items[chCat].keys()))[0])

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