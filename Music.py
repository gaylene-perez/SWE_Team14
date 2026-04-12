from playsound3 import playsound
import random

class PlayMusic():
    
    def __init__(self):

        self.random_number = random.randint(1, 8)
        self.file_path = "Track0" + str(self.random_number) + ".mp3"
    
    def play(self):

        playsound(self.file_path, block=False)