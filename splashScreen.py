from tkinter import *

class Splash:
    def __init__(self, master):
        # Use a Toplevel window over the main root
        self.root = Toplevel(master)

        width = 1000
        height = 637

        # Center the splash screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Remove window decorations
        self.root.overrideredirect(True)

        # Load logo
        self.logo = PhotoImage(file="logo.png")
        label = Label(self.root, image=self.logo)
        label.pack(expand=True, fill=BOTH)

        # Destroy splash after 3 seconds
        self.root.after(3000, self.root.destroy)


