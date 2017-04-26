##Proyecto 1 IA

from tkinter import *
import _thread as thread
import time

global mapa
global plainBoard
global delay
global mostrar
global ruta

root = Tk()
root.title("Proyecto 1 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction
root.configure(background='black')

delay = 0
global test


def rePaint():
   global test
   test.destroy()
   
   test = Text(root, bg = "black",fg = "green")
   test.insert(INSERT,plainBoard)
   test.place(x=150,y=100)




# Define a function for the thread
def threadFunction( threadName):
   global delay
   global mapa
   while True:
      if(delay == 0):
         time.sleep(0.5)
      else:
         time.sleep(delay)
         rePaint()
         print (threadName + " " + time.ctime(time.time()) )

# Create two threads as follows
try:
   thread.start_new_thread( threadFunction, ("Thread-1", ) )
   #thread.start_new_thread( print_time, ("Thread-2", ) )
except:
   print("Error: unable to start thread")



#********** File read ***************

file = open("board.txt", "r")

plainBoard = file.read()
mapa = plainBoard.split("\n")
print(mapa)

#************************************



def send():
   global delay
   global mostrar
   global ruta
   action = E1.get()
   words = action.split(" ")
   if(words[0] == "pasear" and len(words) == 1):
      print("paseando")
   elif(words[0] == "buscar" and len(words) == 1):
      print("buscando")
   elif(words[0] == "mostrar" and len(words) == 2):
      if(words[1] == "on"):
         print("mostrando on")
         mostrar = True
      if(words[1] == "off"):
         print("mostrando off")
         mostrar = False
   elif(words[0] == "animar" and len(words) == 2):
      try:
         a = int(words[1])
         delay = a/1000
         print("animando: " + str(a))
      except ValueError:
         print("Error comando incorrecto")
   elif(words[0] == "ruta" and len(words) == 2):
      if(words[1] == "on"):
         print("ruteando on")
         ruta = True
      if(words[1] == "off"):
         print("ruteando off")
         ruta = True
   elif(words[0] == "clientes" and len(words) == 2):
      try:
         a = int(words[1])
         print("colocando clientes: " + str(a))
      except ValueError:
         print("Error comando incorrecto")
   elif(words[0] == "cliente" and len(words) == 3):
      try:
         a = int(words[1])
         b = int(words[2])
         print("colocando cliente: " + str(a) + " hacia: "+str(b))
      except ValueError:
         print("Error comando incorrecto")
   elif(words[0] == "parquear" and len(words) == 2):
      try:
         a = int(words[1])
         print("parqueando: " + str(a))
      except ValueError:
         print("Error comando incorrecto")
   else:
      print("Error comando incorrecto")
   

test = Text(root, bg = "black")
test.place(x=150,y=100)

B = Button(root, text ="Send", command = send, bg = "green")
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)

root.mainloop()
