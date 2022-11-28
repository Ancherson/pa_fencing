import sys
import curses
import os
import numpy as np
import threading

class player:
    def __init__(self,num,range,attacking_speed,movement_speed,defending_range,blocking_time,score = 0):
        self.attack_range = range
        self.attacking_speed = attacking_speed
        self.movement_speed = movement_speed
        self.defending_range = defending_range
        self.blocking_time = blocking_time
        
        self.score = score
        self.num = num

        
players_actions = []
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

####################################################################################################



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

######################################################################################################

def start_stage(game_array):
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'b',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'b',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
    listener(game_array)
        
        
        
def draw_player(y,x,state,num_player,jump = False):
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
        screen.addstr(y-4,x-1,"   ")
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
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
    
def draw_score(score_1,score_2):
    screen.addstr(yoffset-6,(len(game_array)//2)-(len(f"[{score_1} - {score_2}]")//2),f"[{score_1} - {score_2}]")

#######################################################################################################
    
def listener(game_array):
    i=0
    y=0
    while(True):
        c = screen.getch()
        if c == ord('x'):
            break
        if c == curses.KEY_LEFT:
            left(2)
        if c == curses.KEY_RIGHT:
            right(2)
        if c == curses.KEY_UP:
            up(2)
        if c == curses.KEY_DOWN:
            down(2)
        if c == ord('q'):
            left(1)
        if c == ord('d'):
            right(1)
            
        if c == ord('+'):
            global score
            score += 1
            draw_score(score,0)
        
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()        

###################################################################################################


def left(num,jump = False) :
    x = np.where(game_array%3 == num)[0][0]
    if x - 1 < 0 :
        return
    if  game_array [x-1]%3 != 0 :
        return
    if not(jump) and game_array[x-1] == 3 :
        return
    if x-2 > 0 and game_array [x-2]%3 != 0:
        return
    game_array[x] -= num
    game_array [x-1] += num
    clear_player(yoffset,x+xoffset,num)
    draw_player(yoffset,x+xoffset-1,'a',num)
    x = np.where(game_array%3 == (num%2)+1)[0][0]
    draw_player(yoffset,x+xoffset,'a',(num%2)+1)
    
    
def right(num,jump = False) :
    x = np.where(game_array%3 == num)[0][0]
    if x + 1 >= len(game_array) :
        return
    if  game_array [x+1]%3 != 0 :
        return
    if not(jump) and game_array[x+1] == 3 :
        return
    if x+2 < len(game_array) and game_array [x+2]%3 != 0:
        return
    game_array[x] -= num
    game_array [x+1] += num
    clear_player(yoffset,x+xoffset,num)
    draw_player(yoffset,x+xoffset+1,'a',num)
    x = np.where(game_array%3 == (num%2)+1)[0][0]
    draw_player(yoffset,x+xoffset,'a',(num%2)+1)

def up(num) :
    x = np.where(game_array%3 == num)[0][0]
    clear_player(yoffset,x+xoffset,num)
    draw_player(yoffset-1,x+xoffset,'a',num)
    
def down(num) :
    x = np.where(game_array%3 == num)[0][0]
    clear_player(yoffset-1,x+xoffset,num)
    draw_player(yoffset,x+xoffset,'a',num)



############################################################################################################


stage = stage_read()
game_array = model(stage)
draw_score(10,0)

start_stage(game_array)
