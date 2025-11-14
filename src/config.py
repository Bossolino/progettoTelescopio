import logging
cupola_logger = logging.getLogger("movimenti_cupola") #nome del logger
cupola_logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger
fileHandler = logging.FileHandler("src\\fileLog\\spostamenti.log") #dove si trova il file di log
fileHandler.setFormatter(formatter)
cupola_logger.addHandler(fileHandler)

c_cupola = "0"
c_telescopio = "1"

def sposta_cupola_destra(sposta: int): # funzione per spostare la cupola a destra
    global c_cupola
    if(sposta != 0): #aggiunto il controllo almeno non abbiamo spostamenti inutili nei file di log
        c_cupola = str(int(c_cupola) + sposta)
        cupola_logger.info(f"Cupola spostata a destra di {sposta}. Nuova posizione: {c_cupola}")

def sposta_cupola_sinistra(sposta: int): # funzione per spostare la cupola a sinistra
    global c_cupola
    if(sposta != 0):
        c_cupola = str(int(c_cupola) - sposta)
        cupola_logger.info(f"Cupola spostata a sinistra di {sposta}. Nuova posizione: {c_cupola}")

def reset_posizioni(): # funzione per resettare le posizioni
    global c_cupola, c_telescopio
    c_cupola = c_telescopio
    cupola_logger.info("Posizioni resettate")
def stop_movimento(): # funzione per fermare il movimento
    cupola_logger.info("Movimento fermato")