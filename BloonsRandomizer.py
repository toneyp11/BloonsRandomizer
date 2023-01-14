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
waterBan = False
heroEnabled = True
mainUpgrades = 5
crossUpgrades = 2
numPrimary = 1
numMilitary = 1
numMagic = 1
numSupport = 1

# constants
defaultMessage = "Player Not Active"
maxMonkeys = 5


def gen_UI():
    """Creates the UI upon launch"""
    global players, waterBan, heroEnabled, numPrimary, numMilitary, numMagic, numSupport

    # define the layout of the tabs
    settings = [[sg.Text('Number of Players'),
                # number of players
                 sg.Combo(["1", "2", "3", "4"], key='ui_players', enable_events=True, default_value="1")],
                # number of primary towers
                [sg.Text('Primary Towers', size=10), sg.InputText(key='ui_primary', size=5, default_text="1"),
                 sg.Submit(key='ui_primarySub')],
                # number of military towers
                [sg.Text('Military Towers', size=10), sg.InputText(key='ui_military', size=5, default_text="1"),
                 sg.Submit(key='ui_militarySub')],
                # number of magic towers
                [sg.Text('Magic Towers', size=10), sg.InputText(key='ui_magic', size=5, default_text="1"),
                 sg.Submit(key='ui_magicSub')],
                # number of support towers
                [sg.Text('Support Towers', size=10), sg.InputText(key='ui_support', size=5, default_text="1"),
                 sg.Submit(key='ui_supportSub')],
                # water tower config
                [sg.Text('Ban Water Towers'),
                 sg.Checkbox('', key='ui_waterban', enable_events=True)],
                # hero config
                [sg.Text('Enable Hero'),
                 sg.Checkbox('', key='ui_hero', enable_events=True, default=True)]
                ]

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

        # primary config
        if event == 'ui_primarySub':
            tempNum = parseTowerCount(values['ui_primary'])
            if tempNum == -1:
                sg.Popup('Please input an integer from 0 to ' + str(maxMonkeys), title="Error")
            else:
                numPrimary = tempNum

        # military config
        if event == 'ui_militarySub':
            tempNum = parseTowerCount(values['ui_military'])
            if tempNum == -1:
                sg.Popup('Please input an integer from 0 to ' + str(maxMonkeys), title="Error")
            else:
                numMilitary = tempNum

        # magic config
        if event == 'ui_magicSub':
            tempNum = parseTowerCount(values['ui_magic'])
            if tempNum == -1:
                sg.Popup('Please input an integer from 0 to ' + str(maxMonkeys), title="Error")
            else:
                numMagic = tempNum

        # support config
        if event == 'ui_supportSub':
            tempNum = parseTowerCount(values['ui_support'])
            if tempNum == -1:
                sg.Popup('Please input an integer from 0 to ' + str(maxMonkeys), title="Error")
            else:
                numSupport = tempNum

        # water ban config
        if event == 'ui_waterban':
            waterBan = values['ui_waterban']

        # enable hero config
        if event == 'ui_hero':
            heroEnabled = values['ui_hero']

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


def parseTowerCount(userInput):
    """Takes the user inputted value from the number of monkeys inputs and ensures it is valid. Return -1 if invalid"""
    try:
        towerNum = int(userInput)
        if towerNum < 0 or towerNum > maxMonkeys:
            return -1
        return towerNum
    except ValueError:
        return -1


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

    monkeyList = []

    # generate hero if enabled
    if heroEnabled:
        monkeyList.append(hero())

    # generate primary tower(s)
    for i in range(0, numPrimary):
        monkeyList.append(primary())

    # generate military tower(s)
    for i in range(0, numMilitary):
        monkeyList.append(military())

    # generate magic tower(s)
    for i in range(0, numMagic):
        monkeyList.append(magic())

    # generate support tower(s)
    for i in range(0, numSupport):
        monkeyList.append(support())

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
