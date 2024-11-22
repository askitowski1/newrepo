from ipad_setup import ipadSetup
from psychopy import core, event, visual, gui
import json, os, csv

#getting subject info
expInfo = {'Participant': '', 'Session': '', 'Block': '', 'List': 'B'}
dlg = gui.DlgFromDict(dictionary=expInfo)
if dlg.OK == False:
    core.quit()
info_dlg = gui.Dlg(title="Participant info")

#adding subject info to XLSX
xlsx_file_path = 'participant_info.xlsx'
with open(xlsx_file_path, mode ='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=expInfo.keys())
    writer.writerow(expInfo)

#getting stimuli
selected_list = expInfo['List']
script_dir = os.path.dirname(os.path.abspath(__file__))
stim_file = os.path.join(script_dir,'stimlists', f"CIDMEG_list{selected_list}.json")
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


##Create mouse object
mouse = event.Mouse(visible=True, win=exp.win)
        
#Putting screens in a list to iterate over them
screens = [s1, s2]

#Creating loop through items on each screen
for screen in screens:
    for line in screen:
        line.draw()
    exp.win.flip()
    while mouse.getPressed()[0]:
        pass
    while True:
        if event.Mouse(win=exp.win).getPressed()[0]:
            break
        
#loading stimuli
with open(stim_file, 'r') as file:
    data = json.load(file)
    
image_names = data['stims']


#displaying stimuli
images = []
for i in data['stims']:
    for j in i:
        for k in j:
            image_path = os.path.join(image_dir, f"{k}")
            if os.path.isfile(image_path):
                image_stim = visual.ImageStim(win=exp.win, image=image_path, pos=(0, 0))
                image_stim.draw()
                exp.win.flip() 
                core.wait(0.7) 

            exp.pressable_region(exp.win, pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=False)
            
            if event.Mouse(win=exp.win).getPressed()[0]:
                if exp.is_pressed(mouse):
                    exp.win.close()
                    core.quit()
                
            #backup way to quit while testing
            if event.getKeys(keyList=['space']):
                exp.win.close()
                core.quit()

            image_time =  round(exp.win.flip(), 4)
            exp.image_timings.append((k, image_time))
            print(f"Displayed {k} at {image_time} seconds")
            
            #adding timing info to CSV
            timing_data = 'timing_info.xlsx'
            headers = ['image', 'image time']
            with open(timing_data, mode ='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames = headers)
                
                if file.tell() == 0:
                    writer.writeheader()
                    
                timing_info = {'image': k, 'image time': image_time}
                
                writer.writerow(timing_info)

exp.win.close()
