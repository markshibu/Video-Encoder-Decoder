import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import time
import math

main = Tk()
main.geometry('750x500')
progBarVal = DoubleVar()
QFValue = 0.1;


#List Box that Implements Reorder by Dragging
class myListbox(tkinter.Listbox):
    def __init__(self, master, **kw):
        kw['selectmode'] = tkinter.SINGLE
        tkinter.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i

##############
#   METHODS
##############
def add():
	main.files = filedialog.askopenfiles(mode = 'rb', title = 'Select Images for Encoding')
	for file in main.files:
		FileList.insert(END,file.name)

def remove():
	file = FileList.curselection()
	if file != ():
		fileIndex = int(file[0])
		FileList.delete(fileIndex)

def clear():
	FileList.delete(0,END)

def updateQF(value):
	global QFValue
	QFValue = value

def encoding():
	global QFValue
	global progBarVal

	i = 0
	progBarVal.set(0)

	files = FileList.get(0,END)
	numFiles = len(files)
	if numFiles == 0:
		messagebox.showinfo("Error", "No Files Selected")
		return

	#Disable Encoding and Decoding when one is active
	encodeButton.configure(state=tkinter.DISABLED)
	decodeButton.configure(state=tkinter.DISABLED)

	start = time.time()
	fileName = outputFile.get()
	if fileName == "":
		fileName = "output.bin"
	print(fileName)

	for file in files:
		i+= 1
		progBarVal.set(i/numFiles * 100)
		main.update()
		time.sleep(0.25)

	totaltime = time.time() - start

	#Renable Encoding and Decoding
	encodeButton.configure(state=tkinter.ACTIVE)
	decodeButton.configure(state=tkinter.ACTIVE)

	message = "Encoded "+str(numFiles)+" files with QF Value of "+str(QFValue) +" in "+str(round(totaltime,3))+" seconds"
	messagebox.showinfo("Encoding Complete", message)


def decoding():
	global progBarVal
	main.decodefile = filedialog.askopenfile(mode = 'rb', title = "Choose a File to Decode")
	start = time.time()
	print(main.decodefile.name)
	totaltime = time.time() - start



###############
#    FRAMES
###############

fileFrame = Frame(master = main)
fileButtonFrame = Frame(master = fileFrame)
quitFrame = Frame(master = main)
encodeDecodeFrame = Frame(master = main)
outputFrame = Frame(master = main)
progressFrame = Frame(master = main)
qualityFrame = Frame(master = main)


###############
#	OBJECTS
###############

#LIST BOX
FileList = myListbox(fileFrame, width = 80, height = 15)#selectmode = SINGLE,

#ADD/REMOVE FILE BUTTONS
fileLabel = Label(fileFrame,justify='left', text ='Selected Files For Encoding')
addFileButton = Button(fileButtonFrame,text="Add File(s)", command = add)
removeFileButton = Button(fileButtonFrame, text = "Remove File", command = remove)
clearAllButton = Button(fileButtonFrame, text = "Clear All", command = clear)

fileLabel.pack(side = TOP)
addFileButton.pack(side = TOP)
removeFileButton.pack(side = TOP, pady = 3)
clearAllButton.pack(side = TOP)

#QUALITY FACTOR FRAME
qualityLabel = Label(qualityFrame,justify='left', text = 'Quality Factor: ')
qualityFactor = Scale(qualityFrame, variable = QFValue, orient = "horizontal", length = 250,\
		from_ = 0.1, to = 1.5, resolution = 0.1, command = updateQF)
qualityLabel.pack(side = LEFT)
qualityFactor.pack(side = LEFT)

#OUTPUT FRAME
outputLabel = Label(outputFrame, justify='left', text='Output File Name:')
outputFile = Entry(outputFrame, width = 40)
outputFile.delete(0,END)

outputLabel.pack(side = LEFT)
outputFile.pack(side = LEFT)

#ENCODE DECODE BUTTONS
encodeButton = Button(encodeDecodeFrame,text="Encode Files", command = encoding)
decodeButton = Button(encodeDecodeFrame, text="Decode File", command = decoding)

decodeButton.pack(side = RIGHT,padx = 10)
encodeButton.pack(side = RIGHT,padx = 10)

#PROGRESS BAR FRAME
progBarLabel = Label(progressFrame, justify='left', text='Progress')
progBar = ttk.Progressbar(progressFrame, orient = "horizontal", length = 400, mode = "determinate",\
		maximum = 100, value = 0, variable = progBarVal)

progBarLabel.pack(side=TOP)
progBar.pack(fill = X, pady = 3)


#QUIT BUTTON
quitButton = Button(quitFrame, text="QUIT", fg = "white", bg="red", command = main.destroy)
quitButton.pack(side = RIGHT)


#FRAME POSITIONING
fileFrame.pack(side = TOP, pady = 5)
FileList.pack(side = LEFT)
fileButtonFrame.pack(side = RIGHT)

qualityFrame.pack(side = TOP, pady = 5)
outputFrame.pack(side = TOP, pady = 5)
encodeDecodeFrame.pack(side = TOP)
progressFrame.pack(side = TOP, pady = 5)
quitFrame.pack(side = TOP)

main.title("EC504 Video Encoder/Decoder")

main.mainloop()