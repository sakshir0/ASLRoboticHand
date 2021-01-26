import serial, time, argparse 

# Parse verbose flag
parser = argparse.ArgumentParser() 
parser.add_argument("-v", "--verbosity", required=False, action="count", help="Verbose flag")
args = parser.parse_args() 
verbose = False

if args.verbosity:
    verbose = True

# Open Serial port to connect with Arduino
try: 
    arduino = serial.Serial(
        port = '/dev/tty.usbmodem14101',
        baudrate = 9600, 
        timeout = 1
    )
    if not arduino.isOpen():
        arduino.open()
        time.sleep(1)
        if(verbose):
            print("Connected to Arduino succesfully")
except Exception as e:
    print(e)


# ------------ BEGINNING OF MAIN LOOP ------------ #
while True: 
    # Write input to arduino 
    phrase = input("Please enter a string: \n") 
    print("Input: " + phrase + "\n") 
    arduino.write(phrase.lower().encode())

arduino.close()
