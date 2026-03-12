import serial
import serial.tools.list_ports
import threading
from fileLog.Log import logger_seriale
from settings import settings
#variabile in cui settare la porta
#nome_device = "" #nome del device collegato
#variabile per continuare ad ascoltare finchè vuole l'utente o il programma non termina


ser = None
thread_ascolto = None

def getPorteDisponibili(): # prendo le porte disponibili
    porte = {}
    porte_computer = serial.tools.list_ports.comports()
    for porta in porte_computer:
        porte[porta.device]=porta.description
        print(f"{porte[porta.device]}")
    return porte

porte = getPorteDisponibili()

def setPorta(): #funzione per ottenere la porta collegata al device
    global porte
    for device, desc in porte.items():
        if desc == settings.seriale.nome_device:
            settings.seriale.porta_seriale = device
            return device
    else:
        logger_seriale.error("Dispositivo non trovato!") # impostare avviso di errore
        return False

def start_ascolto(porta:str):# funzione per avviare l'ascolto
    global ser, thread_ascolto
    if settings.seriale.porta_seriale == "" or not (settings.seriale.porta_seriale.is_open):
        return logger_seriale.error("Porta seriale non indicata!")
    if settings.seriale.porta_seriale in porte: # controllo se la porta impostata è disponibile
        settings.seriale.ascolta = True
        ser = serial.Serial(port=porta, baudrate=9600, timeout=1)
        thread_ascolto = threading.Thread(target=ascolto, daemon=True) #creazione thread per ascoltare la porta
        try:
            thread_ascolto.start() # se la porta è libera avvio il thread
            print("Thread avviato!")
            logger_seriale.info("Thread avviato!")
        except Exception as e:
            print("Thread non avviato!")
            logger_seriale.error(f"Thread non avviato: {e}")
    else:
        logger_seriale.error(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")
        print(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")
    
def ascolto():# funzione per ascoltare la porta
    global ser
    settings.seriale.inAscolto = True
    while settings.seriale.ascolta:
        try:
            dato = ser.readline()
            dato_str = dato.decode('utf-8', errors='ignore').strip()
            if dato_str:
                logger_seriale.info(f"Ricevuto: {dato_str}")
                print(f"Ricevuto: {dato_str}")
        except Exception as e:
            logger_seriale.error(f"Errore seriale: {e}")
            break
    print("Thread chiuso.")
    logger_seriale.info("Thread chiuso.")

def stop_ascolto(e=None):
    global thread_ascolto, ser
    if thread_ascolto and thread_ascolto.is_alive():
        settings.seriale.ascolta = False
        thread_ascolto.join(timeout=2)  # 👈 ASPETTA che finisca!
        
        if ser and ser.is_open:
            ser.close() #chiudo la porta

        print("✓ Thread fermato")


