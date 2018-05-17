#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time, serial, csv
import sys, glob, qdarkstyle
import thread
##########################################################
plotLen =  500#Numero de Muestras totales
threshold = 50
ksamples = 50
scale = 200
msamples = plotLen/ksamples
geophone = "Out"
uData=['---.--','---.--','---.--','---.--','---.--','---.--','---.--','---.--','---.--']
uDatat =[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
tData = []
pData = []
row = 0
rowsTotal = 2000
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
                      baudrate=115200, 
                      timeout=0.1)
# plot array
def matrixInit():
    global pData
    pData = []
    for i in range(8):
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
fig2.setLabel(axis="bottom",text="Esfuerzo",units="kg")
fig2.setLabel(axis="left",text="Desplazamiento",units="mm")
fig2.setLabel(axis="top",text='<span style="color: #FFF; font-size: 12pt;">Deformacion vs Esfuerzo</span>')
fig2.setLabel(axis="right",text='-')
fig2.setYRange(-10.0,10.0);
fig2.showGrid(x=True, y=True)

curve1 = fig2.plot(pen='g',name="M1")
curve2 = fig2.plot(pen='g',name="M2")
curve3 = fig2.plot(pen='g',name="M3")
curve4 = fig2.plot(pen='g',name="M4")
curve5 = fig2.plot(pen='g',name="M5")
curve6 = fig2.plot(pen='g',name="M6")
curve6 = fig2.plot(pen='g',name="M7")
curve6 = fig2.plot(pen='g',name="M8")

curve1.setData(pData[0])
curve2.setData(pData[1])
curve3.setData(pData[2])
curve4.setData(pData[3])
curve5.setData(pData[4])
curve6.setData(pData[5])
curve6.setData(pData[6])
curve6.setData(pData[7])

textMax = pg.TextItem(html='<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">Presione Inicio</span></div>', anchor=(-0.3,1), angle=0, fill=(0, 0, 255, 100))
fig2.addItem(textMax)

tab1 = pg.TableWidget()
items = ["M1(mm)","M2(mm)","M3(mm)","M4(mm)","M5(mm)","M6(mm)","M7(mm)","M8(mm)","Fx(Kg)"] 
tab1.setRowCount(rowsTotal)
tab1.setColumnCount(9)

tab1.setHorizontalHeaderLabels(items)

softlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FFF; font-size: 14pt;">Ensayo de Compresion Axial y Diagonal</span></div>')
loadlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Esfuerzo: %s T</span></div>'%(uData[8]))
microlabel = QtGui.QLabel('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Deformaciones: M1: %s, M2: %s, M3: %s, M4: %s, M5: %s, M6: %s, M7: %s, M8: %s</span></div>'%(uData[0],uData[1],uData[2],uData[3],uData[4],uData[5],uData[6],uData[7]))

portlabel = QtGui.QLabel("Puerto:")
geolabel = QtGui.QLabel("Geofono:")
spelabel = QtGui.QLabel("Frec.:")
thruDatatesLabel = QtGui.QLabel("Humbral:")
thresEdit = QtGui.QLineEdit(str(threshold))
timeLabel = QtGui.QLabel("Duracion: 10ms")

rstBtn = QtGui.QPushButton('Reset')
tareBtn = QtGui.QPushButton('Tare')
strstpBtn = QtGui.QPushButton('Inicio/Pausa')
saveBtn = QtGui.QPushButton('Guardar')
exitBtn = QtGui.QPushButton('Salir')

speedSel = QtGui.QComboBox()
speedSel.addItem('50KHz')
speedSel.addItem('25KHz')
speedSel.addItem('10KHz')
speedSel.addItem('5KHz')
#speedSel.addItem('1KHz')

geoSel = QtGui.QComboBox()
geoSel.addItem('Llegada')
geoSel.addItem('Salida')

portSel = QtGui.QComboBox()
for port in serialPorts:
    portSel.addItem(port)


softlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
loadlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
microlabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
portlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)


thresEdit.setMaxLength(3)
thresEdit.setMaximumSize(QtCore.QSize(0.1 * thresEdit.width(),thresEdit.height()))
speedSel.setMaximumSize(QtCore.QSize(0.1 * speedSel.width(),speedSel.height()))


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
win1.addWidget(portlabel,col=0)
win1.addWidget(portSel,col=1)
win1.addWidget(tareBtn,col=2)
win1.addWidget(rstBtn,col=3)
win1.addWidget(strstpBtn,col=11)
win1.addWidget(saveBtn,col=12)
win1.addWidget(exitBtn,col=13)

def changeThreshold():
    global threshold
    threshold = int(thresEdit.text())

def startstop():
    global flagLog
    flagLog = not(flagLog)
    if flagLog:
        textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">...Grabando</span></div>')
    else:
        textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">...Pausa</span></div>')

def reset():
    global row,tData,pData
    matrixInit()
    textMax.setHtml('<div style="text-align: center;"><span style="color: #FF0; font-size: 12pt;">Presione Inicio</span></div>')
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
    while True:
        try:
            outPut = cPort.readline()
            if "," in outPut:
                outPut = outPut.replace('\r\n','')
                outPut = outPut.split(',')
                if len(outPut)==9:
                    for z in range(len(outPut)):
                        if outPut[z] == '999.99':
                            outPut[z] = '---.--'
                            uData[z]=0.0
                        else:
                            uData[z]=float(outPut[z])
                            outPut[z] = "%2.2f"%(float(outPut[z])-uDatat[z])
                    print "",outPut[8]
                    outPut[8]="%2.1f"%(float(outPut[8])/scale)
                    microlabel.setText('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Deformaciones: M1: %s, M2: %s, M3: %s, M4: %s, M5: %s, M6: %s, M7: %s, M8: %s</span></div>'%(outPut[0],outPut[1],outPut[2],outPut[3],outPut[4],outPut[5],outPut[6],outPut[7]))
                    loadlabel.setText('<div style="text-align: center;"><span style="color: #FF0; font-size: 16pt;">Esfuerzo: %s T</span></div>'%outPut[8])            
                    if flagLog:
                        for z in range(len(outPut)):
                            newdata = QtGui.QTableWidgetItem()
                            newdata.setText(outPut[z])
                            tab1.setItem(row,z,newdata)
                            if z<8:
                                pData[z].remove(pData[z][0])
                                pData[z].append(uData[z]-uDatat[z])
                        curve1.setData(pData[0])
                        curve2.setData(pData[1])
                        curve3.setData(pData[2])
                        curve4.setData(pData[3])
                        curve5.setData(pData[4])
                        curve6.setData(pData[5])
                        curve6.setData(pData[6])
                        curve6.setData(pData[7])
                        
                        tData.append(outPut)
                        row = row+1
        except:
            time.sleep(1)
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
            
            writer.writerow(['M1(mm)','M2(mm)','M3(mm)','M4(mm)','M5(mm)','M6(mm)','M7(mm)','M8(mm)','Fx(Kg)'])
            for myrow in tData:
                rawdata = [myrow[0],myrow[1],myrow[2],myrow[3],myrow[4],myrow[5],myrow[6],myrow[7],myrow[8]]
                writer.writerow(rawdata)


def portsel():
    global cPort
    serialPort = str(portSel.currentText())
    print "SerialPort:", serialPort
    try:
        cPort.close()
    except:
        pass

    cPort = serial.Serial(port=serialPort,
                  baudrate=115200, 
                  timeout=.1)
    cPort.flushInput()
    cPort.flushOutput()

def exit():
    app.quit()



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

