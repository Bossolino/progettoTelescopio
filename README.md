# 🛰️ Progetto "Osservatorio Astronomico"

## 🎓 Descrizione generale
Il progetto **"Osservatorio Astronomico"** nasce dalla collaborazione tra le classi di **Elettronica** e **Informatica** dell’Istituto Tecnico Tecnologico “Leonardo da Vinci” di Foligno.  
L’obiettivo è realizzare un **sistema automatizzato per il controllo della cupola di un osservatorio astronomico**, sincronizzato con la posizione del telescopio gestito tramite software professionale **MaxIm DL**.

Il progetto integra competenze **hardware** e **software** per simulare il funzionamento di un vero osservatorio automatizzato.

---

## 💻 Gruppo Software

### 🎯 Obiettivo generale
Progettare e realizzare un **programma in Python**, con interfaccia grafica sviluppata in **Flet**, che permetta di:
- **Comunicare con il driver ASCOM** del telescopio per leggere le coordinate in tempo reale (Alt/Az).
- **Inviare comandi di controllo** (rotazione, apertura, chiusura, reset, ecc.) alla **scheda elettronica** che gestisce la cupola.
- **Monitorare lo stato del sistema** e fornire feedback visivo all’utente.
- **Testare e collaudare** il sistema in simulazione o con dispositivi reali.
- **Collaborare con il gruppo documentazione** per integrare manuali tecnici e relazioni di progetto.

---

## 🧩 Attività principali del gruppo software
1. **Analisi del problema**
   - Studio della sincronizzazione tra telescopio e cupola motorizzata.
   - Identificazione dei requisiti funzionali e delle interfacce di comunicazione.
   - Definizione dei comandi da inviare al microcontrollore.

2. **Progettazione**
   - Studio dell’interfaccia **ASCOM** e delle librerie Python necessarie (`pywin32`, `pythonnet`).
   - Definizione del **protocollo di comunicazione seriale** (USB/COM).
   - Creazione dei **diagrammi di flusso** e dell’**architettura software**.
   - Progettazione della **GUI con Flet**, semplice, intuitiva e funzionale.

3. **Sviluppo**
   - Implementazione del programma in Python con moduli dedicati a:
     - **Comunicazione ASCOM**: lettura delle coordinate del telescopio.
     - **Controllo hardware**: invio dei comandi seriali al microcontrollore.
     - **Interfaccia grafica Flet**: gestione pulsanti, indicatori di stato, log attività e finestre di controllo.
   - Test del codice tramite **ASCOM Telescope Simulator** o telescopio reale.

4. **Collaudo e validazione**
   - Verifica del corretto funzionamento del sistema integrato (software + hardware).
   - Test della sincronizzazione automatica cupola/telescopio.
   - Debug e ottimizzazione della comunicazione e della GUI.

---

## 🧠 Obiettivi formativi e competenze

### Obiettivi specifici
- Progettare un **software di interfacciamento utente** per un sistema di controllo automatizzato.
- Integrare componenti **hardware e software** in un unico sistema funzionante.
- Acquisire e utilizzare **dati da dispositivi esterni** tramite driver ASCOM.
- Applicare **protocolli di comunicazione seriale** per dispositivi embedded.
- Realizzare un’interfaccia utente **moderna con Flet**, reattiva e facile da usare.
- Produrre una **documentazione tecnica completa** (manuale utente, relazione, presentazione).
- Lavorare in **team interdisciplinari**, rispettando tempi e ruoli.

### Competenze in uscita
- Sviluppo di software Python per la comunicazione con dispositivi esterni.
- Gestione di driver ASCOM e protocolli seriali.
- Realizzazione di **GUI professionali con Flet**.
- Documentazione chiara e completa di progetti tecnici.
- Capacità di collaborazione, problem solving e gestione autonoma delle attività.

---

## 🧰 Strumenti utilizzati
- **Python 3.x**
  - Librerie: `flet`, `pywin32`, `pythonnet`, `serial`
- **ASCOM Platform** e **ASCOM Telescope Simulator**
- **Microcontrollore** (es. Arduino, ESP32, STM32)
- **Software di documentazione**: Word, PowerPoint, Draw.io
- **Editor di codice**: VS Code / PyCharm

---

## 🖥️ Interfaccia Grafica con Flet
L’interfaccia sarà sviluppata con **[Flet](https://flet.dev)**, un framework moderno per Python che consente di creare applicazioni web, desktop e mobile con componenti reattivi.  
La GUI dovrà includere:
- Pulsanti di **apertura/chiusura cupola** e **rotazione**.
- Indicatori visivi di **stato del sistema** (connessione, errori, posizione).
- Una **console log** per mostrare comunicazioni e messaggi diagnostici.
- Una sezione per **configurazione** (porte seriali, parametri di connessione).

---

## 📦 Prodotto finale
- Software Python funzionante che sincronizza **cupola e telescopio**.  
- **Interfaccia grafica Flet** con funzioni di controllo e monitoraggio.  
- **Documentazione tecnica completa**, con manuale utente, schemi e relazione.  
- **Presentazione multimediale** del progetto per la valutazione finale.

---

## 👥 Gruppo Software – Ruoli consigliati
| Ruolo | Descrizione |
|-------|--------------|
| **Project Manager** | Coordina il lavoro e gestisce tempi e attività. |
| **Programmatore principale** | Sviluppa il codice Python e l’integrazione ASCOM. |
| **UI Designer / Flet Developer** | Progetta e realizza l’interfaccia grafica. |
| **Tester** | Esegue test e debug del sistema completo. |
| **Documentalista tecnico** | Cura la stesura del manuale e dei diagrammi. |

---

## 🧾 Valutazione
La valutazione del gruppo software terrà conto di:
- Correttezza e funzionalità del codice.  
- Qualità e usabilità dell’interfaccia Flet.  
- Completezza della documentazione.  
- Capacità di collaborazione e autonomia nel lavoro.  
- Presentazione finale del progetto.

---

## 📅 Durata stimata
**Totale: 20 ore**
- Analisi e progettazione: 6 ore  
- Sviluppo e test: 8 ore  
- Collaudo e presentazione: 6 ore  

---

> ✨ *"Un osservatorio automatizzato è il risultato dell’unione tra elettronica, software e passione per l’innovazione. Ogni riga di codice contribuisce a far muovere la volta celeste sullo schermo."*
