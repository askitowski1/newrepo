from ipad_setup import ipadSetup
from psychopy import core, event, visual, gui
import json, os, csv, openpyxl
from openpyxl import Workbook, load_workbook

#getting subject info
expInfo = {'Participant': '', 'Session': '', 'Block': '', 'List': 'B'}
dlg = gui.DlgFromDict(dictionary=expInfo, order=['Participant', 'Session', 'Block', 'List'], title="Participant info")
if dlg.OK == False:
    core.quit()

#getting stimuli
selected_list = expInfo['List']
script_dir = os.path.dirname(os.path.abspath(__file__))
stim_file  = os.path.join(script_dir,'stimlists', f"CIDMEG_list{selected_list}.json")
image_dir = os.path.join(script_dir, 'images')

#adding data to excel file
try:
    wb = load_workbook('Subject Info.xlsx')
    ws1 = wb.active
except FileNotFoundError:
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Subject Info"
    ws1.append(["Participant", "Session", "Block", "List", "Timing"])
participant = expInfo['Participant']

ws1.append([expInfo['Participant'], expInfo['Session'], expInfo['Block'], expInfo['List']])
ws2 = wb.create_sheet(participant)
ws2.append(['Image', 'Image Time', 'Difference', 'Average'])

row = 2
col = 5
while ws1.cell(row=row, column=col).value is not None:
    row += 1 
link = f"Subject Info.xlsx#{participant}!A1"
cell = ws1.cell(row=row, column=col)

cell.hyperlink = link
cell.value = "link"
wb.save('Subject Info.xlsx')

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
# core.wait(5) #surface is stuck on the first few images for a seemingly random amount of time. 
#              this kind of helped but theres prob a better fix

#displaying preloaded images
previous_time = None
image_start_time = core.getTime() 
button = exp.pressable_region(exp.win, pos=(0.75, -0.8), size=(0.39, 0.2), outline_color=False)
for i in image_names:
    for j in i:
        for k in j:
            if k in exp.preloaded_images:
                image_stim = exp.preloaded_images[k]
                image_stim.draw()
                button.draw()
                exp.win.flip() 

            # Track region press
            if event.Mouse(win=exp.win).getPressed()[0]:
                if exp.is_pressed(mouse):
                    exp.win.close()
                    core.quit()

            # Backup way to quit while testing
            if event.getKeys(keyList=['space']):
                exp.win.close()
                core.quit()

            # Logging image timings
            image_time = round(core.getTime(), 4)
            exp.image_timings.append((k, image_time))
            # Adding timing info to excel file
            difference = None
            if previous_time is not None:
                difference = round(image_time - previous_time, 3)
            previous_time = image_time

            ws2.append([k, image_time, difference])
            wb.save('Subject Info.xlsx')
            print(f"Displayed {k} at {image_time} seconds")
            
            while core.getTime() - image_start_time < .700:
                core.wait(0.001)
            image_start_time = core.getTime()
# Close the window 
exp.win.close()