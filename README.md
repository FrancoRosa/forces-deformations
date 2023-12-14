# Forces & Deformation Datalogger

This device is built upon the BluePill (STM32F103), an Arduino-like microcontroller board. It collects data from six Mitutoyo micrometers and a load cell to perform analyses related to forces and deformations.

## Instrucciones
El software esta realizado con Python, que es una plataforma de uso libre, de la misma manera el software se provee con esa misma filosofia, que permite a los usuarios hacer las modificaciones que quieran y les dá libertad de compartir el programa

Instrucciones de instalacion en  Windows:

- Instalar python-2.7.14 o superior con las configuraciones por defecto

- Editar las variables de entorno del sistema añadiendo las siguientes direcciones a la etiqueta "Path":
	C:\Python27;C:\Python27\Scripts;

- Abrir una ventana de comandos dentro de la carpeta que contiene este archivo e insertar los siguientes comandos uno despues de otro:
	pip install PyQt4==4.11.4
	pip install numpy==1.14.0
	pip install pyqtgraph==0.10.0
	pip install pyserial==2.7

- Una vez instalados los requerimientos anteriores, buscamos en archivo deformimetros.py y al hacerle doble click, podremos acceder al software


