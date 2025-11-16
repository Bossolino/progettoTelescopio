import flet as ft
from pathlib import Path
from config import tema



def main(page: ft.Page):
     #impostazioni pagina
    page.title = "HOME"
    page.padding = 30
    page.spacing = 20
    page.theme_mode = tema

    isClear = True



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
            opzioni.append(ft.DropdownOption(key = i["path"], text=i["nome"]))
        return opzioni
    

    

    contenuto = ft.ListView(spacing=20, padding=20, auto_scroll=True, expand=True)
    def clear():
        nonlocal isClear
        contenuto.controls.clear()
        isClear = not isClear
        print("fai schifo merda")
        pulsante_clear.disabled = not isClear
        page.update()

    pulsante_clear = ft.ElevatedButton(
        text="clear",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: clear()
    )


    def new_riga(riga : str):
        contenuto.controls.append(ft.Text(riga.strip(), color=ft.Colors.WHITE))


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
            if contenuto.controls != None:
                isClear = True
            pulsante_clear.disabled = not isClear
            page.update()


    def selezione(e): # quando viene selezionata un opzione
        print("Selezionato:", e.control.value)
        carica_contenuto(e.control.value)
        page.update()

    select = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        enable_filter=True,
        editable=True,
        leading_icon=ft.Icons.SEARCH,
        expand=True,
        label="Giorno",
        options=crea_opzioni(nomiFile),
        on_change=selezione,
    )

    layout = ft.Column(
        [select, contenuto],
        alignment=ft.MainAxisAlignment.CENTER, # allinea gli elementi in colonna dall'inizio in verticale
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # allinea gli elementi in colonna al centro orizzontalmente

    )

    page.add(layout, pulsante_clear)

ft.app(main)