import logging

logger_seriale = logging.getLogger("logger_seriale") #nome del logger
logger_seriale.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #formato del logger
try:
    fileHandler = logging.FileHandler("src\\fileLog\\ascolto_seriale.log") #dove si trova il file di log
except Exception as e:
    print("Errore nella creazione del file di log:", e)
    
fileHandler.setFormatter(formatter)
logger_seriale.addHandler(fileHandler)
