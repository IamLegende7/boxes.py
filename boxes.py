import curses

class TUI:
    #############
    ### BOXES ###
    #############
    @staticmethod
    def box(window, size,coords, top:str,side:str, tl:str,tr:str=None,bl:str=None,br:str=None):
        ### CORNER DEFAULTS ###
        if tr == None:
            tr = tl
        if bl == None:
            bl = tl
        if br == None:
            br = tl
        ### DRAW THE BOX ###
        window.addstr(coords[1], coords[0], f"{tl}" + f"{top}" * (size[0] - 2) + f"{tr}")
        window.addstr(coords[1] + size[1] - 1, coords[0], f"{bl}" + f"{top}" * (size[0] - 2) + f"{br}")
        for i in range(1, size[1] - 1):
            window.addstr(coords[1] + i, 0, f"{side}")
            window.addstr(coords[1] + i, coords[0] + size[0] - 1, f"{side}")

    ##################
    ### MENU LOGIC ###
    ##################
    class Menu:
        def update_options(self):
            self.curses_options = 0
            if self.bold:
                self.curses_options |= curses.A_BOLD
            if self.coulor != 0:
                self.curses_options |= curses.color_pair(self.coulor)

        def display_entry(self, entry_label: str, y: int):
            ### OPTIONS ###
            if y == self.selected_option:
                entry_options = self.curses_options | curses.A_REVERSE
            else:
                entry_options = self.curses_options

            ### DISPLAY ###
            try:
                self.menu_pad.addstr(y, 0, entry_label, entry_options)
                return 0
            except:
                return 1

        def tick(self, keypress):
            ### PROCCESS KEYPRESSES ###
            match keypress:
                case curses.KEY_UP:
                    if self.selected_option - 1 >= 0:
                        self.selected_option -= 1
                        if self.selected_option <= 0 + self.scroll - 1:
                            scroll -= 1
                case curses.KEY_DOWN:
                    if self.selected_option + 1 <= len(self.contents) - 1:
                        self.selected_option += 1
                        if self.selected_option >= self.height + self.scroll:
                            self.scroll += 1
                case 10:
                    if self.contents[self.selected_option][1] == "nothing":
                        return False, self.selected_option
                    else:
                        self.contents[self.selected_option][1]()
                case curses.KEY_BACKSPACE, 127, 8:
                    if allow_back:
                        return True, self.selected_option

            ### DISPLAY MENU ###
            if self.full_refresh:
                self.menu_pad.clear()
                y = 0
                for menu_content in self.contents:
                    self.display_entry(menu_content[0], y)
                    y += 1

            elif self.selected_option != self.old_selected_option:
                self.display_entry(self.contents[self.old_selected_option][0], self.old_selected_option)
                self.display_entry(self.contents[self.selected_option][0], self.selected_option)
            
            self.menu_pad.refresh(0,0, self.scroll,0, self.height+self.scroll,self.width)

        # Contents must be fed into like this:
        # [(name, funtion to call)]
        def __init__(self, menu_win, contents, allow_back: bool = False):
            ### WIN / PAD SETUP ###
            self.height, self.width = menu_win.getmaxyx()
            self.win_origin_coords = menu_win.getparyx()
            self.pad_height = len(contents)
            self.pad_width = max(max(len(x[0]) for x in contents), self.width)
            self.menu_pad = curses.newpad(self.pad_height, self.pad_width)

            ### MENU SETTINGS SETUP ###
            self.coulor = 0
            self.bold = False
            self.allow_back = allow_back

            ### INTERNAL VARS ###
            self.contents = contents
            self.full_refresh = True
            self.selected_option = 0
            self.old_selected_option = 0
            self.scroll = 0

            ### RUNNING FUNCTIONS
            self.update_options()

            self.tick(None)
            menu_win.refresh()

    ##################
    ### INIT LOGIC ###
    ##################
    def __init__(self):
        ### TREM ###
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        ### COLOURS ###
        curses.start_color()
        self.init_colours()

    def init_colours(self):
        #curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def cleanup(self):
        curses.nocbreak()
        curses.echo()