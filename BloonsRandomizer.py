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

# constants
gamemodeList = ["Default", "Primary Only", "Military Only", "Magic Only", "Support Only"]
defaultMessage = "Player Not Active"


def gen_UI():
    """Creates the UI upon launch"""
    global players
    global gamemode

    # define the layout of the tabs
    settings = [[sg.Text('Number of Players'),
                 sg.Combo(["1", "2", "3", "4"], key='ui_players', enable_events=True, default_value="1")],
                [sg.Text('Gamemode'),
                 sg.Combo(gamemodeList, key='ui_gamemode', enable_events=True, default_value="Default")]]
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

        if event == sg.WIN_CLOSED:
            break
    window.close()


def playerListHandler(window):
    """Maintains the lists for each player"""
    for i in range(0, int(players)):
        window["ui_list" + str(i + 1)].update(generateMonkeyList())

    # clears out the empty players' listboxes
    count = int(players)
    while count < 4:
        window["ui_list" + str(count + 1)].update([defaultMessage])
        count += 1


def hero():
    """Generates a random hero"""
    randInt = random.randint(0, 13)

    if randInt == 0:
        return Tower("Quincy")
    elif randInt == 1:
        return Tower("Gwendolin")
    elif randInt == 2:
        return Tower("Striker Jones")
    elif randInt == 3:
        return Tower("Obyn Greenfoot")
    elif randInt == 4:
        return Tower("Geraldo")
    elif randInt == 5:
        return Tower("Captain Churchill")
    elif randInt == 6:
        return Tower("Benjamin")
    elif randInt == 7:
        return Tower("Ezili")
    elif randInt == 8:
        return Tower("Pat Fusty")
    elif randInt == 9:
        return Tower("Adora")
    elif randInt == 10:
        return Tower("Admiral Brickell")
    elif randInt == 11:
        return Tower("Etienne")
    elif randInt == 12:
        return Tower("Sauda")
    elif randInt == 13:
        return Tower("Psi")


def primary():
    """Generates a random primary tower"""
    randInt = random.randint(0, 5)

    if randInt == 0:
        return Tower("Dart Monkey")
    elif randInt == 1:
        return Tower("Boomerang Monkey")
    elif randInt == 2:
        return Tower("Bomb Shooter")
    elif randInt == 3:
        return Tower("Tack Shooter")
    elif randInt == 4:
        return Tower("Ice Monkey")
    elif randInt == 5:
        return Tower("Glue Gunner")


def military():
    """Generates a random military tower"""
    randInt = random.randint(0, 6)

    if randInt == 0:
        return Tower("Sniper Monkey")
    elif randInt == 1:
        return Tower("Monkey Sub")
    elif randInt == 2:
        return Tower("Monkey Buccaneer")
    elif randInt == 3:
        return Tower("Monkey Ace")
    elif randInt == 4:
        return Tower("Heli Pilot")
    elif randInt == 5:
        return Tower("Mortar Monkey")
    elif randInt == 6:
        return Tower("Dartling Gunner")


def magic():
    """Generates a random magic tower"""
    randInt = random.randint(0, 4)

    if randInt == 0:
        return Tower("Wizard Monkey")
    elif randInt == 1:
        return Tower("Super Monkey")
    elif randInt == 2:
        return Tower("Ninja Monkey")
    elif randInt == 3:
        return Tower("Alchemist")
    elif randInt == 4:
        return Tower("Druid")


def support():
    """Generates a random support tower"""
    randInt = random.randint(0, 3)

    if randInt == 0:
        return Tower("Banana Farm")
    elif randInt == 1:
        return Tower("Spike Factory")
    elif randInt == 2:
        return Tower("Monkey Village")
    elif randInt == 3:
        return Tower("Engineer Monkey")


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
    main = mainPath()
    cross = crossPath(main)

    # default generation
    if gamemode == "Default":
        monkeyList = [hero(),
                      primary(),
                      military(),
                      magic(),
                      support(),
                      "Main Path: " + str(main),
                      "Cross Path: " + str(cross)]
        return monkeyList

    # primary monkeys generation
    if gamemode == "Primary Only":
        monkeyList = [hero(),
                      primary(),
                      "Main Path: " + str(main),
                      "Cross Path: " + str(cross)]
        return monkeyList

        # military monkeys generation
    if gamemode == "Military Only":
        monkeyList = [hero(),
                      military(),
                      "Main Path: " + str(main),
                      "Cross Path: " + str(cross)]
        return monkeyList

    # magic monkeys generation
    if gamemode == "Magic Only":
        monkeyList = [hero(),
                      magic(),
                      "Main Path: " + str(main),
                      "Cross Path: " + str(cross)]
        return monkeyList

    # support monkeys generation
    if gamemode == "Support Only":
        monkeyList = [hero(),
                      support(),
                      "Main Path: " + str(main),
                      "Cross Path: " + str(cross)]
        return monkeyList


class Tower:
    """Contains all relevant data for a tower in-game"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


if __name__ == "__main__":
    gen_UI()
