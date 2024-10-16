from psychopy import visual, core, event
import json, os

win = visual.Window(fullscr=True, color='black')
box = visual.Rect(win=win, width=1, height=1, fillColor='white')


words = [
    [['tiger', 'sport', 'jump', 'ball', 'play'], ['loop', 'cry', 'scare', 'spooky', 'dance']],
    [['out', 'strike', 'bunt', 'hit', 'homer'], ['basket', 'jersey', 'dunk', 'score', 'shoot']]
]
stim_file = "C:\\Users\\Experiment\\Desktop\\CIDMEG_Exp\\stimlists\\CIDMEG_listA.json"
image_file = "C:\\Users\\Experiment\\Desktop\\CIDMEG_Exp\\images"
print(image_file[0])
with open(stim_file, 'r') as file:
    data = json.load(file)

mouse = event.Mouse(visible = False, win = win)
intro = visual.TextBox2(win=win, text = u"Welcome to the experiment, touch anywhere to start")
starting = visual.TextBox2(win=win, text = u"Loading...") 
ending = visual.TextBox2(win=win, text= u"Thank you for playing")
while True:
    intro.draw()
    win.flip()
    if mouse.getPressed()[0]: 
        starting.draw()
        win.flip()
        core.wait(2)
                
        for i in data['stims']:
            for j in i:
                for k in j:
                    image_path = os.path.join(image_file, f"{k}")
                    if os.path.isfile(image_path):
                        window_size = win.size
                        image_stim = visual.ImageStim(win=win, image=image_path, pos=(0, 0))
                        image_stim.draw()
                        win.flip()
                    else:
                        print("File does not exist.")
                    if event.getKeys(keyList=['space']):
                        win.close()
                        core.quit()
                    if mouse.getPressed()[0]:
                        win.close()
                        ending.draw()
                        win.flip()
                        core.wait(2)
                        core.quit()
                
                    core.wait(0.7)
            
             
            
win.close()
core.quit()
