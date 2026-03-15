"""
import tkinter as tk

class BaseMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._style()
        self._key_input()

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self, parent) -> None:
        # menu
        menu = tk.Frame(parent, bg="black")
        menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        for i in range(6):
            menu.columnconfigure(i, weight=1)
        self._menu(menu, 0, "F1\nAdd\nPlayer", self.add_player)
        self._menu(menu, 1, "F2\nLoad\nPlayers", self.load_players_from_db)
        self._menu(menu, 2, "F5\nStart\nGame", self.start_game)
        self._menu(menu, 3, "F10\nSwitch\nNetwork", self.switch_network)
        self._menu(menu, 4, "F12\nClear\nPlayers", self.reset_players)
        self._menu(menu, 5, "ESC\nExit", self.master.quit)

    def _menu(self, parent, col: int, text: str, cmd) -> None:
        bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
        bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _key_input(self) -> None:
        self.master.bind("<F1>", self.add_player)
        self.master.bind("<F2>", self.load_players_from_db)
        self.master.bind("<F5>", lambda e: self.start_game)
        self.master.bind("<F10>", self.switch_network)
        self.master.bind("<F12>", self.reset_players)
        self.master.bind("<Escape>", lambda e: self.quit)
"""

import tkinter as tk

class BaseMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._style()
        self._key_input()

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self, parent) -> None:
    #     # menu
        menu = tk.Frame(parent, bg="black")
        menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        for i in range(6):
            menu.columnconfigure(i, weight=1)
    #     self._menu(menu, 0, "F1\nAdd\nPlayer", self.add_player)
    #     self._menu(menu, 1, "F2\nLoad\nPlayers", self.load_players_from_db)
    #     self._menu(menu, 2, "F5\nStart\nGame", self.start_game)
    #     self._menu(menu, 3, "F10\nSwitch\nNetwork", self.switch_network)
    #     self._menu(menu, 4, "F12\nClear\nPlayers", self.reset_players)
    #     self._menu(menu, 5, "ESC\nExit", self.master.quit)

    def _menu(self, parent, col: int, text: str, cmd) -> None:
        bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
        bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    # def _key_input(self) -> None:
    #     self.master.bind("<F1>", self.add_player)
    #     self.master.bind("<F2>", self.load_players_from_db)
    #     self.master.bind("<F5>", lambda e: self.start_game)
    #     self.master.bind("<F10>", self.switch_network)
    #     self.master.bind("<F12>", self.reset_players)
    #     self.master.bind("<Escape>", lambda e: self.quit)

"""
