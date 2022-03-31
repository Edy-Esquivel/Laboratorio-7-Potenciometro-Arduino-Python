from webbrowser import BackgroundBrowser
from pyqtgraph.Qt import QtGui, QtCore 
import pyqtgraph as pg 
from pyfirmata import Arduino, util 
import time 
import os
import tkinter
from tkinter import messagebox
 
port = '/dev/cu.usbmodem2201' 
board = Arduino(port) 
Led1 = board.digital[13]
                                         
it = util.Iterator(board) 
it.start() 

#ventana = tkinter.Tk()
#ventana.geometry("640x480")
app = QtGui.QApplication([]) 
win = pg.GraphicsWindow(title='Medición en tiempo Real- INCISO 2 - Laboratorio 7') 
win.setBackground('white')
p = win.addPlot(title='Gráfica en tiempo real de Valor de Potenciometro de 0-50-100 %' )
curva = p.plot(pen = 'r') 
os.system("clear")
print ("")
print ("Conectado a Tarjeta Arduino")
print ("")
 
p.setRange(yRange=[0,100]) 
dataX = [] 
dataY = [] 
lastY=0 
 
analog0=board.get_pin('a:0:i') 
 
def Update(): 
    global curva, dataX, dataY, lastY, nuevoDato 
     
    dato = analog0.read() 
    if dato is not None: 
       nuevoDato = dato*100
       print (nuevoDato,"%") 
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
    if nuevoDato > 50:
            win = pg.GraphicsWindow(title='ALERTA DE PORCENTAJE SOBRE LIMITADO') 
            p = win.addPlot(title='HAZ SOBREPASADO EL 50% PERMITIDO')
            win.setBackground('red')
            print('ALERTA DE PORCENTAJE SOBRE LIMITADO')            
            Led1.write(1)
    else:
            Led1.write(0)
     
    curva.setData(dataY, dataX) 
    QtGui.QApplication.processEvents() 
     
try: 
    while True: Update() 
     
except KeyboardInterrupt: 
    pg. QtGui. Application.exec_() 
    board.exit()