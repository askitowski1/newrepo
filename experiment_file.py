from ipad_setup import ipadSetup
#from excel_timing import adding_data, saving_timing_data
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
stim_file = os.path.join(script_dir,'stimlists', f"CIDMEG_list{selected_list}.json")
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
ws2.append(['Image', 'Image Time', 'Difference'])

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
        
#loading stimuli names
with open(stim_file, 'r') as file:
    data = json.load(file)
image_names = data['stims']

#preloading images
exp.preload(image_dir)

#making loading bars and text
bar = visual.Rect(win = exp.win, size=(0.78, 0.2), lineColor = 'white', fillColor = 'white') #start at -.39 because that is the left edge of a size .78, .2 rectangle
text = exp.make_text(exp.win, "Stimuli loading...", color='white', font='Calibri', pos = (0, -.4) ,size = 0.1)
#bar2 = visual.Rect(win = exp.win, size=(0.0, 0.2), pos = (0,-.6), lineColor = 'white', fillColor = 'lightblue')

#filling bar2
total_images = len(os.listdir(image_dir))
images_loaded = 0


for file_name in os.listdir(image_dir):
    image_path = os.path.join(image_dir, file_name)
    if os.path.isfile(image_path) and file_name.lower().endswith(('.jpg')):
        exp.preloaded_images[file_name] = visual.ImageStim(win=exp.win, image=image_path, pos=(0, 0))

        #filling bar2
        images_loaded += 1
        bar.width = .78 * (images_loaded/ total_images) #this is filling from the middle
        bar.pos = (-.39 + bar.width/2, -.6)
        
        #making bar and text
        bar.draw()
        text.draw()
#        bar2.draw()
        exp.win.flip()
#create mouse
mouse = event.Mouse(visible = True, win = exp.win)

#displaying preloaded images
previous_time = None
for i in image_names:
    for j in i:
        for k in j:
            if k in exp.preloaded_images:
                image_stim = exp.preloaded_images[k]
                image_stim.draw()
                exp.win.flip() 
                core.wait(0.69)

            # Track region press
            exp.pressable_region(exp.win, pos=(0.6, -0.8), size=(0.78, 0.2), outline_color=False)

            if event.Mouse(win=exp.win).getPressed()[0]:
                if exp.is_pressed(mouse):
                    exp.win.close()
                    core.quit()

            # Backup way to quit while testing
            if event.getKeys(keyList=['space']):
                exp.win.close()
                core.quit()

            # Logging image timings
            image_time = round(exp.win.flip(), 4)
            exp.image_timings.append((k, image_time))
            # Adding timing info to excel file
            difference = None
            if previous_time is not None:
                difference = round(image_time - previous_time, 3)
            previous_time = image_time

            ws2.append([k, image_time, difference])
            wb.save('Subject Info.xlsx')
            print(f"Displayed {k} at {image_time} seconds")
# Close the window 
exp.win.close()
#wb.save('Subject Info.xlsx')