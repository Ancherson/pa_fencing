import sys
import curses
import os


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
        c = stdscr.getch()
        if c == ord('s'):
            break
        elif c == ord('v'):
            break
        elif c == ord('c'):
            break
        elif c == ord('d'):
            # stdscr.addstr(i,y,character_empty)
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
        



print("<o>\n |_/\n |\n/|   \u2588")

print("############")
