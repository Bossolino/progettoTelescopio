import serial
import serial.tools.list_ports
import threading
from fileLog.LogSeriale import logger_seriale

porta_seriale = ""
ascolta = False

def apri_ascolto(porta:str):
    ascolto = serial.Serial(port=f'{porta}', timeout=1)
    while ascolta:
        logger_seriale.info(f"Ricevuto dato dalla seriale: {ascolto.readline()}")
        print(f"Ricevuto dato dalla seriale: {ascolto.readline()}")

def start_ascolto():
    global ascolta 
    ascolta = True
    if porta_seriale in getPorteDisponibili():
        thread_ascolto.start()
    else:
        logger_seriale.error(f"La porta seriale {porta_seriale} non è disponibile.")
        print(f"La porta seriale {porta_seriale} non è disponibile.")
    
def stop_ascolto():
    global ascolta
    ascolta = False

def getPorteDisponibili():
    porte = []
    porte_computer = serial.tools.list_ports.comports()
    for porta in porte_computer:
        porte.append(porta.device)
        print(porta.device)
    return porte


thread_ascolto = threading.Thread(target=lambda e: apri_ascolto(porta_seriale))

start_ascolto()