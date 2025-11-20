import serial # type: ignore
import serial.tools.list_ports # type: ignore
import threading
from fileLog.Log import logger_seriale

porta_seriale = "" #variabile in cui settare la porta
nome_device = "" #nome del device collegato
ascolta = False #variabile per continuare ad ascoltare finchè vuole l'utente o il programma non termina

def ascolto(porta:str):# funzione per ascoltare la porta
    ascolto = serial.Serial(port=f'{porta}', timeout=1)
    while ascolta:
        logger_seriale.info(f"Ricevuto dato dalla seriale: {ascolto.readline()}") #leggo la riga inviata nella porta e la scrivo in un log
        print(f"Ricevuto dato dalla seriale: {ascolto.readline()}")

def start_ascolto():# funzione per avviare l'ascolto
    global ascolta 
    global porta_seriale
    if porta_seriale == "":
        return logger_seriale.error("Porta seriale non indicata!")
    if porta_seriale in getPorteDisponibili(): # controllo se la porta impostata è disponibile
        ascolta = True
        thread_ascolto.start() # se la porta è libera avvio il thread
    else:
        logger_seriale.error(f"La porta seriale {porta_seriale} non è disponibile.")
        print(f"La porta seriale {porta_seriale} non è disponibile.")
    
def stop_ascolto():
    global ascolta
    ascolta = False

def getPorteDisponibili(): # prendo le porte disponibili
    porte = {}
    porte_computer = serial.tools.list_ports.comports()
    for porta in porte_computer:
        porte[porta.device]=porta.description
        #print(f"{porte[porta.device]}")
    return porte



def setPorta(): #funzione per ottenere la porta collegata al device
    porte = getPorteDisponibili() 
    for porta in porte: 
        if porta.description == nome_device: #controlla se la porta è quella giusta cioè quella collegata al device
            porta_seriale = porta.name #mette la porta seriale trovata nella variabile vuota porta_seriale
            return porta_seriale
    else:
        logger_seriale.error("Dispositivo non trovato!") # impostare avviso di errore
        return False


thread_ascolto = threading.Thread(target=lambda e: ascolto(porta_seriale)) #creazione thread per ascoltare la porta
