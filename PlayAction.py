import tkinter as tk
from BaseMenu import BaseMenu

class PlayAction(BaseMenu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._style()
        self._ui()

    def _style(self) ->None:
        self.master.config(background="black")
        self.configure(background="black")

    def _ui(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        content = tk.Frame(self, bg="black")
        content.grid(row=0, column=0, sticky="nsew")

        content.rowconfigure(0, weight=3) #current scores
        content.rowconfigure(1, weight=2) #game action
        content.rowconfigure(2, weight=0) #countdown timer
        content.rowconfigure(3, weight=0) #menu
        content.columnconfigure(0, weight=1)

        #current scores
        self.current_game_score(content)
        #game action
        self.game_action(content)
        #countdown timer
        self.countdown_timer(content)
        #menu
        super()._ui(content)

    def current_game_score(self, parent):
        #--top section holding both teams and score totals--
        #showing one example here so you have an idea on what this outline needs to be filled out with
        # score = tk.Frame(self, bg="black")
        # score.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        current_score = tk.Frame(self, bg="black")
        current_score.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        #--scoreboard rows/columns--
        #here needing score.rowconfigure(x, weight=y) or score.columnconfigure(m, weight=n)
        
        #title row
        #team row
        #score row
        #red column
        #green column

        #--title: CURRENT SCORES--
        #fg means foreground, bg means background
        #title label (score, text=, font=("Courier New", size, "bold"), fg=, bg=)
        #add label to grid, so title.grid()

        #--red team panel (left)--
        #frame
        #title
        #red_player = tk.Lable()
        #red_player.pack(anchor="w")
        #red_score = tk.Label()
        #red_score.pack(anchor="e")

        #--green team panel (left)--
        #frame
        #title
        #green_player = tk.Label()
        #green_player.pack(anchor="w")
        #green_score = tk.Label()
        #green_score.pack(anchor="e")

        #--team totals--
        #red_total = tk.Label()
        #red_total.grid()

        #green_total = tk.Label()
        #green_total.grid()
        pass

    def game_action(self, parent):
        #similar to las t function but now this parft is the section showing the live log
        #action = tk.Frame(self, bg="blue")
        #action.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        #--title--

        #--log container--

        #--listbox--
        # self.action_listbox = tk.Listbox(log, bg="blue", fg="white", font="Courier New", 16, "bold"), relief="flat", borderwidth=0)
        # self.action_listbox.grid(row=0, column=0, sticky="nsew")
        pass

    def countdown_timer(self, parent):
        pass

