
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

#function to handle the selection of the outgoing serial port
def on_outgoing_port_selected(event):
    print("inside on_outgoing_port_selected")
    selected_outgoing_port = SerialPortOutgoingCombobox.get()
    selected_incoming_port = SerialPortIncomingCombobox.get()

    if selected_outgoing_port == selected_incoming_port:
        # Find a new port for the incoming combobox
        all_ports = SerialPortIncomingCombobox['values']
        for port in all_ports:
            if port != selected_outgoing_port:
                SerialPortIncomingCombobox.set(port)
                break # Exit after finding the first available port

#function to refresh the serial ports in the combobox
def RefreshPorts():
    print("inside refresh ports")
    #get the list of available com ports
    ComPortList = [comport.device for comport in serial.tools.list_ports.comports()]
    print(ComPortList)
    if not ComPortList:
        SerialPortOutgoingCombobox['values'] = ["No Comm Ports Available"]
        SerialPortOutgoingCombobox.current(0) #display the value at 0
        SerialPortIncomingCombobox['values'] = ["No Comm Ports Available"]
        SerialPortIncomingCombobox.current(0)
    elif len(ComPortList) == 1:
        SerialPortIncomingCombobox['values'] = ComPortList
        SerialPortIncomingCombobox.current(0)
        SerialPortOutgoingCombobox['values'] = ["No Comm Ports Available"]
        SerialPortOutgoingCombobox.current(0)
    else:
        # Sort ports by the number in the port name, handles cases like 'COM10' vs 'COM2'
        try:
            sorted_ports = sorted(ComPortList, key=lambda x: int("".join(filter(str.isdigit, x))))
        except ValueError:
            # Fallback to alphanumeric sort if port names are not standard (e.g., /dev/ttyS0)
            sorted_ports = sorted(ComPortList)

        SerialPortIncomingCombobox['values'] = sorted_ports
        SerialPortIncomingCombobox.current(0) # Set to the lowest port
        SerialPortOutgoingCombobox['values'] = sorted_ports
        SerialPortOutgoingCombobox.current(0)

#function to clean up as the window closes, close serial ports, files etc
def MainWindowClose():
    print("Window Exiting")
    MainWindow.destroy()

#*********************************************  Code to set up window   *********************************************
MainWindow = tkinter.Tk() #initiate the main window
MainWindow.title("Seadraulics Program") #set the window title
MainWindow.iconbitmap("Seadraulics.ico") #add the Seadraulics gear to the top left window
MainWindow.geometry("800x600")  #set the minimum size of the window on open

# Configure the grid layout
MainWindow.grid_rowconfigure(0, weight=1)
MainWindow.grid_rowconfigure(1, weight=0)
MainWindow.grid_rowconfigure(2, weight=0)
MainWindow.grid_rowconfigure(3, weight=0)
MainWindow.grid_rowconfigure(4, weight=0)
MainWindow.grid_rowconfigure(5, weight=0)
MainWindow.grid_rowconfigure(6, weight=0)
MainWindow.grid_rowconfigure(7, weight=0)
MainWindow.grid_rowconfigure(8, weight=0)
MainWindow.grid_columnconfigure(0, weight=1)
MainWindow.grid_columnconfigure(1, weight=1)
MainWindow.grid_columnconfigure(2, weight=1)
MainWindow.grid_columnconfigure(3, weight=1)


#*********************************************   Code to set up widgets   *********************************************
#place the logo on the screen
LogoImage = Image.open("Seadraulics-logo-FC.png") #open the image
LogoImageSizeX = LogoImage.width #fetch the width and height
LogoImageSizeY = LogoImage.height
LogoPercentageSize=0.5  #set the amount to resize by
LogoResized = LogoImage.resize((int(LogoImageSizeX*LogoPercentageSize), int(LogoImageSizeY*LogoPercentageSize))) #resize the logo
LogoPhoto = ImageTk.PhotoImage(LogoResized)   #covert to a form that can be displayed
LogoLabel = tkinter.Label(image=LogoPhoto) #create the label to display the image
LogoLabel.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky='n')

#add a separator
ttk.Separator(MainWindow, orient='horizontal').grid(row=1, columnspan=4, sticky='ew')

#************************************************Out going serial port set up on the window********************************************
#put a label for the outgoing serial port combo box
SerialPortOutgoingLabel = tkinter.Label(MainWindow, text="Outgoing Serial Port ")
SerialPortOutgoingLabel.grid(row=2, column=0, sticky='w', padx=10, pady=5)
#Add combobox to select Outgoing com port
SerialPortOutgoingCombobox=ttk.Combobox(MainWindow, values=["No Comm Ports Available"], width=30)
SerialPortOutgoingCombobox.grid(row=2, column=1, sticky='we', padx=10, pady=5)
SerialPortOutgoingCombobox.bind("<<ComboboxSelected>>", on_outgoing_port_selected)

#Add the connect to outgoing serial port button
SerialPortConnectOutgoingButton=tkinter.Button(MainWindow, width= 25, bg='Green', text="Outgoing Serial Port Connect", command=SerialConnectOutgoing)
SerialPortConnectOutgoingButton.grid(row=2, column=2, padx=10, pady=5)

#Add the refresh ports button
RefreshPortsButtonOutgoing=tkinter.Button(MainWindow, text="Refresh Ports", command=RefreshPorts)
RefreshPortsButtonOutgoing.grid(row=2, column=3, padx=10, pady=5)

#add a separator
ttk.Separator(MainWindow, orient='horizontal').grid(row=3, columnspan=4, sticky='ew')

#************************************************Incoming serial port set up on the window************************************************
#put a label for the incoming serial port combo box
SerialPortIncomingLabel = tkinter.Label(MainWindow, text="Incoming Serial Port ")
SerialPortIncomingLabel.grid(row=4, column=0, sticky='w', padx=10, pady=5)

#Add combobox to select incoming com port
SerialPortIncomingCombobox=ttk.Combobox(MainWindow, values=["No Comm Ports Available"], width=30)
SerialPortIncomingCombobox.grid(row=4, column=1, sticky='we', padx=10, pady=5)

#Add the connect to incoming serial port button
SerialPortIncomingConnectButton=tkinter.Button(MainWindow, width= 25, bg='Green', text="Incoming Serial Port Connect", command=SerialConnectIncoming)
SerialPortIncomingConnectButton.grid(row=4, column=2, padx=10, pady=5)

#Add the refresh ports button
RefreshPortsButtonIncoming=tkinter.Button(MainWindow, text="Refresh Ports", command=RefreshPorts)
RefreshPortsButtonIncoming.grid(row=4, column=3, padx=10, pady=5)

#add a separator
ttk.Separator(MainWindow, orient='horizontal').grid(row=5, columnspan=4, sticky='ew')

#************************************************Logging filename window set up************************************************
#place a label for the file name entry box
FilenameLabel = tkinter.Label(MainWindow, text='Filename')
FilenameLabel.grid(row=6, column=0, sticky='w', padx=10, pady=5)

#place an Entry box for entry of filename
FilenameEntryBox = tkinter.Entry(MainWindow, width=30, border=4, textvariable=CompleteFilenameString)
FilenameEntryBox.bind('<Return>', SetFilename )   #if the user hits return call the function
FilenameEntryBox.insert(0,FilenameString)   #initialize with the current default filename
FilenameEntryBox.grid(row=6, column=1, sticky='we', padx=10, pady=5)

#place select folder button
SelectFolderButton = tkinter.Button(MainWindow, text="Select Folder", command=SetFolder)
SelectFolderButton.grid(row=6, column=2, padx=10, pady=5)

#place a button to turn logging on and off
LoggingButton = tkinter.Button(MainWindow, text="Turn Logging ON", bg='Green', command=LoggingOnOff)
LoggingButton.grid(row=6, column=3, padx=10, pady=5, sticky='e')

#add a separator
ttk.Separator(MainWindow, orient='horizontal').grid(row=7, columnspan=4, sticky='ew')

#define the label to show the current folder and filename
CompleteFilenameString=FolderString+FilenameString
print(CompleteFilenameString)
FilenameLocationLabel = tkinter.Label(MainWindow, text=CompleteFilenameString)
FilenameLocationLabel.grid(row=8, column=0, columnspan=4, sticky='w', padx=10, pady=5)

RefreshPorts() #as the window opens refresh the serial ports

#MainWindow setup and invoking
MainWindow.protocol(name="WM_DELETE_WINDOW", func=MainWindowClose)    #if the user hits the windows close button enter here to close off files and serial ports and destroy
MainWindow.mainloop()
