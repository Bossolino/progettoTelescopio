import flet as ft
from seriale import getPorteDisponibili
import serial.tools.list_ports
import json
from pages import router
from settings import settings

def finestraSettings(page: ft.Page):
    page.title = "Impostazioni"
    page.theme_mode = settings.page.theme
    page.window.width = settings.page.windowWidth
    page.window.height = settings.page.windowHeight

    def init_settings_fields():
        #init TEMA
        global settings
        print(f"init Tema dropdown: {dropdownTema.value}")
        print(f"settings theme: {settings.page.theme}")
        if settings.page.theme == ft.ThemeMode.LIGHT or settings.page.theme == "LIGHT":
            dropdownTema.value = "LIGHT"
            settings.page.theme = ft.ThemeMode.LIGHT
            dropdownTema.leading_icon=ft.Icons.LIGHT_MODE
        elif settings.page.theme== ft.ThemeMode.DARK or settings.page.theme == "DARK":
            dropdownTema.value = "DARK"
            settings.page.theme = ft.ThemeMode.DARK
            dropdownTema.leading_icon = ft.Icons.DARK_MODE
        elif settings.page.theme == ft.ThemeMode.SYSTEM or settings.page.theme == "SYSTEM":
            dropdownTema.value = "SYSTEM"
            settings.page.theme = ft.ThemeMode.SYSTEM
            dropdownTema.leading_icon=ft.Icons.COMPUTER
        page.theme_mode = settings.page.theme
        #init PORTA
        porte_disp = getPorteDisponibili()
        if len(porte_disp) != 0:
            for porta, nome in porte_disp.items():
                print(f"porta: {porta}")
                dropdownPorta.options.append(ft.DropdownOption(key=f"{porta}", text=f"{porta} : {nome}"))
                if settings.seriale.porta_seriale == porta:
                    dropdownPorta.value = porta
            if settings.seriale.porta_seriale != "":
                dropdownPorta.value = settings.seriale.porta_seriale
            else:
                dropdownPorta.value = " "
        else: 
            dropdownPorta.options.append(ft.DropdownOption(key=f"none", text=f"Nessun devide trovato"))
            dropdownPorta.value = "none"
            dropdownPorta.disabled = True
        #print(dropdownPorta.value)
        page.update()

    def getSelectionTheme(e):
        global settings
        print(e)
        selezione = e.data
        print(f"selezione: {selezione}")
        if selezione == "DARK":
            settings.page.theme = ft.ThemeMode.DARK
            dropdownTema.leading_icon=ft.Icons.DARK_MODE
        elif selezione == "LIGHT":
            settings.page.theme = ft.ThemeMode.LIGHT
            dropdownTema.leading_icon=ft.Icons.LIGHT_MODE
        elif selezione == "SYSTEM":
            settings.page.theme = ft.ThemeMode.SYSTEM
            dropdownTema.leading_icon=ft.Icons.COMPUTER
        settings.setSetting("page","tema", selezione)
        page.theme_mode = settings.page.theme
        page.update()

    def initLabelNome():
        return settings.seriale.nome_device

    dropdownTema = ft.Dropdown(
        options=[
            ft.DropdownOption(key="DARK", text="Scuro", leading_icon=ft.Icons.DARK_MODE),
            ft.DropdownOption(key="LIGHT", text="Chiaro", leading_icon=ft.Icons.LIGHT_MODE),
            ft.DropdownOption(key="SYSTEM", text="Sistema", leading_icon=ft.Icons.COMPUTER)
        ], on_change= getSelectionTheme, leading_icon="", label="Tema dell'applicazione"
    ) 
    
    #settings.setSetting("seriale","nomeDevice",e.data)

    dropdownPorta = ft.Dropdown(
        options=[ft.DropdownOption(key=" ", text="Seleziona...", disabled=True)], label="Porta del device", on_change=settings.seriale.savePorta
    )

    btn_home = ft.ElevatedButton(icon=ft.Icons.ARROW_LEFT, text="HOME", on_click= lambda e: router.go("home", page))

    navbar = ft.Row([btn_home])
    body = ft.Row([dropdownTema, dropdownPorta], spacing=50)
    finestra = ft.Column([navbar,body], spacing=100)

    # Layout principale
    layout = ft.Column(
        [finestra],
        alignment=ft.MainAxisAlignment.START, # allinea gli elementi in colonna dall'inizio in verticale
        horizontal_alignment=ft.CrossAxisAlignment.START, # allinea gli elementi in colonna al centro orizzontalmente
        expand=True,  #  importantissimo: riempie tutta la finestra
    )

    
    init_settings_fields()
    initLabelNome()
    page.add(layout)
    return layout
