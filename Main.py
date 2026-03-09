#Team 14
#CSCE 35103-001
#Spring 2026
from tkinter import *
from splashScreen import Splash
from PlayerScreen import PlayerScreen

class Main:

    #UDP SOCKETS--> MOVED TO udp.py!!!
    #set up 2 udp sockets for transmission of data to/from players
        #socket 7500 to broadcast
            #format of transmission: single int (equip. id of player hit)
        #socket 7501 to receive (allow to receive for any ip addr)
            #format of received data: int:int
            #(equip. id of player transm : equip. id of player hit)
                #broadcast equip. id of player hit
    #use localhost (127.0.0.1) for network addr
        #include functionality to change network addr

    #SPLASH SCREEN
    #display splash screen for 3 seconds upon startup
    def __init__(self):
        #initializes the main program
        self.root = Tk()
        self.root.title("MAIN APP")

        # run splash screen first
        self.show_splash()

        #matching player screen to splash screen size
        width = 1000
        height = 637
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # then open player entry screen
        self.open_player_screen()

        # start main loop
        self.root.mainloop()

    def show_splash(self):
        splash = Splash(self.root)
        # wait until splash is closed before continuing
        self.root.wait_window(splash.root)

    #button to open player entry screen
    def open_player_screen(self):
        self.screen = PlayerScreen(self.root)
        self.screen.pack(fill="both", expand=True)


    #GAME
    #f5 or start button moves to next screen (play action screen)
        #3 areas that will constantly be updating
            #count down timer
            #during game play, random mp3 music file will be playing
            #(files provided), sync mp3 countdown with game countdown
                #for 6 minute games

                #30 second warning before starting
                    #broadcast code 202

                #play by play action will be shown in a window on
                #main screen, events can scroll off as window fills

            #cumulative team scores
                #high team score will flash during play

            #individual scores
                #(+10pts per opp, -10pts per same team tag)
                #if player tags member of own team, player tagged
                #as well as player tagging -10pts
                    #broadcast own equip. id and equip. id of who
                    #they hit (2 transmissions)
                #code 53 received
                    #red base has been scored
                    #if player is on green team, +100pts & base icon
                    #displays to the left of their codename
                #code 43 received
                    #green base has been scored
                    #if player is on red team, +100pts & base icon
                    #displays to the left of their codename

                #displayed highest to lowest on each team
    #after game ends, leave display at play action screen
    #add button to get back to player entry screen
        #broadcast code 221 three times

if __name__ == "__main__":
    Main()

