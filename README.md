# Boxes
[![Python 3.13.5+](https://img.shields.io/badge/python-3.13.5+-blue.svg)](https://www.python.org/downloads/) [![License: 2-Clause-BSD](https://img.shields.io/badge/BSD-yellow.svg)](https://opensource.org/license/bsd-2-clause)

Boxes is a collection of tools for making TUI python projects.

## Dependencies

Boxes uses curses, with comes with python, so nothing must be installed additionally

## How to use

### Setup

First you will have to import the package:

```python
import curses
from boxes-tui import TUI
```

Now you will need to create a new TUI object intance:

```python
my_tui = TUI()
```

After that you can use the tools that this package supplies.

### Tool usage

See [example.py](https://github.com/IamLegende7/boxes-tui/blob/main/example.py) for a basic TUI script example.

1. Menu

    **Creation**

    This simple menu is navigatable by arrow keys and enter.

    You have to pass in the lable and a function to execute; all in a list.

    Here is an example for a super basic menu:

    ```python
    my_menu = tui.Menu(stdscr, [("Hello", tui.nothing), ("Quit", quit_app)])
    ```

    Here the entrys get stored as a list of tuples of ```(label, function_to_call)```


    As you can see, you also put in a window. Its values (aka the origin coord and the height & width) will be used for the Menu.

    You can chage them later using:

    ```python
    my_menu.chage_values(x, y, width, height)
    ```

    **Ticking**

    Ticking refreshes the menu and processes keypresses. For values it returns, see Returns

    You can tick the function using:

    ```python
    my_menu.tick(key)
    ```

    ```key``` can be gotten by using:

    ```python
    key = stdsrc.getch()
    ```    

    **Returns**

    When ticking, the menu may (when the user presses "enter" or "backspace") return a tuple of ```(index, return_of_the_function)```

    Were ```index``` is the index of the entry the user selected. -1 if the user pressed backspace.

    ```return_of_the_function``` is whatever the function may have returned, that has been called by the menu.

##
If you encounter any bug, optimization issue or anything else you would like me to change, please feel free to let me know :)