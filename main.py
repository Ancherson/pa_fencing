import sys
import curses
import os
import numpy as np
import threading
import time

class player:
    def __init__(self,num,range,attacking_speed,movement_speed,defending_range,blocking_time,score = 0,state = 's'):
        self.attack_range = int(range)
        self.attacking_speed = int(attacking_speed)
        self.movement_speed = int(movement_speed)
        self.defending_range = int(defending_range)
        self.blocking_time = int(blocking_time)
        
        self.score = int(score)
        self.num = int(num)
        
        self.state = state
    
    def toString(self) :
        return (f"{self.attack_range}\n{self.attacking_speed}\n{self.movement_speed}\n{self.defending_range}\n{self.blocking_time}\n{self.score}\n{self.num}\n")
   
   
   
    
alarm_clock = threading.Event()
finish = threading.Event()
finish.clear()

pause = threading.Lock()
players_lock = threading.Lock()


players_actions = [[(),()],[(),()]]
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
        stage_file = ("stage1.ffscene")
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
    curses.curs_set(0)
    screen.timeout(300)
    curses.cbreak()
    screen.keypad(True)
    screen.resize(10, 60)
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'s',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'s',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
    screen.refresh()
        
def reset_stage():
    
    for i in range (0,6):
        screen.addstr(yoffset-i,xoffset," "*len(game_array))
    screen.refresh()
    screen.addstr(yoffset,xoffset,"#"*len(game_array))
    draw_player(yoffset,np.where(game_array%3 == 1)[0][0]+xoffset,'s',1)
    draw_player(yoffset,np.where(game_array%3 == 2)[0][0]+xoffset,'s',2)
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
    screen.refresh()
    
def clear_stage():
    for i in range (0,5):
        screen.addstr(yoffset-i,xoffset," "*len(game_array))
    screen.refresh()
        
        
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
    screen.refresh()
            
def clear_player(y,x,num_player,jump = False):
    if jump :
        y-=1
    if num_player == 1 :
        screen.addstr(y-4,x-1,"   ")
        screen.addstr(y-3,x,"  ")
        screen.addstr(y-2,x," ")
        screen.addstr(y-1,x-1,"   ")
        screen.addstr(y-3,x+1,"  ")
        screen.addstr(y-2,x+1,"  ")
                
    else :
        screen.addstr(y-4,x-1,"   ")
        screen.addstr(y-3,x-1,"  ")
        screen.addstr(y-2,x," ")
        screen.addstr(y-1,x,"   ")
        screen.addstr(y-3,x-2," ")
        screen.addstr(y-2,x-3,"  ")
    for elt in np.where(game_array == 3)[0] :
        screen.addch(yoffset-1,elt+xoffset,obstacle)
    screen.refresh()
        
def draw_score(score_1,score_2):
    screen.addstr(yoffset-6,(len(game_array)//2)-(len(f"[{score_1} - {score_2}]")//2),f"[{score_1} - {score_2}]")
    screen.refresh()
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
    if jump :
        clear_player(yoffset-1,x+xoffset,num)
        draw_player(yoffset-1,x+xoffset-1,players[num-1].state,num)
    else :
        clear_player(yoffset,x+xoffset,num)   
        draw_player(yoffset,x+xoffset-1,players[num-1].state,num)
    x = np.where(game_array%3 == (num%2)+1)[0][0]
    draw_player(yoffset,x+xoffset,players[(num%2)].state,(num%2)+1)
    screen.refresh()
    
    
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
    if jump :
        clear_player(yoffset-1,x+xoffset,num)
        draw_player(yoffset-1,x+xoffset+1,players[num-1].state,num)
    else :
        clear_player(yoffset,x+xoffset,num)
        draw_player(yoffset,x+xoffset+1,players[num-1].state,num)
    x = np.where(game_array%3 == (num%2)+1)[0][0]
    draw_player(yoffset,x+xoffset,players[(num%2)].state,(num%2)+1)
    screen.refresh()

def up(num) :
    x = np.where(game_array%3 == num)[0][0]
    clear_player(yoffset,x+xoffset,num)
    draw_player(yoffset-1,x+xoffset,players[num-1].state,num)
    screen.refresh()
    
def down(num) :
    x = np.where(game_array%3 == num)[0][0]
    if game_array[x] > 2 :
        scoring((num%2)+1)
        return
    clear_player(yoffset-1,x+xoffset,num)
    draw_player(yoffset,x+xoffset,players[num-1].state,num)
    screen.refresh()

def jump_left(num,sequence) :
    x = np.where(game_array%3 == num)[0][0]
    if sequence == 1 or sequence == 2 :
        left(num,True)
        players_actions[num-1][1][1][0] = players[num-1].movement_speed 
        players_actions[num-1][1][1][1] = sequence+1
    elif sequence == 0 :
        up(num)
        players_actions[num-1][1][1][0] = players[num-1].movement_speed 
        players_actions[num-1][1][1][1] = sequence+1
    else :
        down(num)
        players_actions[num-1][1] = ()

def jump_right(num,sequence):
    x = np.where(game_array%3 == num)[0][0]
    if sequence == 1 or sequence == 2 :
            right(num,True)
            players_actions[num-1][1][1][0] = players[num-1].movement_speed
            players_actions[num-1][1][1][1] = sequence+1
    elif sequence == 0 :
        up(num)
        players_actions[num-1][1][1][0] = players[num-1].movement_speed
        players_actions[num-1][1][1][1] = sequence+1
    else :
        down(num)
        players_actions[num-1][1] = ()
        
       
 
#####################################################################################################        

# OFFENSIVE AND DEFENSIVE ACTION

def scoring(num = 0) :
    if num != 0 :
        players[num-1].score += 1
    if players[num-1].score == 15 :
        finish.set()
        alarm_clock.set()
        screen.keypad(False)
        curses.echo()
        curses.curs_set(1)
        curses.nocbreak()
        curses.endwin()

        print(f"PLayer {num} won ! {players[0].score} - {players[1].score}")        
        return

    clear_stage()
    global game_array
    game_array = model(stage)
    reset_stage()
    draw_score(players[0].score,players[1].score)
    for player in players_actions :
        for action in player :
            action = ()
    
def attack(num_attacker):
    num_defender = (num_attacker%2)+1
    x = np.where(game_array%3 == num_attacker)[0][0]
    y = np.where(game_array%3 == num_defender)[0][0]
    
    if players[num_attacker-1].attack_range >= abs(y-x) :
        if  players[num_defender-1].state == 'b' and players[num_defender-1].defending_range >= abs(y-x):
            return
        elif players[num_defender-1].state == 'a' and players[num_defender-1].attack_range >= abs(y-x) :
            scoring()
        else :
            scoring(num_attacker)
    
############################################################################################################

def loop(fps):
    while(True) :
        time.sleep(1/fps)
        pause.acquire()
        pause.release()
        players_lock.acquire()
        for player in players_actions :
            for action in player :
                if action :
                    action[1][0] -= 1
        players_lock.release()
        alarm_clock.set()
        if finish.is_set() :
            break
    alarm_clock.set()
    
def actualizer():
    while(True):
        alarm_clock.wait()
        alarm_clock.clear()
        players_lock.acquire()
        for i in range(len(players_actions)) :
            action = players_actions[i][0] 
            if action and action[1][0] > 0:
                    if action[0] == 'a' and players[i].state != 'a':
                        players[i].state = 'a'
                        x = np.where(game_array%3 == i+1)[0][0]
                        if (players_actions[i][1]) and (players_actions[i][1][0] == 'i' or players_actions[i][1][0] == 'k') :
                            clear_player(yoffset,x+xoffset,i+1,True)
                            draw_player(yoffset,x+xoffset,'a',i+1,True)
                        else :
                            clear_player(yoffset,x+xoffset,i+1)
                            draw_player(yoffset,x+xoffset,'a',i+1)
                        attack(i+1)
                    if action[0] == 'b' and players[i].state != 'b':
                        players[i].state = 'b'
                        x = np.where(game_array%3 == i+1)[0][0]
                        if (players_actions[i][1]) and (players_actions[i][1][0] == 'i' or players_actions[i][1][0] == 'k') :
                            clear_player(yoffset,x+xoffset,i+1,True)
                            draw_player(yoffset,x+xoffset,'b',i+1,True)
                        else :
                            clear_player(yoffset,x+xoffset,i+1)
                            draw_player(yoffset,x+xoffset,'b',i+1)
                    
                        
            else :
                if players[i].state != 's' :
                    if (players_actions[i][1]) and (players_actions[i][1][0] == 'i' or players_actions[i][1][0] == 'k') :
                        x = np.where(game_array%3 == i+1)[0][0]
                        clear_player(yoffset,x+xoffset,i+1,True)
                        draw_player(yoffset,x+xoffset,'s',i+1,True)
                    else :
                        x = np.where(game_array%3 == i+1)[0][0]
                        clear_player(yoffset,x+xoffset,i+1)
                        draw_player(yoffset,x+xoffset,'s',i+1)
                players_actions[i][0] = ()
                players[i].state = 's'

                
                    
            mouv = players_actions[i][1]
            if mouv and mouv[1][0] <= 0:
                state = mouv[0]
                if state == 'l' :
                    left(i+1)
                    players_actions[i][1] = ()
                elif state == 'r' :
                    right(i+1)
                    players_actions[i][1] = ()
                elif state == 'i' :
                    jump_left(i+1,mouv[1][1])
                elif state == 'k' :
                    jump_right(i+1,mouv[1][1])
            
        players_lock.release()
        if finish.is_set() :
            break
    
    
def listener():
    while(True):
        c = screen.getch()
        if pause.locked() :
            if c == curses.KEY_F1 :
                pause.release()
                continue
            elif c == ord('x'):
                break  
            else :
                continue
            
        
        if c == curses.KEY_LEFT:
            players_lock.acquire()
            if not players_actions[2-1][1] :
                players_actions[2-1][1] = ('l',[players[2-1].movement_speed])
            players_lock.release()
            
        elif c == curses.KEY_RIGHT:
            players_lock.acquire()
            if not players_actions[2-1][1] :
                players_actions[2-1][1] = ('r',[players[2-1].movement_speed])
            players_lock.release()
            
        elif c == ord('l'):
            players_lock.acquire()
            if not players_actions[2-1][1] :
                players_actions[2-1][1] = ('i',[players[2-1].movement_speed,0])
            players_lock.release()
            
        elif c == ord('m'):
            players_lock.acquire()
            if not players_actions[2-1][1] :
                players_actions[2-1][1] = ('k',[players[2-1].movement_speed,0])
            players_lock.release()
            
        elif c == ord('o'):
            players_lock.acquire()
            if not players_actions[2-1][0] :
                players_actions[2-1][0] = ('a',[players[2-1].attacking_speed])
            players_lock.release()
            
        elif c == ord('p'):
            players_lock.acquire()
            if not players_actions[2-1][0] :
                players_actions[2-1][0] = ('b',[players[2-1].blocking_time])
            players_lock.release()    
            
                
                
                
        elif c == ord('q'):
            players_lock.acquire()
            if not players_actions[1-1][1] :
                players_actions[1-1][1] = ('l',[players[1-1].movement_speed])
            players_lock.release()
            
        elif c == ord('d'):
            players_lock.acquire()
            if not players_actions[1-1][1] :
                players_actions[1-1][1] = ('r',[players[1-1].movement_speed])
            players_lock.release()   
                 
        elif c == ord('a'):
            players_lock.acquire()
            if not players_actions[1-1][1] :
                players_actions[1-1][1] = ('i',[players[1-1].movement_speed,0])
            players_lock.release()
            
        elif c == ord('e'):
            players_lock.acquire()
            if not players_actions[1-1][1] :
                players_actions[1-1][1] = ('k',[players[1-1].movement_speed,0])
            players_lock.release()
            
        elif c == ord('z'):
            players_lock.acquire()
            if not players_actions[1-1][0] :
                players_actions[1-1][0] = ('a',[players[1-1].attacking_speed])
            players_lock.release() 
            
        elif c == ord('s'):
            players_lock.acquire()
            if not players_actions[1-1][0] :
                players_actions[1-1][0] = ('b',[players[1-1].blocking_time])
            players_lock.release()   
            
        elif c == ord('x'):
            break        
        elif c == curses.KEY_F1 :
            if pause.locked():
                pause.release()
            else :
                pause.acquire()
                
        if finish.is_set() :
            break   
        
        
    if pause.locked():
        pause.release() 
    finish.set()
    alarm_clock.set()
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.curs_set(1)
    curses.endwin() 



stage = stage_read()
game_array = model(stage)
draw_score(0,0)

p = player_read("fast_arm.char",1)
p2 = player_read("fast_arm.char",2)
players = [p,p2]

start_stage(game_array)
thread_listening = threading.Thread(target=listener,)
thread_actualizer = threading.Thread(target=actualizer,)
thread_fps = threading.Thread(target=loop,args = (10,))
thread_fps.start()
thread_listening.start()
thread_actualizer.start()

