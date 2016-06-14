import pygame 
import librosa
import csv
from threading import Thread

class Model(object):
    class Player(Thread):
        def run(self):
            pygame.mixer.music.load("res/music/cmm.wav")
            pygame.mixer.music.play()
        
    # Member Variables
    controller = None
    def __init__(self, controller):
        self.controller = controller
        pygame.init()
        pygame.mixer.init()

    def playSound(self):
        player = self.Player()
        player.start()

    def beatDetect(self, path):
        y, sr = librosa.load(path)
        hop_length = 64
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
        
        #this grabs all the frame times for which the beat happens
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)
        
        #this outputs to a csv file
        librosa.output.times_csv('beat_times_sample.csv', beat_times) 
        
        with open('beat_times_sample.csv', 'rb') as f:
            reader = csv.reader(f)
            output = list(reader)
        
        #this prints out the first frame of which the beat occurs for the arrow
        #to move
        rtn = []
        for current in output:
            rtn.append(float(current[0]))
        return rtn
