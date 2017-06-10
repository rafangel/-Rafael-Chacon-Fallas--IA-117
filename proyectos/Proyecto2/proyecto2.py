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
global homeBuildings
global workBuildings
global test
global clients
global lastPos
global spot
global free
global newClient
global heatMap
global X  # customizables values
global D  # for heat map calculations
global taxis


delay = 0
mostrar = False
ruta = False
pasear = False
parquear = False
buscar = False
blockList = []
homeBuildings = []
workBuildings = []
clients = []
lastPos = []
spot = []
free = True
newClient = True
heatMap = []
X = 2
D = 1
taxis = []


#structure of node: [I,J,G,H,parentI,parentJ]
#structure of path: [ [node1 I,node1 J],[node2 I,node2 J],...]
#structure of block: [x,y]
#structure of home: [pos in blocklist, people there at the moment]
#structure of working place: [pos in blocklist, people there at the moment]
#structure of taxi: [name,I,J,state,path,copy of map for history]



#*************** GUI ***************** 
root = Tk()
root.title("Proyecto 2 IA")
root.geometry("900x640")#size of the root window
root.resizable(0, 0) #Don't allow resizing in the x or y direction
root.configure(background='black')




#****** check if pos is valid ********

def validMove(I,J):
   global mapa
   if(I >= 0 and I < len(mapa)):
      if(J >= 0 and J < len(mapa[I])):
         if(mapa[I][J] == " " or mapa[I][J] == "+" or mapa[I][J] == "*"):
            return True
         
   return False



#******* estimated distance *********

def heuristic(iniI,iniJ,endI,endJ):
   global heatMap
   total = 0
   while(iniI != endI or iniJ != endJ):
      
      if(iniI > endI and validMove(iniI-1,iniJ)):
         iniI-=1 #move up
         total += 1 + int(heatMap[iniI][iniJ])
         
      elif(iniI < endI and validMove(iniI+1,iniJ)):
         iniI+=1 #move down
         total += 1 + int(heatMap[iniI][iniJ])

      elif(iniJ > endJ and validMove(iniI,iniJ-1)):
         iniJ-=1 #move left
         total += 1 + int(heatMap[iniI][iniJ])
         
      elif(iniJ < endJ and validMove(iniI,iniJ+1)):
         iniJ+=1 #move right
         total += 1 + int(heatMap[iniI][iniJ])
         
      else:#rare cases
         if(iniJ == endJ):
            iniJ+=2#around de corner
            if(iniI > endI):
               iniI-=1 #move up
            if(iniI < endI):
               iniI+=1 #move down
            total += 15 #penalize this special case with 5 in each space
         if(iniI == endI):
            iniI+=2#around de corner
            if(iniJ > endJ):
               iniJ-=1 #move left
            if(iniJ < endJ):
               iniJ+=1 #move right
            total += 15 #penalize this special case with 5 in each space
         
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
   global heatMap
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
      g = current[2]+1+int(heatMap[currI][currJ])
      
      if(validMove(currI-1,currJ) and not inList(closedList,currI-1,currJ) and not inList(openList,currI-1,currJ)): #valid to move up and not in closed or open list
         
         h = heuristic(currI-1,currJ,endI,endJ)
         node = [currI-1,currJ,g,h,currI,currJ]
         openList.append(node)
            
      if(validMove(currI+1,currJ) and not inList(closedList,currI+1,currJ) and not inList(openList,currI+1,currJ)): #valid to move down and not in closed or open list
         
         h = heuristic(currI+1,currJ,endI,endJ)
         node = [currI+1,currJ,g,h,currI,currJ]
         openList.append(node)

      if(validMove(currI,currJ-1) and not inList(closedList,currI,currJ-1) and not inList(openList,currI,currJ-1)): #valid to move left and not in closed or open list

         h = heuristic(currI,currJ-1,endI,endJ)
         node = [currI,currJ-1,g,h,currI,currJ]
         openList.append(node)

      if(validMove(currI,currJ+1) and not inList(closedList,currI,currJ+1) and not inList(openList,currI,currJ+1)): #valid to move right and not in closed or open list

         h = heuristic(currI,currJ+1,endI,endJ)
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
   global homeBuildings
   global workBuildings
   global mapa
   global clients
   blockList = [] #reset variable
   i = 1                   # ignore first
   while(i<len(mapa)-2):   # and last row
      row = mapa[i]
      j = 1                      #ignore first
      while(j<len(row)-2):       #and last column
         #print("in loop: " + row + " with i: "+ str(i) + " j: " + str(j) + " value: " + row[j])
         if(row[j-1]=="|" and row[j+1]=="|"):
            prevRow =mapa[i-1]
            nextRow = mapa[i+1]
            if(len(prevRow)>j and len(nextRow)>j): #checks maps dimensions 
               if(prevRow[j]=="-" and nextRow[j]=="-"):#block detected
                  blockList.append([j,i]) #structure of block: [x,y]

                  if(row[j] == "."): #homes
                     homeBuildings.append([len(blockList)-1,0]) #structure of home: [pos in blocklist, people there at the moment]
                     
                  if(row[j] == "/"):#working place
                     workBuildings.append([len(blockList)-1,0]) #structure of working place: [pos in blocklist, people there at the moment]

                     
                     #clients.append([len(blockList)-1,-1]) #structure of client: [begin,end] => begin at current block and end isn't generated here because not all blocks have been counted 
         j+=1
      i+=1



#***** add taxis to line of map ******

def taxisInLine(i):
   global taxis
   global mapa
   line = mapa[i]
   j=0
   while(j<len(taxis)):
      if(taxis[j][1] == i): #the taxi is in that line
         line = line[0:taxis[j][2]] + taxis[j][0] + line[taxis[j][2]+1:]
      j+=1
   return line
         


#**** Map to string for printing *****

def mapToPlain():
   global mostrar
   global ruta
   s = ""
   i = 0                 
   while(i<len(mapa)):
      line = taxisInLine(i)
      s += line + "\n"
      i = i+1
   return s 



#********** begin heat map ***********

def beginHeatMap():
   global heatMap
   global mapa

   i=0
   while(i<len(mapa)-1):
      j=0
      heatMap.append(mapa[i])
      while(j<len(mapa[i])-1):
         if(mapa[i][j] == " "):
            heatMap[i] = heatMap[i][0:j] +"0"+ heatMap[i][j+1:]#initial
         j+=1
      
      i+=1
   


#********** Read File ****************

def readBoard():
   global plainBoard
   global mapa
   
   file = open("board.txt", "r")
   plainBoard = file.read()
   mapa = plainBoard.split("\n")
   mapa = mapa[0:len(mapa)-1] #eliminate final \n
   countBlocks()
   beginHeatMap()



#*************************************

def hireTaxis(n):
   global taxis
   global mapa
   names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
   if(n>=len(names)):
      n=len(names)-1 #fix max amount of taxis
   i=0
   while(i<n):
      posI = random.randint(0,len(mapa)-1)
      posJ = random.randint(0,len(mapa[posI])-1)
      while(not validMove(posI,posJ)):
         posI = random.randint(0,len(mapa)-1)
         posJ = random.randint(0,len(mapa[posI])-1)
            
      state = 0
      path=[]
      history = mapa
      taxis.append([names[i],posI,posJ,state,path,history]) #taxi structure: [name,I,J,state,path,copy of map for history]
      i+=1
   


#********** parse command ************
   
def send():

   global blockList
   global delay
   global mostrar
   global ruta
   global clients
   global pasear
   global parquear
   global buscar
   global spot
   
   words = getAction()

   if(words[0] == "animar" and len(words)==2):
      n = words[1]
      
   elif(words[0] == "clientes" and len(words)==2):
      n = words[1]
      
   elif(words[0] == "cliente" and len(words)==3):
      home = words[1]
      work = words[2]
      
   elif(words[0] == "taxis" and len(words)==2):
      print(words)
      n = int(words[1])
      print(n)
      hireTaxis(n)
      rePaint()
      
   elif(len(words[0])==1): #actions for one taxi
      taxi = words[0]
      
   else:
      print("error, wrong action")
   
     
   
#********* get text in entry *********

def getAction():
   action = E1.get()
   E1.delete(0,END)
   words = action.split(" ")
   return words


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


readBoard()
rePaint()
#print(Astar(1,2,5,11))


root.mainloop()
