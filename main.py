import sys
import curses
import os
import numpy as np

def start_stage():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    # character = "<o>\n |_/\n |\n/|"
    # character_empty = "   \n    \n  \n  \n \n"


    stdscr.refresh()
    i=0
    y=0
    while(True):
        sys.stdin.reconfigure(newline=None)
        c = stdscr.getch()
        if c == ord('s'):
            stdscr.addstr(i,y,"s")
            y+= 1
            
        elif c == ord('q'):
            stdscr.addstr(i,y,"q")
            y+= 1
        elif c == ord('c'):
            stdscr.addstr(i,y,"c")
            y+= 1
        elif c == curses.KEY_LEFT:
            y-=1
        elif c == ord('m'):
            break
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def stage_read():
    if len(sys.argv) == 1:
        stage_file = os.path.abspath("stage1.ffscene")
    else :
        if sys.argv[1].split(".")[-1] != "ffscene" :
            print("enter a .ffscene file please !")
        stage_file = os.path.abspath(sys.argv[1])

    with open(stage_file) as file :
       return file.readline()
        

def model(stage):
    game_array = np.zeros(len(stage),dtype=int)
    game_array[stage.find('1')] = 1
    game_array[stage.find('2')] = 2
    for (count,char) in enumerate(stage):
        if char == 'x':
            game_array[count] = 3
    print(game_array)
    

# print("<o>\n |_/\n |\n/|   \u2588")

# print("############")

stage = stage_read()
model(stage)
