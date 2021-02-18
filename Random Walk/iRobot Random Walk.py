import numpy as np
from pycreate2 import Create2
import time
import RPi.GPIO as GPIO
from io import open
import datetime


#iRobot and RaspberryPi Configuration
GPIO.setmode(GPIO.BCM) #configuracion BCM de puertos 
#Puerto de comunicacion USB RASP-iRobot e inicio comunicación
port = '/dev/ttyUSB0' 
bot = Create2(port)
bot.start()
bot.full()
#puertos de sensores
BS_L = 20
BS_R = 21
CS = 16
GPIO.setup(CS,GPIO.IN)
GPIO.setup(BS_L,GPIO.IN)
GPIO.setup(BS_R,GPIO.IN)
sensors = bot.get_sensors()
Sizq = GPIO.input(BS_L)
Sder = GPIO.input(BS_R)
Scol = GPIO.input(CS)

def createProbMatrix(N,M,X,Y):
    prob = [1/2, 1/2, 0, 0]
    
    if X in range(1,M-1) and Y in range(1,N-1):
        prob = [0.25,0.25,0.25,0.25] # Default probability 1/4
    # Upper-left corner
    elif X == 0 and Y == M-1 :       
        prob = [0, 1/2, 1/2, 0]
    # Upper-right corner
    elif X == M-1 and Y == N-1:   
        prob = [0, 0, 1/2, 1/2]
    # Lower-right corner
    elif X == M-1 and Y == 0: 
        prob = [1/2, 0, 0, 1/2]
    # Lower-left corner
    elif X == 0 and Y == 0:
        prob = [1/2, 1/2, 0, 0] 
    # Top row
    elif X in range(1,M-1) and Y == N-1:
        prob = [0, 1/3, 1/3, 1/3]    #Can't go NORTH
    # Bottom row
    elif X in range(1,M-1) and Y == 0:
        prob = [1/3, 1/3, 0, 1/3]  #Can't go SOUTH
    # Left column
    elif X == 0 and Y in range(1,M-1):
        prob = [1/3, 1/3, 1/3, 0]    #Can't go WEST
    # Right column
    elif X == M-1 and Y in range(1,M-1):
        prob = [1/3, 0, 1/3, 1/3]  #Can't go EAST
    # Set stopping point in probability matrix
    
    return prob


#aqui se ha recibido la dirección de giro, entonces de acuerdo a ello se definen
#diferentes  movimientos.      
def moveRobot1(Head,Step,BS_L,BS_R,Scol):
    

    
    if Head == 'Norte':
        if Step == 0: 
            bot.drive_direct(-100,-100)
            time.sleep(0.1)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step ==1:
            bot.drive_direct(-100,100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 2:
            bot.drive_direct(100,-100)
            time.sleep(3)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 3:      
            bot.drive_direct(100,-100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
    
    elif Head == 'Sur':
        if Step == 0:
            bot.drive_direct(100,-100)
            time.sleep(3)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 1:
            bot.drive_direct(100,-100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 2:
            bot.drive_direct(-100,-100)
            time.sleep(0.1)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 3:
            bot.drive_direct(-100,100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
   
    elif Head == 'Este':
        if Step == 0:
            bot.drive_direct(100,-100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step ==1:
            bot.drive_direct(-100,-100)
            time.sleep(0.1)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 2:
            bot.drive_direct(-100,100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 3:
            bot.drive_direct(100,-100)
            time.sleep(3)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
   
    elif Head == 'Oeste':
        if Step == 0:
            bot.drive_direct(-100,100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step ==1:
            bot.drive_direct(100,-100)
            time.sleep(3)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 2:
            bot.drive_direct(100,-100)
            time.sleep(1.50)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
        elif Step == 3:
            bot.drive_direct(-100,-100)
            time.sleep(0.1)
            bot.drive_stop()
            time.sleep(1)
            hs = 0
    
    time.sleep(1)
    return hs 


def Seguidor(BS_L,BS_R,Scol,hs):
    print("seguidor")
    DataS = GPIO.input(Scol)
    Sizq = GPIO.input(BS_L)
    Sder = GPIO.input(BS_R)
    while ((Sizq == 0 and Sder == 0) or (Sizq == 0 and Sder == 1) or (Sizq == 1 and Sder == 0)) and DataS == 0:               
        DataS = GPIO.input(Scol)
        Sizq = GPIO.input(BS_L)
        Sder = GPIO.input(BS_R)
        
        if Sizq == 0 and Sder == 0:
            bot.drive_direct(-100,-100)
            time.sleep(0.1)
                
        elif Sizq == 0 and Sder == 1:      
            bot.drive_direct(-100,100)
            time.sleep(0.1)
            
        elif Sizq == 1 and Sder == 0:
            bot.drive_direct(100,-100)
            time.sleep(0.1)
    if DataS == 1:
        DataS = 1
    bot.drive_direct(-120,-100)
    time.sleep(1.5) 



    return DataS

def Heading(ns):
    print("llego a heading")
    if ns == 2:
        Head = 'Sur'
    elif ns == 0:
        Head = 'Norte'
    elif ns == 1:
        Head = 'Este'
    elif ns == 3:
        Head = 'Oeste'
    return Head

#---------------------------------- MAIN CODE -------------------------------------------------   
def main():
    # Square 
    M = 4
    N = 4
    #first position
    Head = 'Norte'
    hs = 0
    #repetitions 
    repeat = 1  
    # Number of steps since starting
    num_steps = 0 
    # Starting Location
    X = 0 
    Y = 0
    #sensor and TXT
    DataS = GPIO.input(CS)
    sensors = bot.get_sensors()
    bate = sensors.battery_charge
    Datos_I = open("RW_R4002_32.txt","w")
    Path_list = open("Path_Final.txt","w")
    while repeat != 0:  
        while DataS == 0:
            print("X= " + str(X) + "Y= " + str(Y))
            # Run the random walk until arrival to goal 
            probM = createProbMatrix(N,M,X,Y)
            next_step = np.random.choice(4,1,p = probM)
            print("Head= " + str(Head))    
            print("hs= " + str(hs))
            print("Step= " + str(next_step))
            sensors = bot.get_sensors()
            bate = sensors.battery_charge 
            vol = sensors.voltage
            cur = sensors.current
            num_steps += 1
            Hora = datetime.datetime.now()
            Datos_I.write(str(Hora) + " " + str(bate) + " " + str(vol) + " " + str(cur)+ " " + str(num_steps) + "\n") 
            Path_list.write(str(X) + " " + str(Y) + " " + str(num_steps) + "\n" )
                       
            if next_step == 0:                  # Go North
                Y+=1
                hs = moveRobot1(Head,next_step,BS_L,BS_R,CS)  
            elif next_step == 1:                # Go East
                X+=1
                hs = moveRobot1(Head,next_step,BS_L,BS_R,CS)
            elif next_step == 2:                # Go south
                Y-=1
                hs = moveRobot1(Head,next_step,BS_L,BS_R,CS)
            elif next_step == 3:                # Go West
                X-=1
                hs = moveRobot1(Head,next_step,BS_L,BS_R,CS)
            Head = Heading(next_step)
                
            print("Head= " + str(Head))    
            print("hs= " + str(hs))
            DataS = Seguidor(BS_L, BS_R, CS, hs)    
            #Guardamos información
        sensors = bot.get_sensors()
        bate = sensors.battery_charge 
        vol = sensors.voltage
        cur = sensors.current
        num_steps += 1
        Hora = datetime.datetime.now()
        Datos_I.write(str(Hora) + " " + str(bate) + " " + str(vol) + " " + str(cur) + " " + str(num_steps) + "\n") 
        Path_list.write(str(X) + " " + str(Y) + " " + str(num_steps) + "\n" )
        Datos_I.close()
        Path_list.close()         
        bot.stop()
        bot.close()



#---------------------------------- Start Up -------------------------------------------------   
main()
   

        
    
 
 