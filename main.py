import sys
import curses
import os
import numpy as np
import threading
import time

class player:
    def __init__(self,num,range,attacking_speed,movement_speed,defending_range,blocking_time,score = 0,state = ('r',)):
        self.attack_range = range
        self.attacking_speed = attacking_speed
        self.movement_speed = movement_speed
        self.defending_range = defending_range
        self.blocking_time = blocking_time
        
        self.score = score
        self.num = num
        
        self.state = state
    
    def toString(self) :
        return (f"{self.attack_range}\n{self.attacking_speed}\n{self.movement_speed}\n{self.defending_range}\n{self.blocking_time}\n{self.score}\n{self.num}\n")
   
   
   
    
alarm_clock = threading.Event()
pause = threading.Lock()

players_actions = []
players = []
running = True

head = "<o>"
arm1  = "|_"
arm2  = "_| "
hips = "|"
legs1 = "/|"
legs2 = "|\\"
attack_char = "_"
block1 = "|"
rest1 = "\\"
rest2 = "/"

obstacle = "\u2588"
xoffset = 2
yoffset = 9


screen = curses.initscr()

####################################################################################################

# INITIALIZING FUNCTION


def stage_read():
    if len(sys.argv) == 1:
        stage_file = os.path.abspath("/mnt/d/Informatique/M1/Prog_av/pa_fencing/stage1.ffscene")
    else :
        if sys.argv[1].split(".")[-1] != "ffscene" :
            print("enter a .ffscene file please !")
        stage_file = os.path.abspath(sys.argv[1])

    with open(stage_file) as file :
       return file.readline()
   
def player_read(file_name,num):
    if file_name.split(".")[-1] != "char" :
        print("enter a .char file please !")
    with open(file_name) as file:
        val = file.read().split()
        return player(num,val[0],val[1],val[2],val[3],val[4])

            
   
   
def model(stage):
    game_array = np.zeros(len(stage),dtype=int)
    game_array[stage.find('1')] = 1
    game_array[stage.find('2')] = 2
    for (count,char) in enumerate(stage):
        if char == 'x':
            game_array[count] = 3
    return game_array

######################################################################################################

# DRAWING FUNCTIONS

def start_stage(game_array):
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'b',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'b',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
        
def reset_stage(game_array):
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'b',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'b',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
        
        
def draw_player(y,x,state,num_player,jump = False):
    if(jump) :
        y-= 1
    if num_player == 1 :
        screen.addstr(y-4,x-1,head)
        screen.addstr(y-3,x,arm1)
        screen.addstr(y-2,x,hips)
        screen.addstr(y-1,x-1,legs1)
        if state == 'a':
            screen.addstr(y-3,x+2,attack_char)
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
            screen.addstr(y-3,x-2,attack_char)
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
    

###################################################################################################

# DEPLACEMENT

def left(num,jump = False) :
    x = np.where(game_array%3 == num)[0][0]
    if x - 1 < 0 :
        return
    if  game_array [x-1]%3 != 0 :
        if jump :
            scoring((num%2)+1)
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
    if  game_array [x+1]%3 != 0:
        if jump :
            scoring((num%2)+1)
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
    if game_array[x] > 2 :
        scoring((num%2)+1)
    clear_player(yoffset-1,x+xoffset,num)
    draw_player(yoffset,x+xoffset,'a',num)

def jump_left(num,sequence) :
    x = np.where(game_array%3 == num)[0][0]
    if sequence != 0 or sequence != 3 :
        left(num,True)
        players_actions[num-1][1][1] = (players[num-1].movement_speed,sequence+1)
    elif sequence == 0 :
        up(num)
        players_actions[num-1][1][1] = (players[num-1].movement_speed,sequence+1)
    else :
        down(num)
        players_actions[num-1][1] = ()

def jump_right(num,sequence):
    x = np.where(game_array%3 == num)[0][0]
    if sequence != 0 or sequence != 3 :
            right(num,True)
            players_actions[num-1][1][1] = (players[num-1].movement_speed,sequence+1)
    elif sequence == 0 :
        up(num)
        players_actions[num-1][1][1] = (players[num-1].movement_speed,sequence+1)
    else :
        down(num)
        players_actions[num-1][1] = ()
        
       
 
#####################################################################################################        

# OFFENSIVE AND DEFENSIVE ACTION

def scoring(num = 0) :
    if num != 0 :
        players[num-1].score += 1
    if players[num-1].score == 15 :
        running = False
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()
        print(f"PLayer {num} won ! {players[num-1].score} - {players[num%2].score}")        
        return
    global game_array
    game_array = model(stage)
    reset_stage()
    for player in players_actions :
        for action in player :
            action = ()
    
def attack(num_attacker):
    num_defender = (num_attacker%2)+1
    x = np.where(game_array%3 == num_attacker)[0][0]
    y = np.where(game_array%3 == (num_defender)+1)[0][0]
    
    if num_attacker == 1 :
        if y in game_array[x:x+players_actions[num_attacker-1][0][0]] :
            if players_actions[num_defender-1][0][0] == 'b' and players_actions[num_defender-1][0][1][1] >= y-x:
                return
            elif players_actions[num_defender-1][0][0] == 'a' and players_actions[num_defender-1][0][1][1] >= y-x :
                scoring()
            else :
                scoring(num_attacker)
    elif num_attacker == 2 :
        if y in game_array[x-players_actions[num_attacker-1][0][0]:x] :
            if players_actions[num_defender-1][0][0] == 'b' and players_actions[num_defender-1][0][1][1] >= x-y:
                return
            elif players_actions[num_defender-1][0][0] == 'a' and players_actions[num_defender-1][0][1][1] >= x-y :
                scoring()
            else :
                scoring(num_attacker)
    
############################################################################################################

def loop(fps):
    while(running) :
        time.sleep(1/fps)
        threading.Lock.acquire(pause)
        threading.Lock.release(pause)
        threading.Lock.acquire(players_actions)
        for player in players_actions :
            for action in player :
                if action :
                    action[1][0] -= 1
        threading.Lock.release(players_actions)
        alarm_clock.clear()
    
def actualizer():
    while(running):
        alarm_clock.wait()
        threading.Lock.acquire(players_actions)
        for i in len(players_actions) :
            mouv = players_actions[i][1]
            if mouv and mouv[1] <= 0:
                state = mouv[0]
                if state == 'l' :
                    left(i+1)
                    mouv = ()
                elif state == 'r' :
                    right(i+1)
                    mouv = ()
                elif state == 'i' :
                    jump_left(i+1,mouv[1][2])
                elif state == 'k' :
                    jump_left(i+1,mouv[1][2])
            action = players_actions[i][0] 
            if action and action[1] > 0:
                    if action[0] == 'a' :
                        attack(i+1)
            else :
                action = ()
                    
        threading.Lock.release(players_actions)
    
    
    
def listener():
    while(running):
        c = screen.getch()
        
        if c == curses.KEY_LEFT:
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][1] :
                players_actions[2-1][1] = ('l',[players[2-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == curses.KEY_RIGHT:
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][1] :
                players_actions[2-1][1] = ('r',[players[2-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('l'):
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][1] :
                players_actions[2-1][1] = ('i',[players[2-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('m'):
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][1] :
                players_actions[2-1][1] = ('k',[players[2-1].movement_speed,0])
            threading.Lock.release(players_actions)
            
        elif c == ord('o'):
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][0] :
                players_actions[2-1][0] = ('a',[players[2-1].attacking_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('p'):
            threading.Lock.acquire(players_actions)
            if players_actions[2-1][0] :
                players_actions[2-1][0] = ('b',[players[2-1].blocking_time])
            threading.Lock.release(players_actions)    
            
                
                
                
        elif c == ord('q'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][1] :
                players_actions[1-1][1] = ('l',[players[1-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('d'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][1] :
                players_actions[1-1][1] = ('r',[players[1-1].movement_speed])
            threading.Lock.release(players_actions)   
                 
        elif c == ord('a'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][1] :
                players_actions[1-1][1] = ('i',[players[1-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('e'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][1] :
                players_actions[1-1][1] = ('k',[players[1-1].movement_speed])
            threading.Lock.release(players_actions)
            
        elif c == ord('z'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][0] :
                players_actions[1-1][0] = ('a',[players[1-1].attacking_speed])
            threading.Lock.release(players_actions) 
            
        elif c == ord('s'):
            threading.Lock.acquire(players_actions)
            if players_actions[1-1][0] :
                players_actions[1-1][0] = ('b',[players[1-1].blocking_time])
            threading.Lock.release(players_actions)   
        elif c == ord('x'):
            break        
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin() 
    running = False       




stage = stage_read()
game_array = model(stage)
draw_score(10,0)

p = player_read("fast_arm.char",1)
p2 = player_read("fast_arm.char",2)

thread_listening = threading.Thread(listener())
thread_actualizer = threading.Thread(actualizer())
thread_fps = threading.Thread(loop())
start_stage(game_array)
thread_listening.start()
thread_actualizer.start()
thread_actualizer.start()
