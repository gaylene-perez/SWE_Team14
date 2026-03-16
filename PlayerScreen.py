import tkinter as tk  # gui
from tkinter import messagebox, simpledialog
from dataclasses import dataclass
from typing import List

from PlayAction import PlayAction
import database
from database import insert_player, playerIdExist
from BaseMenu import BaseMenu

# PLAYER SCREEN
# red team (odd eq id) / green team (even eq id)
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


# PLAYER SCREEN
class PlayerScreen(BaseMenu):
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

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="black")
        content.grid(row=0, column=0, sticky="nsew")

        content.rowconfigure(0, weight=0)  #title
        content.rowconfigure(1, weight=1) #team
        content.rowconfigure(2, weight=0)  #menu
        content.columnconfigure(0, weight=1)

        # title
        title = tk.Label(content, text="PLAYER ENTRY SCREEN", font=("Courier New", 20, "bold"), fg="white",bg="black")  # fg = foreground (text color), bg = background
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # sticky="w" means aligned left

        #roster
        main = tk.Frame(content, bg="black")
        main.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)  # red
        main.columnconfigure(1, weight=1)  # green

        # red team
        red_panel = self._team_panel(main, "RED TEAM", bg="black", accent="red")
        red_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # green team
        green_panel = self._team_panel(main, "GREEN TEAM", bg="black", accent="green")
        green_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._build_rows(red_panel, team="red")
        self._build_rows(green_panel, team="green")

        super()._ui(content) #base menu

        # menu
        menu = tk.Frame(content, bg="black")
        menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        for i in range(6):
            menu.columnconfigure(i, weight=1)
        self._menu(menu, 0, "F1\nAdd\nPlayer", self.add_player)
        self._menu(menu, 1, "F2\nLoad\nPlayers", self.load_players_from_db)
        self._menu(menu, 2, "F5\nStart\nGame", self.start_game)
        self._menu(menu, 3, "F10\nSwitch\nNetwork", self.switch_network)
        self._menu(menu, 4, "F12\nClear\nPlayers", self.reset_players)
        self._menu(menu, 5, "ESC\nExit", self.quit)
        button = tk.Button(self, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)

    def _make_scroll(self, parent, bg: str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        vbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview, width=5)
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

        canvas.bind("<Return>", _bind_wheel)
        inner.bind("<Return>", _bind_wheel)

        canvas.bind("<Leave>", _unbind_wheel)
        inner.bind("<Leave>", _unbind_wheel)

        return canvas, inner

    # def _menu(self, parent, col: int, text: str, cmd) -> None:
    #     bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
    #     bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _team_panel(self, parent, title:str, bg="black", accent="white") -> tk.Frame:
        panel = tk.Frame(parent, bg=bg, bd=2, relief="groove")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        header = tk.Label(panel, text=title, font=("Courier New", 20, "bold"), fg=accent, bg=bg)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        body_container = tk.Frame(panel, bg=bg)
        body_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        canvas, inner = self._make_scroll(body_container, bg)

        inner.columnconfigure(0, weight=0, minsize=2) #index/player id
        inner.columnconfigure(1, weight=1, minsize=180) #codename
        inner.columnconfigure(2, weight=1, minsize=10) #equipment id

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
        #header
        tk.Label(body, text="CODENAME", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)

        cell_style = {"bg": bg, "fg": "white", "font": ("Courier New", 12, "bold"), "relief": "groove", "bd": 2, "anchor": "w", "padx": 6}

        for i in range(1, MAX_PLAYERS + 1):
            index = tk.Label(body, text=str(i), font=("Courier New", 20, "bold"), fg="white", bg=bg)
            index.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            code = tk.Label(body, bg=bg, fg="white", font=("Courier New", 14, "bold"), relief="groove", anchor="w", padx=6)
            code.grid(row=i, column=1, padx=3, pady=10, sticky="ew")

            rows.append({"codename": code})

        if team == "red":
            self.red_rows = rows
        else:
            self.green_rows = rows

    def _key_input(self, event=None):
        self.master.bind("<F1>", self.add_player)
        self.master.bind("<F2>", self.load_players_from_db)
        self.master.bind("<F5>", lambda event: self.start_game())
        self.master.bind("<F10>", self.switch_network)
        self.master.bind("<F12>", self.reset_players)
        self.master.bind("<Escape>", lambda e: self.quit())

    def _write_player_to_row(self, team:str, player:PlayerEntry) -> None:
        rows = self.red_rows if team == "red" else self.green_rows
        index = len(self.red_players) - 1 if team == "red" else len(self.green_players) - 1

        if 0 <= index < len(rows):
            rows[index]["codename"].config(text=player.codename)

    #helper for duplicate check in _handle_new_player
    def _existing_player(self, player_id):
        for player in self.red_players + self.green_players:
            if player.player_id == player_id:
                return True
        return False

    #duplicate player id helper
    def _handle_duplicate(self, player_id_int, popup, player_id_entry):
        messagebox.showerror("Error", f"Player ID {player_id_int} already exists!", parent=popup) #parent=popup: belongs to popup window

        # enable input into player id after popup messagve
        def refocus_player_id():
            popup.lift()
            popup.focus_force()
            player_id_entry.focus_force()
            player_id_entry.selection_range(0, tk.END)
            print("DEBUG: duplicate focus =", popup.focus_get())

        popup.after(1, refocus_player_id)

    #new player helper
    def _handle_new_player(self, popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry):
        player_id = player_id_var.get().strip()
        codename = codename_var.get().strip()
        equipment_id = equipment_id_var.get().strip()

        #player/equipment id cannot be blank
        if not player_id:
            messagebox.showerror("Error", "Player ID required!", parent=popup)
            return
        if not equipment_id:
            messagebox.showerror("Error", "Equipment ID required!", parent=popup)
            return

        #integer check for player/equipment
        try:
            player_id_int = int(player_id)
            # print(f"DEBUG raw player_id='{player_id}' parsed={player_id_int}")
        except ValueError:
            messagebox.showerror("Error", "Player ID must be integer!", parent=popup)
            return
        try:
            equipment_id_int = int(equipment_id)
        except ValueError:
            messagebox.showerror("Error", "Equipment ID must be integer!", parent=popup)
            return

        #no duplicate player id
        if self._existing_player(player_id_int):
            self._handle_duplicate(player_id_int, popup, player_id_entry)
            return

        existing_codename = playerIdExist(player_id_int)
        if existing_codename:
            codename = existing_codename
            messagebox.showinfo("Player Found", f"Codename: {codename}", parent=popup)
        else:
            if not codename:
                messagebox.showerror("Error", "Codename is required for new player!", parent=popup)

                # enable input into codename after popup message
                def refocus_codename():
                    popup.lift()
                    popup.focus_force()
                    codename_entry.focus_force()
                    codename_entry.selection_range(0, tk.END)

                popup.after(1, refocus_codename)
                return

            insert_player(player_id_int, codename)

        player = PlayerEntry(player_id_int, codename, equipment_id_int)
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        if red_team:
            if len(self.red_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Unable to add. Red team full!", parent=popup)
                return
            self.red_players.append(player)
            self._add_to_team("red", player)
        if green_team:
            if len(self.green_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Unable to add. Green team full!", parent=popup)
                return
            self.green_players.append(player)
            self._add_to_team("green", player)

        if not existing_codename:
            messagebox.showinfo("Added", "New player added to database", parent=popup)

        # clear entries
        player_id_var.set("")
        codename_var.set("")
        equipment_id_var.set("")

        popup.destroy()

    def _add_to_team(self, team: str, player: PlayerEntry):
        if team == "red":
            self._write_player_to_row("red", player)
        elif team == "green":
            self._write_player_to_row("green", player)
        else:
            return
        print(f"{player.codename} (ID: {player.player_id}, EQ: {player.equipment_id})")  #in terminal

    # Add player to database and team
    def add_player(self, event=None):
        player_id_var = tk.StringVar()
        codename_var = tk.StringVar()
        equipment_id_var = tk.StringVar()

        popup = tk.Toplevel(self.master)
        popup.title("Add Player")
        popup.configure(bg="black")
        popup.resizable(width=False, height=False)
        popup.transient(self.master)
        popup.grab_set()

        label_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold")}
        entry_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold"), "insertbackground": "white"}

        tk.Label(popup, text="PLAYER ID:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        player_id_entry = tk.Entry(popup, textvariable=player_id_var, **entry_style)
        player_id_entry.grid(row=0, column=1, padx=10, pady=5)
        player_id_entry.focus()

        tk.Label(popup, text="CODENAME:", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        codename_entry = tk.Entry(popup, textvariable=codename_var, **entry_style)
        codename_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="EQUIPMENT ID:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.equipment_entry = tk.Entry(popup, textvariable=equipment_id_var, **entry_style)
        self.equipment_entry.grid(row=2, column=1, padx=10, pady=5)

        #player id field check
        def check_player_id():
            player_id = player_id_var.get().strip()
            if not player_id:
                return

            try:
                player_id_int = int(player_id)
            except ValueError:
                messagebox.showerror("Error", "Player ID must be an integer!", parent=popup)
                return

            if self._existing_player(player_id_int):
                self._handle_duplicate(player_id_int, popup, player_id_entry)
                return

            existing_codename = playerIdExist(player_id_int)
            if existing_codename:
                codename_var.set(existing_codename)
                self.equipment_entry.focus()
            else:
                codename_var.set("")
                codename_entry.focus()

        player_id_entry.bind("<Return>", lambda e: check_player_id())
        codename_entry.bind("<Return>", lambda e: self.equipment_entry.focus())
        self.equipment_entry.bind("<Return>", lambda e: self._handle_new_player(popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry))

        tk.Button(popup, text="ADD", command=lambda: self._handle_new_player(popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry)).grid(row=3, column=0, columnspan=2, pady=10)

    def load_players_from_db(self):
        print("DEBUG: database.conn =", database.conn)

        if not database.conn:
            return

        try:
            print("DEBUG: Loading players from DB...")
            with database.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM players")
                records = cursor.fetchall()
                print("DEBUG: records =", records)

            for player_id, codename, equipment_id in records:
                player = PlayerEntry(player_id, codename, equipment_id)

                # if equipment_id % 2 == 1:
                if len(self.red_players) < MAX_PLAYERS:
                    self.red_players.append(player)
                    self._write_player_to_row("red", player)
                # else:
                elif len(self.green_players) < MAX_PLAYERS:
                    self.green_players.append(player)
                    self._write_player_to_row("green", player)
        except Exception as e:
            print(f"Error loading players from database: {e}")

    def start_game(self, event=None):
        # messagebox.showinfo("Start Game", "Not wired yet.")
        """Code up f5 key or equivalent to switch to play action display and start game (you can do this in
        the original window or start another window)"""
        play_window = tk.Toplevel(self.master)
        play_window.title("PLAY GAME")
        #root.title("PLAY GAME")
        play_window.geometry("1000x637")
        #root.mainloop()
        

        screen = PlayAction(play_window, red_players=self.red_players, green_players=self.green_players)
        screen.pack(fill="both", expand=True)

        #root.mainloop()


    # change IP address
    def switch_network(self, event=None):
        ip = simpledialog.askstring("Switch Network", f"Current IP: {self.ip}\nEnter new IP:")
        if ip:
            self.ip = ip
            messagebox.showinfo("Network Changed", f"New IP: {self.ip}")

    # Reset all players
    def reset_players(self, event=None) -> None:
        self.red_players.clear()
        self.green_players.clear()

        for row in self.red_rows:
            row["codename"].config(text="")
        for row in self.green_rows:
            row["codename"].config(text="")

        self.player_id_var.set("")
        self.codename_var.set("")
        self.equipment_id_var.set("")

    def quit(selfself):
        self.master.destroy()

    # def start_game(self, event=None):
    #     # messagebox.showinfo("Start Game", "Not wired yet.")
    #     """Code up f5 key or equivalent to switch to play action display and start game (you can do this in
    #     the original window or start another window)"""
    #     root = tk.Tk()
    #     root.title("PLAY GAME")
    #     root.geometry("900x500")
    
    #     # Player Action Screen
    #     root.rowconfigure(0, weight=1)
    #     root.columnconfigure(0, weight=1)
    
    #     action_content = tk.Frame(root, bg="black")
    #     action_content.grid(row=0, column=0, sticky="nsew")
    
    #     action_content.rowconfigure(0, weight=1) #score
    #     action_content.rowconfigure(1, weight=1) #action
    #     action_content.rowconfigure(2, weight=0) #Time remaining
    #     action_content.columnconfigure(0, weight=1)
    
    #     #score
    #     score = tk.Frame(action_content, bg="black")
    #     score.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    #     #action
    #     action = tk.Frame(action_content, bg="blue")
    #     score.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    
    #     #Time remianing
    #     timer = tk.Frame(action_content, bg="black")
    #     timer.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    #     # title1 = Current Scores
    #     title1 = tk.Label(action_content, text="Current Scores", font=("Courier New", 20, "bold"), fg="green", bg="black")
    #     title1.grid(row=0, column=1, padx=20, pady=10, sticky="e") # alligned right
        
    #     # title2 = XP
    #     title2 = tk.Label(action_content, text="XP", font=("Courier New", 20, "bold"), fg="red", bg="black")
    #     title2.grid(row=0, column=0, padx=20, pady=10, sticky="w") # alligned left
    
    #     root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")

    #trying to match splash screen
    width = 1000
    height = 637

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    screen = PlayerScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()

"""
import tkinter as tk  # gui
from tkinter import messagebox, simpledialog
from dataclasses import dataclass
from typing import List

import database
from database import insert_player, playerIdExist
from BaseMenu import BaseMenu

# PLAYER SCREEN
# red team (odd eq id) / green team (even eq id)
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


# PLAYER SCREEN
class PlayerScreen(BaseMenu):
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

    def _style(self) -> None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="black")
        content.grid(row=0, column=0, sticky="nsew")

        content.rowconfigure(0, weight=0)  #title
        content.rowconfigure(1, weight=1) #team
        content.rowconfigure(2, weight=0)  #menu
        content.columnconfigure(0, weight=1)

        # title
        title = tk.Label(content, text="PLAYER ENTRY SCREEN", font=("Courier New", 20, "bold"), fg="white",bg="black")  # fg = foreground (text color), bg = background
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # sticky="w" means aligned left

        #roster
        main = tk.Frame(content, bg="black")
        main.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)  # red
        main.columnconfigure(1, weight=1)  # green

        # red team
        red_panel = self._team_panel(main, "RED TEAM", bg="black", accent="red")
        red_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # green team
        green_panel = self._team_panel(main, "GREEN TEAM", bg="black", accent="green")
        green_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self._build_rows(red_panel, team="red")
        self._build_rows(green_panel, team="green")

        super()._ui(content) #base menu

        # # menu
        # menu = tk.Frame(content, bg="black")
        # menu.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        # for i in range(6):
        #     menu.columnconfigure(i, weight=1)
        # self._menu(menu, 0, "F1\nAdd\nPlayer", self.add_player)
        # self._menu(menu, 1, "F2\nLoad\nPlayers", self.load_players_from_db)
        # self._menu(menu, 2, "F5\nStart\nGame", self.start_game)
        # self._menu(menu, 3, "F10\nSwitch\nNetwork", self.switch_network)
        # self._menu(menu, 4, "F12\nClear\nPlayers", self.reset_players)
        # self._menu(menu, 5, "ESC\nExit", self.quit)
        # button = tk.Button(self, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)

    def _make_scroll(self, parent, bg: str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        vbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview, width=5)
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

        canvas.bind("<Return>", _bind_wheel)
        inner.bind("<Return>", _bind_wheel)

        canvas.bind("<Leave>", _unbind_wheel)
        inner.bind("<Leave>", _unbind_wheel)

        return canvas, inner

    # def _menu(self, parent, col: int, text: str, cmd) -> None:
    #     bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
    #     bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _team_panel(self, parent, title:str, bg="black", accent="white") -> tk.Frame:
        panel = tk.Frame(parent, bg=bg, bd=2, relief="groove")
        panel.rowconfigure(1, weight=1)
        panel.columnconfigure(0, weight=1)

        header = tk.Label(panel, text=title, font=("Courier New", 20, "bold"), fg=accent, bg=bg)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        body_container = tk.Frame(panel, bg=bg)
        body_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        canvas, inner = self._make_scroll(body_container, bg)

        inner.columnconfigure(0, weight=0, minsize=2) #index/player id
        inner.columnconfigure(1, weight=1, minsize=180) #codename
        inner.columnconfigure(2, weight=1, minsize=10) #equipment id

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
        #header
        tk.Label(body, text="CODENAME", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)

        # cell_style = {"bg": bg, "fg": "white", "font": ("Courier New", 12, "bold"), "relief": "groove", "bd": 2, "anchor": "w", "padx": 6}

        for i in range(1, MAX_PLAYERS + 1):
            index = tk.Label(body, text=str(i), font=("Courier New", 20, "bold"), fg="white", bg=bg)
            index.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            code = tk.Label(body, bg=bg, fg="white", font=("Courier New", 14, "bold"), relief="groove", anchor="w", padx=6)
            code.grid(row=i, column=1, padx=3, pady=10, sticky="ew")

            rows.append({"codename": code})

        if team == "red":
            self.red_rows = rows
        else:
            self.green_rows = rows

    # def _key_input(self, event=None):
    #     self.master.bind("<F1>", self.add_player)
    #     self.master.bind("<F2>", self.load_players_from_db)
    #     self.master.bind("<F5>", lambda e: self.start_game())
    #     self.master.bind("<F10>", self.switch_network)
    #     self.master.bind("<F12>", self.reset_players)
    #     self.master.bind("<Escape>", lambda e: self.quit())

    def _write_player_to_row(self, team:str, player:PlayerEntry) -> None:
        rows = self.red_rows if team == "red" else self.green_rows
        index = len(self.red_players) - 1 if team == "red" else len(self.green_players) - 1

        if 0 <= index < len(rows):
            rows[index]["codename"].config(text=player.codename)

    #helper for duplicate check in _handle_new_player
    def _existing_player(self, player_id):
        for player in self.red_players + self.green_players:
            if player.player_id == player_id:
                return True
        return False

    #duplicate player id helper
    def _handle_duplicate(self, player_id_int, popup, player_id_entry):
        messagebox.showerror("Error", f"Player ID {player_id_int} already exists!", parent=popup) #parent=popup: belongs to popup window

        # enable input into player id after popup messagve
        def refocus_player_id():
            popup.lift()
            popup.focus_force()
            player_id_entry.focus_force()
            player_id_entry.selection_range(0, tk.END)
            print("DEBUG: duplicate focus =", popup.focus_get())

        popup.after(1, refocus_player_id)

    #new player helper
    def _handle_new_player(self, popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry):
        player_id = player_id_var.get().strip()
        codename = codename_var.get().strip()
        equipment_id = equipment_id_var.get().strip()

        #player/equipment id cannot be blank
        if not player_id:
            messagebox.showerror("Error", "Player ID required!", parent=popup)
            return
        if not equipment_id:
            messagebox.showerror("Error", "Equipment ID required!", parent=popup)
            return

        #integer check for player/equipment
        try:
            player_id_int = int(player_id)
            # print(f"DEBUG raw player_id='{player_id}' parsed={player_id_int}")
        except ValueError:
            messagebox.showerror("Error", "Player ID must be integer!", parent=popup)
            return
        try:
            equipment_id_int = int(equipment_id)
        except ValueError:
            messagebox.showerror("Error", "Equipment ID must be integer!", parent=popup)
            return

        #no duplicate player id
        if self._existing_player(player_id_int):
            self._handle_duplicate(player_id_int, popup, player_id_entry)
            return

        existing_codename = playerIdExist(player_id_int)
        if existing_codename:
            codename = existing_codename
            messagebox.showinfo("Player Found", f"Codename: {codename}", parent=popup)
        else:
            if not codename:
                messagebox.showerror("Error", "Codename is required for new player!", parent=popup)

                # enable input into codename after popup message
                def refocus_codename():
                    popup.lift()
                    popup.focus_force()
                    codename_entry.focus_force()
                    codename_entry.selection_range(0, tk.END)

                popup.after(1, refocus_codename)
                return

            insert_player(player_id_int, codename)

        player = PlayerEntry(player_id_int, codename, equipment_id_int)
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        if red_team:
            if len(self.red_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Unable to add. Red team full!", parent=popup)
                return
            self.red_players.append(player)
            self._add_to_team("red", player)
        if green_team:
            if len(self.green_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Unable to add. Green team full!", parent=popup)
                return
            self.green_players.append(player)
            self._add_to_team("green", player)

        if not existing_codename:
            messagebox.showinfo("Added", "New player added to database", parent=popup)

        # clear entries
        player_id_var.set("")
        codename_var.set("")
        equipment_id_var.set("")

        popup.destroy()

    def _add_to_team(self, team: str, player: PlayerEntry):
        if team == "red":
            self._write_player_to_row("red", player)
        elif team == "green":
            self._write_player_to_row("green", player)
        else:
            return
        print(f"{player.codename} (ID: {player.player_id}, EQ: {player.equipment_id})")  #in terminal

    def _equipment_popup(self, records) -> None: #enter all eq id when loading from db
        popup = tk.Toplevel(self.master)
        popup.title("Enter equipment IDs")
        popup.configure(bg="black")
        popup.resizable(width=False, height=False)
        popup.transient(self.master)
        popup.grab_set()

        label_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold")}
        entry_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold"), "insertbackground": "white"}

        tk.Label(popup, text="PLAYER ID", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w") #header
        tk.Label(popup, text="CODENAME", **label_style).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Label(popup, text="EQUIPMENT ID", **label_style).grid(row=0, column=2, padx=10, pady=10, sticky="w")

        equipment_vars = []

        for i, (player_id, codename) in enumerate(records, start=1):
            tk.Label(popup, text=str(player_id), **label_style).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            tk.Label(popup, text=codename, **label_style).grid(row=i, column=1, padx=10, pady=5, sticky="w")

            equipment_var = tk.StringVar()
            equipment_entry = tk.Entry(popup, textvariable=equipment_var, **entry_style)
            equipment_entry.grid(row=i, column=2, padx=10, pady=5)

            equipment_vars.append((player_id, codename, equipment_var))

        tk.Button(
            popup,
            text="Continue",
            command=lambda: self._finish_db_load(popup, equipment_vars),
            font=("Courier New", 12, "bold")).grid(row=len(records) + 1, column=1, padx=10, pady=15, sticky="ew")
        tk.Button(
            popup,
            text="Cancel",
            command=popup.destroy,
            font=("Courier New", 12, "bold")).grid(row=len(records) + 1, column=2, padx=10, pady=15, sticky="ew")

    def _finish_db_load(self, popup, equipment_vars) -> None:
        loaded_players = []
        used_eid = set()

        for player_id, codename, equipment_var in equipment_vars:
            equipment_text = equipment_var.get().strip()
            if not equipment_text: #empty check
                messagebox.showerror("Error", f"Equipment ID required for {codename}!", parent=popup)
                return

            try:
                equipment_id = int(equipment_text) #integer check
            except ValueError:
                messagebox.showerror("Error", f"Equipment ID for {codename} must be integer!", parent=popup)
                return

            if equipment_id in used_eid: #duplicate check
                messagebox.showerror("Error", f"Duplicate equipment ID {equipment_id}", parent=popup)
                return

            used_eid.add(equipment_id)
            loaded_players.append(PlayerEntry(player_id, codename, equipment_id))
        self.reset_players()

        for player in loaded_players:
            red_team = (player.equipment_id % 2 == 1)
            green_team = (player.equipment_id % 2 == 0)

            if red_team:
                if len(self.red_players) >= MAX_PLAYERS:
                    messagebox.showerror("Error", "Unable to add. Red team full!", parent=popup)
                    return
                self.red_players.append(player)
                self._add_to_team("red", player)
            if green_team:
                if len(self.green_players) >= MAX_PLAYERS:
                    messagebox.showerror("Error", "Unable to add. Green team full!", parent=popup)
                    return
                self.green_players.append(player)
                self._add_to_team("green", player)

        popup.destroy()
        messagebox.showinfo("Success", f"Successfully loaded {len(loaded_players)} players!", parent=self.master)

    # Add player to database and team
    def add_player(self, event=None):
        player_id_var = tk.StringVar()
        codename_var = tk.StringVar()
        equipment_id_var = tk.StringVar()

        popup = tk.Toplevel(self.master)
        popup.title("Add Player")
        popup.configure(bg="black")
        popup.resizable(width=False, height=False)
        popup.transient(self.master)
        popup.grab_set()

        label_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold")}
        entry_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold"), "insertbackground": "white"}

        tk.Label(popup, text="PLAYER ID:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        player_id_entry = tk.Entry(popup, textvariable=player_id_var, **entry_style)
        player_id_entry.grid(row=0, column=1, padx=10, pady=5)
        player_id_entry.focus()

        tk.Label(popup, text="CODENAME:", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        codename_entry = tk.Entry(popup, textvariable=codename_var, **entry_style)
        codename_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="EQUIPMENT ID:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.equipment_entry = tk.Entry(popup, textvariable=equipment_id_var, **entry_style)
        self.equipment_entry.grid(row=2, column=1, padx=10, pady=5)

        #player id field check
        def check_player_id():
            player_id = player_id_var.get().strip()
            if not player_id:
                return

            try:
                player_id_int = int(player_id)
            except ValueError:
                messagebox.showerror("Error", "Player ID must be an integer!", parent=popup)
                return

            if self._existing_player(player_id_int):
                self._handle_duplicate(player_id_int, popup, player_id_entry)
                return

            existing_codename = playerIdExist(player_id_int)
            if existing_codename:
                codename_var.set(existing_codename)
                self.equipment_entry.focus()
            else:
                codename_var.set("")
                codename_entry.focus()

        player_id_entry.bind("<Return>", lambda e: check_player_id())
        codename_entry.bind("<Return>", lambda e: self.equipment_entry.focus())
        self.equipment_entry.bind("<Return>", lambda e: self._handle_new_player(popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry))

        tk.Button(popup, text="ADD", command=lambda: self._handle_new_player(popup, player_id_var, codename_var, equipment_id_var, player_id_entry, codename_entry)).grid(row=3, column=0, columnspan=2, pady=10)

    def load_players_from_db(self, event=None):
        print("DEBUG: database.conn =", database.conn)

        if not database.conn:
            messagebox.showerror("Database Error", "No database connection.", parent=self.master)
            return

        confirm = messagebox.askyesno(
            "Load Players from Database",
            "Loading from database will override any newly added players with the same player ID.\n Do you want to continue?",
            parent=self.master)
        if not confirm:
            return

        try:
            print("DEBUG: Loading players from DB...")
            with database.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM players")
                records = cursor.fetchall()
                print("DEBUG: records =", records)

            if not records: #empty db
                messagebox.showinfo("Loading Players...", "No players found.", parent=self.master)
                return

            self._equipment_popup(records)

        except Exception as e:
            messagebox.showerror("Database Error",f"Error loading players from database: {e}", parent=self.master)

    def start_game(self, event=None):
        # messagebox.showinfo("Start Game", "Not wired yet.")
        # Code up f5 key or equivalent to switch to play action display and start game (you can do this in
        # the original window or start another window)
        play_window = tk.Toplevel(self.master)
        play_window.title("PLAY GAME")
        play_window.resizable(width=False, height=False)
        # root = tk.Tk()
        # root.title("PLAY GAME")
        # root.geometry("900x500")
        # root.mainloop()

    # change IP address
    def switch_network(self, event=None):
        ip = simpledialog.askstring("Switch Network", f"Current IP: {self.ip}\nEnter new IP:")
        if ip:
            self.ip = ip
            messagebox.showinfo("Network Changed", f"New IP: {self.ip}")

    # Reset all players
    def reset_players(self, event=None) -> None:
        self.red_players.clear()
        self.green_players.clear()

        for row in self.red_rows:
            row["codename"].config(text="")
        for row in self.green_rows:
            row["codename"].config(text="")

        self.player_id_var.set("")
        self.codename_var.set("")
        self.equipment_id_var.set("")

    def quit(self):
        self.master.destroy()

    # def start_game(self, event=None):
    #     # messagebox.showinfo("Start Game", "Not wired yet.")
    #     Code up f5 key or equivalent to switch to play action display and start game (you can do this in
    #     the original window or start another window)
    #     root = tk.Tk()
    #     root.title("PLAY GAME")
    #     root.geometry("900x500")
    #
    #     # Player Action Screen
    #     root.rowconfigure(0, weight=1)
    #     root.columnconfigure(0, weight=1)
    #
    #     action_content = tk.Frame(root, bg="black")
    #     action_content.grid(row=0, column=0, sticky="nsew")
    #
    #     action_content.rowconfigure(0, weight=1) #score
    #     action_content.rowconfigure(1, weight=1) #action
    #     action_content.rowconfigure(2, weight=0) #Time remaining
    #     action_content.columnconfigure(0, weight=1)
    #
    #     #score
    #     score = tk.Frame(action_content, bg="black")
    #     score.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    #
    #     #action
    #     action = tk.Frame(action_content, bg="blue")
    #     score.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    #
    #     #Time remianing
    #     timer = tk.Frame(action_content, bg="black")
    #     timer.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    #
    #     root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")

    #trying to match splash screen
    width = 1000
    height = 637

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    screen = PlayerScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()
"""

