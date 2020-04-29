# imports python bluetooth package
import bluetooth

# imports python package for threading processes
import threading

#import tinydb, for storing data in json file
from tinydb import TinyDB, Query

# define the global buffer variable to store data from the bluetooth connection
buffer = ""

# initialises tinydb in db.json
db = TinyDB('db.json')

# function to set up bluetooth with arduino
def setup_bluetooth():  
    # takes in global variable called bluetooth_socket
    global bluetooth_socket
    try:
        # connects to mac address of arduino bluetooth unit
        bluetooth_socket.connect(("98:D3:31:F5:18:44", 1))   

    except bluetooth.BluetoothError:
        # code to run if connection fails
        print("IT FAILED")

# background function to take bluetooth input into variable
def check_bluetooth_input():
    # takes in global variables into scope of function
    global bluetooth_socket
    global buffer

    # begins loop to run in background while running variable is true
    while running:          
        try:
            #sets variable req to data recieved over bluetooth from arduino
            req = bluetooth_socket.recv(10)
        except:
            # error handling
            print("Goodbye!")
        
        # adds data from bluetooth to global buffer variable
        buffer += str(req, 'utf-8')

# function to end program
def end_program():
    # takes in global variables
    global running
    global bluetooth_socket
    running = False
    bluetooth_socket.close()

# sets up bluetooth socket to be used over RFCOMM
bluetooth_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

setup_bluetooth()

running = True

try:
    # sets up bluetooth input function to run in background
    bt_thread = threading.Thread(target=check_bluetooth_input, args=())
    bt_thread.start()
except:
    print("failed")

try:
    while True:
        # sets x value to whatever input user submits
        x = input()

        # if user submits list, display list of names
        if x == "list":
            # goes through all of the ids inside the variable separated by semicolon
            for i in buffer.split(';'):
                if len(i) > 4:
                    # looks up person in tinydb database based on the id of the nfc tag
                    Person = Query()
                    result = db.search(Person.id == i)[0]
                    print(result['name'])
        if x == "exit":
            # if user types exit end program
            end_program()
            break
except KeyboardInterrupt:
    # if user exits program by using control+c end program
    end_program()
    pass
