from pygame import mixer
import random

class PlayMusic():
    
    def __init__(self):

        self.random_number = random.randint(1, 8)
        self.file_path = "Track0" + str(self.random_number) + ".mp3"
    
    def play(self):

        mixer.init()
        mixer.music.load(self.file_path)
        mixer.music.play()
