from ipad_setup import ipadSetup
from psychopy import core, event, visual, gui, logging
import json, os, time, subprocess

#keyboard on
subprocess.Popen('osk', shell=True)

#setting log
logging.console.setLevel(logging.EXP)
logging.LogFile('experiment_log.log', level = logging.EXP)

#getting subject info
expInfo = {'Participant': '', 'Session': '', 'Block': '', 'List': 'B'}
dlg = gui.DlgFromDict(dictionary=expInfo, order=['Participant', 'Session', 'Block', 'List'], title="Participant info")
if dlg.OK == False:
    core.quit()

#keyboard off 
if dlg.OK == True:
    os.system('taskkill /im osk.exe /f') #not working great, still need to fix
    
#getting stimuli
selected_list = expInfo['List']

#setting directory to save timing from shortcut
os.chdir(os.path.dirname(os.path.abspath(__file__)))
script_dir = os.getcwd()
stim_file  = os.path.join(script_dir,'stimlists', f"CIDMEG_list{selected_list}.json")
image_dir = os.path.join(script_dir, 'images')

exp = ipadSetup()

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
            break
        
#loading stimuli names
with open(stim_file, 'r') as file:
    data = json.load(file)
image_names = data['stims']

#preloading images
exp.preload(image_dir)

#create mouse
mouse = event.Mouse(visible = True, win = exp.win)

#resetting clock so it's at 0 when images start
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
previous_time = None
image_start_time = 0
button = exp.pressable_region(exp.win, pos=(0.75, -0.8), size=(0.39, 0.2), outline_color=False)

#showing images
for i in image_names:
    for j in i:
        for k in j:
            if k in exp.preloaded_images:
                image_stim = exp.preloaded_images[k]
                image_stim.draw()
                button.draw()
                exp.win.flip() 

                #geting image time immediately and logging difference
                image_start_time = globalClock.getTime()
                if previous_time is not None:
                    difference = round(image_start_time - previous_time, 3)
                else:
                    difference = 0
                logging.exp(f"Displayed {k} at {image_start_time}, at a {difference}s interval")

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

            #making loop to make each image last .7s
            while globalClock.getTime() - image_start_time < .700:
                core.wait(0.001)
            #timing worked better for 60Hz monitor
            #while globalClock.getTime() - image_start_time < .6847:
                #core.wait(0.012)
            image_start_time = globalClock.getTime()
# Close the window 
exp.win.close()
