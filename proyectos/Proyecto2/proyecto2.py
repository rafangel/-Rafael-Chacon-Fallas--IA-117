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
global X 
global N   
global D 
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
X = 3 # customizables 
N = 2 # values for heat 
D = 1 # map calculations
taxis = []
showPeople = False


#structure of node: [I,J,G,H,parentI,parentJ]
#structure of path: [ [node1 I,node1 J],[node2 I,node2 J],...]
#structure of block: [i,j]
#structure of home: [pos in blocklist, people there at the moment]
#structure of working place: [pos in blocklist, people there at the moment]
#structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
#structure of client: [home,work,start working time, inHome, taxiCalled] (IDs in blockList) 



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

   lastI = -1
   lastJ = -1
   
   none = False
   while(iniI != endI or iniJ != endJ):
      #print("heuristic iniI: "+str(iniI)+" iniJ: "+str(iniJ)+" endI: "+str(endI)+" endJ: "+str(endJ)+" lastI: "+str(lastI)+" lastJ: "+str(lastJ))

      if(iniJ > endJ and validMove(iniI,iniJ-1) and (lastI!=iniI or lastJ!=iniJ-1)):
         lastI = iniI
         lastJ = iniJ
         iniJ-=1 #move left
         total += 1 + int(heatMap[iniI][iniJ])
         none = False
      elif(iniI > endI and validMove(iniI-1,iniJ)and (lastI!=iniI-1 or lastJ!=iniJ)):
         lastI = iniI
         lastJ = iniJ
         iniI-=1 #move up
         total += 1 + int(heatMap[iniI][iniJ])
         none = False
      elif(iniI < endI and validMove(iniI+1,iniJ) and (lastI!=iniI+1 or lastJ!=iniJ)):
         lastI = iniI
         lastJ = iniJ
         iniI+=1 #move down
         total += 1 + int(heatMap[iniI][iniJ])
         none = False
      
      elif(iniJ < endJ and validMove(iniI,iniJ+1) and (lastI!=iniI or lastJ!=iniJ+1)):
         lastI = iniI
         lastJ = iniJ
         iniJ+=1 #move right
         total += 1 + int(heatMap[iniI][iniJ])
         none = False
         
         
      else:#rare cases
         if(none):#entered in none "if" last cicle
            if(validMove(iniI,iniJ-1) and (lastI!=iniI or lastJ!=iniJ-1)):
               lastI = iniI
               lastJ = iniJ
               iniJ-=1 #move left
               total += 1 + int(heatMap[iniI][iniJ])
               none = False

            elif(validMove(iniI-1,iniJ) and (lastI!=iniI-1 or lastJ!=iniJ)):
               lastI = iniI
               lastJ = iniJ
               iniI-=1 #move up
               total += 1 + int(heatMap[iniI][iniJ])
               none = False
               
            elif(validMove(iniI+1,iniJ) and (lastI!=iniI+1 or lastJ!=iniJ)):
               lastI = iniI
               lastJ = iniJ
               iniI+=1 #move down
               total += 1 + int(heatMap[iniI][iniJ])
               none = False
               
            elif(validMove(iniI,iniJ+1) and (lastI!=iniI or lastJ!=iniJ+1)):
               lastI = iniI
               lastJ = iniJ
               iniJ+=1 #move right
               total += 1 + int(heatMap[iniI][iniJ])
               none = False
            
         else:
            none = True
         
   return total



#*** check if end is in openlist ****

def goalNotFound(endI,endJ,openList):
   i=0
   while(i<len(openList)):
      if(openList[i][0] == endI and openList[i][1] == endJ):
         return False
      i+=1

   return True


#* return lowest F node in openList *

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
      
      if(validMove(currI-1,currJ) and not inList(closedList,currI-1,currJ) and not inList(openList,currI-1,currJ)):
         #valid to move up and not in closed or open list
         
         h = heuristic(currI-1,currJ,endI,endJ)
         node = [currI-1,currJ,g,h,currI,currJ]
         openList.append(node)
            
      if(validMove(currI+1,currJ) and not inList(closedList,currI+1,currJ) and not inList(openList,currI+1,currJ)):
         #valid to move down and not in closed or open list
         
         h = heuristic(currI+1,currJ,endI,endJ)
         node = [currI+1,currJ,g,h,currI,currJ]
         openList.append(node)

      if(validMove(currI,currJ-1) and not inList(closedList,currI,currJ-1) and not inList(openList,currI,currJ-1)):
         #valid to move left and not in closed or open list

         h = heuristic(currI,currJ-1,endI,endJ)
         node = [currI,currJ-1,g,h,currI,currJ]
         openList.append(node)

      if(validMove(currI,currJ+1) and not inList(closedList,currI,currJ+1) and not inList(openList,currI,currJ+1)):
         #valid to move right and not in closed or open list

         h = heuristic(currI,currJ+1,endI,endJ)
         node = [currI,currJ+1,g,h,currI,currJ]
         openList.append(node)

   #out of while
   if(openList != []): #goal reached
      
      current = getNode(closedList,endI,endJ)
      path = [[current[0],current[1]]]
      #path structure [ [node1 I,node1 J],[node2 I,node2 J],...]
      
      while(current[0] != current[4] or current[1] != current[5]):
         #only initial node is its own parent
         current = getNode(closedList,current[4],current[5])# move current to parent node
         path.insert(0,[current[0],current[1]]) #add node pos to de beginning of path

   return path[1:] #eliminate starting pos




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
                     homeBuildings.append([len(blockList)-1,0])
                     #structure of home: [pos in blocklist, people there at the moment]
                     
                  if(row[j] == "/"):#working places
                     workBuildings.append([len(blockList)-1,0])
                     #structure of working place: [pos in blocklist, people there at the moment]

                     
         j+=1
      i+=1


#*** add person to block in list ****

def addPersonInBlock(Pos):
   global homeBuildings
   global workBuildings
   i=0
   while(i<len(homeBuildings)):
      if(homeBuildings[i][0] == Pos):
         homeBuildings[i][1] +=1
      i+=1

   j=0
   while(j<len(workBuildings)):
      if(workBuildings[j][0] == Pos):
         workBuildings[j][1] +=1
      j+=1



#** remove person to block in list ***

def removePersonInBlock(Pos):
   global homeBuildings
   global workBuildings
   i=0
   while(i<len(homeBuildings)):
      if(homeBuildings[i][0] == Pos):
         homeBuildings[i][1] -=1
      i+=1

   j=0
   while(j<len(workBuildings)):
      if(workBuildings[j][0] == Pos):
         workBuildings[j][1] -=1
      j+=1



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

def taxisInLine(line,i):
   global taxis
   
   j=0
   while(j<len(taxis)):
      if(taxis[j][1] == i): #the taxi is in that line
         line = line[0:taxis[j][2]] + taxis[j][0] + line[taxis[j][2]+1:]
      j+=1
   return line


#***** copy mapa to add * and + ******
def copyMap():
   global mapa
   global taxis
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]

   copia = []          # force copy to be in 
   copia.extend(mapa)  # different memory space
   i=0
   while(i<len(taxis)):
      
      if(taxis[i][5]): #mostrar on
         history = taxis[i][7]
         j=0
         while(j<len(history)):
            pos = history[j] #structure [i,j]
            copia[pos[0]] = copia[pos[0]][0:pos[1]] + "*" + copia[pos[0]][pos[1]+1:]
            j+=1

      if(taxis[i][6]): #ruta on
         path = taxis[i][4]
         k=0
         while(k<len(path)):
            pos = path[k] #structure [i,j]
            copia[pos[0]] = copia[pos[0]][0:pos[1]] + "+" + copia[pos[0]][pos[1]+1:]
            k+=1

      i+=1
      
   return copia

   
   


#**** Map to string for printing *****

def mapToPlain():
   global showPeople
   s = ""
   i = 0

   copia = copyMap()
   
   while(i<len(copia)):
      line = taxisInLine(copia[i],i)
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


#**** search if pos is in history *****

def inHistory(i,j,history):

   k=0
   while(k<len(history)):
      pos = history[k]
      if(pos[0]==i and pos[1]==j):
         return True
      k+=1
   return False



#** search blank space not in history **

def nextBlank(ID):
   global taxis
   global mapa

   taxi = taxis[ID]
   history = taxi[7]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   bestI = -1
   bestJ = -1
   distance = 1000000
   i = 0      
   while(i<len(mapa)-1):   
      row = mapa[i]
      j = 0                     
      while(j<len(row)-1):
         if(row[j] == " " and not inHistory(i,j,history)):
            d2 = abs(i-taxi[1])+abs(j-taxi[2])
            if(distance>d2):
               bestI =i
               bestJ =j
               distance = d2
         j = j+1
      i= i+1
   if(bestI != -1):
      return [bestI,bestJ]
   else:
      return []

#**************************************

def decreaseJams():
   global heatMap
   global D

   i=0
   while(i<len(heatMap)):
      j=0
      while(j<len(heatMap[i])):
         try:
            num = int(heatMap[i][j])
            if(num > 0): 
               num -= D
               if(num<0):#minimun value
                  num = 0
            
               heatMap[i] = heatMap[i][0:j] + str(num)+ heatMap[i][j+1:]
            j+=1
         except ValueError:
            j+=1
      i+=1
   


#***** amount of taxis in the pos *****

def taxisThere(I,J):
   global taxis
   num = 0
   k=0
   while(k<len(taxis)):
      taxi = taxis[k]
      if(taxi[1]==I and taxi[2]==J):
         num+=1
      k+=1
   return num
   


#*** caculate delay for taxi in Jam ***

def carJam(ID):
   global taxis
   global heatMap
   global X
   global N
   global D

   taxi = taxis[ID]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   I=taxi[1]
   J=taxi[2]
   if(N <= taxisThere(I,J)):
      num = int(heatMap[I][J])+X
      if(num >9): #max value to prevent errors
         num = 9
      heatMap[I] = heatMap[I][0:J] + str(num)+ heatMap[I][J+1:]
      taxis[ID][9] = num
      
   

#***** move taxi one step in path *****

def advancePath(ID):
   global taxis
   
   taxi = taxis[ID]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   path = taxi[4]
   nextI = path[0][0]
   nextJ =  path[0][1]
   taxis[ID][1] = nextI
   taxis[ID][2] = nextJ
   path.pop(0)
   taxis[ID][4] = path
   taxis[ID][7].append([nextI,nextJ]) #add current pos to history
   carJam(ID)
      


def move(ID,i,j):
   global taxis
   taxis[ID][1] = i
   taxis[ID][2] = j
   taxis[ID][7].append([i,j]) #add current pos to history
   carJam(ID)
   
#**** move taxi in state pasear ******

def pasearTaxi(ID):
   global taxis
   
   taxi = taxis[ID]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   path = taxi[4]
   history = taxi[7]
   
   if(len(path) >0):#in the middle of a not trivial move
      advancePath(ID)

   else:

      posBlank = nextBlank(ID) # structure: [i,j]
      i = taxi[1]
      j = taxi[2]
      
      left = mapa[i][j-1]
      right = mapa[i][j+1]
      up = mapa[i-1][j]
      down = mapa[i+1][j]
      
      # quick search at adjacent spaces
      if(right == " " and not inHistory(i,j+1,history)):
         move(ID,i,j+1)
      elif(down == " " and not inHistory(i+1,j,history)):
         move(ID,i+1,j)
      elif(left == " " and not inHistory(i,j-1,history)):
         move(ID,i,j-1)
      elif(up == " " and not inHistory(i-1,j,history)):
         move(ID,i-1,j)

      # long walk over visited spaces
      elif(posBlank != []): #unvisited space
         taxis[ID][4] = Astar(i,j,posBlank[0],posBlank[1]) #sets path
         advancePath(ID)
   


#****** search for new client *******

def searchClient(ID):
   global taxis
   global clients
   global blockList
   global homeBuildings
   global workBuildings
   
   taxi = taxis[ID]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   i=0
   closestClient = []
   distance = 1000000
   clientID = -1
   while(i<len(clients)):
      client = clients[i]
      #structure of client: [home,work,start working time, inHome, taxiCalled,outOfWork]
      if(not client[4]):#client have not ask for a taxi
         taxiI=taxi[1]
         taxiJ=taxi[2]
         block = blockList[client[0]] #[i,j]
         d2 = abs(taxiI - block[0])+abs(taxiJ - block[1])
         if(distance > d2):#closest client
            closestClient = client
            distance = d2
            clientID = i
      i+=1
      
   if(closestClient != []):
      block = blockList[closestClient[0]] #[i,j]
      taxis[ID][4] = Astar(taxis[ID][1],taxis[ID][2],block[0]+2,block[1]) #path
      taxis[ID][8] = clientID
      clients[clientID][4] = True #client called a taxi


#** pick up client at home or work **

def pickUpClient(ID):
   global clients
   global taxis
   global blockList
   
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
   #structure of client: [home,work,start working time, taxiCalled,outOfWork]
   taxi = taxis[ID]
   clients[taxi[8]][3] = False #client not longer in home
   client = clients[taxi[8]]
   removePersonInBlock(client[0])
   block = blockList[client[1]]
   taxis[ID][4] = Astar(taxi[1],taxi[2],block[0]+2,block[1])#set new path


#*** leave client at home or work ***

def leaveClient(ID):
   global clients
   client = clients[ID]
   #structure of client: [home,work,start working time, inHome, taxiCalled,outOfWork]
   addPersonInBlock(client[1])
   
   


#******* taxis state machine ********

def moveTaxis():
   global taxis
   global clients

   i=0
   while(i<len(taxis)):
      taxi = taxis[i]
      #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
      state = taxi[3]
      path = taxi[4]
      clientID = taxi[8]
      wait = taxi[9]

      if(wait>0):
         taxis[i][9]-= 1

      else:

         if(state == "parquear"):
            if(len(path)>0):
               advancePath(i)
               
         if(state == "pasear"):
            pasearTaxi(i)
            
         if(state == "buscar"):
            
            if(clientID != -1):
               if(len(path)>0):
                  advancePath(i)
               else:
                  #either pick up or leave client
                  client = clients[taxi[8]]
                  #structure of client: [home,work,start working time, inHome, taxiCalled,outOfWork]
                  if(client[3]):
                     pickUpClient(i)
                  else:
                     leaveClient(clientID)
                     taxis[i][8] = -1
            else:
               searchClient(i)
            
            

        

      i+=1





#** Define a function for the thread ************************************************************************
def threadFunction( threadName):
   global delay
   global mapa
   i = 0
   while True:
      time.sleep(0.1)
      if(delay != 0): 
         if(i*0.1>delay):
            decreaseJams()
            moveTaxis()
            rePaint()
            i=0
         else:
            i=i+1
         
         

#******** Create new thread **********
try:
   thread.start_new_thread( threadFunction, ("Thread-1", ) )
except:
   print("Error: unable to start thread")





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



#******** create N taxis *************

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
            
      state = "parquear" #initial state
      path=[]
      history = [[posI,posJ]]
      taxis.append([names[i],posI,posJ,state,path,False,False,history,-1,0])
      #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]
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
      
      clients.append([home,work,0,True,False,False])
      #structure of client: [home,work,start working time, inHome, taxiCalled,outOfWork]
      i+=1
      

#******** change taxi state **********

def changeTaxiState(state,i):
   global taxis
   taxis[i][3] = state #change state
   taxis[i][4] = [] #reset path



#******* resets taxi history *********
   
def clearTaxiHistory(i):
   global taxis
   taxis[i][7] = [] #erase history of moves

   

#***** sets taxi path to block *******
def pathToBlock(i,num):
   global taxis
   global blockList
   block = blockList[num] #structure of block: [i,j]
   #find new path, parking in the bottom of the building
   taxis[i][4] = Astar(taxis[i][1],taxis[i][2],block[0]+2,block[1]) 
   


#******* commands of one taxi ********

def taxiAction(words):
   global taxis
   global blockList
   i=0
   name = words[0]
   #structure of taxi: [name,I,J,state,path,mostrar,ruta,history of moves,clientID,waitingTime]

   
   
   while(i<len(taxis)):
      if(taxis[i][0] == name):
         if(len(words) == 2):
            if(words[1] == "pasear"):
               changeTaxiState(words[1],i)
               print("state=pasear para taxi "+taxis[i][0])
               return True
            elif(words[1] == "buscar"):
               changeTaxiState(words[1],i)
               print("state=buscar para taxi "+taxis[i][0])
               return True
            elif(words[1] == "clear"):
               clearTaxiHistory(i)
               print("historial borrado para taxi "+taxis[i][0])
               return True
            else:
               return False
            
         elif(len(words) == 3):
            if(words[1] == "parquear"):
               
               changeTaxiState(words[1],i)
               num = int(words[2])
               if(num <len(blockList)):
                  pathToBlock(i,num)
                  print("state=parquear para taxi "+taxis[i][0]+ " hacia cuadra "+words[2])
                  return True
               
            elif(words[1] == "mostrar"):
               if(words[2] == "on"):
                  print("mostrar ON para taxi "+taxis[i][0])
                  taxis[i][5] = True
                  return True
               elif(words[2] == "off"):
                  print("mostrar OFF para taxi "+taxis[i][0])
                  taxis[i][5] = False
                  return True
            elif(words[1] == "ruta"):
               if(words[2] == "on"):
                  print("ruta ON para taxi "+taxis[i][0])
                  taxis[i][6] = True
                  return True
               elif(words[2] == "off"):
                  print("ruta OFF para taxi "+taxis[i][0])
                  taxis[i][6] = False
                  return True
               
            else:
               return False
            
      i+=1
         
   return False
      



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

   if(words[0] == "animar" and len(words)==2):
      n = int(words[1])
      delay = n/1000
      print("animando a "+str(n)+" ms")
      
   elif(words[0] == "clientes" and len(words)==2):
      n = int(words[1])
      addClients(n)
      print("creados "+str(n)+" clientes")
      
   elif(words[0] == "cliente" and len(words)==3):
      home = int(words[1])
      work = int(words[2])
      if(validHome(home) and validWorkPlace(work)):
         clients.append([home,work,0,True,False,False])
         #structure of client: [home,work,start working time, inHome, taxiCalled,outOfWork]
         homeBuildings[getHome(home)][1] += 1 #at one person to that building
         print("cliente agregado con home: "+str(home)+" y work: "+str(work))
      else:
         print("error invalid blockID for home or work")
      
   elif(words[0] == "taxis" and len(words)==2):
      n = int(words[1])
      hireTaxis(n)
      print("contratados "+str(n)+" taxis")

   elif(words[0] == "personas" and len(words)==2):
      if(words[1]=="on"):
         showPeople = True
         print("personas on")
      elif(words[1]=="off"):
         showPeople = False
         print("personas off")
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
      if(not taxiAction(words)):
         print("error comando incorrecto")
      
   else:
      print("error, comando incorrecto")

   
   
     
   
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
