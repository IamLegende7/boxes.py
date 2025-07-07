#####       boxes.py       #####
# 
# Boxes is a template for TUI python projects
#
# Boxes uses curses, with comes with python, so nothing must be installed additionally
# 
#####      made by L7      #####

# Copyright (c) 2025
# Legende_7  All rights reserved.
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
import os
from pathlib import Path

Dir_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(Dir_path)

# Check if a diary already exists    
txt = Path("Text.txt")
if not txt.is_file():
    # Create an empty file (or overwrite if it exists)
    with open("Text.txt", "w") as file:
        pass

def tui(stdscr):
    curses.curs_set(0)  # Disable cursor visibility

    # Support functions
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

    def window(height: int, width: int, y: int=0, x: int=0, border: bool=True):  # Have to expand on this furtherw
        win = curses.newwin(height, width, y, x)
        if border:
            win.border(0)
        return win

    def menu(y: int, x: int, options: list, commands: list, selected_option: int=0, bold: bool=False, allow_back: bool=False):
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
                commands[selected_option]()
                return False, selected_option
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if allow_back:
                    return True, selected_option
    
    def scribe(scribe_win, scribe_text: str = "", read_only: bool=False):
        scroll = 0
        max_width = stdscr.getmaxyx()[1]
        cursor_pos = 0
        curses.curs_set(1)
        key = False
        newline_trigger = False
        cursor_y = 0
        height = 100
        while True:
            if ( key == curses.KEY_DOWN and cursor_y < lines ) or key == 10 or newline_trigger:
                if cursor_y >= height + scroll - 1:
                    scroll += 1
            if cursor_y == 0 + scroll and scroll > 0:
                scroll -= 1
            newline_trigger = False
            # Key logic
            if key == curses.KEY_LEFT:
                if cursor_pos > 0:
                    cursor_pos -= 1
            elif key == curses.KEY_RIGHT:
                if cursor_pos < len(scribe_text):
                    cursor_pos += 1
            elif key == curses.KEY_DOWN:
                if cursor_y < lines:
                    # Find the start of the next line
                    n = cursor_pos
                    line_width = cursor_x
                    while n < len(scribe_text):
                        if scribe_text[n] == "\n":
                            n += 1
                            break
                        elif scribe_text[n] == "\t":
                            line_width += 5
                        else:
                            line_width += 1
                        if line_width >= width:
                            n += 1
                            break
                        n += 1
                    cursor_pos = n
                    # Position the cursor inside the next line
                    x = 0
                    while cursor_pos < len(scribe_text) and x < cursor_x:
                        if scribe_text[cursor_pos] == "\n":
                            break
                        elif scribe_text[cursor_pos] == "\t":
                            x += 5
                            if x >= width:
                                break
                        else:
                            x += 1
                            if x >= width:
                                break
                        cursor_pos += 1 
            elif key == curses.KEY_UP:
                if cursor_y > 0:
                    # Find the start of the previous line
                    n = cursor_pos
                    line_width = cursor_x
                    while n > 0:
                        n -= 1
                        if scribe_text[n] == "\n":
                            break
                        elif scribe_text[n] == "\t":
                            line_width -= 5
                        else:
                            line_width -= 1
                        if line_width < 0:
                            break
                    cursor_pos = n
                    # Move backward from the end of the previous line
                    x = line_lengths[cursor_y - 1] # Start from the end of the line
                    while cursor_pos >= 0 and x - 1 >= cursor_x:
                        cursor_pos -= 1
                        if x < 0:
                            break
                        if scribe_text[cursor_pos] == "\n":
                            break
                        elif scribe_text[cursor_pos] == "\t":
                            x -= 5
                            if x < cursor_x:
                                cursor_pos -= 1
                                break
                        else:
                            x -= 1
                            if x < cursor_x:
                                break
            elif key == curses.KEY_HOME:
                cursor_pos -= cursor_x
            elif key == curses.KEY_END:
                cursor_pos += line_lengths[cursor_y] - cursor_x
            elif key == curses.KEY_BACKSPACE and not read_only:
                if cursor_pos > 0:
                    scribe_text = scribe_text[:cursor_pos - 1] + scribe_text[cursor_pos:]
                    cursor_pos -= 1
            elif key == 10 and not read_only:  # Enter key
                scribe_text = scribe_text[:cursor_pos] + "\n" + scribe_text[cursor_pos:]
                cursor_pos += 1
            elif key == 9 and not read_only:  # Tab key
                scribe_text = scribe_text[:cursor_pos] + "\t" + scribe_text[cursor_pos:]
                cursor_pos += 1
            elif key == curses.KEY_F2:  # Saving
                scribe_win.clear()
                scribe_win.refresh()
                curses.curs_set(0) 
                return scribe_text
            elif key == curses.KEY_F4:  # Exiting without Saving
                scribe_win.clear()
                scribe_win.refresh()
                curses.curs_set(0) 
                return False
            elif key == False:
                nothing()
            elif key in range(32, 126) or key in ( 167, 176 ) and not read_only:  # Add printable characters to the text
                # Add a char to the text
                scribe_text = scribe_text[:cursor_pos] + chr(key) + scribe_text[cursor_pos:]
                cursor_pos += 1
            elif read_only == True:
                scribe_win.clear()
                scribe_win.refresh()
                curses.curs_set(0) 
                return scribe_text
            
            # Rendering the text
            height, width = scribe_win.getmaxyx()
            scribe_win.clear()
            x_pos = 0
            y_pos = 0
            cursor_y = 0
            cursor_x = 0
            line_length = 0
            line_lengths = []
            for x in range(len(scribe_text)):
                if scribe_text[x] == "\n":
                    y_pos += 1
                    x_pos = 0
                    line_lengths.append(line_length)
                    line_length = 0
                elif scribe_text[x] == "\t":
                    if x_pos + 5 >= max_width - 3:
                        y_pos += 1
                        x_pos = 0
                        line_lengths.append(line_length)
                        newline_trigger = True
                        line_length = 0
                    else:
                        x_pos += 5
                        line_length += 1
                else:
                    if x_pos + 1 >= max_width - 3:
                        y_pos += 1
                        x_pos = 0
                        line_lengths.append(line_length)
                        newline_trigger = True
                        line_length = 0
                        if y_pos - scroll >= 0 and y_pos - scroll < height:
                            scribe_win.addstr(y_pos - scroll, x_pos, scribe_text[x])
                    else:
                        if y_pos - scroll >= 0 and y_pos - scroll < height:
                            scribe_win.addstr(y_pos - scroll, x_pos, scribe_text[x])
                        x_pos += 1
                        line_length += 1
                if cursor_pos == x + 1:
                    cursor_x = x_pos
                    cursor_y = y_pos
            lines = y_pos
            line_lengths.append(line_length)
            stdscr.addstr(1, width - max(5, len(f"{cursor_x} {cursor_y}")) - 1, f"{cursor_x} {cursor_y}")
            scribe_win.move(cursor_y - scroll, cursor_x)
            stdscr.refresh()
            scribe_win.refresh()
            key = stdscr.getch()
            stdscr.addstr(1, width - max(5, len(f"{cursor_x} {cursor_y}")) - 1, " " * max(5, len(f"{cursor_x} {cursor_y}")))

    # Pages
    def scribe_write():
        text = ""
        with open("Text.txt", "r") as txt_file:
            for x in txt_file:
                text = text + x
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "Scribe  ---  Save: F2  Exit: F4")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        scribe_win = window(height - 5, width - 3, 4, 1, False)
        text = scribe(scribe_win, text)
        if not isinstance(text, bool):
            with open("Text.txt", "w") as txt_file:
                txt_file.write(text)
        return
    
    def scribe_read():
        text = ""
        with open("Text.txt", "r") as txt_file:
            for x in txt_file:
                text = text + x
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "Scribe  ---  Exit: F2, F4")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        scribe_win = window(height - 5, width - 3, 4, 1, False)
        scribe(scribe_win, text, True)
        return

    def example_text():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "Example Text")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(5, 2, "Hello World!")
        stdscr.getch()
        return
    
    def back_page(sel):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(1, 2, "No")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        stdscr.addstr(5, 2, "U cant back out of tis <3")
        stdscr.addstr(7, 2, f"Selected option was: {sel}")
        stdscr.getch()
        return

    def main():
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        box(3, width - 1, 0, 0, "━", "┃", "┏", "┓", "┗", "┛")  # Example for the box function
        stdscr.addstr(1, 2, "Main Menu")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        while True:
            back, sel = menu(5, 2, ["Say Hello", "Write Something", "Read that something", "Quit"], [example_text, scribe_write, scribe_read, bye], 0, True, True)  # Example on how to use the menu function
            if back:    # You can also do something when backspace is pressed (like go back one page or something) ... have to set allow_back = True
                back_page(sel)

    # Main code
    main() # Calling the first page

if __name__ == "__main__":
    curses.wrapper(tui)