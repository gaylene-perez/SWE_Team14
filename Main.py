#Team 14
#CSCE 35103-001
#Spring 2026
from tkinter import Tk
from tkinter import *


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
    from tkinter import *

    class Splash:
        def __init__(self):
            #setting up the blank screen
            width = 1000
            height = 637

            self.root = Tk()

            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = int((screen_width / 2) - (width / 2))
            y = int((screen_height / 2) - (height / 2))

            #adjusting where the screen will pop up
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            #removing the header
            self.root.overrideredirect(True)

            # adding logo
            self.logo = PhotoImage(file="logo.png")  
            label = Label(self.root, image=self.logo)
            label.pack(expand=True, fill=BOTH)

            #inserting the logo
            self.root.after(3000, self.root.destroy)
            self.root.mainloop()


    # Run splash screen
    Splash()
    

    #PLAYER SCREEN
        #red team (odd) / green team (even)
        #max 15 players per team

        #f12 clears all entries
        #prompt for player id
            #query database for code name
            #if not found, allow new name entry to add to database

        #prompt for equipment id that player is using (int)


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

