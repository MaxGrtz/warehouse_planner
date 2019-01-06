from tkinter import Tk 
import gui
from subprocess import Popen, PIPE
 

# try to install dependencies
try:
    process = Popen(['pip', 'install', '-r', 'requirements.txt'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
except:
    print('tried to install dependencies but failed, please update your python and pip versions!')
    print('alternatively ignore this message and install dependencies yourself')

# run application
window = Tk()
warehouse_gui = gui.Gui(window)
window.mainloop()