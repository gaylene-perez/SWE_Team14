import tkinter as tk  # gui
from tkinter import messagebox, simpledialog
from dataclasses import dataclass
from typing import List
from database import insert_player, playerIdExist

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
    codename: str
    equipment_id: int


# PLAYER SCREEN
class PlayerScreen(tk.Frame):
    ip = "127.0.0.1"

    def __init__(self, master):
        super().__init__(master)
        self.master = master

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

    def _ui(self) -> None:
        # self.master.configure(bg="black")
        # self.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="black")
        content.grid(row=0, column=0, sticky="nsew")
        # content.pack(fill="both", expand=True)

        content.rowconfigure(0, weight=0)  #title
        content.rowconfigure(1, weight=0) #form
        content.rowconfigure(2, weight=1)  #team
        content.rowconfigure(3, weight=0) #menu
        content.columnconfigure(0, weight=1)

        # title
        title = tk.Label(content, text="PLAYER ENTRY SCREEN", font=("Courier New", 20, "bold"), fg="white",bg="black")  # fg = foreground (text color), bg = background
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # sticky="w" means aligned left

        #form
        form = tk.Frame(content, bg="black")
        form.grid(row=1, column=0, padx=10, pady=(10,6), sticky="w")
        # form = tk.Frame(main, bg="black")
        # form.grid(row=0, column=0, sticky="n", padx=(0, 20))
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        label_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold")}
        entry_style = {"bg": "black", "fg": "white", "font": ("Courier New", 12, "bold"), "insertbackground": "white", "relief": "groove"}

        # codename
        tk.Label(form, text="CODENAME:", **label_style).grid(row=0, column=0, sticky="e", padx=(0, 10), pady=4)
        self.codename_entry = tk.Entry(form, textvariable=self.codename_var, **entry_style)
        self.codename_entry.grid(row=0, column=1, sticky="ew", pady=4)

        # equipment id
        tk.Label(form, text="EQUIPMENT ID:", **label_style).grid(row=1, column=0, sticky="e", padx=(0, 10), pady=4)
        self.equipment_entry = tk.Entry(form, textvariable=self.equipment_id_var, **entry_style)
        self.equipment_entry.grid(row=1, column=1, sticky="ew", pady=4)

        self.codename_entry.bind("<Return>", self.add_player)
        self.equipment_entry.bind("<Return>", self.add_player)

        #roster
        main = tk.Frame(content, bg="black")
        main.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)  # red
        main.columnconfigure(1, weight=1)  # green

        # red team
        red_panel = self._team_panel(main, "RED TEAM", bg="black", accent="red")
        red_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # tk.Label(self, text="RED TEAM (ODD)").grid(row=7, column=0)
        # self.red_listbox = tk.Listbox(self, height=10, width=30)
        # self.red_listbox.grid(row=8, column=0)

        # green team
        green_panel = self._team_panel(main, "GREEN TEAM", bg="black", accent="green")
        green_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        # tk.Label(self, text="GREEN TEAM (EVEN)").grid(row=7, column=1)
        # self.green_listbox = tk.Listbox(self, height=10, width=30)
        # self.green_listbox.grid(row=8, column=1)

        self._build_rows(red_panel, team="red")
        self._build_rows(green_panel, team="green")

        # menu
        menu = tk.Frame(content, bg="black")
        menu.grid(row=3, column=0, sticky="ew", padx=16, pady=(0, 12))
        for i in range(5):
            menu.columnconfigure(i, weight=1)
        self._menu(menu, 0, "F1\nAdd\nPlayer", self.add_player)
        self._menu(menu, 1, "F5\nStart\nGame", self.start_game)
        self._menu(menu, 2, "F10\nSwitch\nNetwork", self.switch_network)
        self._menu(menu, 3, "F12\nClear\nPlayers", self.reset_players)
        self._menu(menu, 4, "ESC\nExit", self.quit)
        # button = tk.Button(self, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)


    def _menu(self, parent, col: int, text: str, cmd) -> None:
        bn = tk.Button(parent, text=text, command=cmd, fg="blue", bg="#8a8a8a", activebackground="#9a9a9a", relief="ridge", bd=2, font=("Courier New", 10, "bold"), height=3)
        bn.grid(row=0, column=col, padx=6, pady=8, sticky="ew")

    def _make_scroll(self, parent, bg:str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        vbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview, width=3)
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
        #headers
        # tk.Label(body, text="#", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(body, text="PLAYER\nID", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=0, sticky="w", padx=10)
        tk.Label(body, text="CODENAME", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=1, sticky="w", padx=10)
        tk.Label(body, text="EQUIPMENT\nID", font=("Courier New", 14, "bold"), fg=accent, bg=bg).grid(row=0, column=2, sticky="w", padx=10)

        cell_style = {"bg": bg, "fg": "white", "font": ("Courier New", 12, "bold"), "relief": "groove", "bd": 2, "anchor": "w", "padx": 6}

        for i in range(1, MAX_PLAYERS + 1):
            index = tk.Label(body, text=str(i), font=("Courier New", 20, "bold"), fg="white", bg=bg)
            index.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            code = tk.Entry(body, bg=bg, relief="groove")
            code.grid(row=i, column=1, padx=3, pady=10, sticky="ew")

            eid = tk.Entry(body, bg=bg, relief="groove")
            eid.grid(row=i, column=2, padx=3, pady=3, sticky="ew")

            rows.append({"codename": code, "equipment": eid})

        if team == "red":
            self.red_rows = rows
        else:
            self.green_rows = rows

    def _key_input(self):
        # self.master.bind("<F1>", lambda e: self.handle_new_player())
        self.master.bind("<F1>", self.add_player)
        # root.bind("<F5>", self.start_game)
        self.master.bind("<F5>", lambda e: self.start_game())
        # self.master.bind("<F10>", lambda e: self.switch_network())
        # self.master.bind("<F12>", lambda e: self.reset_players())
        self.master.bind("<F12>", self.reset_players)
        # self.master.bind("<Escape>", self.quit())
        self.master.bind("<Escape>", lambda e: self.quit())

        # k = Tk()
        # k.bind("<F12>", self.reset_players()) #bind(event, function)

    # def query_player(self, codename: str) -> PlayerEntry:
    #     for entry in self.red_players:
    #         if entry.codename == codename:
    #             return entry
    #     for entry in self.green_players:
    #         if entry.codename == codename:
    #             return entry
    #     return None
    #

    def _write_player_to_row(self, team:str, player:PlayerEntry) -> None:
        rows = self.red_rows if team == "red" else self.green_rows
        index = len(self.red_players) - 1 if team == "red" else len(self.green_players) - 1

        if 0 <= index < len(rows):
            rows[index]["codename"].config(text=player.codename)
            rows[index]["equipment"].config(text=player.equipment_id)


    # Add player to database and team
    # def add_new_player(self, player: PlayerEntry) -> None:
    def add_player(self, event=None):
        # player_id = int(self.player_id_var.get().strip()) #add team and assign player id in next available slot/row
        codename = self.codename_var.get().strip()
        equipment_id = self.equipment_id_var.get().strip()

        if not equipment_id:
            messagebox.showerror("Error", "Equipment ID is required!")
            return

        try:
            equipment_id_int = int(equipment_id)
        except ValueError:
            messagebox.showerror("Error", "Equipment ID must be integers!")
            return

        existing_codename = playerIdExist(equipment_id_int)
        if existing_codename:
            codename = existing_codename
            messagebox.showinfo("Player Found", f"Codename: {codename}")
        else:
            if not codename:
                messagebox.showerror("Error", "Enter a codename for new player")
                return
            insert_player(codename, equipment_id)
            messagebox.showinfo("Added", "New player added to database")

        player = PlayerEntry(codename, equipment_id_int)
        red_team = (player.equipment_id % 2 == 1)
        green_team = (player.equipment_id % 2 == 0)

        if red_team:
            if len(self.red_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Red team has 15 players!")
                return
            self.red_players.append(player)
            self.add_to_team("red", player)
        if green_team:
            if len(self.green_players) >= MAX_PLAYERS:
                messagebox.showerror("Error", "Green team has 15 players!")
                return
            self.green_players.append(player)
            self.add_to_team("green", player)

        self.add_to_team(player)

        # clear entries
        self.codename_var.set("")
        self.equipment_id_var.set("")

    def add_to_team(self, team: str, player: PlayerEntry):
        if player.equipment_id % 2 == 1:
            if len(self.red_players) < MAX_PLAYERS:
                self._write_player_to_row("red", player)
                # self.red_listbox.insert(tk.END, f"{player.codename} (ID:{player.player_id}, EQ:{player.equipment_id})")
            else:
                messagebox.showerror("Error", "Red team full!")
        else:
            if len(self.green_players) < MAX_PLAYERS:
                self._write_player_to_row("green", player)
                # self.green_listbox.insert(tk.END,f"{player.codename} (ID:{player.player_id}, EQ:{player.equipment_id})") #in terminal
            else:
                messagebox.showerror("Error", "Green team full!")

    # Remove selected player
    # def remove_player(self):
    #     red_index = self.red_listbox.curselection()
    #     green_index = self.green_listbox.curselection()
    #
    #     if red_index:
    #         idx = red_index[0]
    #         self.red_listbox.delete(idx)
    #         self.red_players.pop(idx)
    #     elif green_index:
    #         idx = green_index[0]
    #         self.green_listbox.delete(idx)
    #         self.green_players.pop(idx)
    #     else:
    #         messagebox.showinfo("Remove Player", "Select a player to remove first.")

    # Reset all players
    def reset_players(self, event=None) -> None:
        self.red_players.clear()
        self.green_players.clear()

        for row in self.red_rows:
            row["codename"].config(text="")
            row["equipment"].config(text="")
        for row in self.green_rows:
            row["codename"].config(text="")
            row["equipment"].config(text="")

        self.codename_var.set("")
        self.equipment_id_var.set("")


    def start_game(self, event=None):
        # messagebox.showinfo("Start Game", "Not wired yet.")
        """Code up f5 key or equivalent to switch to play action display and start game (you can do this in
        the original window or start another window)"""
        root = tk.Tk()
        root.title("PLAY GAME")
        root.geometry("900x500")
        root.mainloop()

    # change IP address
    def switch_network(self):
        # temp = self.ip
        # self.ip = simpledialog.askstring("Input", f"Current IP address: {self.ip}\nPlease enter a valid IP address:", parent=root)
        #
        # if self.ip is None:
        #     self.ip = temp
        #
        # return self.ip
        ip = simpledialog.askstring("Switch Network", f"Current IP: {self.ip}\nEnter new IP:")
        if ip:
            self.ip = ip
            messagebox.showinfo("Network Changed", f"New IP: {self.ip}")

    def quit(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAYER SCREEN")
    # root.geometry("900x500")
    root.state("zoomed")
    screen = PlayerScreen(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()