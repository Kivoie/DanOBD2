import obd
from obd import OBDStatus
import math
import time
import sys
import colorama
import re
from tabulate import tabulate
colorama.init()

clrLine = print("\033[F\033[K")
clrScreen = print("\x1b[2J")


print("If using USB, please ensure your adapter on both ends is not loose.")

#Scans for available serial and wireless (bluetooth) ports on computer
ports = obd.scan_serial()
port_list = print("Available ports: " + str(ports))

connection = obd.OBD() #Connects to the first port in the list

#A loop that determines the connection status of the ELM adapter.
#Loop will break once the connection is fully established between the vehicle and the computer

print(str(ports) + " connection status: ")

while True:

    if connection.status() is OBDStatus.NOT_CONNECTED:
        print("\033[31m" + "ELM adapter not connected to computer.", end="\r")   #the END argument tells the cursor to CR but not LF
        time.sleep(1)
        print("\033[31m\033[K", end="\r")
        time.sleep(1)
        print("", end="\r")
    elif connection.status() is OBDStatus.ELM_CONNECTED():
        print("ELM adapter discovered. No signal.")
        time.sleep(1)
        clrLine
    elif connection.status() is OBDStatus.OBD_CONNECTED():
        print("ELM adapter signal established. No vehicle ignition.")
        time.sleep(1)
        clrLine
    elif connectoin.status() is OBDStatus.CAR_CONNECTED():
        print("Vehicle ignition signal received. Communication successful.\n")
        break

#Shows some vehicle diagnostics from vehicle sensors.
print("OBD-II ELM327 Adapter version: " + str(obd.commands.ELM_VERSION))
print("OBD-II detected voltage: " + str(obd.commands.ELM_VOLTAGE))
print("Fuel levels: " + str(obd.commands.FUEL_LEVEL))