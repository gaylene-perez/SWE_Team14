# This is the prototype script for the switch_network function. The official function is implemented in PlayerScreen.py

import tkinter as tk #gui
# from tkinter import *
from tkinter import messagebox
from dataclasses import dataclass
from typing import List
from tkinter import simpledialog

ip = "127.0.0.1"

button = tk.Button(root, text="CLICK TO SWITCH NETWORKS", command=self.switch_network, fg="blue", bg="light gray", height=2, width=25)
        button.pack(pady=10)

def switch_network(self):
        temp = self.ip
        self.ip = simpledialog.askstring("Input", f"Current IP address: {self.ip}\nPlease enter a valid IP address:", parent=root)

        if self.ip is None:
            self.ip = temp

        return self.ip
