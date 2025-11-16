import logging
from logging.handlers import TimedRotatingFileHandler

cupola_logger = logging.getLogger("cupola") #nome del logger
cupola_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger

try:
    fileHandler = TimedRotatingFileHandler(
        filename="src\\fileLog\\spostamenti.log",
        when="D",
        interval=1,
        backupCount=7,
        utc=False
        
        ) #dove si trova il file di log
    
    fileHandler.suffix = "%d-%m-%y"
except Exception as e:
    print("Errore nella creazione del file di log:", e)
    
fileHandler.setFormatter(formatter)
cupola_logger.addHandler(fileHandler)
