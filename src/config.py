import logging
from pathlib import Path
import flet as ft
import asyncio

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


#lista per i log

# creo la lista
lista = ft.ListView(spacing=10, padding=20, width=150, auto_scroll=True)

# Funzione per aggiungere nuove righe
def new_riga(riga : str):
    lista.controls.append(ft.Text(riga.strip(), color=ft.Colors.WHITE))


def new_lista_log (page: ft.Page ,nome_file : str):


    last_size = 0      # dimensione precedente del file
    file_path = Path(nome_file)

    # Funzione chiamata periodicamente
    # capire come chiamarla più volte
    def update_log():
        nonlocal last_size

        if not file_path.exists(): # se non esiste il file non fa nulla
            return

        # Controlla se il file è cresciuto
        new_size = file_path.stat().st_size
        if new_size == last_size:
            return  # nessuna nuova riga

        # Legge solo le nuove righe
        with open(file_path, "r") as f:

            f.seek(last_size) # vado ne''ultimo punto di lettura
            nuove_righe = f.readlines() # leggo le nuove righe
            last_size = new_size
            for riga in nuove_righe:
                new_riga(riga)
        
        # lista.update()

    
    update_log()
    return ft.Container(
        content=lista
    )
    

   
