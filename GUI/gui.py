from tkinter import *
from tkinter import ttk
import time

main = Tk()
main.geometry('500x500')
progBarVal = 0

class myListbox(Listbox):
	def __init__(self, frame, **kwargs):
		kwargs['selectmode'] = tkinter.SINGLE
		self.currIndex = None

################
#   FUNCTIONS
################
def add():
	FileList.insert(END,1)
	#print("insert")

def remove():
	file = FileList.curselection()
	if file != ():
		fileIndex = int(file[0])
		FileList.delete(fileIndex,fileIndex)
		#print("remove at ",fileIndex)

def clear():
	FileList.delete(0,END)


#NEED TO IMPLEMENT ENCODING AND DECODING FUNCTIONS
def encoding():
	fileName = outputFile.get()
	if fileName == "":
		fileName = "output.bin"
	print(fileName)
	

def decoding(): 
	print("IM DECODING")


###############
#    FRAMES
###############

fileFrame = Frame(master = main)
fileButtonFrame = Frame(master = fileFrame)
quitFrame = Frame(master = main)
encodeDecodeFrame = Frame(master = main)
outputFrame = Frame(master = main)
progressFrame = Frame(master = main)


###############
#	OBJECTS
###############

#LIST BOX
FileList = Listbox(fileFrame,width = 50, height = 15)


#ADD/REMOVE FILE BUTTONS

addFileButton = Button(fileButtonFrame,text="Add File", command = add)
removeFileButton = Button(fileButtonFrame, text = "Remove File", command = remove)
clearAllButton = Button(fileButtonFrame, text = "Clear All", command = clear)

addFileButton.pack(side = TOP)
removeFileButton.pack(side = TOP)
clearAllButton.pack(side = TOP)


#OUTPUT ENTRY
outputLabel = Label(outputFrame, justify='left', text='Output File Name:')
outputFile = Entry(outputFrame, width = 40)
outputFile.delete(0,END)

outputLabel.pack(side = LEFT)
outputFile.pack(side = LEFT)

#ENCODE DECODE BUTTONS
encodeButton = Button(encodeDecodeFrame,text="Encode Files", command = encoding)
decodeButton = Button(encodeDecodeFrame, text="Decode File", command = decoding)

decodeButton.pack(side = RIGHT)
encodeButton.pack(side = RIGHT)

#PROGRESS BAR
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

outputFrame.pack(side = TOP, pady = 5)
encodeDecodeFrame.pack(side = TOP)
progressFrame.pack(side = TOP, pady = 5)
quitFrame.pack(side = TOP)

main.title("EC504 Video Encoder/Decoder")

main.mainloop()