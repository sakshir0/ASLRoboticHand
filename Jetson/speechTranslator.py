import serial, time
import speech_recognition as sr
import keyboard


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


# Set up voice recognition
r = sr.Recognizer()
mic = sr.Microphone()


# ------------ BEGINNING OF MAIN LOOP ------------ #
print('Start\n')
while True: 
    with mic as source: 
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)    

        try: 
            data = r.recognize_google(audio)
            print('Input: ' + data)
            arduino.write(data.lower().encode())
        except Exception as e: 
            print(e)
        
arduino.close()
