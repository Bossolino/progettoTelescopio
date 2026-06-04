import flet as ft
from pathlib import Path
from settings import settings
from pages import router

def finestraLog(page: ft.Page):
    #impostazioni pagina
    page.title = "log"
    page.padding = 30
    page.spacing = 20
    page.theme_mode = settings.page.theme
    page.window_width = settings.page.windowWidth   # larghezza finestra
    page.window_height = settings.page.windowHeight   # altezza finestra

    isClear = True #per abilitare il pulsante clear che tanto se abilita lo stesso

    btn_home = ft.ElevatedButton(icon=ft.Icons.ARROW_LEFT, text="HOME", on_click= lambda e: router.go("home", page))


    # nomiFile = ["giorno 1", "froci", "pezzi di merda", "src/fileLog/spostamenti.log"] # vanno passati i nomi dei file
    nomiFile = [
        {"nome" : "giorno 1", "path" : ""},
        {"nome" : "froci", "path" : ""},
        {"nome" : "pezzi di merda", "path" : ""},
        {"nome" : "file log", "path" : "src/fileLog/spostamenti.log"},
    ]
    
    
    def crea_opzioni(nomiFile): # creo le opzioni
        opzioni = []
        for i in nomiFile:
            opzioni.append(ft.DropdownOption(key = i["path"], text=i["nome"])) # opzioni
        return opzioni
    

    
    # contenuto del file
    contenuto = ft.ListView(spacing=10, padding=10, auto_scroll=True, expand=True)
    # funzione per eliminare cio che si vede a nel contenuto
    def clear():
        nonlocal isClear
        contenuto.controls.clear()
        isClear = not isClear
        print("fai schifo merda")
        pulsante_clear.disabled = not isClear # disabilito il pulsante in base allo stato della variabile
        page.update()

    pulsante_clear = ft.ElevatedButton( # pulsante per eliminare
        text="clear",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: clear() # richiamo la funzione clear () al click
    )


    def new_riga(riga : str):
        contenuto.controls.append(ft.Text(riga.strip(), color=ft.Colors.WHITE)) # aggiungo le righe


    def carica_contenuto(nome_file):
        nonlocal isClear
        file_path = Path(nome_file)

        if not file_path.exists(): # se non esiste il file non fa nulla
            return
        
        # Legge solo le nuove righe
        with open(file_path, "r") as f:

            righe = f.readlines() 
            for riga in righe:
                new_riga(riga)
                print(riga)
            if contenuto.controls != None:
                isClear = True
            pulsante_clear.disabled = not isClear
            page.update()


    def selezione(e): # quando viene selezionata un opzione
        print("Selezionato:", e.control.value)
        clear()
        carica_contenuto(e.control.value)
        page.update()

    select = ft.Dropdown(  # creazione select
        border=ft.InputBorder.UNDERLINE,
        enable_filter=True,
        editable=True,
        leading_icon=ft.Icons.SEARCH,
        expand=True,
        label="Giorno",
        options=crea_opzioni(nomiFile),
        on_change=selezione,
    )

    header = ft.Row(
        [
            btn_home,
            pulsante_clear
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    body = ft.Container(
        content=ft.Column(
            [
                select,
                contenuto
            ],
            expand=True
        ),
        expand=True
    )

    layout = ft.Column(
        [
            header,
            body
        ],
        expand=True
    )


    # page.add(layout)
    page.update()
    return layout