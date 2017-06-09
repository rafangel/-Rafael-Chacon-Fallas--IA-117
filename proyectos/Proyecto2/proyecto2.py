##Proyecto 2 IA

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
global parquear
global buscar
global blockList
global test
global clients
global lastPos
global spot
global free
global newClient


delay = 0
blockList = []
clients = []
mostrar = False
ruta = False
pasear = False
parquear = False
buscar = False
lastPos = []
spot = []
free = True
newClient = True


#*************** GUI ***************** 
root = Tk()
root.title("Proyecto 2 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction
root.configure(background='black')



#**estimated distance ignoring walls**

def heuristic(iniI,iniJ,endI,endJ):
   
   total = 0
   while(iniI != endI and iniJ != endJ):
      
      if(iniI > endI):
         iniI-=1 #move up
         total +=1
         
      if(iniI < endI):
         iniI+=1 #move down
         total +=1

      if(iniJ > endJ):
         iniJ-=1 #move left
         total +=1
         
      if(iniJ < endJ):
         iniJ+=1 #move right
         total +=1
         
   return total



#*** check if end is in openlist ****

def goalNotFound(endI,endJ,openList):
   i=0
   while(i<len(openList)):
      if(openList[i][0] == endI and openList[i][1] == endJ):
         return False
      i+=1

   return True


#************************************

def lowestF(openList):

   oldF = openList[0][2] + openList[0][3]
   pos = 0
   i=1
   while(i<len(openList)):
      newF = openList[i][2] + openList[i][3]
      if(newF <= oldF):
         oldF = newF
         pos = i
      i+=1
         
   return pos


#****** check if pos is valid ********

def validMove(I,J):
   global mapa
   if(I >= 0 and I < len(mapa)):
      if(J >= 0 and J < len(mapa[I])):
         if(mapa[I][J] == " " or mapa[I][J] == "+" or mapa[I][J] == "*"):
            return True
         
   return False


#**** checks if node is in list ****

def inList(lista,I,J):
   k=0
   while(k<len(lista)):
      if(lista[k][0]== I and lista[k][1]== J):
         return True
      k+=1
      
   return False


#*** get node from its positions ****

def getNode(lista,I,J):
   k=0
   while(k<len(lista)):
      if(lista[k][0]== I and lista[k][1]== J):
         return lista[k]
      k+=1
   


#********* search best path *********

def Astar(iniI,iniJ,endI,endJ):
   global mapa
   openList = []
   closedList = []

   h=heuristic(iniI,iniJ,endI,endJ)
   current = [iniI,iniJ,0,h,iniI,iniJ] #structure of node: [I,J,G,H,parentI,parentJ]
   
   
   openList.append(current)

   while(openList != [] and goalNotFound(endI,endJ,closedList)):

      pos = lowestF(openList)
      current = openList.pop(pos)
      closedList.append(current)
      currI = current[0]
      currJ = current[1]
      g = current[2]+1
      
      if(validMove(currI-1,currJ) and not inList(closedList,currI-1,currJ)): #valid to move up and not in closed list
         
         if(not inList(openList,currI-1,currJ)):
            h = heuristic(iniI,iniJ,currI-1,currJ)
            node = [currI-1,currJ,g,h,currI,currJ]
            openList.append(node)
            
      if(validMove(currI+1,currJ) and not inList(closedList,currI+1,currJ)): #valid to move down and not in closed list
         
         if(not inList(openList,currI+1,currJ)):
            h = heuristic(iniI,iniJ,currI+1,currJ)
            node = [currI+1,currJ,g,h,currI,currJ]
            openList.append(node)

      if(validMove(currI,currJ-1) and not inList(closedList,currI,currJ-1)): #valid to move left and not in closed list

         if(not inList(openList,currI,currJ-1)):
            h = heuristic(iniI,iniJ,currI,currJ-1)
            node = [currI,currJ-1,g,h,currI,currJ]
            openList.append(node)

      if(validMove(currI,currJ+1) and not inList(closedList,currI,currJ+1)): #valid to move right and not in closed list

         if(not inList(openList,currI,currJ+1)):
            h = heuristic(iniI,iniJ,currI,currJ+1)
            node = [currI,currJ+1,g,h,currI,currJ]
            openList.append(node)

   #out of while
   if(openList != []): #goal reached
      
      current = getNode(closedList,endI,endJ)
      path = [[current[0],current[1]]] #path structure [ [node1 I,node1 J],[node2 I,node2 J],...]
      
      while(current[0] != current[4] or current[1] != current[5]): #only initial node is its own parent

              current = getNode(closedList,current[4],current[5])# move current to parent node
              path.insert(0,[current[0],current[1]]) #add node pos to de beginning of path

   return path




#** count amount of buildings in map **

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
                     clients.append([len(blockList)-1,-1]) #structure of client: [begin,end] => begin at current block and end isn't generated here because not all blocks have been counted 
         j= j+1
      i= i+1


#**** Map to string for printing *****

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



#********** Read File ****************

def readBoard():
   global plainBoard
   global mapa
   
   file = open("board.txt", "r")
   plainBoard = file.read()
   mapa = plainBoard.split("\n")

   countBlocks()


#********** parse command ************
   
def send():
   readBoard()
   rePaint()
   print(Astar(1,2,5,11))
   


#********** refresh GUI **************
   
def rePaint():
   global test
   
   test.destroy()

   test = Text(root, bg = "black",fg = "green")
   test.place(x=150,y=100)
   test.insert(INSERT,mapToPlain())



#*************** GUI *****************
   
test = Text(root, bg = "black")
test.place(x=150,y=100)


B = Button(root, text ="Send", command = send, bg = "green")
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)

root.mainloop()
