from tkinter import Tk
from tkinter.filedialog import askopenfilename

def seleccionar_archivo(titulo):
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askopenfilename(title=titulo) # show an "Open" dialog box and return the path to the selected file
	return filename