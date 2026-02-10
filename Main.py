#Team 14
#CSCE 35103-001
#Spring 2026

class Main:

    #UDP SOCKETS
    #set up 2 udp sockets for transmission of data to/from players
        #socket 7500 to broadcast
            #format of transmission: single int (equip. id of player hit)
        #socket 7501 to receive (allow to receive for any ip addr)
            #format of received data: int:int
            #(equip. id of player transm : equip. id of player hit)
                #broadcast equip. id of player hit
    #use localhost (127.0.0.1) for network addr
        #include functionality to change network addr
    
    import socket

localIP     = "0.0.0.0"
localPort   = 7501
bufferSize  = 1024
msgFromServer       = "Hello UDP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)

import socket

msgFromClient       = "Hello UDP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("127.0.0.1", 7501)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# enable broadcasts
socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])

print(msg)


    #SPLASH SCREEN
    #display splash screen for 3 seconds upon startup
from tkinter import *
from PIL import Image, ImageTk

class Splash:
    def __init__(self) -> None:
        # Setting up a blank screen
        width = 1000
        height = 700

        self.root = Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width / 2)
        y_coordinate = (screen_height / 2) - (height / 2)

        # Adjust where the screen pops up
        self.root.geometry("%dx%d+%d+%d" %
                           (width, height, x_coordinate, y_coordinate))

        # Removing the page heading
        self.root.overrideredirect(1)

        Frame(self.root, width=427, height=241, bg='black').place(x=50, y=100)

        # Adding the logo
        im = Image.open("logo.jpg")
        logo = im.resize((width, height))
        LOGO = ImageTk.PhotoImage(logo)

        # Inserting the logo
        logo_label = Label(image=LOGO, bg='black')
        logo_label.place(x=0, y=0)

        self.root.after(3000, lambda: self.root.destroy())
        mainloop()

    #PLAYER SCREEN
        #red team / green team
        #max 15 players per team

        #f12 clears all entries
        #prompt for player id
            #query database for code name
            #if not found, allow new name entry to add to database

        #prompt for equipment id that player is using (int)

        #broadcast equip. id through udp port 7500

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

