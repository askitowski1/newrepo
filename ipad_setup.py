#Trying to figure out some classes. Just copied the imports
#from psychopy_setup to start

import os
from psychopy import core,gui,visual,data,logging,event
import psychtoolbox as pt
import csv
import json

class ipadSetup(object):
    def __init__(self):
        self.win = visual.Window(fullscr = True, color = 'black')
        self.text_stims = []
        self.pressable_regions = []
        self.image_timings = []
        self.preloaded_images = {}
       
    
    #creating text
    def make_text(self, win, text, color=[1,1,1], font='Arial', size=0.2, pos=(0,0)):
        text_stim = visual.TextStim(win = self.win, text=text, color=color, font=font, height=size, pos=pos)
        self.text_stims.append(text_stim)
        return text_stim
        
    #creating pressable region
    def pressable_region(self, win, pos=(0.6,-0.8), size=(0.3, 0.2), fillColor=False, outline_color='blue'):
        region = visual.Rect(win=self.win, pos=pos, size=size, fillColor=fillColor, lineColor=outline_color)
        self.pressable_regions.append(region)
        return region
        
    #track presses
    def is_pressed(self, mouse):
        for region in self.pressable_regions:
            if mouse.isPressedIn(region):
                return True 
        return False
            
    def preload(self, image_dir):
        for file_name in os.listdir(image_dir):
            image_path = os.path.join(image_dir, file_name)
            if os.path.isfile(image_path) and file_name.lower().endswith(('.jpg')):
                self.preloaded_images[file_name] = visual.ImageStim(win=self.win, image=image_path, pos=(0, 0))
        print("All images are preloaded")

        
    