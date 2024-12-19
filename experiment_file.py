
from surface_setup import surfaceSetup
from Loading_stims import versionTracker
from psychopy import core, event, visual, gui, logging
import json, os, csv, openpyxl
from openpyxl import Workbook, load_workbook

#setting log 
logging.console.setLevel(logging.EXP)
logging.LogFile('experiment_log.log', level = logging.EXP)

#getting stimuli
current_stims = versionTracker()
script_dir = os.path.dirname(os.path.abspath(__file__))
stim_file  = os.path.join(script_dir,'stimlists', f"CIDMEG_list{current_stims}.json")
image_dir = os.path.join(script_dir, 'images')

exp = surfaceSetup()

#making text and pressable regions
s1 = [
exp.make_text(exp.win, "Welcome to the game!", color=[1,1,1], font='Arial'),
exp.make_text(exp.win, "Click here to contiue", size=0.1, pos=(0.6,-0.8)),
exp.pressable_region(exp.win, pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=True)
]

s2 = [
exp.make_text(exp.win, "These are the instructions....", color='white', font='Calibri'),
exp.make_text(exp.win, "Click here to contiue", size=0.1, pos=(0.6,-0.8)),
exp.pressable_region(exp.win, pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=True)
]

#Create mouse 
mouse = event.Mouse(visible=True, win=exp.win)

#Creating loop through items on each screen
screens = [s1, s2]
for screen in screens:
    for line in screen:
        line.draw()
    exp.win.flip()
    while mouse.getPressed()[0]:
        pass
    while True:
        if event.Mouse(win=exp.win).getPressed()[0]:
            if exp.is_pressed(mouse):
                break

#loading stimuli names
with open(stim_file, 'r') as file:
    data = json.load(file)
image_names = data['stims']

#preloading images
exp.preload(image_dir)

#create mouse
mouse = event.Mouse(visible = True, win = exp.win)

#resetting clock so its at 0 when images start
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
previous_time = None
image_start_time = 0 
button = exp.pressable_region(exp.win, pos=(0.75, -0.8), size=(0.39, 0.2), outline_color=True)

for i in image_names:
    for j in i:
        for k in j:
            if k in exp.preloaded_images:
                exp.win.flip() 
                
                #getting image time immediately and logging difference
                image_start_time = globalClock.getTime()
                if previous_time is not None:
                    difference = round(image_start_time - previous_time, 6)
                else:
                    difference = 0
                logging.exp(f"Displayed: {k} at {image_start_time}, at a {difference}s interval")
                
                #set previous_time to image_start_time for next trial
                previous_time = image_start_time
                
                #quit with click 
                if event.Mouse(win=exp.win).getPressed()[0]:
                    if exp.is_pressed(mouse):
                        exp.win.close()
                        core.quit()

                # Backup way to quit while testing
                if event.getKeys(keyList=['space']):
                    exp.win.close()
                    core.quit()
                
                image_stim = exp.preloaded_images[k]
                image_stim.draw()
                button.draw()
                #making a loop to make each image last .7s
                while globalClock.getTime() - image_start_time < .697:
                    core.wait(0.001)
            
