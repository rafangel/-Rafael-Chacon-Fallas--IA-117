##Proyecto 1 IA

from tkinter import *
import _thread as thread
import time
import random

global mapa
global plainBoard
global delay
global mostrar
global ruta
global pasear
global blockList
global test
global clients
global lastPos


root = Tk()
root.title("Proyecto 1 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction
root.configure(background='black')

delay = 0
blockList = []
clients = []
mostrar = False
ruta = False
lastPos = []


def moveLeft():
   global mapa
   global lastPos
   posU = isOnMap("U")
   mapa[posU[1]] = mapa[posU[1]][:posU[0]] + "*" + mapa[posU[1]][posU[0] + 1:]
   mapa[posU[1]] = mapa[posU[1]][:posU[0]-1] + "U" + mapa[posU[1]][posU[0]:]
   lastPos = posU

def moveRight():
   global mapa
   global lastPos
   posU = isOnMap("U")
   mapa[posU[1]] = mapa[posU[1]][:posU[0]] + "*" + mapa[posU[1]][posU[0] + 1:]
   mapa[posU[1]] = mapa[posU[1]][:posU[0]+1] + "U" + mapa[posU[1]][posU[0]+2:]
   lastPos = posU

def moveUp():
   global mapa
   global lastPos
   posU = isOnMap("U")
   mapa[posU[1]] = mapa[posU[1]][:posU[0]] + "*" + mapa[posU[1]][posU[0] + 1:]
   mapa[posU[1]-1] =  mapa[posU[1]-1][:posU[0]] + "U" + mapa[posU[1]-1][posU[0] + 1:]
   lastPos = posU
   
def moveDown():
   global mapa
   global lastPos
   posU = isOnMap("U")
   mapa[posU[1]] = mapa[posU[1]][:posU[0]] + "*" + mapa[posU[1]][posU[0] + 1:]
   mapa[posU[1]+1] =  mapa[posU[1]+1][:posU[0]] + "U" + mapa[posU[1]+1][posU[0] + 1:]
   lastPos = posU




def pasearNext():
   global mapa
   global lastPos
   posBlank = isOnMap(" ")
   posU = isOnMap("U")


   left = mapa[posU[1]][posU[0]-1]
   right = mapa[posU[1]][posU[0]+1]
   up = mapa[posU[1]-1][posU[0]]
   down = mapa[posU[1]+1][posU[0]]
   
   # quick search at adjacent spaces
   if(right == " "):
      moveRight()
   elif(down == " "):
      moveDown()
   elif(left == " "):
      moveLeft()
   elif(up == " "):
      moveUp()

   # long walk over visited spaces
   elif(posBlank != []): #unvisited space
      
      if(posBlank[1] == posU[1]): #same row *****************************
         
         if(posBlank[0] < posU[0]): #previous column
            
            if((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]): #valid move
               moveLeft()
            elif((down==" " or down=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveDown()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            elif((right==" " or right=="*") and lastPos != [posU[0],posU[1]+1]):
               moveRight()
            
               
         else:#column at right
            
            if((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]):
               moveDown()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
               
      elif(posBlank[1] < posU[1]): #previous row **********************

         if(posBlank[0] == posU[0]):
            
            if((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            elif((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
            elif((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]):
               moveDown()
               
         elif(posBlank[0] < posU[0]): #previous column
            
            if((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            elif((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]):
               moveDown()
            elif((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            
               
         else:# next column
            
            if((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            elif((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]):
               moveDown()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()

      else:#posBlank[1] > posU[1] next row  *****************************

         if(posBlank[0] == posU[0]):
            
            if((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]): 
               moveDown()
            elif((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]):
               moveUp()
               
         elif(posBlank[0] < posU[0]): #previous column
            
            if((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]): 
               moveDown()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
            elif((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]):
               moveUp()
               
         else:# next column
            
            if((right==" " or right=="*") and lastPos != [posU[0]+1,posU[1]]):
               moveRight()
            elif((down==" " or down=="*") and lastPos != [posU[0],posU[1]+1]):
               moveDown()
            elif((left==" " or left=="*") and lastPos != [posU[0]-1,posU[1]]):
               moveLeft()
            elif((up==" " or up=="*") and lastPos != [posU[0],posU[1]-1]): 
               moveUp()
            
         
      

def isOnMap(value):
   global mapa
   i = 0                 
   while(i<len(mapa)-1):   
      row = mapa[i]
      j = 0                     
      while(j<len(row)-1):
         if(row[j] == value):
            return [j,i] # structure: [x,y]
         j = j+1
      i= i+1
   return []


def countBlocks():
   global blockList
   global mapa
   global clients
   blockList = [] #reset variable
   i = 1                   # ignore first
   while(i<len(mapa)-2):   # and last row
      row = mapa[i]
      j = 1                      #ignore first
      while(j<len(row)-2):       #and last column
         #print("in loop: " + row + " with i: "+ str(i) + " j: " + str(j) + " value: " + row[j])
         #print()
         if(row[j-1]=="|" and row[j+1]=="|"):
            prevRow =mapa[i-1]
            nextRow = mapa[i+1]
            if(len(prevRow)>j and len(nextRow)>j): #map shapes
               if(prevRow[j]=="-" and nextRow[j]=="-"):#block detected
                  blockList.append([j,i]) #structure of block: [x,y]
                  if(row[j] != "."): #client on block
                     clients.append([len(blockList)-1,-1])
                     #structure of client: [begin,end] => begin at current block and end isn't generated here because not all blocks have been counted 
                     

         j= j+1
      i= i+1
   print("counting blocks:")
   print(blockList)



def mapToPlain():
   global mapa
   global mostrar
   global ruta
   s = ""
   i = 0                 
   while(i<len(mapa)-1):
      line = mapa[i]
      if(mostrar == False):
         line = line.replace("*"," ")
      if(ruta == False):
         line = line.replace("+"," ")
      s = s + line + "\n"
      i = i+1
   return s[:-1] #eliminate last "\n"

   
def rePaint():
   global test
   
   test.destroy()

   test = Text(root, bg = "black",fg = "green")
   test.place(x=150,y=100)
   test.insert(INSERT,mapToPlain())




# Define a function for the thread
def threadFunction( threadName):
   global delay
   global mapa
   global pasear
   i = 0
   while True:
      time.sleep(0.1)
      if(delay != 0): 
         if(i*0.1>delay):
            if(pasear):
               pasearNext()
            rePaint()
            i=0
         else:
            i=i+1
         
         

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
#print(mapa)

countBlocks()

#************************************



def send():
   global blockList
   global delay
   global mostrar
   global ruta
   global clients
   global pasear
   action = E1.get()
   words = action.split(" ")
   
   if(words[0] == "pasear" and len(words) == 1):
      pasear = True
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
         if(a<len(blockList)-1):
            if(a>0):
               i = 0
               while(i<a):
                  begin = random.randint(0,len(blockList))
                  end = random.randint(0,len(blockList))
                  if(begin != end):
                     clients.append([begin,end])
                  else: #bad random, try again
                     i=i-1
                  i = i+1
            print("clientes: ")
            print(clients)
         else:
            print("Error cuadra desconocida")
      except ValueError:
         print("Error comando incorrecto")
         
   elif(words[0] == "cliente" and len(words) == 3):
      try:
         a = int(words[1])
         b = int(words[2])
         if(a<len(blockList)-1 and b<len(blockList)-1 and a != b):
            clients.append([a,b])
            print("cliente:")
            print(clients)
         else:
            print("Error cuadras desconocidas o iguales")
      except ValueError:
         print("Error comando incorrecto")
         
   elif(words[0] == "parquear" and len(words) == 2):
      try:
         a = int(words[1])
         if(a<len(blockList)-1):
            print("parqueando: " + str(a))
         else:
            print("Error cuadra desconocida")
      except ValueError:
         print("Error comando incorrecto")
         
   else:
      print("Error comando desconocido")
   

test = Text(root, bg = "black")
test.place(x=150,y=100)
rePaint()

B = Button(root, text ="Send", command = send, bg = "green")
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)

root.mainloop()
