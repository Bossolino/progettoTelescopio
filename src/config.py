c_cupola = "0"
c_telescopio = "1"

def sposta_cupola_destra(sposta: int):
    global c_cupola
    c_cupola = str(int(c_cupola) + sposta)
    print(f"Cupola spostata a destra di {sposta}. Nuova posizione: {c_cupola}")

def sposta_cupola_sinistra(sposta: int):
    global c_cupola
    c_cupola = str(int(c_cupola) - sposta)
    print(f"Cupola spostata a sinistra di {sposta}. Nuova posizione: {c_cupola}")

def reset_posizioni():
    global c_cupola, c_telescopio
    c_cupola = c_telescopio
    print("Posizioni resettate")
def stop_movimento():
    print("Movimento fermato")