#Trying to figure out some classes. Just copied the imports
#from psychopy_setup to start

import os
from psychopy import core,gui,visual,data,logging,event
from PIL import Image
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
        #creating variables
        bar = visual.Rect(win = self.win, size=(0.78, 0.2), lineColor = 'white', fillColor = 'white') #start at -.39 because that is the left edge of a size .78, .2 rectangle
        text = self.make_text(self.win, "Stimuli loading...", color='white', font='Calibri', pos = (0, -.4) ,size = 0.1)
        total_images = len(os.listdir(image_dir))
        images_loaded = 0
        for file_name in os.listdir(image_dir):
            image_path = os.path.join(image_dir, file_name)
            if os.path.isfile(image_path) and file_name.lower().endswith(('.jpg')):
                try:
                    # Resize image
                    with Image.open(image_path) as img:
                        img = img.resize((768, 768)) #all images were 1024x1024 or 2048x2048, this way they load on surface
                        self.preloaded_images[file_name] = visual.ImageStim(win=self.win, image=img, pos=(0, 0))
                    
                    images_loaded += 1
                    bar.width = .78 * (images_loaded/ total_images) #this is filling from the middle
                    bar.pos = (-.39 + bar.width/2, -.6) #keeps it filling from left side
        
                    #making bar and text
                    bar.draw()
                    text.draw()
                    self.win.flip()
                    
                    print(f"{file_name} loaded: {images_loaded}/ {total_images}")
                except Exception as e:
                    print(f"Could not load {file_name}: {e}")
        print("All images are preloaded")
        
