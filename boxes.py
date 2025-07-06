#####       boxes.py       #####
# 
# Boxes is a template for TUI python projects
#
# Boxes uses curses, with comes with python, so nothing must be installed additionally
# 
#####      made by L7      #####

# Copyright (c) 2025
# Legende_7 [On Github: IamLegende7]  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER OR CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, 
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) 
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import curses

def tui(stdscr):
    curses.curs_set(0)  # Enable cursor visibility

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Helping with some function stuff
    def nothing():
        return
    def bye():
        quit()

    # Drawing Functions
    def box(height: int, width: int, y: int, x: int, top: str, side: str, tl: str, tr: str=None, bl: str=None, br: str=None,):
        if tr == None:
            tr = tl
        if bl == None:
            bl = tl
        if br == None:
            br = tl
        # Draw a box
        stdscr.addstr(y, x, f"{tl}" + f"{top}" * (width - 2) + f"{tr}")  # Top border
        stdscr.addstr(y + height - 1, x, f"{bl}" + f"{top}" * (width - 2) + f"{br}")  # Bottom border
        for i in range(1, height - 1):
            stdscr.addstr(y + i, 0, f"{side}")
            stdscr.addstr(y + i, x + width - 1, f"{side}")
        stdscr.refresh()

    def window(height: int, width: int, y: int=0, x: int=0):  # Have to expand on this furtherw
        win = curses.newwin(height, width, y, x)
        win.border(0)
        return win

    def menu(y: int, x: int, options: list, command: list, selected_option: int=0, bold: bool=False, allow_back: bool=False):
        # Display the menu
        for idx, option in enumerate(options):
            if idx == selected_option:
                if bold:
                    stdscr.addstr(y + idx, x, option, curses.A_REVERSE | curses.A_BOLD)  # Highlight selected option
                else:
                    stdscr.addstr(y + idx, x, option, curses.A_REVERSE)  # Highlight selected option
            else:
                if bold:
                    stdscr.addstr(y + idx, x, option, curses.A_BOLD)
                else:
                    stdscr.addstr(y + idx, x, option)
        stdscr.refresh()
        old_selected_option = None

        while True:
            # Refresh the menu
            for idx, option in enumerate(options):
                if idx == selected_option:
                    if bold:
                        stdscr.addstr(y + idx, x, option, curses.A_REVERSE | curses.A_BOLD)  # Highlight selected option
                    else:
                        stdscr.addstr(y + idx, x, option, curses.A_REVERSE)  # Highlight selected option
                if idx == old_selected_option:
                    if bold:
                        stdscr.addstr(y + idx, x, option, curses.A_BOLD)  # "Unhighlight" the option no longer selected
                    else:
                        stdscr.addstr(y + idx, x, option)  # "Unhighlight" the option no longer selected
            stdscr.refresh()

            # Get the pressed key
            key = stdscr.getch()

            # Process keypresses
            if key == curses.KEY_UP:
                if selected_option - 1 >= 0:
                    old_selected_option = selected_option
                    selected_option -= 1  # Move up
            elif key == curses.KEY_DOWN:
                if selected_option + 1 <= len(options) - 1:
                    old_selected_option = selected_option
                    selected_option += 1  # Move down

            elif key == curses.KEY_ENTER or key == 10:  # Enter key
                command[selected_option]()
                return False, selected_option
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if allow_back:
                    return True, selected_option
    
    # Pages
    def example_text():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "Example Text")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(5, 2, "[ Hewo! ] >  UWU")
        stdscr.getch()
        main()
    
    def no_back(sel):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "No")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(5, 2, "U cant back out of tis <3")
        stdscr.addstr(7, 2, f"Selected option was: {sel}")
        stdscr.getch()
        main()

    def main():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")  # Example for the box function
        stdscr.addstr(1, 2, "Main Menu")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        back, sel = menu(5, 2, ["Say 'UWU'", "Get the Hell out of there"], [example_text, bye], 0, True, True)  # Example on how to use the menu function
        if back:    # You can also do something when backspace is pressed (like go back one page or something) ... have to set allow_back = True
            no_back(sel)

    # Main code
    main() # Calling the main page

if __name__ == "__main__":
    curses.wrapper(tui)