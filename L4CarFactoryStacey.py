#Name:Erin Stacey
# Class: Concurrency
# Lab: Condition Variables for Selective Waiting
# Make a production line for a automobile production facilty
import threading
import time 
carCounter = 0
#Buffers and printsafe
def printsafe(part,num):
   
   safePrintLock = threading.Lock()
   with safePrintLock:
       if part == "fab1pro":
           return print("Fab1 produced Car"+str(num)+"\n")
       elif part == "fab1sent":
           return print("Fab1 sent Car"+str(num)+" to painting queue\n")
       elif part == "fab2pro":
           print("Fab2 produced Car"+str(num)+ "\n")
           return
       elif part == "fab2sent":
           print("Fab2 sent Car"+str(num)+" to painting queue\n")
           return
       elif part == "paintsent":
           print("Painting sent Car" + str(num) +" to Finishing\n")
           return
       elif part == "paintBufferFull":
           print("Painting queue full!!!!!!!")
           return
       elif part == "finishingfull":
         print("Finsihing queue full\n")
         return
       elif part == "paintBufferRec":
           print("Painting queue received Car" +str(num)+"\n")
           return
       elif part == "finishrec":
         print("Finishing received Car"+str(num)+"\n")
         return 
       elif part == "finishsent":
         print("Finishing sent Car"+str(num)+" to Completed\n")
         return
       elif part == "Car":
          print("Car" + str(num) + " Completed!!!\n")
          return 
      
       else:
          pass

class PaintBuffer(object):
   """
   Paint car buffer section.

   """
   def __init__(self):
      
      self.count = 0
      self.buffer = []
      self.max = 4
      self.condition = threading.Condition()
   def place(self,item):
    with self.condition:
       
       while(self.count == self.max):
          print("Painting queue full!!!!!!!")
          self.condition.wait()
       self.buffer.append(item)
       self.count+=1
       self.condition.notify_all()
       printsafe("paintBufferRec",item)
   def take(self):
     with self.condition:
        while(self.count == 0 or len(self.buffer) == 0):
           print("wait Paint buffer")
           self.condition.wait()
        item=self.buffer.pop()
        self.count-=1
        self.condition.notify_all()
        return item


class FinishingBuffer(object):
   """
     Finishing line for cars that are finished.
   """
   def __init__(self):
      self.buffer = []
      self.Max = 4
      self.counttwo = 0
      self.condition = threading.Condition()
   def place(self,item):
      
      
      with self.condition:
         
        while(self.counttwo >= self.Max):
           
           printsafe("finishingfull",0)
           self.condition.wait()
        self.buffer.append(item)
      
        self.counttwo+=1
        self.condition.notify_all()
   def take(self):
      with self.condition:
        
        while(self.counttwo == 0 or len(self.buffer)== 0):
          print("FinishBufferWaitTake")
          self.condition.wait()
        item=self.buffer.pop()
        self.counttwo-=1
        self.condition.notify_all()
        return item
        

          

condition = threading.Condition()
p = PaintBuffer()
f = FinishingBuffer()

#thread functions completed,finish,painting,fab1,and fab2


def completed(num):
  """
Gives the print statment of the car that was completed.
"""
  printsafe("Car",num)
 
def finish():
    """
   Sends the car to Finishing Buffer.
   """
    for i in range(1,21):
      num = f.take()
    
      printsafe("finishrec",num)
    
      printsafe("finishsent",num)
      
      
      
      completed(num)
    print("Done.")
    

def painting():
   """
   Sends the car to Painting Buffer.
   """
   for i in range(1,21):
      
      num = p.take()
      
      f.place(num)
     
      
      
      printsafe("paintsent",num)

def fab1():
   """
    Sends ten cars to the painting function.

   """
  
   global p
   global carCounter
   #printing number of times 
   for i in range(1,11):
      
      carCounter+=1
      p.place(carCounter)
      
      printsafe("fab1pro",carCounter)
      printsafe("fab1sent",carCounter)
      
    
      
          
      

def fab2():
     """
       Sends ten cars to the painting function.

     """
     global p
     global carCounter
   
     for i in range(1,11):
     
      
    
      
       carCounter+=1
     
       p.place(carCounter)
       printsafe("fab2pro",carCounter)

       printsafe("fab2sent",carCounter)
    
     
      
      



    
t1 = threading.Thread(target=fab1)
t2 = threading.Thread(target=fab2)
t3 = threading.Thread(target=painting)
t4 = threading.Thread(target=finish)
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()



