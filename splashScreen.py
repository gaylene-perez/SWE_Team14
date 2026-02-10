from tkinter import *
from PIL import Image, ImageTk

class Splash:
    def __init__(self):
        #setting up the blnk screen
        width = 1000
        height = 700

        self.root = Tk()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        #adjusting where the screen will pop up
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        #removing the page heading
        self.root.overrideredirect(True)

        #adding the logo
        im = Image.open("logo.jpg")
        logo = im.resize((width, height))
        self.LOGO = ImageTk.PhotoImage(logo)

        #inserting the logo
        label = Label(self.root, image=self.LOGO)
        label.pack()

        self.root.after(3000, self.root.destroy)
        self.root.mainloop()

