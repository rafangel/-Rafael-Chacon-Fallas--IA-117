##Proyecto 1 IA

from tkinter import *

root = Tk()
root.title("Proyecto 1 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction

file = open("board.txt", "r")

board = file.read()
print(board)


def send():
   messagebox.showinfo( "Hello Python", "Sending commmand")

B = Button(root, text ="Send", command = send)
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)

root.mainloop()
