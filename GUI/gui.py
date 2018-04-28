import tkinter as tk
from tkinter.ttk import *

main = tk.Tk()
main.geometry('500x500')
FileList = tk.Listbox(main, width = 40, height = 20)
#FileList.
i = 1

# class customListBox(tk.Listbox):
# 	def __init__(self):
# 		self.pack()


def say_hi():
	for x in FileList:
		print(x)

def add():
	FileList.insert(tk.END,1)
	print("insert")
	

def delete():
	FileList.delete(0,tk.END)

frame = Frame(master=main)

hi_there = tk.Button(frame, text = "Hello World\n(clickme)", command = say_hi)
hi_there.pack(side = "left")

add = tk.Button(frame,text="ADD", command = add())
add.pack(side = "bottom")

delete = tk.Button(frame, text = "DELETE", command = delete())
delete.pack(side = "bottom")

quit = tk.Button(frame, text="QUIT", fg = "white", bg="red", command = main.destroy)
quit.pack(side = "right")

FileList.pack(side = "top")
frame.pack(side = "bottom")


main.mainloop()