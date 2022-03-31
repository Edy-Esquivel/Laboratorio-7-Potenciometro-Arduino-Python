from pyqtgraph.Qt import QtGui, QtCore 
import pyqtgraph as pg 
from pyfirmata import Arduino, util 
import time 
import os
 
port = '/dev/cu.usbmodem2201' 
board = Arduino(port) 
Led1 = board.digital[13]
                                         
it = util.Iterator(board) 
it.start() 

app = QtGui.QApplication([]) 
win = pg.GraphicsWindow(title='Medición en tiempo Real - INCISO 2 y 3 - Laboratorio 7') 
win.setBackground('bisque')
p = win.addPlot(title='Gráfica en tiempo real de 0 - 5 Voltios en variación de Potenciometro' )
curva = p.plot(pen = 'r') 
os.system("clear")
print ("")
print ("Conectado a Tarjeta Arduino")
print ("")
 
p.setRange(yRange=[0,5]) 
dataX = [] 
dataY = [] 
lastY=0 
 
analog0=board.get_pin('a:0:i') 
 
def Update(): 
    global curva, dataX, dataY, lastY, nuevoDato 
     
    dato = analog0.read() 
    if dato is not None: 
       nuevoDato = dato*5
       print ("Potenciometro: ", nuevoDato," Voltios") 
       time.sleep(.5) 
       
    else: 
        nuevoDato=0 
         
    dataX.append (nuevoDato) 
    dataY.append (lastY) 
    lastY+=1 
    
     
    if len(dataX)>200: 
        os.system("clear")
        print ("")
        print ("Simulación ha finalizado")
        print ("")
        print ("------------------------------------")
        print ("Se procederá a finalizar el programa")
        print ("------------------------------------")
        print ("")
        print ("")
        Led1.write(0)
        time.sleep(3)  
        pg. QtGui. Application.exec_() 
        board.exit()
        os.system("clear")
    if nuevoDato >= 4.97:
        win = pg.GraphicsWindow(title='ALERTA DE LIMITE ALCANZADO') 
        p = win.addPlot(title='HAZ LLEGADO AL 100% PERMITIDO, DEBES DISMINUIR')
        win.setBackground('red')
        print('ALERTA DE PORCENTAJE Alcanzado')   

        Led1.write(1)
        time.sleep(0.5)
        Led1.write(0)
        time.sleep(0.5)
        
     
    curva.setData(dataY, dataX) 
    QtGui.QApplication.processEvents() 
     
try: 
    while True: Update() 
     
except KeyboardInterrupt: 
    pg. QtGui. Application.exec_() 
    board.exit()