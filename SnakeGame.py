#!/usr/bin/env python3.4
# By Igoru99 (C) 2016 year
import time
import win32api
import pythoncom
import pyHook
import threading
import os
import random
from colorama import Fore, Back, Style, init


data = ['0' for i in range(200)]  # Game box 10*20
scores = 0  # Scores
python = [110,130,150]  # List of coordinats the snake
is_game = True  # Checking of game end
key = 1  # Pressed key


def OnKeyboardEvent(event):
    global key
    LEFT = win32api.GetKeyState(0x25)
    RIGHT = win32api.GetKeyState(0x27)
    UP = win32api.GetKeyState(0x26)
    DOWN = win32api.GetKeyState(0x28)
    if LEFT<0:
        key = 4
    elif RIGHT<0:
        key = 3
    elif UP<0:
        key = 2
    elif DOWN<0:
        key = 1

def EventListener():
    """
    Function for listening pressed keys
    """
    hm = pyHook.HookManager()
    hm.KeyAll = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

def ini():
    """
    Function of initialization the game
    """
    global data
    init()
    for i in range(0,20):
        data[i] = Back.WHITE +  '-' + Back.BLACK
    for i in range(0, 200, 20):
        data[i] = Back.WHITE +  '|' + Back.BLACK
    for i in range(19, 200, 20):
        data[i] = Back.WHITE +  '|' + Back.BLACK
    for i in range(181,199):
        data[i] = Back.WHITE +  '-' + Back.BLACK
    generate_eat()

def move(forward):
    """
    Function of move the snake
    """
    global python
    last_pos = int()
    data[python[0]] = '0'
    last_pos = python.pop(0)
    if forward == 1:  # down
        python.append(python[len(python)-1]+20)
    elif forward == 2:  # up
        python.append(python[len(python)-1]-20)
    elif forward == 3:  # right
        python.append(python[len(python)-1]+1)
    elif forward == 4:  # left
        python.append(python[len(python)-1]-1)
    if data[python[len(python)-1]] == Back.WHITE +  '-' + Back.BLACK or data[python[len(python)-1]] == Back.WHITE +  '|' + Back.BLACK or data[python[len(python)-1]] == Back.GREEN +  '*' + Back.BLACK:
        last_index = len(python)-1
        python.remove(python[last_index])
        new_python = []
        new_python.append(last_pos)
        new_python.extend(python)
        python = new_python.copy()
        game_end()
        show()
        return False
    elif data[python[len(python)-1]] == Back.YELLOW + '$' + Back.BLACK:
        global scores
        scores += 1
        add_body(last_pos)
        generate_eat()
        return True
    else:
        return True

def add_body(last_pos):
    """
    Increase the lenght of the snake
    """
    global python
    new_python = []
    new_python.append(last_pos)
    new_python.extend(python)
    python = new_python.copy()

def generate_eat():
    """
    Function of generation food
    """
    is_generate = False
    while is_generate is False:
        i = random.randint(0,199)
        if data[i] == '0':
            data[i] = Back.YELLOW + '$' + Back.BLACK
            is_generate = True

def game_end():
    global is_game
    is_game = False
    for i in range(63, 76):
        data[i] = Back.RED +  '-' + Back.BLACK
    data[63] = Back.RED + '+' + Back.BLACK
    data[75] = Back.RED + '+' + Back.BLACK
    for i in range(103, 116):
        data[i] = Back.RED + '-' + Back.BLACK
    data[103] = Back.RED + '+' + Back.BLACK
    data[115] = Back.RED + '+' + Back.BLACK
    t = 0
    l = '| Game end! |'
    for i in range(83,96):
        data[i] = Back.RED + l[t] + Back.BLACK
        t += 1
    return

def show():
    """
    Print game box in console
    """
    for i in python:
        if data[i] == '0' or data[i] == Back.YELLOW + '$' + Back.BLACK or data[i] == Back.GREEN + '*' + Back.BLACK:
            data[i] = Back.GREEN + '*' + Back.BLACK
    string = Back.WHITE + '|' + 18*'-' + '|\n' + '|' + 4*' ' + Back.BLUE + 'Scores: ' + str(scores) + Back.WHITE + (6-len(str(scores)))*' ' + '|\n' + Back.BLACK
    for i in range(10):
        for j in range(20*i, 20*i+20):
               string += data[j]
        else:
            string += '\n'
    print(string)
    

ini()
show()
time.sleep(1)

t = threading.Thread(target=EventListener) # Creating new threading for EventListener
t.daemon = True
t.start()

while True:  # Body of the game
    os.system('cls')
    if move(key) is False:
        break
    show()
    time.sleep(1)
    
input('Press Enter to exit.')
