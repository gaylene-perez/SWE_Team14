import tkinter as tk #gui
# from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass
from typing import List

# PLAYER SCREEN
# red team (odd) / green team (even)
# max 15 players per team

# f12 clears all entries
# prompt for player id
    #query database for code name
    #if not found, allow new name entry to add to database

#prompt for equipment id that player is using (int)
    #print("Enter data to send: ")

MAX_PLAYERS = 15 #max 15 players per team

@dataclass
class PlayerEntry:
    player_id: int
    codename: str
    equipment_id: int

# pid = self._parse_int(self.player_id_var.get(), "Player ID")
# codename = self.codename_var.get().strip()
#PLAYER SCREEN
class PlayerScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.player_id_var = tk.StringVar()
        self.codename_var = tk.StringVar()
        self.equipment_id_var = tk.StringVar()

        self.red_players: List[PlayerEntry] = [] #red, odd eq id
        self.green_players: List[PlayerEntry] = [] #green, even eq id

        self._ui()
        self._key_input()

    def _ui(self) -> None: #_method internal/protected
        #title
        title = tk.Label(self, text="PLAYER ENTRY SCREEN", font=("Times New Roman", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w") #sticky="w" means aligned left

        #player id
        tk.Label(self, text="PLAYER ID").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.player_id_var).grid(row=1, column=2, padx=10, pady=5, sticky="w")

        #codename
        tk.Label(self, text="CODENAME").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.codename_var).grid(row=2, column=2, padx=10, pady=5, sticky="w")

        #equipment id
        tk.Label(self, text="EQUIPMENT ID").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        tk.Entry(self, textvariable=self.equipment_id_var).grid(row=3, column=2, padx=10, pady=5, sticky="w")

        #buttons
        tk.Label(self, text="ADD PLAYER (F1)").grid(row=15, column=1, padx=10, pady=10, sticky="ew") #sticky="ew" fills cell
        tk.Label(self, text="START GAME (F5)").grid(row=15, column=2, padx=10, pady=5, sticky="ew")
        tk.Label(self, text="CLEAR ALL (F12)").grid(row=15, column=3, padx=10, pady=5, sticky="ew")

        #red team
        tk.Label(self, text="RED TEAM (ODD)").grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.red_listbox = tk.Listbox(self, height=12, width=30)
        self.red_listbox.grid(row=2, column=2, rowspan=3, padx=10, pady=5)

        #green team
        tk.Label(self, text="GREEN TEAM (EVEN)").grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        self.green_listbox = tk.Listbox(self, height=12, width=30)
        self.green_listbox.grid(row=6, column=2, rowspan=3, padx=10, pady=5)

    def _key_input(self) -> None:
        self.master.bind("<F12>", self.reset_players)
        # k = Tk()
        # k.bind("<F12>", self.reset_players()) #bind(event, function)

    def query_player(self, codename: str) -> PlayerEntry:
        for entry in self.red_players:
            if entry.codename == codename:
                return entry
        for entry in self.green_players:
            if entry.codename == codename:
                return entry
        return None

    def add_new_player(self, player: PlayerEntry):
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        if red_team:
            if len(self.red_players) < MAX_PLAYERS:
                self.red_players.append(player)
            else:
                messagebox.showerror("Error", "Red team has 15 players!")
                return
        if green_team:
            if len(self.green_players) < MAX_PLAYERS:
                self.green_players.append(player)
            else:
                messagebox.showerror("Error", "Green team has 15 players!")

    def reset_players(self):
        self.red_players = []
        self.green_players = []

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")
    root.geometry("700x800")

    screen = PlayerScreen(root)
    screen.pack()

    root.mainloop()