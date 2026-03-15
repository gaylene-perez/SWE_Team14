"""
import tkinter as tk
from BaseMenu import BaseMenu

class PlayAction(BaseMenu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

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

    def _current_game_score(self, parent):
        #--top section holding both teams and score totals--
        #showing one example here so you have an idea on what this outline needs to be filled out with
        # score = tk.Frame(self, bg="black")
        # score.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
        current_score = tk.Frame(self, bg="black")
        current_score.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        #--scoreboard rows/columns--
        #here needing score.rowconfigure(x, weight=y) or score.columnconfigure(m, weight=n)
        
        #title row
        current_score.rowcongigure(0, weight=0)
        
        #team row
        current_score.rowconfigure(1, weight=1)
        
        #score row
        current_score.rowconfigure(2, weight=2)
        
        #red column
        current_score.columnconfigure(0, weight=1)
        
        #green column
        current_score.columnconfigure(1, weight=1)

        #--title: CURRENT SCORES--
        #fg means foreground, bg means background
        #title label (score, text=, font=("Courier New", size, "bold"), fg=, bg=)
        #add label to grid, so title.grid()

        # title1 = Current Scores
        title1 = tk.Label(current_score, text="Current Scores", font=("Courier New", 20, "bold"), fg="green", bg="black")
        title1.grid(row=0, column=1, padx=20, pady=10, sticky="e") # alligned right
        
        # title2 = XP
        title2 = tk.Label(current_score, text="XP", font=("Courier New", 20, "bold"), fg="red", bg="black")
        title2.grid(row=0, column=0, padx=20, pady=10, sticky="w") # alligned left

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
        # pass

    def _game_action(self, parent):
        #similar to last function but now this parft is the section showing the live log
        #action = tk.Frame(self, bg="blue")
        #action.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        current_action = tk.Frame(self, bg="blue")
        current_action.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        #--title--

        #--log container--

        #--listbox--
        # self.action_listbox = tk.Listbox(log, bg="blue", fg="white", font="Courier New", 16, "bold"), relief="flat", borderwidth=0)
        # self.action_listbox.grid(row=0, column=0, sticky="nsew")
        # pass

    def _countdown_timer(self, parent):

        timer = tk.Frame(self, bg="black")
        timer.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("PLAY GAME")

    #trying to match splash screen
    width = 1000
    height = 637

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    screen = PlayAction(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()
"""

import tkinter as tk
from BaseMenu import BaseMenu

class PlayAction(BaseMenu):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self._style()
        self._ui()

    def _key_input(self) ->None:
        pass

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

        content.rowconfigure(0, weight=1) #current scores
        content.rowconfigure(1, weight=1) #game action
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
        current_score.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        #--scoreboard rows/columns--
        #here needing score.rowconfigure(x, weight=y) or score.columnconfigure(m, weight=n)
        
        #title row
        current_score.rowconfigure(0, weight=0)
        
        #team row
        current_score.rowconfigure(1, weight=1)
        
        #score row
        current_score.rowconfigure(2, weight=2)
        
        #red column
        current_score.columnconfigure(0, weight=1)
        
        #green column
        current_score.columnconfigure(1, weight=1)

        #--title: CURRENT SCORES--
        #fg means foreground, bg means background
        #title label (score, text=, font=("Courier New", size, "bold"), fg=, bg=)
        #add label to grid, so title.grid()

        # title1 = Current Scores
        title1 = tk.Label(current_score, text="Current Scores", font=("Courier New", 20, "bold"), fg="green", bg="black")
        title1.grid(row=0, column=1, padx=20, pady=10, sticky="e") # alligned right
        
        # title2 = XP
        title2 = tk.Label(current_score, text="XP", font=("Courier New", 20, "bold"), fg="red", bg="black")
        title2.grid(row=0, column=0, padx=20, pady=10, sticky="w") # alligned left

        #--red team panel (left)--
        #frame
        #title
        red_team_title = tk.Label(current_score, text="RED TEAM", font=("Courier New", 20, "bold"), fg="white", bg="black")
        red_team_title.grid(row=1, column=0, padx=20, pady=10, sticky="n")
        #red_player = tk.Lable()
        #red_player.pack(anchor="w")
        #red_score = tk.Label()
        #red_score.pack(anchor="e")

        #--green team panel (left)--
        #frame
        #title
        green_team_title = tk.Label(current_score, text="GREEN TEAM", font=("Courier New", 20, "bold"), fg="white", bg="black")
        green_team_title.grid(row=1, column=1, padx=20, pady=10, sticky="n")
        #green_player = tk.Label()
        #green_player.pack(anchor="w")
        #green_score = tk.Label()
        #green_score.pack(anchor="e")

        #--team totals--
        #red_total = tk.Label()
        #red_total.grid()

        #green_total = tk.Label()
        #green_total.grid()
        # pass

    def game_action(self, parent):
        #similar to last function but now this parft is the section showing the live log
        #action = tk.Frame(self, bg="blue")
        #action.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        current_action = tk.Frame(self, bg="blue")
        current_action.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        #--title--
        current_action_title = tk.Label(current_action, text="Current Game Action", font=("Courier New", 20, "bold"), fg="white", bg="blue")
        current_action_title.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
        
        #--log container--

        #--listbox--
        # self.action_listbox = tk.Listbox(log, bg="blue", fg="white", font="Courier New", 16, "bold"), relief="flat", borderwidth=0)
        # self.action_listbox.grid(row=0, column=0, sticky="nsew")
        # pass

    def countdown_timer(self, parent):

        timer = tk.Frame(self, bg="black")
        timer.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        # pass

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GAME SCREEN")

    #trying to match splash screen
    width = 1000
    height = 637

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    screen = PlayAction(root)
    screen.pack(fill="both", expand=True)

    root.mainloop()
