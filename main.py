import obd
from obd import OBDStatus
import math
import time
import sys
import colorama
import re
import os
from tabulate import tabulate
import tkinter
from tkinter import *
from tkinter import messagebox
colorama.init()                     #initialize colorama

print("\x1b[2J", end="\r")          #ASCII escape sequence for clearing command line

ports = obd.scan_serial()                               #scans for all serial ports
port_list = print("Available ports: " + str(ports))     #prints all available ports, both wired and bluetooth


#Window title and dimensions
obdGUI = tkinter.Tk()                                           #The main class
obdGUI.title("DanOBD2 - A lightweight OBD2 reader and logger")  #Window title
obdGUI.geometry("1280x720")                                     #Width x Height of the window in pixels
obdGUI.resizable(0,0)                                           #Comment out this line to enable resizing and maximizing of the window

conAsync = obd.Async()              #Asynchronous querrying. Safer alternative to the obd.OBD() class, and is also inherits everything from obd.OBD().
    


def connectToCar():

    #console.config(state=DISABLED)
    #while True:
    console.config(state=NORMAL)
    if conAsync.status() is OBDStatus.NOT_CONNECTED:                                    #checks if the elm adapter is NOT connected
        console.insert(END, "\nELM adapter not connected to computer.")
        #errBlink()
    elif conAsync.status() is OBDStatus.ELM_CONNECTED:                                  #checks to see if the elm adapter IS connected to the computer
        console.insert(END, "\nELM adapter discovered. No signal.")
        #errBlink()
    elif conAsync.status() is OBDStatus.OBD_CONNECTED:                                  #checks to see if a link is established between the elm adapter and the obd2 port
        console.insert(END, "\nELM-OBD link established. No vehicle ignition. Start the vehicle to continue.")
        #errBlink()
    elif conAsync.status() is OBDStatus.CAR_CONNECTED:                                  #checks to see if the elm adapter and obd2 are able to communicate with each other
        console.insert(END, "\nVehicle ignition signal received. Communication successful.")
            #break
    console.config(state=DISABLED)
    console.see(tkinter.END)
    
    #console.pack()
    
def disconnectFromCar():
    conAsync.stop()
    time.sleep(2)
    if conAsync.status() is OBDStatus.CAR_CONNECTED:
        messagebox.showinfo(title = "ELM adapter unable to disconnect", message = "The ELM adapter is unable to be disconnected at this time.")
    else:
        messagebox.showinfo(title = "ELM adapter disconnected", message = "You may now safely remove your ELM adapter.")
    
    
def gtfo():
    exitConfirmation = messagebox.askyesno(title = "Quit", message = "Are you sure you want to exit?")      #confirmation message
    if exitConfirmation is True:
        if conAsync.status() is not OBDStatus.NOT_CONNECTED:
            disconnectFromCar()
        else:
            conAsync.stop()
        exit()

vaporwave = PhotoImage(file = ".\\assets\\DanOBD2_background.png")      #The background for the program located in the base directory
bgLabel = tkinter.Label(obdGUI, image=vaporwave)                #the image above is now a label
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)                #place the image at coords 0,0 with no stretching or fitting

#Buttons
button1 = Button(obdGUI, text = "Connect to car", width = 30, command = connectToCar)       #Connect to the car button
button1.place(x = 10, y = 10)
button2 = Button(obdGUI, text = "Show logs", width = 30)                                    #Show logging information button
button2.place(x = 10, y = 40)
button3 = Button(obdGUI, text = "Exit", width = 30, command = gtfo)                         #stops the elm adapter and quits the program
button3.place(x = 10, y = 70)


scroll = Scrollbar(obdGUI, takefocus=0)
console = Text(obdGUI, width = 64, height = 55, yscrollcommand = scroll.set)                #textbox dimensions
console.place(x=812, y=0)                                                                   #textbox coordinates
console.config(background = "black", foreground = "yellow")
scroll.pack(side="right", fill=Y)
scroll.config(command=console.yview)
enableText = console.config(state=NORMAL)
console.insert(END, ("Available ports: " + str(ports)))
disableText = console.config(state=DISABLED)

obdGUI.mainloop()               #start the program

exit()                          #exit program obviously

# ####################################################################################################################################################
# everything after this point is garbage and will not be run

def errBlink():                     #this function makes it possible for the previous print statement to blink red. Can only be used in the console
        time.sleep(1)
        print("\033[K", end="\r")   #ASCII escape sequence for clearing line
        time.sleep(1)


print("===========================================\n\
  ____               ___  ____  ____ ____  \n\
 |  _ \\  __ _ _ __  / _ \\| __ )|  _ \\___ \\ \n\
 | | | |/ _` | '_ \\| | | |  _ \\| | | |__) |\n\
 | |_| | (_| | | | | |_| | |_) | |_| / __/ \n\
 |____/ \\__,_|_| |_|\\___/|____/|____/_____|")
#clrLine = print("\033[F" + "\033[K", end="\r")

print("If using USB, please ensure your adapter on both ends is not loose.")

#Scans for available serial and bluetooth ports on computer


#conOBD = obd.OBD() #Connects to the first port in the list
conAsync = obd.Async() #Asynchronous querrying. Safer alternative to the obd.OBD() class, and is also a child of that class.

#A loop that determines the connection status of the ELM adapter.
#Loop will break once the connection is fully established between the vehicle and the computer

print(str(ports) + " connection status: ")

while True:

    if conAsync.status() is OBDStatus.NOT_CONNECTED:
        print("\033[31m" + "ELM adapter not connected to computer.", end="\r")   #the END argument tells the cursor to CR but not LF
        errBlink()
    elif conAsync.status() is OBDStatus.ELM_CONNECTED:
        print("\033[32m" + "ELM adapter discovered. \033[31mNo signal.", end="\r")
        errBlink()
    elif conAsync.status() is OBDStatus.OBD_CONNECTED:
        print("\033[32m" + "ELM-OBD link established. \033[31mNo vehicle ignition. Start the vehicle to continue.", end="\r")
        errBlink()
    elif conAsync.status() is OBDStatus.CAR_CONNECTED:
        print("\033[32m" + "Vehicle ignition signal received. Communication successful." + "\033[39m")
        conAsync.start()
        time.sleep(3)
        break

tableFields = [["ELM327 Adapter Version", conAsync.query(obd.commands.ELM_VERSION)],        #ELM adapter version
                ["Detected Voltage", conAsync.query(obd.commands.ELM_VOLTAGE)],             #OBD2 voltage
                ["Current Fuel Level", conAsync.query(obd.commands.FUEL_LEVEL)],            #Fuel level in percentage
                ["Current Fuel Status", conAsync.query(obd.commands.FUEL_STATUS)],          #Fuel status (returns 2 strings)
                ["Engine Fuel Rate", conAsync.query(obd.commands.FUEL_RATE)],               #Fuel rate
                ["Ambient Air Temperature", conAsync.query(obd.commands.AMBIANT_AIR_TEMP)], #Outside air temperature
                ["Intake Air Temperature", conAsync.query(obd.commands.INTAKE_TEMP)],       #Intake air temperature
                ["Mass Airflow Rate", conAsync.query(obd.commands.MAF)],                    #MAF rate
                ]
tableHeaders = ["Vehicle Sensor", "Value"]  #table headers

while True: #This loop refreshs the table every 1 second with new data queried from the OBD2 port

    print("\x1b[2J", end="\r")
    print("-" * 10 + " \033[36mEngine Runtime:\033[39m " + str(conAsync.query(obd.commands.RUN_TIME)) + " elapsed." + ("-" * 10))
    print(tabulate(tableFields, tableHeaders, tablefmt="fancy_grid"))
    time.sleep(1)
    
conAsync.stop()