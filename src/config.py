import logging
from pathlib import Path
import flet as ft
import asyncio
from fileLog.Log import cupola_logger 


tema = ""

c_cupola = "0"
c_telescopio = "1"

def sposta_cupola_destra(sposta: int): # funzione per spostare la cupola a destra
    global c_cupola
    if(sposta != 0): #aggiunto il controllo almeno non abbiamo spostamenti inutili nei file di log
        c_cupola = str(int(c_cupola) + sposta)
        cupola_logger.info(f"destra di {sposta}. pos: {c_cupola}")

def sposta_cupola_sinistra(sposta: int): # funzione per spostare la cupola a sinistra
    global c_cupola
    if(sposta != 0):
        c_cupola = str(int(c_cupola) - sposta)
        cupola_logger.info(f"sinistra di: {sposta}. pos: {c_cupola}")

def reset_posizioni(): # funzione per resettare le posizioni
    global c_cupola, c_telescopio
    c_cupola = c_telescopio
    cupola_logger.info("reset")
def stop_movimento(): # funzione per fermare il movimento
    cupola_logger.info("stop")


#lista per i log

# creo la lista
lista = ft.ListView(spacing=10, padding=20, width=300, auto_scroll=True)

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
    

   
