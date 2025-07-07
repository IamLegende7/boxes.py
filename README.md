# Boxes
[![Python 3.13.5+](https://img.shields.io/badge/python-3.13.5+-blue.svg)](https://www.python.org/downloads/) [![License: 2-Clause-BSD](https://img.shields.io/badge/BSD-yellow.svg)](https://opensource.org/license/bsd-2-clause)

Boxes is a template for my TUI python projects

## Dependencies

Boxes uses curses, with comes with python, so nothing must be installed additionally

## How to use
1. ```box```

   This function draws a box (crazy, right?)
   
   Arguments:
   
     1. ```height``` and ```width```
   
     2. ```y``` , ```x``` : y, x position
   
     3. ```top``` : char used for  the top and bottom,
   
     4. ```side``` : char used for the left and right
   
     5. ```tl``` : char used for the top left corner
   
     6. ```tr``` : char used for the top right corner
   
     7. ```bl``` : char used for the bottom left corner
   
     8. ```br``` : char used for the bottom right corner
   
   Basic example:
   ```Python
   height, width = stdscr.getmaxyx()
   box(height, width - 1, "━", "┃", "┏", "┓", "┗", "┛")    
   ```

3. ```window```
 
   This function just makes and returns a window. I will add more soon.

4. ```menu```

   This is a simple function to create a menu that can be navigated with the arrow-keys, enter and optionally backspace
   
   Arguments:
   
     1. ```y``` , ```x``` : y, x position
   
     2. ```options``` : a list of Strings to display as the options
   
     3. ```commands``` : a list of functions to call, corrosponding to the optiond, **DONT ADD THEM AS STRINGS (dont use "" or '')**
   
     4. ```selected_option``` : optional, starting posision of the "cursor", default 0
   
     5. ```bold``` : if the options are written bold
   
     6. ```allow_back``` : if backspace can be used to get out of the menu

   Examples:

   ```Python
   back, sel = menu(5, 2, ["Say Hello", "Write Something", "Read that something", "Quit"], [example_text, scribe_write, scribe_read, bye], 0, True, True)  # Example on how to use the menu function
   ```

   ```back``` will be true, if the menu was left using backspace, allowing for something like this:

   ```Python
   if back:
       back() # Another function to call in this case
   ```

   ```sel``` will return the index of the currently selected option, no matter how the menu was left.

   This is very useful, if you want the user to select from something else than a hardcoded list; you can use the function ```nothing``` in the commands-list (one for every entry is still required!) to only return the index, processing it outside of the menu function:

   ```Python
   options = []
   commands = []
   for x in options_to_process:
       options.append(x)
       commands.append(nothing)
   back, sel = menu(0, 0, options, commands, 0, True, False)
   chosen_option = options_to_process[sel]
   ```
5. ```scribe```
    
    Scribe is a simple text "editor". It allows for most characters to be written and can be navigated using the arrow-keys and home & end keys.
    
    It comes with text-wrap build-in.

    It even has a srcolling feature for longer texts!

    In the examples below, the function is used to write and read a file, called ```Text.txt```.

    ```Python
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
        stdscr.addstr(1, 2, "Scribe  ---  Save: F2  Exit: F4")
        box(height - 3, width - 1, 3, 0, "━", "┃", "┏", "┓", "┗", "┛")
        scribe_win = window(height - 5, width - 3, 4, 1, False)
        scribe(scribe_win, text, True)
        return
    ```

    The scribe function requires a window, to work in and a starting text in the form of a string.
    
    If the 3rd function, ```read_only``, is set to ```True``` the text can only be viewed, not edited.

    The scribe function will return the edited Text, if the editor was left with F2 (aka the text was saved), otherwise it will return ```False```.

## Structure

Obviosly not a must, but I like this structure

**Pages**

In the function ``` tui ``` remove (or change) the give examples listed under the comment ``` # Pages ```:

```Python
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
    stdscr.addstr(1, 2, "Scribe  ---  Save: F2  Exit: F4")
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
        if back:    # You can also do something when backspace is pressed (like go back one page or something) ... have to set allow_back = True though
            back_page(sel)
```
You can then later call these functions to call the diffrent pages you want.

**Main code**

Under the comment ``` # Main code ``` (still in the ``` tui ``` function) you can add your main code.

Again: you would want to add all the page-related code to the pages functions, however here you can call the first page and set some varibles first

```Python
    # Main code
    main() # Calling the first page
```

##
If you encounter any bug, optimization issue or anything else you would like me to change, please feel free to let me know :)