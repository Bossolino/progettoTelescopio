import logging
from logging.handlers import TimedRotatingFileHandler

# gestore log per spostamento cupola
cupola_logger = logging.getLogger("cupola") #nome del logger
cupola_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger

try:
    fileHandler_cupola = TimedRotatingFileHandler( #handler per la rotazione deifile
        filename="src\\fileLog\\spostamenti.log",
        when="D",
        interval=1,
        backupCount=7,
        utc=False
        
        ) #dove si trova il file di log
    
    fileHandler_cupola.suffix = "%d-%m-%y" #inserire la data del giorno come suffisso 
except Exception as e:
    print("Errore nella creazione del file di log:", e)
    
fileHandler_cupola.setFormatter(formatter)
cupola_logger.addHandler(fileHandler_cupola)

# gestore log per la parte della seriale
logger_seriale = logging.getLogger("seriale") #nome del logger
logger_seriale.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger
try:
    fileHandler_seriale = TimedRotatingFileHandler( #handler per la rotazione deifile
        filename="src\\fileLog\\ascolto_seriale.log",
        when="D",
        interval=1,
        backupCount=7,
        utc=False
        
        ) #dove si trova il file di log
    
    fileHandler_seriale.suffix = "%d-%m-%y" #dove si trova il file di log
except Exception as e:
    print("Errore nella creazione del file di log:", e)
    
fileHandler_seriale.setFormatter(formatter)
logger_seriale.addHandler(fileHandler_seriale)