import curses           # For now you still need to import curses
from boxes import TUI

# A simple example for boxes.py usage

def main(stdscr):

    # you can pass functions into the menu contents
    # here is one to quit the program
    def quit_app():
        tui.cleanup() # Dont worry; the curses wrapper will make shure nothing will break.
        quit()

    # Make a new Menu intance
    tui = TUI()

    # Make new menu instance
    main_menu = tui.Menu(stdscr, [("Hello", lambda: None), ("Example Page", lambda: None), ("Quit", quit_app)])
    
    # set the key to anything. Its recomended do use ```None```
    key = None

    # Main loop
    while True:
        # tick the menu and pass in the keypress
        main_menu.tick(key)
        stdscr.refresh()
        key = stdscr.getch()  # Make shure to run getch() **after** ticking the menu

if __name__ == "__main__":
    curses.wrapper(main) # Call using the curses wrapper for security when crashing
                         # Boxes.py doesn't support **not** using the wrapper for now (not planning on adding this)