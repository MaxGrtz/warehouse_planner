
# try to install dependencies
from subprocess import Popen, PIPE

answer = input('Do you want to install dependencies automatically before starting? [y/n]: \n')
try:
    if (answer == 'y') or (answer == 'Y'):
        print('checking dependencies...')
        process = Popen(['pip', 'install', '-r', 'requirements.txt'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        print(stdout)
        print(stderr)
    else:
        print('trying to start without checking dependencies...')
        print('please install dependencies yourself (see requirements.txt) and restart if problems occur!')

except:
    print('tried to install dependencies but failed, please update your python (to 3.7x) and pip versions!')
    print('alternatively ignore this message and install dependencies yourself (see requirements.txt)')


# run application
from tkinter import Tk 
import gui

window = Tk()
warehouse_gui = gui.Gui(window)
window.mainloop()