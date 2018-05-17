#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time, serial, csv
import sys, glob, qdarkstyle
import thread
##########################################################
scale = 219.3310    #Escala para Kg
plotLen =  500		#Numero de Muestras totales
threshold = 50
ksamples = 50
msamples = plotLen/ksamples
geophone = "Out"
uData=['---.--','---.--','---.--','---.--','---.--','---.--','---.--']
uDatat =[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
tData = []
pData = []
M1=[0,0.01]
C1=[0,0]
row = 0
plotType=0
##########################################################

flagLog = False

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            print "SerialPort:", port
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
        #except:
            pass
    return result

serialPorts = serial_ports()

if len(serialPorts)>=1:
    serialPort=serialPorts[0]
    print "SerialPort:", serialPort
    cPort = serial.Serial(port=serialPort,
                      baudrate=9600, 
                      timeout=0.1)
# plot array
def matrixInit():
    global pData, M1, C1
    M1 = [0,0.1]
    C1 = [0,0]
    pData = []
    for i in range(6):
        pData.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

matrixInit()


#############################
# Grapichs Layout
#############################
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())

win.setWindowTitle('Compresion Axial y Diagonal')
pg.setConfigOptions(antialias=True)

#############################
# Layout
win1 = pg.LayoutWidget()
win.setCentralWidget(win1)

fig2 = pg.PlotWidget(title='<div style="text-align: center;"><span style="color: #FFF; font-size: 13pt;">Micrometros</span></div>')
fig2.setLabel(axis="left",text="Deformaciones",units="mm")
fig2.setLabel(axis="bottom",text="Tiempo",units="s")
fig2.setLabel(axis="top",text='<span style="color: #FFF; font-size: 12pt;">Deformacion vs Tiempo</span>')
fig2.setLabel(axis="right",text='-')
fig2.setYRange(-10.0,10.0);
fig2.showGrid(x=True, y=True)
fig2.addLegend()


curve1 = fig2.plot(pen=(  0,240,20),name="M1")
curve2 = fig2.plot(pen=( 40,200,20),name="M2")
curve3 = fig2.plot(pen=( 80,160,20),name="M3")
curve4 = fig2.plot(pen=(120,120,20),name="M4")
curve5 = fig2.plot(pen=(160, 80,20),name="M5")
curve6 = fig2.plot(pen=(200, 40,20),name="M6")

curve1.setData(pData[0])
curve2.setData(pData[1])
curve3.setData(pData[2])
curve4.setData(pData[3])
curve5.setData(pData[4])
curve6.setData(pData[5])


textMax = pg.TextItem(html='<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">Presione Inicio</span></div>', anchor=(-0.3,1), angle=0, fill=(0, 0, 255, 100))
fig2.addItem(textMax)

tab1 = pg.TableWidget()
items = ["M1(mm)","M2(mm)","M3(mm)","M4(mm)","M5(mm)","M6(mm)","Fx(Kg)"] 
tab1.setRowCount(1000)
tab1.setColumnCount(7)

tab1.setHorizontalHeaderLabels(items)

softlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FFF; font-size: 14pt;">Ensayo de Compresion Axial y Diagonal</span></div>')
loadlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Carga: %s Kg</span></div>'%(uData[6]))
microlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Deformaciones: M1: %s, M2: %s, M3: %s, M4: %s, M5: %s, M6: %s,</span></div>'%(uData[0],uData[1],uData[2],uData[3],uData[4],uData[5]))


plotBtn = QtGui.QPushButton('Plot') 

portlabel = QtGui.QLabel("Puerto:")
portSel = QtGui.QComboBox()
for port in serialPorts:
    portSel.addItem(port)

rstBtn = QtGui.QPushButton('Reset')
tareBtn = QtGui.QPushButton('Tare')
strstpBtn = QtGui.QPushButton('Inicio/Pausa')
saveBtn = QtGui.QPushButton('Guardar')
exitBtn = QtGui.QPushButton('Salir')



softlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
loadlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
microlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
portlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

win.showFullScreen()
win1.addWidget(softlabel,0,0,1,14)
win1.nextRow()
win1.addWidget(loadlabel,1,0,1,14)
win1.nextRow()
win1.addWidget(microlabel,2,0,1,14)
win1.nextRow()
win1.addWidget(fig2,3,0,1,7)
win1.addWidget(tab1,3,7,1,7)
win1.nextRow()
win1.addWidget(plotBtn,col=0)
win1.addWidget(portlabel,col=3)
win1.addWidget(portSel,col=4)
win1.addWidget(tareBtn,col=5)
win1.addWidget(rstBtn,col=6)
win1.addWidget(strstpBtn,col=11)
win1.addWidget(saveBtn,col=12)
win1.addWidget(exitBtn,col=13)

def plotEvsD():
    fig2.setTitle(title='<div style="text-align: center;"><span style="color: #FFF; font-size: 13pt;">Carga vs Micrometro M1</span></div>')
    fig2.setLabel(axis="left",text="Esfuerzo",units="Kg")
    fig2.setLabel(axis="bottom",text="Deformacion",units="mm")
    fig2.setLabel(axis="top",text='<span style="color: #FFF; font-size: 12pt;">Esfuerzo vs Deformacion</span>')
    fig2.setLabel(axis="right",text='-')
    fig2.setYRange(-10.0,10.0);
    fig2.showGrid(x=True, y=True)
    
    #curve1 = fig2.plot(pen='g',name="M1")
    curve1.setData(M1,C1)
    curve2.clear()
    curve3.clear()
    curve4.clear()
    curve5.clear()
    curve6.clear()
    

def plotDvsT():
    fig2.setTitle(title='<div style="text-align: center;"><span style="color: #FFF; font-size: 13pt;">Micrometros M1 - M6</span></div>')
    fig2.setLabel(axis="left",text="Deformaciones",units="mm")
    fig2.setLabel(axis="bottom",text="Tiempo",units="s")
    fig2.setLabel(axis="top",text='<span style="color: #FFF; font-size: 12pt;">Deformacion vs Tiempo</span>')
    fig2.setLabel(axis="right",ntext='-')
    fig2.setYRange(-10.0,10.0);
    fig2.showGrid(x=True, y=True)
    #curve1 = fig2.plot(pen='g',name="M1")
    curve2 = fig2.plot(pen=( 40,200,20),name="M2")
    curve3 = fig2.plot(pen=( 80,160,20),name="M3")
    curve4 = fig2.plot(pen=(120,120,20),name="M4")
    curve5 = fig2.plot(pen=(160, 80,20),name="M5")
    curve6 = fig2.plot(pen=(200, 40,20),name="M6")
    curve1.setData(pData[0])
    curve2.setData(pData[1])
    curve3.setData(pData[2])
    curve4.setData(pData[3])
    curve5.setData(pData[4])
    curve6.setData(pData[5])
                        

def plotChanger():
    global plotType
    print plotType
    
    plotType = plotType + 1
    if plotType>1:
        plotType=0

    if plotType==0:
        plotDvsT()

    if plotType==1:
        plotEvsD()


def startstop():
    global flagLog
    flagLog = not(flagLog)
    if flagLog:
        textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">...Grabando</span></div>')
    else:
        textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">...Pausa</span></div>')

def reset():
    global row,tData,pData,flagLog
    matrixInit()
    #if flagLog:
    #    textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">Presione Inicio</span></div>')
    tab1.clearContents()
    tData = []
    row=0

def tare():
    global uData,uDatat
    for z in range(len(uData)):
        uDatat[z] = uData[z]

def getData():
    global cPort, threshold
    global tData,uDatat,uData,row
    global plotType, flagLog
    global C1,M1
    while True:
        try:
            outPut = cPort.readline()
            if "," in outPut:
                outPut = outPut.replace('\r\n','')
                outPut = outPut.split(',')
                if len(outPut)==7:
                    for z in range(len(outPut)):
                        if outPut[z] == '999.99':
                            outPut[z] = '---.--'
                            uData[z]=0.0
                        else:
                            uData[z]=float(outPut[z])
                            outPut[z] = "%2.2f"%(float(outPut[z])-uDatat[z])
                    outPut[6]="%2.1f"%(float(outPut[6])/scale)
                    microlabel.setText('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Deformaciones: M1: %s, M2: %s, M3: %s, M4: %s, M5: %s, M6: %s,</span></div>'%(outPut[0],outPut[1],outPut[2],outPut[3],outPut[4],outPut[5]))
                    loadlabel.setText('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Carga: %s Kg</span></div>'%outPut[6])            
                    
                    if flagLog:
                        M1.append(uData[0])
                        C1.append(float(outPut[6]))
                        for z in range(len(outPut)):
                            newdata = QtGui.QTableWidgetItem()
                            newdata.setText(outPut[z])
                            tab1.setItem(row,z,newdata)
                            if z<6:
                                pData[z].remove(pData[z][0])
                                pData[z].append(uData[z]-uDatat[z])
                        
                        if plotType==0:
                            curve1.setData(pData[0])
                            curve2.setData(pData[1])
                            curve3.setData(pData[2])
                            curve4.setData(pData[3])
                            curve5.setData(pData[4])
                            curve6.setData(pData[5])
                        
                        if plotType==1:
                            curve1.setData(M1,C1)
                            
                        tData.append(outPut)
                        row = row+1
        except:
            time.sleep(10)
            pass


def savecsv(self):
    path = QtGui.QFileDialog.getSaveFileName(
        parent = None, 
        caption='Guardar Archivo', 
        directory='', 
        filter='CSV(*.csv)')
    datetime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    if not path.isEmpty():

        with open(unicode(path.append('_%s.csv'%datetime)), 'wb') as stream:
            writer = csv.writer(stream)
            writer.writerow(['Fecha:',time.strftime("%Y/%m/%d", time.localtime())])
            writer.writerow(['Hora:',time.strftime("%H:%M:%S", time.localtime())])
            
            writer.writerow(['M1(mm)','M2(mm)','M3(mm)','M4(mm)','M5(mm)','M6(mm)','Fx(Kg)'])
            for myrow in tData:
                rawdata = [myrow[0],myrow[1],myrow[2],myrow[3],myrow[4],myrow[5],myrow[6]]
                writer.writerow(rawdata)


def portsel():
    global cPort
    serialPort = str(portSel.currentText())
    print "SerialPort:", serialPort
    cPort = serial.Serial(port=serialPort,
                  baudrate=115200, 
                  timeout=.1)
    cPort.flushInput()
    cPort.flushOutput()

def exit():
    app.quit()


plotBtn.clicked.connect(plotChanger)
rstBtn.clicked.connect(reset)    
tareBtn.clicked.connect(tare)    
strstpBtn.clicked.connect(startstop)    
saveBtn.clicked.connect(savecsv)    
exitBtn.clicked.connect(exit)    
portSel.activated[str].connect(portsel)
## Start Qt event loop unless running in interactive mode or using pyside.

thread.start_new_thread( getData, ())
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("windowsvista"))
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

