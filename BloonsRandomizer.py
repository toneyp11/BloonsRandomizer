#!/usr/bin/env python3
# BloonsRandomizer.py

"""
Used to randomize towers in Bloons Tower Defense 6 (BTD6)
Intended to create challenge modes

Last Updated for Version 34.3.6116
"""
import random

import PySimpleGUI as sg

# global variables
players = 1
gamemode = "Default"
waterBan = False

# constants
gamemodeList = ["Default", "Primary Only", "Military Only", "Magic Only", "Support Only"]
defaultMessage = "Player Not Active"


def gen_UI():
    """Creates the UI upon launch"""
    global players
    global gamemode
    global waterBan

    # define the layout of the tabs
    settings = [[sg.Text('Number of Players'),
                 sg.Combo(["1", "2", "3", "4"], key='ui_players', enable_events=True, default_value="1")],
                [sg.Text('Gamemode'),
                 sg.Combo(gamemodeList, key='ui_gamemode', enable_events=True, default_value="Default")],
                [sg.Text('Ban Water Towers'),
                 sg.Checkbox('', key='ui_waterban', enable_events=True)]]
    results = [[sg.Button("Generate"),
                sg.Listbox(values=[defaultMessage], key="ui_list1", size=(30, 30)),
                sg.Listbox(values=[defaultMessage], key="ui_list2", size=(30, 30)),
                sg.Listbox(values=[defaultMessage], key="ui_list3", size=(30, 30)),
                sg.Listbox(values=[defaultMessage], key="ui_list4", size=(30, 30))]]

    # combine the tabs
    tabgrp = [[sg.TabGroup([[sg.Tab('Settings', settings),
                             sg.Tab('Monkey Results', results)]])]]

    # create the window
    window = sg.Window("Bloons Randomizer", tabgrp)

    # accept user input until the window closes
    while True:
        event, values = window.read()

        # players config
        if event == 'ui_players':
            players = values['ui_players']

        # generates new tower lists
        if event == 'Generate':
            playerListHandler(window)

        # gamemode config
        if event == 'ui_gamemode':
            gamemode = values['ui_gamemode']

        # water ban config
        if event == 'ui_waterban':
            waterBan = values['ui_waterban']

        if event == sg.WIN_CLOSED:
            break
    window.close()


def playerListHandler(window):
    """Maintains the lists for each player"""
    for i in range(0, int(players)):
        window["ui_list" + str(i + 1)].update(createList())

    # clears out the empty players' listboxes
    count = int(players)
    while count < 4:
        window["ui_list" + str(count + 1)].update([defaultMessage])
        count += 1


def hero():
    """Generates a random hero"""
    randInt = random.randint(0, 13)
    main = 0
    cross = 0

    if randInt == 0:
        return Tower("Quincy", water=False, main=main, cross=cross)
    elif randInt == 1:
        return Tower("Gwendolin", water=False, main=main, cross=cross)
    elif randInt == 2:
        return Tower("Striker Jones", water=False, main=main, cross=cross)
    elif randInt == 3:
        return Tower("Obyn Greenfoot", water=False, main=main, cross=cross)
    elif randInt == 4:
        return Tower("Geraldo", water=False, main=main, cross=cross)
    elif randInt == 5:
        return Tower("Captain Churchill", water=False, main=main, cross=cross)
    elif randInt == 6:
        return Tower("Benjamin", water=False, main=main, cross=cross)
    elif randInt == 7:
        return Tower("Ezili", water=False, main=main, cross=cross)
    elif randInt == 8:
        return Tower("Pat Fusty", water=False, main=main, cross=cross)
    elif randInt == 9:
        return Tower("Adora", water=False, main=main, cross=cross)
    elif randInt == 10:
        return Tower("Admiral Brickell", water=True, main=main, cross=cross)
    elif randInt == 11:
        return Tower("Etienne", water=False, main=main, cross=cross)
    elif randInt == 12:
        return Tower("Sauda", water=False, main=main, cross=cross)
    elif randInt == 13:
        return Tower("Psi", water=False, main=main, cross=cross)


def primary():
    """Generates a random primary tower"""
    randInt = random.randint(0, 5)
    main = mainPath()
    cross = crossPath(main)

    if randInt == 0:
        return Tower("Dart Monkey", water=False, main=main, cross=cross)
    elif randInt == 1:
        return Tower("Boomerang Monkey", water=False, main=main, cross=cross)
    elif randInt == 2:
        return Tower("Bomb Shooter", water=False, main=main, cross=cross)
    elif randInt == 3:
        return Tower("Tack Shooter", water=False, main=main, cross=cross)
    elif randInt == 4:
        return Tower("Ice Monkey", water=False, main=main, cross=cross)
    elif randInt == 5:
        return Tower("Glue Gunner", water=False, main=main, cross=cross)


def military():
    """Generates a random military tower"""
    randInt = random.randint(0, 6)
    main = mainPath()
    cross = crossPath(main)

    if randInt == 0:
        return Tower("Sniper Monkey", water=False, main=main, cross=cross)
    elif randInt == 1:
        return Tower("Monkey Sub", water=True, main=main, cross=cross)
    elif randInt == 2:
        return Tower("Monkey Buccaneer", water=True, main=main, cross=cross)
    elif randInt == 3:
        return Tower("Monkey Ace", water=False, main=main, cross=cross)
    elif randInt == 4:
        return Tower("Heli Pilot", water=False, main=main, cross=cross)
    elif randInt == 5:
        return Tower("Mortar Monkey", water=False, main=main, cross=cross)
    elif randInt == 6:
        return Tower("Dartling Gunner", water=False, main=main, cross=cross)


def magic():
    """Generates a random magic tower"""
    randInt = random.randint(0, 4)
    main = mainPath()
    cross = crossPath(main)

    if randInt == 0:
        return Tower("Wizard Monkey", water=False, main=main, cross=cross)
    elif randInt == 1:
        return Tower("Super Monkey", water=False, main=main, cross=cross)
    elif randInt == 2:
        return Tower("Ninja Monkey", water=False, main=main, cross=cross)
    elif randInt == 3:
        return Tower("Alchemist", water=False, main=main, cross=cross)
    elif randInt == 4:
        return Tower("Druid", water=False, main=main, cross=cross)


def support():
    """Generates a random support tower"""
    randInt = random.randint(0, 3)
    main = mainPath()
    cross = crossPath(main)

    if randInt == 0:
        return Tower("Banana Farm", water=False, main=main, cross=cross)
    elif randInt == 1:
        return Tower("Spike Factory", water=False, main=main, cross=cross)
    elif randInt == 2:
        return Tower("Monkey Village", water=False, main=main, cross=cross)
    elif randInt == 3:
        return Tower("Engineer Monkey", water=False, main=main, cross=cross)


def mainPath():
    """Generates a main path for upgrading a tower"""
    return random.randint(1, 3)


def crossPath(mainTowerPath):
    """Generates the cross path for upgrading a tower (the line that can only be upgraded twice)
    Also ensures that the cross path is not equal to the main path since that is not possible in game"""
    cross = random.randint(1, 3)
    while cross == mainTowerPath:
        cross = random.randint(1, 3)
    return cross


def generateMonkeyList():
    """Creates the full list of usable monkeys for a player"""

    # default generation
    if gamemode == "Default":
        monkeyList = [hero(),
                      primary(),
                      military(),
                      magic(),
                      support()]
        return monkeyList

    # primary monkeys generation
    if gamemode == "Primary Only":
        monkeyList = [hero(),
                      primary()]
        return monkeyList

    # military monkeys generation
    if gamemode == "Military Only":
        monkeyList = [hero(),
                      military()]
        return monkeyList

    # magic monkeys generation
    if gamemode == "Magic Only":
        monkeyList = [hero(),
                      magic()]
        return monkeyList

    # support monkeys generation
    if gamemode == "Support Only":
        monkeyList = [hero(),
                      support()]
        return monkeyList


def checkConditions(towerList):
    """Checks a list of towers to make sure it meets the required conditions"""
    # Check for no water towers allowed
    if waterBan:
        for tower in towerList:
            if tower.water:
                return False
    return True


def createList():
    """Generates a list of towers and verifies that it meets the required conditions"""
    monkeyList = generateMonkeyList()
    validList = checkConditions(monkeyList)
    while not validList:
        monkeyList = generateMonkeyList()
        validList = checkConditions(monkeyList)
    return monkeyList


class Tower:
    """Contains all relevant data for a tower in-game"""

    def __init__(self, name, water, main, cross):
        self.name = name
        self.water = water
        self.main = main
        self.cross = cross

    def __str__(self):
        return str(self.name + " (" + str(self.main) + "," + str(self.cross) + ")")


if __name__ == "__main__":
    gen_UI()
