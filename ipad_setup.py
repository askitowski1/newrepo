#Trying to figure out some classes. Just copied the imports
#from psychopy_setup to start

import os
from psychopy import core,gui,visual,data,logging,event #,sound,microphone
from psychopy.hardware import keyboard
import psychtoolbox as pt
import csv
import time
import json

class ipadSetup(object):
    def __init__(self, stim_file):
        self.window()
        self.text_stims = []
        self.pressable_regions = []
        self.stim_file = stim_file
        #self.image_file = "C:\\Users\\Experiment\\Desktop\\CIDMEG_Exp\\images"
        self.data = self.load_stimuli()
        self.info = {
            'participant': '',
            'session': '1',
            'block': '1',
            'list': 'A' 
            }
            
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_file = os.path.join(script_dir,'images')
        os.chdir(script_dir)
        print(os.getcwd())
    
    #loading stimuli
    def load_stimuli(self):
        with open(self.stim_file, 'r') as file:
            data = json.load(file)
        return data
        
    #creating the window
    def window(self):
        self.win = visual.Window(fullscr = True, color = [0,0,0])
    
    #creating text
    def make_text(self, text, color=[1,1,1], font='Arial', size=0.2, pos=(0,0)):
        text_stim = visual.TextStim(win = self.win, text=text, color=color, font=font, height=size, pos=pos)
        self.text_stims.append(text_stim)
        
    #showing text
    def show_all(self):
        for text_stim in self.text_stims:
            text_stim.draw()
        for region in self.pressable_regions:
            region.draw()
        self.win.flip()
        
    #creating pressable region
    def pressable_region(self, pos=(0.6,-0.8), size=(0.3, 0.2), fillColor=False, outline_color='blue'):
        region = visual.Rect(win=self.win, pos=pos, size=size, fillColor=fillColor, lineColor=outline_color)
        self.pressable_regions.append(region)
        
    #track presses
    def is_pressed(self, mouse):
        for region in self.pressable_regions:
            if mouse.isPressedIn(region):
                return True #still have to add what it does. now just making it end
            return False
            
    #set up experiment
    def run_experiment(self):
        if self.data is None:
            print("Missing data")
            return
        mouse = event.Mouse()
        for i in self.data['stims']:
            for j in i:
                for k in j:
                    image_path = os.path.join(self.image_file, f"{k}")
                    if os.path.isfile(image_path):
                        image_stim = visual.ImageStim(win=self.win, image=image_path, pos=(0, 0))
                        image_stim.draw()
                        self.show_all()
                        
                        #hold image for 0.7
                        core.wait(0.7)
                        
                    else:
                        print("File does not exist.")
                        # Create a clickable region for the user to press during the experiment
                    #self.pressable_region(pos=(0.6, -0.8), size=(0.3, 0.2), outline_color='blue')  # Adjust position/size as needed
    
                    if event.getKeys(keyList=['space']):
                        self.win.close()
                        core.quit()
                    if mouse.getPressed()[0]:
                        if self.is_pressed(mouse):
                            self.win.close()
                            core.quit()
                            
                    
        