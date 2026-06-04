import serial
import serial.tools.list_ports
import threading
from fileLog.Log import logger_seriale
from settings import settings
import time

ser = None
thread_ascolto = None
refresh_callback = None
serial_lock = threading.Lock()  # evita conflitti tra ascolto e set_pos


def set_refresh_callback(cb):
    global refresh_callback
    refresh_callback = cb


def getPorteDisponibili():
    porte = {}
    porte_computer = serial.tools.list_ports.comports()
    for porta in porte_computer:
        porte[porta.device] = porta.description
        print(f"{porte[porta.device]}")
    return porte


porte = getPorteDisponibili()


def setPorta():
    global porte
    for device, desc in porte.items():
        if desc == settings.seriale.nome_device:
            settings.seriale.porta_seriale = device
            return device
    logger_seriale.error("Dispositivo non trovato!")
    return False


def start_ascolto(porta: str):
    global ser, thread_ascolto
    if settings.seriale.porta_seriale == "":
        return logger_seriale.error("Porta seriale non indicata!")
    if settings.seriale.porta_seriale in porte:
        settings.seriale.ascolta = True
        ser = serial.Serial(port=porta, baudrate=9600, timeout=1)
        thread_ascolto = threading.Thread(target=ascolto, daemon=True)
        try:
            thread_ascolto.start()
            print("Thread avviato!")
            logger_seriale.info("Thread avviato!")
        except Exception as e:
            print("Thread non avviato!")
            logger_seriale.error(f"Thread non avviato: {e}")
    else:
        logger_seriale.error(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")
        print(f"La porta seriale {settings.seriale.porta_seriale} non è disponibile.")


def init_ascolto(ser: serial.Serial):
    logger_seriale.info("Attendo boot Arduino...")
    time.sleep(3)
    ser.reset_input_buffer()

    deadline = time.time() + 10  # riprova per max 10 secondi
    while time.time() < deadline:
        ser.write(b"POS\n")
        time.sleep(0.6)

        raw = ser.readline()
        logger_seriale.info(f"RAW: {raw}")

        if not raw:
            logger_seriale.warning("Nessuna risposta, riprovo...")
            continue

        riga = raw.decode('utf-8', errors='ignore').strip()
        logger_seriale.info(f"Decodificato: '{riga}'")

        # Risposta attesa: POS;42
        if riga.startswith("POS;"):
            try:
                valore = int(riga.split(";")[1])
                settings.seriale.pos_cup = valore
                settings.seriale.ready = True
                logger_seriale.info(f"Init OK — posizione: {valore}°")
                return True
            except ValueError:
                logger_seriale.error(f"Valore non parsabile: '{riga}'")

        # Arduino manda POS=42 dall'encoder durante il boot
        elif riga.startswith("POS="):
            try:
                valore = int(riga.split("=")[1])
                settings.seriale.pos_cup = valore
                settings.seriale.ready = True
                logger_seriale.info(f"Init OK via POS= — posizione: {valore}°")
                return True
            except ValueError:
                logger_seriale.error(f"Valore non parsabile: '{riga}'")

        else:
            logger_seriale.warning(f"Risposta ignorata: '{riga}', riprovo...")

    logger_seriale.error("Init fallita: timeout dopo 10 secondi.")
    return False


def ascolto():
    global ser
    settings.seriale.inAscolto = True

    if not init_ascolto(ser):
        logger_seriale.error("Ascolto interrotto: init fallita.")
        settings.seriale.inAscolto = False
        return

    logger_seriale.info(f"Posizione iniziale: {settings.seriale.pos_cup}°")

    while settings.seriale.ascolta:
        try:
            with serial_lock:
                dato = ser.readline()

            dato_str = dato.decode('utf-8', errors='ignore').strip()
            if not dato_str:
                continue

            if dato_str.startswith("POS="):
                try:
                    pos = int(dato_str.split("=")[1])
                    settings.seriale.pos_cup = pos
                    logger_seriale.info(f"Encoder: {pos}°")
                    if refresh_callback:
                        refresh_callback()
                except ValueError:
                    logger_seriale.warning(f"Valore non numerico: '{dato_str}'")

            elif dato_str == "BTN":
                logger_seriale.info("Pulsante premuto")

            elif dato_str.startswith("OK"):
                logger_seriale.info(f"Conferma Arduino: {dato_str}")

            elif dato_str.startswith("ERR"):
                logger_seriale.error(f"Errore Arduino: {dato_str}")

            else:
                logger_seriale.warning(f"Messaggio non riconosciuto: '{dato_str}'")

        except Exception as e:
            logger_seriale.error(f"Errore seriale: {e}")
            break

    print("Thread chiuso.")
    logger_seriale.info("Thread chiuso.")


def set_pos(target_pos: int):
    """Muove la cupola alla posizione assoluta target_pos (-180..+180)."""
    if not (-180 <= target_pos <= 180):
        logger_seriale.error(f"Posizione non valida: {target_pos}")
        return

    global ser
    delta = target_pos - settings.seriale.pos_cup
    if delta == 0:
        return

    cmd = f"{'CW' if delta > 0 else 'CCW'};{abs(delta)}\n"

    with serial_lock:  # blocca il thread di ascolto durante l'invio
        try:
            ser.write(cmd.encode())
            logger_seriale.info(f"Inviato: {cmd.strip()} (da {settings.seriale.pos_cup}° a {target_pos}°)")

            raw = ser.readline()
            riga = raw.decode('utf-8', errors='ignore').strip()
            logger_seriale.info(f"Risposta set_pos: {riga}")

            if riga.startswith("OK"):
                # Arduino risponde "OK CW 42" o "OK CCW -10"
                parts = riga.split(" ")
                if len(parts) == 3:
                    try:
                        settings.seriale.pos_cup = int(parts[2])
                        if refresh_callback:
                            refresh_callback()
                    except ValueError:
                        logger_seriale.error(f"Posizione non parsabile nella risposta: '{riga}'")
            elif riga.startswith("ERR"):
                logger_seriale.error(f"Arduino ha rifiutato il comando: {riga}")

        except Exception as e:
            logger_seriale.error(f"Errore set_pos: {e}")


def stop_ascolto(e=None):
    global thread_ascolto, ser
    if thread_ascolto and thread_ascolto.is_alive():
        settings.seriale.ascolta = False
        thread_ascolto.join(timeout=2)

        if ser and ser.is_open:
            ser.close()

        print("✓ Thread fermato")
        logger_seriale.info("Thread fermato.")