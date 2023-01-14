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
mainUpgrades = 5
crossUpgrades = 2

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
    paths = [0, 0, 0]

    if randInt == 0:
        return Tower("Quincy", water=False, paths=paths)
    elif randInt == 1:
        return Tower("Gwendolin", water=False, paths=paths)
    elif randInt == 2:
        return Tower("Striker Jones", water=False, paths=paths)
    elif randInt == 3:
        return Tower("Obyn Greenfoot", water=False, paths=paths)
    elif randInt == 4:
        return Tower("Geraldo", water=False, paths=paths)
    elif randInt == 5:
        return Tower("Captain Churchill", water=False, paths=paths)
    elif randInt == 6:
        return Tower("Benjamin", water=False, paths=paths)
    elif randInt == 7:
        return Tower("Ezili", water=False, paths=paths)
    elif randInt == 8:
        return Tower("Pat Fusty", water=False, paths=paths)
    elif randInt == 9:
        return Tower("Adora", water=False, paths=paths)
    elif randInt == 10:
        return Tower("Admiral Brickell", water=True, paths=paths)
    elif randInt == 11:
        return Tower("Etienne", water=False, paths=paths)
    elif randInt == 12:
        return Tower("Sauda", water=False, paths=paths)
    elif randInt == 13:
        return Tower("Psi", water=False, paths=paths)


def primary():
    """Generates a random primary tower"""
    randInt = random.randint(0, 5)
    paths = genPaths()

    if randInt == 0:
        return Tower("Dart Monkey", water=False, paths=paths)
    elif randInt == 1:
        return Tower("Boomerang Monkey", water=False, paths=paths)
    elif randInt == 2:
        return Tower("Bomb Shooter", water=False, paths=paths)
    elif randInt == 3:
        return Tower("Tack Shooter", water=False, paths=paths)
    elif randInt == 4:
        return Tower("Ice Monkey", water=False, paths=paths)
    elif randInt == 5:
        return Tower("Glue Gunner", water=False, paths=paths)


def military():
    """Generates a random military tower"""
    randInt = random.randint(0, 6)
    paths = genPaths()

    if randInt == 0:
        return Tower("Sniper Monkey", water=False, paths=paths)
    elif randInt == 1:
        return Tower("Monkey Sub", water=True, paths=paths)
    elif randInt == 2:
        return Tower("Monkey Buccaneer", water=True, paths=paths)
    elif randInt == 3:
        return Tower("Monkey Ace", water=False, paths=paths)
    elif randInt == 4:
        return Tower("Heli Pilot", water=False, paths=paths)
    elif randInt == 5:
        return Tower("Mortar Monkey", water=False, paths=paths)
    elif randInt == 6:
        return Tower("Dartling Gunner", water=False, paths=paths)


def magic():
    """Generates a random magic tower"""
    randInt = random.randint(0, 4)
    paths = genPaths()

    if randInt == 0:
        return Tower("Wizard Monkey", water=False, paths=paths)
    elif randInt == 1:
        return Tower("Super Monkey", water=False, paths=paths)
    elif randInt == 2:
        return Tower("Ninja Monkey", water=False, paths=paths)
    elif randInt == 3:
        return Tower("Alchemist", water=False, paths=paths)
    elif randInt == 4:
        return Tower("Druid", water=False, paths=paths)


def support():
    """Generates a random support tower"""
    randInt = random.randint(0, 3)
    paths = genPaths()

    if randInt == 0:
        return Tower("Banana Farm", water=False, paths=paths)
    elif randInt == 1:
        return Tower("Spike Factory", water=False, paths=paths)
    elif randInt == 2:
        return Tower("Monkey Village", water=False, paths=paths)
    elif randInt == 3:
        return Tower("Engineer Monkey", water=False, paths=paths)


def genPaths():
    """Generates the paths for a tower and returns an array of three integers that represent the towers"""
    paths = [0, 0, 0]
    main = random.randint(0, 2)
    cross = random.randint(0, 2)
    while cross == main:
        cross = random.randint(0, 2)
        
    # assigns these global variables that determine the number of upgrades a tower can get
    paths[main] = mainUpgrades
    paths[cross] = crossUpgrades
    return paths


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

    def __init__(self, name, water, paths):
        self.name = name
        self.water = water
        self.paths = paths

    def __str__(self):
        return str(self.name + " (" + str(self.paths[0]) + ", " + str(self.paths[1]) + ", " + str(self.paths[2]) + ")")


if __name__ == "__main__":
    gen_UI()
