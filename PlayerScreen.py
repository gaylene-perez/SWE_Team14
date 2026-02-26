import tkinter as tk
from tkinter import messagebox, simpledialog
from dataclasses import dataclass
from typing import List
from database import insert_player, playerIdExist

# PLAYER SCREEN
# red team (odd) / green team (even)
# max 15 players per team

# f12 clears all entries
# prompt for player id
    # query database for codename
    # if not found, allow new name entry to add to database

# prompt for equipment id that player is using (int)
    # print("Enter data to send: ")

MAX_PLAYERS = 15  # max 15 players per team

@dataclass
class PlayerEntry:
    player_id: int
    codename: str
    equipment_id: int

# pid = self._parse_int(self.player_id_var.get(), "Player ID")
# codename = self.codename_var.get().strip()
#PLAYER SCREEN
class PlayerScreen(tk.Frame):

    ip = "127.0.0.1"

    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.player_id_var = tk.StringVar()
        self.codename_var = tk.StringVar()
        self.equipment_id_var = tk.StringVar()

        self.red_players: List[PlayerEntry] = []  # red, odd eq id
        self.green_players: List[PlayerEntry] = []  # green, even eq id

        self.red_rows = []
        self.green_rows = []

        self._style()
        self._ui()
        self._key_input()

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self):
        # self.grid(row=0, column=0, sticky="nsew")
        # self.master.rowconfigure(0, weight=1)
        # self.master.columnconfigure(0, weight=1)
        content = tk.Frame(self, bg="black")
        content.pack(fill="both", expand=True)

        content.rowconfigure(0, weight=0) #title
        content.rowconfigure(1, weight=1) #panel
        content.rowconfigure(2, weight=0) #menu
        content.columnconfigure(0, weight=1)

        # title
        title = tk.Label(content, text="PLAYER ENTRY SCREEN", font=("Courier New", 20, "bold"), fg="white", bg="black") #fg = foreground (text color), bg = background
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w") #sticky="w" means aligned left

        # player id
        tk.Label(self, text="PLAYER ID:").grid(row=1, column=0, sticky="e")
        tk.Entry(self, textvariable=self.player_id_var).grid(row=1, column=1)

        # codename
        tk.Label(self, text="CODENAME:").grid(row=2, column=0, sticky="e")
        tk.Entry(self, textvariable=self.codename_var).grid(row=2, column=1)

        # equipment id
        tk.Label(self, text="EQUIPMENT ID:").grid(row=3, column=0, sticky="e")
        tk.Entry(self, textvariable=self.equipment_id_var).grid(row=3, column=1)

        # buttons
        tk.Button(self, text="ADD PLAYER (F1)", command=self.add_player).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self, text="REMOVE PLAYER", command=self.remove_player).grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(self, text="SWITCH NETWORK", command=self.switch_network).grid(row=6, column=0, columnspan=2, pady=5)

        # red team
        tk.Label(self, text="RED TEAM (ODD)").grid(row=7, column=0)
        self.red_listbox = tk.Listbox(self, height=10, width=30)
        self.red_listbox.grid(row=8, column=0)

        # green team
        tk.Label(self, text="GREEN TEAM (EVEN)").grid(row=7, column=1)
        self.green_listbox = tk.Listbox(self, height=10, width=30)
        self.green_listbox.grid(row=8, column=1)

    def _key_input(self):
        self.master.bind("<F12>", self.reset_players)
        self.master.bind("<F1>", self.add_player)

    # Add player to database and team
    def add_player(self, event=None):
        player_id = self.player_id_var.get().strip()
        codename = self.codename_var.get().strip()
        equipment_id = self.equipment_id_var.get().strip()

        if not player_id or not equipment_id:
            messagebox.showerror("Error", "Player ID and Equipment ID are required!")
            return

        try:
            player_id_int = int(player_id)
            equipment_id_int = int(equipment_id)
        except ValueError:
            messagebox.showerror("Error", "Player ID and Equipment ID must be integers!")
            return

        existing_codename = playerIdExist(player_id_int)
        if existing_codename:
            codename = existing_codename
            messagebox.showinfo("Player Found", f"Codename: {codename}")
        else:
            if not codename:
                messagebox.showerror("Error", "Enter a codename for new player")
                return
            insert_player(player_id_int, codename)
            messagebox.showinfo("Added", "New player added to database")

        player = PlayerEntry(player_id_int, codename, equipment_id_int)
        self.add_to_team(player)

        # clear entries
        self.player_id_var.set("")
        self.codename_var.set("")
        self.equipment_id_var.set("")

    def add_to_team(self, player: PlayerEntry):
        if player.equipment_id % 2 == 1:
            if len(self.red_players) < MAX_PLAYERS:
                self.red_players.append(player)
                self.red_listbox.insert(tk.END, f"{player.codename} (ID:{player.player_id}, EQ:{player.equipment_id})")
            else:
                messagebox.showerror("Error", "Red team full!")
        else:
            if len(self.green_players) < MAX_PLAYERS:
                self.green_players.append(player)
                self.green_listbox.insert(tk.END, f"{player.codename} (ID:{player.player_id}, EQ:{player.equipment_id})")
            else:
                messagebox.showerror("Error", "Green team full!")

    # Remove selected player
    def remove_player(self):
        red_index = self.red_listbox.curselection()
        green_index = self.green_listbox.curselection()

        if red_index:
            idx = red_index[0]
            self.red_listbox.delete(idx)
            self.red_players.pop(idx)
        elif green_index:
            idx = green_index[0]
            self.green_listbox.delete(idx)
            self.green_players.pop(idx)
        else:
            messagebox.showinfo("Remove Player", "Select a player to remove first.")

    # Reset all players
    def reset_players(self, event=None):
        self.red_players.clear()
        self.green_players.clear()
        self.red_listbox.delete(0, tk.END)
        self.green_listbox.delete(0, tk.END)

    # change IP address
    def switch_network(self):
        ip = simpledialog.askstring("Switch Network", f"Current IP: {self.ip}\nEnter new IP:")
        if ip:
            self.ip = ip
            messagebox.showinfo("Network Changed", f"New IP: {self.ip}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")
    screen = PlayerScreen(root)
    screen.pack(padx=10, pady=10)
    root.mainloop()



#PlayerScreen.py For Sprint 3:
"""import tkinter as tk #gui
# from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass
from typing import List
from tkinter import simpledialog


    def _ui(self) -> None: #_method internal/protected


        #title




        #red team
        red_panel = self._team_panel(main, "RED TEAM (ODD)", bg="black", accent="red")
        red_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #green team
        green_panel = self._team_panel(main, "GREEN TEAM (EVEN)", bg="black", accent="green")
        green_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._build_rows(red_panel, team="red")
        self._build_rows(green_panel, team="green")

        #menu
        menu = tk.Frame(content, bg="black")
        menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0,12))
        for i in range(5):
            menu.columnconfigure(i, weight=1)
        self._menu(menu, 0, "F1\nAdd\nPlayer", self.handle_new_player)
        self._menu(menu, 1, "F5\nStart\nGame", self.start_game)
        self._menu(menu, 2, "F10\nSwitch\nNetwork", self.switch_network)
        self._menu(menu, 3, "F12\nClear\nPlayers", self.reset_players)
        self._menu(menu, 4, "ESC\nExit", self.quit)

        button = tk.Button(self, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)
        button.pack(pady=10)

    def _menu(self, parent, col: int, text: str, cmd) -> None:
        bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
        bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _make_scroll(self, parent, bg:str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        vbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas(event):
            canvas.itemconfigure(window_id, width=event.width)

        inner.bind("<Configure>", _on_inner)
        canvas.bind("<Configure>", _on_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # def _bind_to_child
        def _bind_wheel(_event=None):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_wheel(_event=None):
            canvas.unbind_all("MouseWheel")

        # canvas.bind("<Enter>", _enter)
        # inner.bind("<Enter>", _enter)
        #
        # canvas.bind("<Leave>", _leave)
        # inner.bind("<Leave>", _leave)

        # canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return canvas, inner

    def _team_panel(self, parent, title:str, bg="black", accent="white") -> tk.Frame:
        panel = tk.Frame(parent, bg=bg, bd=2, relief="groove")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        header = tk.Label(panel, text=title, font=("Courier New", 20, "bold"), fg=accent, bg=bg)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # body = tk.Frame(panel, bg=bg)
        # body.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        body_container = tk.Frame(panel, bg=bg)
        body_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        canvas, inner = self._make_scroll(body_container, bg)

        inner.columnconfigure(0, weight=1) #checkbox
        inner.columnconfigure(1, weight=1) #index
        inner.columnconfigure(2, weight=1) #player id
        inner.columnconfigure(3, weight=1) #codename

        panel.body = inner
        panel.body_canvas = canvas
        panel.panel_bg = bg
        panel.panel_accent = accent

        return panel

    def _build_rows(self, panel, team:str) -> None:
        body = panel.body
        bg = panel.panel_bg
        accent = panel.panel_accent

        rows = []
        #headers
        tk.Label(body, text="", bg=bg).grid(row=0, column=0) #checkbox
        tk.Label(body, text="#", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(body, text="PLAYER ID", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=2, sticky="w", padx=10)
        tk.Label(body, text="CODENAME", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=3, sticky="w", padx=10)

        for i in range(1, MAX_PLAYERS + 1):
            box = tk.Canvas(body, width=14, height=14, bg=bg, highlightthickness=1, highlightbackground=accent)
            box.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            index = tk.Label(body, text=str(i), font=("Courier New", 20, "bold"), fg="white", bg=bg)
            index.grid(row=i, column=1, padx=10, pady=10, sticky="w")

            pid = tk.Entry(body, bg=bg, relief="groove")
            pid.grid(row=i, column=2, padx=(0,6), pady=3, sticky="ew")

            code = tk.Entry(body, bg=bg, relief="groove")
            code.grid(row=i, column=3, padx=3, pady=10, sticky="ew")

            rows.append({"box": box, "player_id": pid, "codename": code})

        if team == "red":
            self.red_rows = rows
        else:
            self.green_rows = rows


    def _key_input(self) -> None:
        self.master.bind("<F1>", lambda e: self.handle_new_player())
        self.master.bind("<F5>", lambda e: self.start_game())
        self.master.bind("<F10>", lambda e: self.switch_network())
        self.master.bind("<F12>", lambda e: self.reset_players())
        self.master.bind("<Escape>", lambda e: self.quit())
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

    def handle_new_player(self) -> None:
        try:
            pid = int(self.player_id_var.get().strip())
            code = self.codename_var.get().strip()
            eid = int(self.equipment_id_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Player ID & Equipment ID must be an integer.")
            return

        if not code:
            messagebox.showerror("Error", "Codename cannot be empty.")
            return

        player = PlayerEntry(player_id=pid, codename=code, equipment_id=eid)
        self.add_new_player(player)

    def add_new_player(self, player: PlayerEntry) -> None:
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        # #equipment id
        # tk.Label(self, text="EQUIPMENT ID").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.equipment_id_var).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        #
        # #player id
        # tk.Label(self, text="PLAYER ID").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.player_id_var).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        #
        # #codename
        # tk.Label(self, text="CODENAME").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.codename_var).grid(row=2, column=2, padx=10, pady=5, sticky="w")

        if red_team:
            if len(self.red_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Red team has 15 players!")
                return
            self.red_players.append(player)
            self._write_player_to_row("red", player)
        if green_team:
            if len(self.green_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Green team has 15 players!")
                return
            self.green_players.append(player)
            self._write_player_to_row("green", player)

    def _write_player_to_row(self, team:str, player:PlayerEntry) -> None:
        rows = self.red_rows if team == "red" else self.green_rows
        index = len(self.red_players) - 1 if team == "red" else len(self.green_players) - 1

        if 0 <= index < len(rows):
            rows[index]["player_id"].delete(0, tk.END)
            rows[index]["player_id"].insert(0, str(player.player_id))

            rows[index]["codename"].delete(0, tk.END)
            rows[index]["codename"].insert(0, str(player.codename))

    def start_game(self) -> None:
        messagebox.showinfo("Start Game", "Not wired yet.")

    #change IP address
    def switch_network(self):
        temp = self.ip
        self.ip = simpledialog.askstring("Input", f"Current IP address: {self.ip}\nPlease enter a valid IP address:", parent=root)

        if self.ip is None:
            self.ip = temp

        return self.ip

    def reset_players(self) -> None:
        self.red_players = []
        self.green_players = []
        for row in self.red_rows:
            row["player_id"].delete(0, tk.END)
            row["codename"].delete(0, tk.END)
        for row in self.green_rows:
            row["player_id"].delete(0, tk.END)
            row["codename"].delete(0, tk.END)

    def quit(self) -> None:
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")
    root.geometry("900x500")

    screen = PlayerScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()"""


"""
#PlayerScreen.py For Sprint 3: 
import tkinter as tk #gui
# from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass
from typing import List
from tkinter import simpledialog

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

        self.ip = "127.0.0.1"

        self.player_id_var = tk.StringVar()
        self.codename_var = tk.StringVar()
        self.equipment_id_var = tk.StringVar()

        self.red_players: List[PlayerEntry] = [] #red, odd eq id
        self.green_players: List[PlayerEntry] = [] #green, even eq id

        self.red_rows = []
        self.green_rows = []

        self._style()
        self._ui()
        self._key_input()

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self) -> None: #_method internal/protected
        # self.grid(row=0, column=0, sticky="nsew")
        # self.master.rowconfigure(0, weight=1)
        # self.master.columnconfigure(0, weight=1)
        content = tk.Frame(self, bg="black")
        content.pack(fill="both", expand=True)

        content.rowconfigure(0, weight=0) #title
        content.rowconfigure(1, weight=1) #panel
        content.rowconfigure(2, weight=0) #menu
        content.columnconfigure(0, weight=1)

        #title
        title = tk.Label(content, text="PLAYER ENTRY SCREEN", font=("Courier New", 20, "bold"), fg="white", bg="black") #fg = foreground (text color), bg = background
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w") #sticky="w" means aligned left

        #bulk
        main = tk.Frame(content, bg="black")
        main.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        #red team
        red_panel = self._team_panel(main, "RED TEAM (ODD)", bg="black", accent="red")
        red_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        #green team
        green_panel = self._team_panel(main, "GREEN TEAM (EVEN)", bg="black", accent="green")
        green_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._build_rows(red_panel, team="red")
        self._build_rows(green_panel, team="green")

        #menu
        menu = tk.Frame(content, bg="black")
        menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0,12))
        for i in range(5):
            menu.columnconfigure(i, weight=1)
        self._menu(menu, 0, "F1\nAdd\nPlayer", self.handle_new_player)
        self._menu(menu, 1, "F5\nStart\nGame", self.start_game)
        self._menu(menu, 2, "F10\nSwitch\nNetwork", self.switch_network)
        self._menu(menu, 3, "F12\nClear\nPlayers", self.reset_players)
        self._menu(menu, 4, "ESC\nExit", self.quit)

        button = tk.Button(self, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)
        button.pack(pady=10)

    def _menu(self, parent, col: int, text: str, cmd) -> None:
        bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
        bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _make_scroll(self, parent, bg:str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        vbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)

        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas(event):
            canvas.itemconfigure(window_id, width=event.width)

        inner.bind("<Configure>", _on_inner)
        canvas.bind("<Configure>", _on_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # def _bind_to_child
        def _bind_wheel(_event=None):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_wheel(_event=None):
            canvas.unbind_all("MouseWheel")

        # canvas.bind("<Enter>", _enter)
        # inner.bind("<Enter>", _enter)
        #
        # canvas.bind("<Leave>", _leave)
        # inner.bind("<Leave>", _leave)

        # canvas.bind_all("<MouseWheel>", _on_mousewheel)

        return canvas, inner

    def _team_panel(self, parent, title:str, bg="black", accent="white") -> tk.Frame:
        panel = tk.Frame(parent, bg=bg, bd=2, relief="groove")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        header = tk.Label(panel, text=title, font=("Courier New", 20, "bold"), fg=accent, bg=bg)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # body = tk.Frame(panel, bg=bg)
        # body.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        body_container = tk.Frame(panel, bg=bg)
        body_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        canvas, inner = self._make_scroll(body_container, bg)

        inner.columnconfigure(0, weight=1) #checkbox
        inner.columnconfigure(1, weight=1) #index
        inner.columnconfigure(2, weight=1) #player id
        inner.columnconfigure(3, weight=1) #codename

        panel.body = inner
        panel.body_canvas = canvas
        panel.panel_bg = bg
        panel.panel_accent = accent

        return panel

    def _build_rows(self, panel, team:str) -> None:
        body = panel.body
        bg = panel.panel_bg
        accent = panel.panel_accent

        rows = []
        #headers
        tk.Label(body, text="", bg=bg).grid(row=0, column=0) #checkbox
        tk.Label(body, text="#", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(body, text="PLAYER ID", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=2, sticky="w", padx=10)
        tk.Label(body, text="CODENAME", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=3, sticky="w", padx=10)

        for i in range(1, MAX_PLAYERS + 1):
            box = tk.Canvas(body, width=14, height=14, bg=bg, highlightthickness=1, highlightbackground=accent)
            box.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            index = tk.Label(body, text=str(i), font=("Courier New", 20, "bold"), fg="white", bg=bg)
            index.grid(row=i, column=1, padx=10, pady=10, sticky="w")

            pid = tk.Entry(body, bg=bg, relief="groove")
            pid.grid(row=i, column=2, padx=(0,6), pady=3, sticky="ew")

            code = tk.Entry(body, bg=bg, relief="groove")
            code.grid(row=i, column=3, padx=3, pady=10, sticky="ew")

            rows.append({"box": box, "player_id": pid, "codename": code})

        if team == "red":
            self.red_rows = rows
        else:
            self.green_rows = rows


    def _key_input(self) -> None:
        self.master.bind("<F1>", lambda e: self.handle_new_player())
        # self.master.bind("<F5>", lambda e: self.start_game())
        root.bind("<F5>", self.start_game)
        self.master.bind("<F10>", lambda e: self.switch_network())
        self.master.bind("<F12>", lambda e: self.reset_players())
        self.master.bind("<Escape>", lambda e: self.quit())
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

    def handle_new_player(self) -> None:
        try:
            pid = int(self.player_id_var.get().strip())
            code = self.codename_var.get().strip()
            eid = int(self.equipment_id_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Player ID & Equipment ID must be an integer.")
            return

        if not code:
            messagebox.showerror("Error", "Codename cannot be empty.")
            return

        player = PlayerEntry(player_id=pid, codename=code, equipment_id=eid)
        self.add_new_player(player)

    def add_new_player(self, player: PlayerEntry) -> None:
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        # #equipment id
        # tk.Label(self, text="EQUIPMENT ID").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.equipment_id_var).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        #
        # #player id
        # tk.Label(self, text="PLAYER ID").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.player_id_var).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        #
        # #codename
        # tk.Label(self, text="CODENAME").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        # tk.Entry(self, textvariable=self.codename_var).grid(row=2, column=2, padx=10, pady=5, sticky="w")

        if red_team:
            if len(self.red_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Red team has 15 players!")
                return
            self.red_players.append(player)
            self._write_player_to_row("red", player)
        if green_team:
            if len(self.green_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Green team has 15 players!")
                return
            self.green_players.append(player)
            self._write_player_to_row("green", player)

    def _write_player_to_row(self, team:str, player:PlayerEntry) -> None:
        rows = self.red_rows if team == "red" else self.green_rows
        index = len(self.red_players) - 1 if team == "red" else len(self.green_players) - 1

        if 0 <= index < len(rows):
            rows[index]["player_id"].delete(0, tk.END)
            rows[index]["player_id"].insert(0, str(player.player_id))

            rows[index]["codename"].delete(0, tk.END)
            rows[index]["codename"].insert(0, str(player.codename))

    def start_game(self, event):
        """Code up f5 key or equivalent to switch to play action display and start game (you can do this in
        the original window or start another window)"""
        root = tk.Tk()
        root.title("PLAY GAME")
        root.geometry("900x500")
        root.mainloop()

    #change IP address
    def switch_network(self):
        temp = self.ip
        self.ip = simpledialog.askstring("Input", f"Current IP address: {self.ip}\nPlease enter a valid IP address:", parent=root)

        if self.ip is None:
            self.ip = temp

        return self.ip

    def reset_players(self) -> None:
        self.red_players = []
        self.green_players = []
        for row in self.red_rows:
            row["player_id"].delete(0, tk.END)
            row["codename"].delete(0, tk.END)
        for row in self.green_rows:
            row["player_id"].delete(0, tk.END)
            row["codename"].delete(0, tk.END)

    def quit(self) -> None:
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")
    root.geometry("900x500")

    screen = PlayerScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()
"""
