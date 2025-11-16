import logging
from logging.handlers import TimedRotatingFileHandler

cupola_logger = logging.getLogger("movimenti_cupola") #nome del logger
cupola_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger

try:
    fileHandler = TimedRotatingFileHandler("src\\fileLog\\spostamenti.log") #dove si trova il file di log
except Exception as e:
    print("Errore nella creazione del file di log:", e)
    
fileHandler.setFormatter(formatter)
cupola_logger.addHandler(fileHandler)
