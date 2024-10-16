from ipad_setup import ipadSetup
from psychopy import core, event, visual, gui
import json, os, csv

#getting subject info
expInfo = {'Participant': '', 'Session': '', 'Block': '', 'List': ''}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
info_dlg = gui.Dlg(title="Participant info")

#adding subject info to CSV
csv_file_path = 'participant_info.csv'
with open(csv_file_path, mode ='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=expInfo.keys())
    writer.writerow(expInfo)

#getting stimuli
selected_list = expInfo['List']
script_dir = os.path.dirname(os.path.abspath(__file__))
stim_file = os.path.join(script_dir,'stimlists', f"CIDMEG_list{selected_list}.json")

exp = ipadSetup(stim_file)

#making text and pressable regions
exp.make_text("Welcome to the game!", color='white', font='Calibri')
exp.make_text("Click here to contiue", size=0.1, pos=(0.6,-0.8))
exp.pressable_region(pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=True)

#Create mouse and check presses 
mouse = event.Mouse(visible=True, win=exp.win)
while True:
    exp.show_all()
    if mouse.getPressed()[0]:
        if exp.is_pressed(mouse):
            break
#instructions
exp.text_stims.clear()
exp.make_text("These are the instructions....", color='white', font='Calibri')
exp.make_text("Click here to contiue", size=0.1, pos=(0.6,-0.8))
exp.pressable_region(pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=True)

#Create mouse and check presses 
mouse = event.Mouse(visible=True, win=exp.win)
while True:
    exp.show_all()
    if mouse.getPressed()[0]:
        if exp.is_pressed(mouse):
            break
            
            

#Starting experiment 
exp.text_stims.clear()
exp.pressable_regions.clear()
exp.run_experiment()

exp.win.close()
