import serial
from config import *
import threading


def ascolto():
    while ascolta:
        ser = serial.Serial(f'{porta_seriale}', 9600, timeout=1)
        line = ser.readline().decode()
        print(line)
        print("attivo")


thread = threading.Thread(target=ascolto)

thread.start()
