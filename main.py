import sys
import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
head = "<o>"
arm =  " |_/"
low =  " |"
legs = "/|"
print(head)
print(arm)
print(low)
print(legs)


stdscr.addstr(head)
stdscr.refresh()
i=0
while(True):
    c = stdscr.getch()
    if c == ord('s'):
        break
    elif c == ord('a'):
        stdscr.addstr(i+1,0,arm)
        i+=1
    elif c== ord('z'):
        stdscr.addstr(i+1,0,low)
        i += 1

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
