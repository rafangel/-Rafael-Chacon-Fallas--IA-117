##Proyecto 2 IA

from tkinter import *
import _thread as thread
import time
import random

global mapa
global plainBoard
global delay
global blockList
global homeBuildings
global workBuildings
global T1
global T2
global clients
global heatMap
global X  # customizables values
global D  # for heat map calculations
global taxis
global showPeople
global porcentaje
global day
global wakeUpRange


day = 100
wakeUpRange = 10
porcentaje = 30
delay = 0
blockList = []
homeBuildings = []
workBuildings = []
clients = []
heatMap = []
X = 2
D = 1
taxis = []
showPeople = False


#structure of node: [I,J,G,H,parentI,parentJ]
#structure of path: [ [node1 I,node1 J],[node2 I,node2 J],...]
#structure of block: [i,j]
#structure of home: [pos in blocklist, people there at the moment]
#structure of working place: [pos in blocklist, people there at the moment]
#structure of taxi: [name,I,J,state,path,copy of map for history]
#structure of client: [home,work,start working time] (IDs in blockList) 



#*************** GUI ***************** 
root = Tk()
root.title("Proyecto 2 IA")
root.geometry("1100x640")#size of the root window
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
         if(row[j-1]=="|" and row[j+1]=="|"):
            prevRow = mapa[i-1]
            nextRow = mapa[i+1]
            if(len(prevRow)>j and len(nextRow)>j): #checks maps dimensions 
               if(prevRow[j]=="-" and nextRow[j]=="-"):#block detected
                  blockList.append([i,j]) #structure of block: [i,j]
                  if(row[j] == "."): #homes
                     homeBuildings.append([len(blockList)-1,0]) #structure of home: [pos in blocklist, people there at the moment]
                     
                  if(row[j] == "/"):#working places
                     workBuildings.append([len(blockList)-1,0]) #structure of working place: [pos in blocklist, people there at the moment]

                     
         j+=1
      i+=1



#**** add people to block in map *****

def peopleInBlock(Pos):
   global homeBuildings
   global workBuildings
   i=0
   while(i<len(homeBuildings)):
      if(homeBuildings[i][0] == Pos):
         return homeBuildings[i][1]
      i+=1

   j=0
   while(j<len(workBuildings)):
      if(workBuildings[j][0] == Pos):
         return workBuildings[j][1]
      j+=1
   



#**** add people to block in map *****

def peopleInBlocks(line,i):
   global blockList
   j=0
   while(j<len(blockList)):
      if(blockList[j][0] == i): #the block is in that line
         amount = peopleInBlock(j)
         line = line[0:blockList[j][1]] + str(amount) + line[blockList[j][1]+1:]
      j+=1
   return line


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
   global showPeople
   global mapa
   s = ""
   i = 0                 
   while(i<len(mapa)):
      line = taxisInLine(i)
      if(showPeople):
         line = peopleInBlocks(line,i)
      s += line + "\n"
      i = i+1
   return s


#** Heat Map to string for printing ***

def heatMapToPlain():
   global heatMap
   s = ""
   i = 0                 
   while(i<len(heatMap)):
      line = heatMap[i]
      s += line + "\n"
      i = i+1
   return s



#********** begin heat map ***********

def beginHeatMap():
   global heatMap
   global mapa

   i=0
   while(i<len(mapa)):
      j=0
      heatMap.append(mapa[i])
      while(j<len(mapa[i])):
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



#******** create N taxis ************

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


#****** valid blockID as home *******

def getHome(blockID):
   global homeBuildings
   i=0
   while(i<len(homeBuildings)):
      if(homeBuildings[i][0] == blockID):
         return i
      i+=1
   return -1
         

#****** valid blockID as work *******

def getWorkPlace(blockID):
   global workBuildings
   i=0
   while(i<len(workBuildings)):
      if(workBuildings[i][0] == blockID):
         return i
      i+=1
   return -1



#****** valid blockID as home *******

def validHome(home):
   global homeBuildings
   i=0
   while(i<len(homeBuildings)):
      if(homeBuildings[i][0] == home):
         return True
      i+=1
   return False
         

#****** valid blockID as work *******

def validWorkPlace(work):
   global workBuildings
   i=0
   while(i<len(workBuildings)):
      if(workBuildings[i][0] == work):
         return True
      i+=1
   return False
   


#******** create N clients ***********

def addClients(n):
   global clients
   global blockList
   global workBuildings
   global homeBuildings
   i =0
   while(i<n):
      home = random.randint(0,len(homeBuildings)-1)
      work = random.randint(0,len(workBuildings)-1)

      homeBuildings[home][1] +=1
      
      home = homeBuildings[home][0]
      work = workBuildings[work][0]
      
      clients.append([home,work,0])
      i+=1
      


#********** parse command ************
   
def send():

   global blockList
   global delay
   global showPeople
   global clients
   global homeBuildings
   global porcentaje
   global day
   global wakeUpRange
   
   words = getAction()
   print(words)

   if(words[0] == "animar" and len(words)==2):
      n = int(words[1])
      delay = n
      
   elif(words[0] == "clientes" and len(words)==2):
      n = int(words[1])
      addClients(n)
      
   elif(words[0] == "cliente" and len(words)==3):
      home = int(words[1])
      work = int(words[2])
      if(validHome(home) and validWorkPlace(work)):
         clients.append([home,work,0])
         homeBuildings[getHome(home)][1] += 1
      else:
         print("error invalid blockID for home or work")
      
   elif(words[0] == "taxis" and len(words)==2):
      n = int(words[1])
      hireTaxis(n)

   elif(words[0] == "personas" and len(words)==2):
      if(words[1]=="on"):
         showPeople = True
      elif(words[1]=="off"):
         showPeople = False
      else:
         print("error, comando incorrecto")

   elif(words[0] == "trabajar" and len(words)==2):
      n=int(words[1])
      if(n<100 and n>0):
         porcentaje = n
      else:
         print("error porcentaje incorrecto")

   elif(words[0] == "iniciarDia" and len(words)==2):
      n=int(words[1])
      if(n<day-porcentaje):
         wakeUpRange = n
      else:
         print("rango propenso a errores")

   elif(words[0] == "dia" and len(words)==2):
      n=int(words[1])
      day = n
      
   elif(len(words[0])==1): #actions for one taxi
      taxi = words[0]
      
   else:
      print("error, comando incorrecto")

   rePaint()
   
     
   
#********* get text in entry *********

def getAction():
   action = E1.get()
   E1.delete(0,END)
   words = action.split(" ")
   return words


#********** refresh GUI **************
   
def rePaint(): 
   global T1
   global T2
   
   T1.destroy()
   T2.destroy()

   T1 = Text(root, bg = "black",fg = "green")
   T1.place(x=50,y=100)
   T1.insert(INSERT,mapToPlain())

   T2 = Text(root, bg = "black",fg = "green")
   T2.place(x=500,y=100)
   T2.insert(INSERT,heatMapToPlain())




#*************** GUI *****************
   
T1 = Text(root, bg = "black")
T1.place(x=50,y=100)

T2 = Text(root, bg = "black")
T2.place(x=500,y=100)


B = Button(root, text ="Send", command = send, bg = "green")
B.place(x=500,y=500)

E1 = Entry(root, bd =5)
E1.place(x=300,y=500)


readBoard()
rePaint()
#print(Astar(1,2,5,11))


root.mainloop()
