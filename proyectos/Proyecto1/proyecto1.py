##Proyecto 1 IA

from tkinter import *
import _thread as thread
import time


root = Tk()
root.title("Proyecto 1 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction





# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print (threadName + " " + time.ctime(time.time()) )

# Create two threads as follows
try:
   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print("Error: unable to start thread")



#********** File read ***************

file = open("board.txt", "r")

board = file.read()
print(board)

#************************************



def send():
   messagebox.showinfo( "Hello Python", "Sending commmand")

B = Button(root, text ="Send", command = send)
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)

root.mainloop()
