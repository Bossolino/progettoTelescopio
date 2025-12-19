import serial

def ascolto(porta:str):# funzione per ascoltare la porta
    ascolta = serial.Serial(port=f'{porta}', timeout=1)
    while True:
        print(f"Ricevuto dato dalla seriale: {ascolta.readline()}")

ascolto('COM5')