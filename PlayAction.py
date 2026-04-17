import tkinter as tk
import socket
import queue
from tkinter import PhotoImage
from Music import PlayMusic

class PlayAction(tk.Frame):
    def __init__(self, master, red_players=None, green_players=None):
        super().__init__(master)
        self.master = master

        self.music = PlayMusic()
        self.music.play()

        # store PlayerEntry objects
        self.red_players = red_players if red_players else []
        self.green_players = green_players if green_players else []

        #count down timer code: 
        self.time_left = 30
        self.game_time_left = 6 * 60
        self.start_countdown = 30
        self.timer_mode = "start"
        self.timer_running = False
        self.timer_label = None

        #upd setup
        self.localIP = "0.0.0.0"
        self.localPort = 7501
        self.bufferSize = 1024
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.localIP, self.localPort))

        #base icon
        self.base = PhotoImage(file="baseicon.png")
        self.red_player_widget = []
        self.green_player_widget = []

        self.player_score = {}
        self.red_team_score = 0
        self.green_team_score = 0

        #initialize player scores
        for p in self.red_players + self.green_players:
            self.player_score[p.equipment_id] = 0
        
        self._style()
        self.event_queue = queue.Queue()
        self._ui()

    def _key_input(self) -> None:
        pass

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

        content.rowconfigure(0, weight=0)  # current scores
        content.rowconfigure(1, weight=1)  # game action
        content.rowconfigure(2, weight=0)  # countdown timer
        content.rowconfigure(3, weight=0)  # menu
        content.columnconfigure(0, weight=1)

        # current scores
        self.current_game_score(content)
        # game action
        self.game_action(content)
        # countdown timer
        self.countdown_timer(content)

        #home button
        back = tk.Frame(content, bg="black")
        back.grid(row=3, column=0, pady=10, sticky="ew")

        back_btn= tk.Button(back, text="Return to Player Entry", command=self.go_back, fg="blue", bg="gray", activebackground="gray", relief="ridge", bd=2, font=("Courier New", 20, "bold"))
        back_btn.pack()

    def go_back(self):
        self.timer_running = False

        try:
            self.server_socket.close()
        except:
            pass
        self.master.destroy()

    def _make_scroll(self, parent, bg: str):
        canvas = tk.Canvas(parent, bg=bg, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=bg)
        window_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _on_configure(event):
            inner.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_resize(event):
            canvas.itemconfigure(window_id, width=event.width)

        inner.bind("<Configure>", _on_configure)
        canvas.bind("<Configure>", _on_resize)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind(_):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind(_):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _bind)
        canvas.bind("<Leave>", _unbind)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return canvas, inner


    def current_game_score(self, parent):
        current_score = tk.Frame(parent, bg="black")
        self.red_total_var = tk.StringVar(value="0")
        self.green_total_var = tk.StringVar(value="0")
        current_score.grid(row=0, column=0, sticky="nsew")

        # configure rows and columns
        current_score.rowconfigure(0, weight=0)  # title row
        current_score.rowconfigure(1, weight=0)  # team titles
        current_score.rowconfigure(2, weight=1)  # player names + scores
        current_score.rowconfigure(3, weight=0)  # team totals
        current_score.config(height=250)
        current_score.grid_propagate(False)

        current_score.columnconfigure(0, weight=1)  # red team
        current_score.columnconfigure(1, weight=1)  # green team

        # Titles
        title1 = tk.Label(current_score, text="Current Scores", font=("Courier New", 20, "bold"), fg="green", bg="black")
        title1.grid(row=0, column=1, padx=20, pady=10, sticky="ne")

        title2 = tk.Label(current_score, text="XP", font=("Courier New", 20, "bold"), fg="red", bg="black")
        title2.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        # RED TEAM
        red_team_title = tk.Label(current_score, text="RED TEAM", font=("Courier New", 20, "bold"), fg="red", bg="black")
        red_team_title.grid(row=1, column=0, padx=20, pady=10, sticky="n")

        red_container = tk.Frame(current_score, bg="black")
        red_container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        _, self.red_player_frame = self._make_scroll(red_container, "black")
        red_container.config(height=180)
        red_container.grid_propagate(False)
        
        self.red_player_widget = []

        # red_names = [p.codename for p in self.red_players] if self.red_players else ["Player Names"]
        if self.red_players:
            for player in self.red_players:
                row = tk.Frame(self.red_player_frame, bg="black")
                row.grid(sticky="w")

                icon = tk.Label(row, bg="black")
                icon.pack(side="left", padx=(0,5))

                red_player = tk.Label(
                    # current_score,
                    # text="\n".join(red_names),
                    row,
                    text=player.codename,
                    font=("Courier New", 20, "bold"),
                    fg="red",
                    bg="black",
                    justify="left"
                )
                red_player.pack(side="left")
                score_var = tk.StringVar(value="0")
                score_label = tk.Label(row, textvariable=score_var, font=("Courier New", 16, "bold"), fg="red", bg="black")
                score_label.pack(side="right")
                self.red_player_widget.append((player, icon, score_var))
        else:
            red_player = tk.Label(
                self.red_player_frame,
                text="Player Names",
                font=("Courier New", 20, "bold"),
                fg="red",
                bg="black",
                justify="left")
            red_player.pack(anchor="w")
            # red_player_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nw")

        #red_score_frame = tk.Frame(current_score, bg="black")
        #red_score_frame.grid(row=2, column=0, sticky="ne", padx=20, pady=10)
        #tk.Label(red_score_frame, text="0", font=("Courier New", 20, "bold"), fg="red", bg="black").pack(anchor="e")

        # GREEN TEAM
        green_team_title = tk.Label(current_score, text="GREEN TEAM", font=("Courier New", 20, "bold"), fg="green", bg="black")
        green_team_title.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        green_container = tk.Frame(current_score, bg="black")
        green_container.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")
        _, self.green_player_frame = self._make_scroll(green_container, "black")
        green_container.config(height=180)
        green_container.grid_propagate(False)

        self.green_player_widget = []

        # green_names = [p.codename for p in self.green_players] if self.green_players else ["Player Names"]
        if self.green_players:
            for player in self.green_players:
                row = tk.Frame(self.green_player_frame, bg="black")
                row.pack(anchor="w")

                icon = tk.Label(row, bg="black")
                icon.pack(side="left", padx=(0,5))

                green_player = tk.Label(
                    # current_score,
                    # text="\n".join(green_names),
                    row,
                    text=player.codename,
                    font=("Courier New", 20, "bold"),
                    fg="green",
                    bg="black",
                    justify="left"
                )
                green_player.pack(side="left")
                score_var = tk.StringVar(value="0")
                score_label = tk.Label(row, textvariable=score_var, font=("Courier New", 16, "bold"), fg="green", bg="black")
                score_label.pack(side="right")
                self.green_player_widget.append((player, icon, score_var))
        else:
            green_player = tk.Label(
                self.green_player_frame,
                text="Player Names",
                font=("Courier New", 20, "bold"),
                fg="green",
                bg="black",
                justify="left"
            )
            green_player.pack(anchor="w")
            # green_player.grid(row=2, column=1, padx=20, pady=10, sticky="nw")

        green_score_frame = tk.Frame(current_score, bg="black")
        green_score_frame.grid(row=2, column=1, sticky="ne", padx=20, pady=10)
        #tk.Label(green_score_frame, text="0", font=("Courier New", 20, "bold"), fg="green", bg="black").pack(anchor="e")

        # Team totals
        red_total = tk.Label(current_score, textvariable=self.red_total_var, font=("Courier New", 20, "bold"), fg="red", bg="black")
        red_total.grid(row=3, column=0, padx=20, pady=10, sticky="se")

        green_total = tk.Label(current_score, textvariable=self.green_total_var, font=("Courier New", 20, "bold"), fg="green", bg="black")
        green_total.grid(row=3, column=1, padx=20, pady=10, sticky="se")

    #base icon
    def base_scored(self, equipment_id):
        for player, icon, score_var in self.red_player_widget:
            if player.equipment_id == equipment_id:
                icon.config(image=self.base)
                icon.image = self.base
                return
        for player, icon, score_var in self.green_player_widget:
            if player.equipment_id == equipment_id:
                icon.config(image=self.base)
                icon.image = self.base
                return

    def game_action(self, parent):
        current_action = tk.Frame(parent, bg="blue")
        current_action.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        current_action.rowconfigure(1, weight=1)
        current_action.columnconfigure(0, weight=1)

        current_action_title = tk.Label(current_action, text="Current Game Action", font=("Courier New", 20, "bold"), fg="white", bg="blue")
        current_action_title.grid(row=0, column=0, padx=20, pady=10, sticky="n")

        self.current_action_listbox = tk.Listbox(current_action, bg="blue", fg="white", font=("Courier New", 16, "bold"), relief="flat", borderwidth=0)
        self.current_action_listbox.grid(row=1, column=0, sticky="nsew")

    def countdown_timer(self, parent):
        timer = tk.Frame(parent, bg="black")
        timer.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        timer.columnconfigure(0, weight=1)
        timer.columnconfigure(1, weight=1)

        timer_title = tk.Label(timer, text="Time Remaining:", font=("Courier New", 20, "bold"), fg="white", bg="black")
        timer_title.grid(row=0, column=0, padx=20, pady=10, sticky="e")

        self.timer_label = tk.Label(
            timer,
            text="Time Remaining:", 
            font=("Courier New", 20, "bold"),
            fg="yellow", 
            bg="black"
        )
        timer_title.grid(row=0, column=0, padx=20, pady=10, sticky="e")

        self.timer_label = tk.Label(
            timer,
            text=self.format_time(self.start_countdown),
            font=("Courier New", 20, "bold"),
            fg="yellow",
            bg="black"
        )
        self.timer_label.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        self.start_timer()

    def format_time(self, seconds):
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
            #self.timer_label.config(text=self.format_time(self.time_left))

        if self.timer_mode == "start":
            self.timer_label.config(text=self.format_time(self.start_countdown))

            if self.start_countdown > 0:
                self.start_countdown -= 1
                self.after(1000, self.update_timer)
            else: 
                self.timer_mode = "game"
                self.timer_label.config(text="GO!")
                self.server_socket.sendto("202".encode(), ("127.0.0.1", 7500))
                self.listen_for_hits()
                self.after(1000, self.update_timer)

        # 6 minute gameplay timer code: 
        elif self.timer_mode == "game":
            self.timer_label.config(text=self.format_time(self.game_time_left))

            if self.game_time_left > 0:
                self.game_time_left -= 1
                self.after(1000, self.update_timer)
            else: 
                self.timer_mode = "done"
                self.timer_running = False
                self.timer_label.config(text="GAME OVER")

    
    #for traffic generator
    def listen_for_hits(self):
        import threading
        def receive():
            while True:
                 data, addr = self.server_socket.recvfrom(self.bufferSize)
                 message = data.decode()
                 print("Received:", message)
                 #send to UI safely
                 self.event_queue.put(message)
                 #ACK back to traffic generator
                 self.server_socket.sendto("ACK".encode(), addr)
                 
        thread = threading.Thread(target=receive, daemon=True)
        thread.start()
        #start UI polling loop
        self.after(100, self.process_queue)

    def process_queue(self):
        while not self.event_queue.empty():
            message = self.event_queue.get()
            #show raw event
            self.current_action_listbox.insert(tk.END, f"Raw: {message}")
            try:
                attacker, target = message.split(":")
                attacker = int(attacker)
                target = int(target)
            except:
                continue
            #event type detection
            if target == 43:
                event_text = f" BASE HIT by Player {attacker} (RED BASE)"
            elif target == 53:
                event_text = f" BASE HIT by Player {attacker} (GREEN BASE)"
            elif attacker == target:
                event_text = f" FRIENDLY FIRE: Player {attacker}"
            else: 
                event_text = f" HIT: Player {attacker} -> Player {target}"
            #show event
            self.current_action_listbox.insert(tk.END, event_text)
            self.current_action_listbox.yview(tk.END)
            red_ids = [p.equipment_id for p in self.red_players]
            green_ids = [p.equipment_id for p in self.green_players]
            
            if target == 43:
                self.green_team_score += 100
            elif target == 53:
                self.red_team_score += 100
            else:
                if attacker in red_ids and target in green_ids:
                    self.player_score[attacker] += 10
                    self.red_team_score += 10
                elif attacker in green_ids and target in red_ids:
                    self.player_score[attacker] += 10
                    self.green_team_score += 10
                # Friendly Fire Handling
                elif attacker in red_ids and target in red_ids:
                    self.player_score[attacker] -= 10
                    self.player_score[target] -= 10
                    self.red_team_score -= 20
                elif attacker in green_ids and target in green_ids:
                    self.player_score[attacker] -= 10
                    self.player_score[target] -= 10
                    self.green_team_score -= 20
            
            #update player score labels
            for player, icon, score_var in self.red_player_widget:
                score_var.set(str(self.player_score[player.equipment_id]))
            for player, icon, score_var in self.green_player_widget:
                score_var.set(str(self.player_score[player.equipment_id]))

            #update UI
            self.red_total_var.set(str(self.red_team_score))
            self.green_total_var.set(str(self.green_team_score))
            
            #update visuals
            self.base_scored(int(target))
        self.after(100, self.process_queue)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("GAME SCREEN")

    width = 1000
    height = 637

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    # Example PlayerEntry objects (replace with your real PlayerEntry instances)
    class PlayerEntry:
        def __init__(self, id, codename):
            self.equipment_id = id
            self.codename = codename

    red_team = [PlayerEntry(1, "Alice"), PlayerEntry(2, "Bob")]
    green_team = [PlayerEntry(3, "Carol"), PlayerEntry(4, "Dave")]

    screen = PlayAction(root, red_players=red_team, green_players=green_team)
    screen.pack(fill="both", expand=True)

    root.mainloop()
