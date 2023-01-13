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
players = 0


def gen_UI():
    """Creates the UI upon launch"""
    global players

    # define the layout of the tabs
    settings = [[sg.Text('Number of Players'), sg.Combo(["1", "2", "3", "4"], key='ui_players', enable_events=True)]]
    results = [[sg.Button("Generate"),
                sg.Listbox(values=["No active player 1"], key="ui_list1", size=(30, 30)),
                sg.Listbox(values=["No active player 2"], key="ui_list2", size=(30, 30)),
                sg.Listbox(values=["No active player 3"], key="ui_list3", size=(30, 30)),
                sg.Listbox(values=["No active player 4"], key="ui_list4", size=(30, 30))]]

    # combine the tabs
    tabgrp = [[sg.TabGroup([[sg.Tab('Settings', settings),
                           sg.Tab('Monkey Results', results)]])]]

    # create the window
    window = sg.Window("Bloons Randomizer", tabgrp)

    # accept user input until the window closes
    while True:
        event, values = window.read()

        if event == 'ui_players':
            players = values['ui_players']

        if event == 'Generate':
            for i in range(0, int(players)):
                window["ui_list" + str(i+1)].update(generateMonkeyList())

        if event == sg.WIN_CLOSED:
            break
    window.close()


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
    monkeyList = [hero(),
                  primary(),
                  military(),
                  magic(),
                  support(),
                  "Main Path: " + str(main),
                  "Cross Path: " + str(crossPath(main))]
    return monkeyList


class Tower:
    """Contains all relevant data for a tower in-game"""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


if __name__ == "__main__":
    gen_UI()
