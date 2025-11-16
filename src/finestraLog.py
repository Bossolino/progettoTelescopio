import flet as ft
from pathlib import Path



def main(page: ft.Page):
     #impostazioni pagina
    page.title = "HOME"
    page.padding = 30
    page.spacing = 20
    page.dark_theme



    nomiFile = ["giorno 1", "froci", "pezzi di merda", "src/fileLog/spostamenti.log"] # vanno passati i nomi dei file
    
    
    def crea_opzioni(nomiFile): # creo le opzioni
        opzioni = []
        for i in nomiFile:
            opzioni.append(ft.DropdownOption(key = i))
        return opzioni
    



    contenuto = ft.ListView(spacing=10, padding=20, width=300, auto_scroll=True)

    def new_riga(riga : str):
        contenuto.controls.append(ft.Text(riga.strip(), color=ft.Colors.WHITE))

    def carica_contenuto(nome_file):
        file_path = Path(nome_file)

        if not file_path.exists(): # se non esiste il file non fa nulla
            return
        
        # Legge solo le nuove righe
        with open(file_path, "r") as f:

            righe = f.readlines() 
            for riga in righe:
                new_riga(riga)

    def selezione(e):
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

    page.add(select, contenuto)

ft.app(main)