from cProfile import label
from distutils import command
from multiprocessing.dummy import Event
from pickle import FALSE, TRUE
from re import X
import this
import tkinter
from tkinter.ttk import Widget
from turtle import bgcolor # Load the GUI module
from PIL import Image, ImageTk #used to display the Seadraulics logo PNG
import tkinter.filedialog #used to select the folder to save the logging file
import serial
import serial.tools.list_ports
from tkinter import ttk

#define global variables here
LoggingOnOffBool=False #set the default logging button to off
FilenameString = "Test.csv" #set default filename for the edit box
FolderString = "C:\\" #set the default folder location for logging file
CompleteFilenameString=FolderString+FilenameString #Filename and folder location for file open/close commands
SerialPortConnectedIncomingBool=False #no incoming serial port connected
SerialPortConnectedOutgoingBool=False #no outgoing serial port connected

#***********************************  define functions here **********************************
#function to change the colour and text of the logging button
def LoggingOnOff ():
    global LoggingOnOffBool     #use the global variable inside this function
     
    if (LoggingOnOffBool==True) : 
        LoggingOnOffBool=False
        LoggingButton.configure(text='Turn Logging ON ', background='Green')
    else:
        LoggingOnOffBool=True
        LoggingButton.configure(text='Turn Logging OFF', background='Red')
    print (LoggingOnOffBool)

#function to add the filename to the folder location
def SetFilename(event):
    global FilenameString  #ensure use of the global strings
    global FolderString
    global CompleteFilenameString
    global LoggingOnOffBool

    print("Inside Set Filename")
    if (LoggingOnOffBool==False) :
        FilenameString = FilenameEntryBox.get()
        FilenameString += ".csv"
    #print(FilenameString)
    FilenameEntryBox.delete(0, 29)
    FilenameEntryBox.insert(0, FilenameString) #ensure the Entry box has the .csv added after <return>
    CompleteFilenameString=FolderString+FilenameString
    #print(CompleteFilenameString)
    FilenameLocationLabel.config(text=CompleteFilenameString) #update the label text for the complete filename

#function to select the folder location for the logging file
def SetFolder():
    global FolderString #ensure use of the global string
    global CompleteFilenameString
    global FilenameString

    print("Inside Setfolder")
    FolderString = tkinter.filedialog.askdirectory()+'/' #open the dialog and store the folder with added /
    #print(FolderString)
    CompleteFilenameString=FolderString+FilenameString
    FilenameLocationLabel.config(text=CompleteFilenameString) #update the label text for the complete filename

#function to connect/disconnect to the incoming serial data
def SerialConnectIncoming():
    print("inside incoming serial connect")
    global SerialPortConnectedIncomingBool  #use the global variable
    if (SerialPortConnectedIncomingBool==True) : #if true then set to false and get it ready to connect again
        SerialPortConnectedIncomingBool=False
        SerialPortIncomingConnectButton.configure(text='Incoming Serial Port Connect ', background='Green')
    else: #if its false then connect to the serial port if possible
        SerialPortConnectedIncomingBool=True
        SerialPortIncomingConnectButton.configure(text='Incoming Serial Port Disconnect', background='Red')


#function to connect/disconnect to the outcoming serial data
def SerialConnectOutgoing():
    print("inside outgoing serial connect")
    global SerialPortConnectedOutgoingBool  #use the global variable
    if (SerialPortConnectedOutgoingBool==True) : #if true then set to false and get it ready to connect again
        SerialPortConnectedOutgoingBool=False
        SerialPortConnectOutgoingButton.configure(text='Outgoing Serial Port Connect ', background='Green')
    else: #if its false then connect to the serial port if possible
        SerialPortConnectedOutgoingBool=True
        SerialPortConnectOutgoingButton.configure(text='Outgoing Serial Port Disconnect', background='Red')

#function to clean up as the window closes, close serial ports, files etc
def MainWindowClose():
    print("Window Exiting")
    MainWindow.destroy()

#*********************************************  Code to set up window   *********************************************
MainWindow = tkinter.Tk() #initiate the main window
MainWindow.title("Seadraulics Program") #set the window title
MainWindow.iconbitmap("Seadraulics.ico") #add the Seadraulics gear to the top left window
MainWindow.geometry("800x600")  #set the minimum size of the window on open

#*********************************************   Code to set up widgets   *********************************************
#place the logo on the screen
LogoImage = Image.open("Seadraulics-logo-FC.png") #open the image
LogoImageSizeX = LogoImage.width #fetch the width and height
LogoImageSizeY = LogoImage.height
LogoPercentageSize=0.5  #set the amount to resize by
LogoResized = LogoImage.resize((int(LogoImageSizeX*LogoPercentageSize), int(LogoImageSizeY*LogoPercentageSize))) #resize the logo 
LogoPhoto = ImageTk.PhotoImage(LogoResized)   #covert to a form that can be displayed
LogoLabel = tkinter.Label(image=LogoPhoto) #create the label to display the image
LogoLabel.place(x=200, y=100)    #display on the GUI at co-ordinates

#************************************************Logging filename window set up************************************************
#place a button to turn logging on and off
LoggingButton = tkinter.Button(MainWindow, text="Turn Logging ON", bg='Green', command=LoggingOnOff)
LoggingButton.place(x=680, y=550)

#place a label for the file name entry box
FilenameLabel = tkinter.Label(MainWindow, text='Filename')
FilenameLabel.place(x=10, y=550)

#place an Entry box for entry of filename
FilenameEntryBox = tkinter.Entry(MainWindow, width=30, border=4, textvariable=CompleteFilenameString)
FilenameEntryBox.bind('<Return>', SetFilename )   #if the user hits return call the function
FilenameEntryBox.insert(0,FilenameString)   #initialize with the current default filename
FilenameEntryBox.place(x=140, y=550)

#place select folder button
SelectFolderButton = tkinter.Button(MainWindow, text="Select Folder", command=SetFolder)
SelectFolderButton.place(x=400, y=550)

#define the label to show the current folder and filename
CompleteFilenameString=FolderString+FilenameString
print(CompleteFilenameString)
FilenameLocationLabel = tkinter.Label(MainWindow, text=CompleteFilenameString) 
FilenameLocationLabel.place(x=10, y=575)

#get the list of available com ports
ComPortList = [comport.device for comport in serial.tools.list_ports.comports()]
print(ComPortList)

#************************************************Incoming serial port set up on the window************************************************
#put a label for the incoming serial port combo box
SerialPortIncomingLabel = tkinter.Label(MainWindow, text="Incoming Serial Port ")
SerialPortIncomingLabel.place(x=10, y=500)

#Add combobox to select incoming com port
if ComPortList==[]:
    SerialPortIncomingCombobox=ttk.Combobox(MainWindow, values=["No Comm Ports Available"], width=30)
    SerialPortIncomingCombobox.current(0) #display the value at 0 
else:
    SerialPortIncomingCombobox =ttk.Combobox(MainWindow, values = ComPortList, width=30)
    SerialPortIncomingCombobox.current(0) #display the value at 0, user will decide to select a different port
SerialPortIncomingCombobox.place(x=140, y=500)

#Add the connect to incoming serial port button
SerialPortIncomingConnectButton=tkinter.Button(MainWindow, width= 25, bg='Green', text="Incoming Serial Port Connect", command=SerialConnectIncoming)
SerialPortIncomingConnectButton.place(x=400, y=500)

#************************************************Out going serial port set up on the window********************************************
#put a label for the outgoing serial port combo box
SerialPortOutgoingLabel = tkinter.Label(MainWindow, text="Outgoing Serial Port ")
SerialPortOutgoingLabel.place(x=10, y=450)
#Add combobox to select Outgoing com port
if ComPortList==[]:
    SerialPortOutgoingCombobox=ttk.Combobox(MainWindow, values=["No Comm Ports Available"], width=30)
    SerialPortOutgoingCombobox.current(0) #display the value at 0 
else:
    SerialPortOutgoingCombobox =ttk.Combobox(MainWindow, values = ComPortList, width=30)
    SerialPortOutgoingCombobox.current(0) #display the value at 0, user will decide to select a different port
SerialPortOutgoingCombobox.place(x=140, y=450)

#Add the connect to outgoing serial port button
SerialPortConnectOutgoingButton=tkinter.Button(MainWindow, width= 25, bg='Green', text="Outgoing Serial Port Connect", command=SerialConnectOutgoing)
SerialPortConnectOutgoingButton.place(x=400, y=450)

#MainWindow setup and invoking
MainWindow.protocol(name="WM_DELETE_WINDOW", func=MainWindowClose)    #if the user hits the windows close button enter here to close off files and serial ports and destroy
MainWindow.mainloop()

### sample code split string
#text="asdsadf,sdfsdf,sdfsdf,sdf,werw,qweqq,1,2,3,4"
#x= text.split(",")
#print(x)
#['asdsadf', 'sdfsdf', 'sdfsdf', 'sdf', 'werw', 'qweqq', '1', '2', '3', '4']


