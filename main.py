import sys
import curses
import os
import numpy as np
import threading

class player:
    def __init__(self,num,range,attacking_speed,movement_speed,defending_range,blocking_time):
        self.num = num
        self.attack_range = range
        self.attacking_speed = attacking_speed
        self.movement_speed = movement_speed
        self.defending_range = defending_range
        self.blocking_time = blocking_time
        
head = "<o>"
arm1  = "|_"
arm2  = "_| "
hips = "|"
legs1 = "/|"
legs2 = "|\\"
attack = "_"
block1 = "|"
rest1 = "\\"
rest2 = "/"

obstacle = "\u2588"
xoffset = 2
yoffset = 9

screen = curses.initscr()


def stage_read():
    if len(sys.argv) == 1:
        stage_file = os.path.abspath("/mnt/d/Informatique/M1/Prog_av/pa_fencing/stage1.ffscene")
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
    return game_array


def start_stage(game_array):
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    # character = "<o>\n |_/\n |\n/|"
    # character_empty = "   \n    \n  \n  \n \n"
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'b',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'b',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt,obstacle)
    painter(game_array)
        
def draw_player(y,x,state,num_player,jump = False):
    # clear_player(y,x,state,num_player,jump)
    if(jump) :
        y-= 1
    if num_player == 1 :
        screen.addstr(y-4,x-1,head)
        screen.addstr(y-3,x,arm1)
        screen.addstr(y-2,x,hips)
        screen.addstr(y-1,x-1,legs1)
        if state == 'a':
            screen.addstr(y-3,x+2,attack)
        elif state == 'b':
            screen.addstr(y-3,x+2,block1)
        else :
            screen.addstr(y-2,x+2,rest1)
                
    else :
        screen.addstr(y-4,x-1,head)
        screen.addstr(y-3,x-1,arm2)
        screen.addstr(y-2,x,hips)
        screen.addstr(y-1,x,legs2)
        if state == 'a':
            screen.addstr(y-3,x-2,attack)
        elif state == 'b':
            screen.addstr(y-3,x-2,block1)
        else :
            screen.addstr(y-2,x-2,rest2)
            
def clear_player(y,x,num_player,jump = False):
    if(jump) :
        y-= 1
    if num_player == 1 :
        screen.addstr(y-4,x-1,"  ")
        screen.addstr(y-3,x,"  ")
        screen.addstr(y-2,x," ")
        screen.addstr(y-1,x-1,"  ")
        screen.addstr(y-3,x+2," ")
        screen.addstr(y-2,x+2," ")
                
    else :
        screen.addstr(y-4,x-1,"   ")
        screen.addstr(y-3,x-1,"  ")
        screen.addstr(y-2,x," ")
        screen.addstr(y-1,x,"  ")
        screen.addstr(y-3,x-2," ")
        screen.addstr(y-2,x-2," ")
    
def painter(game_array):
    
    i=0
    y=0
    while(True):
        c = screen.getch()
        if c == ord('q'):
            break
        if c == curses.KEY_RIGHT:
            mouv()
        
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()        


def mouv() :
    x = np.where(game_array%3 == 2)[0][0]
    game_array[x] -= 2
    game_array [x-1] += 2
    clear_player(9,x+xoffset,2)
    draw_player(9,x+xoffset-1,'a',2)



stage = stage_read()
game_array = model(stage)
start_stage(game_array)
