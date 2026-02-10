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
