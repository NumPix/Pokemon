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

    typeCol = [color.__dict__[Move.type.upper()], color.END]

    print(moveCol[0] + "•" + Move.name + f" [{target.pp[target.moves.index(Move)]}/{Move.pp}]" +
          moveCol[1] + typeCol[0] + f' |{Move.type}|' + typeCol[1])

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
        if not list(filter(lambda x: x.status != 'Fainted', YourTeam)):
            raise Exception("You Lost")
        time.sleep(1)
        print('------------------------------------------')
        for i in range(len(YourTeam)):
            print(f'({i}) ', end='')
            printHP(YourTeam[i])
        print('------------------------------------------\n')
        print(color.BOLD + 'Choose your next Pokemon!\n' + color.END)
        chPoke = input().strip()
        while not chPoke.isdigit() or int(chPoke) not in [i for i in range(len(YourTeam))] or \
                YourTeam[int(chPoke)] not in list(filter(lambda x: x.status != 'Fainted', YourTeam)):
            print('------------------------------------------')
            for i in range(len(YourTeam)):
                print(f'({i}) ', end='')
                printHP(YourTeam[i])
            print('------------------------------------------\n')
            chPoke = input().strip()
        yNow = YourTeam[int(chPoke)]
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
                print("Do you want to switch pokemon (y/N)?")
                switch = False
                ch = input().lower().strip()
                while ch not in ['y', 'n', 'yes', 'no', '']:
                    ch = input().strip()
                if ch in ['n', 'no', '']: pass
                else:
                    switch = True
                    print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                    print('------------------------------------------')
                    for i in range(len(YourTeam)):
                        print(f'({i}) ', end='')
                        printHP(YourTeam[i])
                    print('------------------------------------------\n')
                    chPoke = input().strip()
                    back = False
                    while not chPoke.isdigit() or int(chPoke) not in [i for i in range(len(YourTeam))] or \
                            YourTeam[int(chPoke)] not in list(filter(lambda x: x.status != 'Fainted', YourTeam)):
                        if chPoke == '':
                            back = True
                            break
                        print('------------------------------------------')
                        for i in range(len(YourTeam)):
                            print(f'({i}) ', end='')
                            printHP(YourTeam[i])
                        print('------------------------------------------\n')
                        chPoke = input().strip()
                    if not back:
                        yNow = YourTeam[int(chPoke)]
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

        time.sleep(1)
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

        time.sleep(1)

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
            print(*["(0) •Attack", "(1) •Pokemon", "(2) •Bag"], sep = "\n", end="\n\n")
            opt = input().strip()
            while opt not in ["0", "1", "2"]:
                print(*["(0) •Attack", "(1) •Pokemon", "(2) •Bag"], sep="\n", end="\n\n")
                opt = input().strip()

            if opt == "0":
                print('------------------------------------------')
                for i in range(4):
                    print(f'({i}) ', end=' ')
                    printMove(yNow, yNow.moves[i])
                print('------------------------------------------\n')
                chMove = input().strip()
                back = False
                while not chMove.isdigit() or int(chMove) not in [i for i in range(len(yNow.moves))] or yNow.moves[int(chMove)] \
                        not in list(filter(lambda x: yNow.pp[yNow.moves.index(x)] > 0, yNow.moves)):
                    if chMove == '':
                        back = True
                        break
                    print('------------------------------------------')
                    for i in range(4):
                        print(f'({i}) ', end=' ')
                        printMove(yNow, yNow.moves[i])
                    print('------------------------------------------\n')
                    chMove = input().strip()
                if back:
                    turn = False
                    continue
                chMove = yNow.moves[int(chMove)]
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

            elif opt == "1":
                print(color.BOLD + "Choose a Pokemon to switch!" + color.END)
                print('------------------------------------------')
                for i in range(len(YourTeam)):
                    print(f'({i}) ', end='')
                    printHP(YourTeam[i])
                print('------------------------------------------\n')
                chPoke = input().strip()
                back = False
                while not chPoke.isdigit() or int(chPoke) not in [i for i in range(len(YourTeam))] or\
                        YourTeam[int(chPoke)] not in list(filter(lambda x: x.status != 'Fainted', YourTeam)):
                    if chPoke == '':
                        back = True
                        break
                    print('------------------------------------------')
                    for i in range(len(YourTeam)):
                        print(f'({i}) ', end='')
                        printHP(YourTeam[i])
                    print('------------------------------------------\n')
                    chPoke = input().strip()
                if back:
                    turn = False
                    continue
                yNow = YourTeam[int(chPoke)]
                dU.add(yNow)
                print(f'{You} send out {yNow.name}!')

            elif opt == "2":
                print()
                for i in range(len(Items)):
                    print(f"({i}) •{list(Items.keys())[i]}")
                print()
                back = False
                chCat = input().strip()
                while not chCat.isdigit() or int(chCat) not in [i for i in range(len(Items))]:
                    if chCat == '':
                        back = True
                        break
                    print()
                    for i in range(len(Items)):
                        print(f"({i}) •{list(Items.keys())[i]}")
                    print()
                    chCat = input().strip()
                if back:
                    turn = False
                    continue

                chCat = list(Items.keys())[int(chCat)]

                print('------------------------------------------')
                for i in range(len(Items[chCat])):
                    it = list(Items[chCat].keys())[i]
                    print(f'({i}) {it.name}\t[{Items[chCat][it]}]')
                print('------------------------------------------')
                chIt = input().strip()
                if chIt == '':
                    back = True
                while chIt not in [str(i) for i in range(len(Items[chCat]))]:
                    if chIt == '':
                        back = True
                        break
                    print('------------------------------------------')
                    for i in range(len(Items[chCat])):
                        it = list(Items[chCat].keys())[i]
                        print(f'({i}) {it.name}\t[{Items[chCat][it]}]')
                    print('------------------------------------------')
                    chIt = input().strip()
                if back:
                    turn = False
                    continue
                if chCat == "pokeballs":
                    list(Items[chCat].keys())[int(chIt)].use()
                else:
                    chIt = list(Items[chCat].keys())[int(chIt)]
                    print('\n' + color.BOLD + f'use {chIt.name} on which pokemon?' + color.END + '\n')
                    print('------------------------------------------')
                    for i in range(len(YourTeam)):
                        print(f'({i}) ', end='')
                        printHP(YourTeam[i])
                    print('------------------------------------------\n')
                    chPoke = input().strip()
                    back = False
                    while not chPoke.isdigit() or int(chPoke) not in [i for i in range(len(YourTeam))]:
                        if chPoke == '':
                            back = True
                            break
                        print('------------------------------------------')
                        for i in range(len(YourTeam)):
                            print(f'({i}) ', end='')
                            printHP(YourTeam[i])
                        print('------------------------------------------\n')
                        chPoke = input().strip()
                    if back:
                        turn = False
                        continue
                    chPoke = YourTeam[int(chPoke)]
                    if chIt.name in healing:
                        if (chPoke.HP == chPoke.stats[0] and chIt.name in healing) or chPoke.status == 'Fainted':
                            print('\nThere is no effect\n')
                            turn = False
                            continue
                        else:
                            chIt.use(target=chPoke)
                            Items[chCat][chIt] -= 1
                            if Items[chCat][chIt] == 0:
                                Items[chCat].pop(chIt)
                    elif chIt.name in pprest:
                        if chIt.name in ['Elixir', 'Max elixir'] and chPoke.pp == [move.pp for move in chPoke.moves]:
                            print('\nThere is no effect\n')
                            turn = False
                            continue
                        elif chIt.name in ['Elixir', 'Max elixir'] and chPoke.pp != [move.pp for move in chPoke.moves]:
                            chIt.use(target=chPoke)
                            Items[chCat][chIt] -= 1
                            if Items[chCat][chIt] == 0:
                                Items[chCat].pop(chIt)
                        elif chIt.name in ['Ether', 'Max ether']:
                            print('\n' + color.BOLD + f'which move pp should be restored?' + color.END + '\n')
                            print('------------------------------------------')
                            for i in range(4):
                                print(f'({i}) ', end=' ')
                                printMove(yNow, yNow.moves[i])
                            print('------------------------------------------\n')
                            chMove = input().strip()
                            back = False

                            while not chMove.isdigit() or int(chMove) not in [i for i in range(len(yNow.moves))] or \
                                    yNow.moves[int(chMove)] \
                                    not in list(filter(lambda x: yNow.pp[yNow.moves.index(x)] > 0, yNow.moves)):
                                if chMove == '':
                                    back = True
                                    break
                                print('------------------------------------------')
                                for i in range(4):
                                    print(f'({i}) ', end=' ')
                                    printMove(yNow, yNow.moves[i])
                                print('------------------------------------------\n')
                                chMove = input().strip()
                            if back:
                                turn = False
                                continue
                            chMove = yNow.moves[int(chMove)]
                            if chPoke.moves[chMove].pp == chPoke.pp[chMove]:
                                print('\nThere is no effect\n')
                                turn = False
                                continue
                            else:
                                chIt.use(target=chPoke, moveId=chMove)
                                Items[chCat][chIt] -= 1
                                if Items[chCat][chIt] == 0:
                                    Items[chCat].pop(chIt)
                    elif chIt.name in map(lambda x: x.name, Items["status restore"].keys()):
                        if chPoke.status == '':
                            print("There is no effect")
                            continue
                        elif chPoke.status == 'Fainted' and chIt.name in ['Revive', 'Max revive', 'Revival herb']:
                            chIt.use(target=chPoke)
                            Items[chCat][chIt] -= 1
                            if Items[chCat][chIt] == 0:
                                Items[chCat].pop(chIt)

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