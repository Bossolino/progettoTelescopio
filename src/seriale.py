import serial
import serial.tools.list_ports
import threading
from fileLog.Log import logger_seriale
from settings import settings
#variabile in cui settare la porta
#nome_device = "" #nome del device collegato
#variabile per continuare ad ascoltare finchè vuole l'utente o il programma non termina

def getPorteDisponibili(): # prendo le porte disponibili
    porte = {}
    porte_computer = serial.tools.list_ports.comports()
    for porta in porte_computer:
        porte[porta.device]=porta.description
        print(f"{porte[porta.device]}")
    return porte

def setPorta(): #funzione per ottenere la porta collegata al device
    porte = getPorteDisponibili()
    for porta in porte: 
        if porta.description == settings.seriale.nome_device: #controlla se la porta è quella giusta cioè quella collegata al device
            settings.seriale.porta_seriale = porta.name #mette la porta seriale trovata nella variabile vuota porta_seriale
            return settings.seriale.porta_seriale
    else:
        logger_seriale.error("Dispositivo non trovato!") # impostare avviso di errore
        return False

def start_ascolto():# funzione per avviare l'ascolto
    if settings.seriale.porta_seriale == "":
        return logger_seriale.error("Porta seriale non indicata!")
    if settings.seriale.porta_seriale in getPorteDisponibili(): # controllo se la porta impostata è disponibile
        settings.seriale.ascolta = True
        print("Thread avviato!")
        thread_ascolto.start() # se la porta è libera avvio il thread
    else:
        logger_seriale.error(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")
        print(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")
    
def ascolto(porta:str):# funzione per ascoltare la porta
    ascolto = serial.Serial(port=f'{porta}', timeout=1)
    settings.seriale.inAscolto = True
    while settings.seriale.ascolta:
        dato = ascolto.readline()
        dato_str = dato.decode('utf-8', errors='ignore').strip()
        if dato_str:
            logger_seriale.info(f"Ricevuto: {dato_str}")
            print(f"Ricevuto: {dato_str}")
    print("Thread chiuso.")
    logger_seriale.info("Thread chiuso.")

def stop_ascolto(e=None):
    global thread_ascolto
    if thread_ascolto and thread_ascolto.is_alive():
        settings.seriale.ascolta = False
        thread_ascolto.join(timeout=2)  # 👈 ASPETTA che finisca!
        print("✓ Thread fermato")

thread_ascolto = threading.Thread(target =lambda: ascolto(settings.seriale.porta_seriale)) #creazione thread per ascoltare la porta
