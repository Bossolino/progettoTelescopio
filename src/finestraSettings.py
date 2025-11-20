import flet as ft
from config import tema
from seriale import porta_seriale, nome_device, getPorteDisponibili
import serial.tools.list_ports
import json

def init_settings(): #print(data["application"]["tema"])
    global tema, porta_seriale, nome_device
    with open("src/assets/settings.json", "r") as f:
        data = json.load(f)
    tema = data["application"]["tema"]
    porta_seriale = data["application"]["portaSeriale"]
    nome_device = data["application"]["nomeDevice"]

def setSetting(setting: str, new_value):
    with open("src/assets/settings.json", "r") as f:
        data = json.load(f)
    data["application"][setting] = new_value
    with open("src/assets/settings.json", "w") as f:
        json.dump(data, f, indent=4)
    return

def editNome(nome:str):
    global nome_device
    nome_device = nome
    print(nome_device)
    return nome_device

def finestraSettings(page: ft.Page):

    page.title = "Ïmpostazioni"
    page.theme_mode = tema
    page.window.maximized = True
    page.window.focused = True

    def init_settings_fields():
        #init TEMA
        global tema, nome_device

        dropdownTema.value = tema
        print(dropdownTema.value)
        if dropdownTema.value == "LIGHT":
            tema = ft.ThemeMode.LIGHT
            dropdownTema.leading_icon=ft.Icons.LIGHT_MODE
        elif dropdownTema.value == "DARK":
            tema = ft.ThemeMode.DARK
            dropdownTema.leading_icon=ft.Icons.DARK_MODE
        else:
            tema = ft.ThemeMode.SYSTEM
            dropdownTema.leading_icon=ft.Icons.COMPUTER
        page.theme_mode = tema
        #init PORTA
        porte_disp = getPorteDisponibili()
        for porta, nome in porte_disp.items():
            print(porta)
            dropdownPorta.options.append(ft.DropdownOption(key=f"{porta}", text=f"{porta} : {nome}"))
        global porta_seriale
        if porta_seriale != "":
            dropdownPorta.value = porta_seriale
        else:
            dropdownPorta.value = " "
        #print(dropdownPorta.value)
        #init NOME
        if nome_device != "":
            txtfield_nome_device.value = nome_device
        page.update()

    def getSelectionTheme(e):
        global tema
        print(e)
        selezione = e.data
        print(selezione)
        if selezione == "DARK":
            tema = ft.ThemeMode.DARK
            dropdownTema.leading_icon=ft.Icons.DARK_MODE
        elif selezione == "LIGHT":
            tema = ft.ThemeMode.LIGHT
            dropdownTema.leading_icon=ft.Icons.LIGHT_MODE
        elif selezione == "SYSTEM":
            tema = ft.ThemeMode.SYSTEM
            dropdownTema.leading_icon=ft.Icons.COMPUTER
        page.theme_mode = tema
        page.update()

    dropdownTema = ft.Dropdown(
        options=[
            ft.DropdownOption(key="DARK", text="Scuro", leading_icon=ft.Icons.DARK_MODE),
            ft.DropdownOption(key="LIGHT", text="Chiaro", leading_icon=ft.Icons.LIGHT_MODE),
            ft.DropdownOption(key="SYSTEM", text="Sistema", leading_icon=ft.Icons.COMPUTER)
        ], on_change= getSelectionTheme, leading_icon="", label="Tema dell'applicazione"
    )

    txtfield_nome_device = ft.TextField(label="Nome del device", hint_text="Inserisci il nome del device",on_change=lambda e: setSetting("nomeDevice",e.data))

    dropdownPorta = ft.Dropdown(
        options=[ft.DropdownOption(key=" ", text="Seleziona...", disabled=True)], label="Porta del device"
    )

    btn_home = ft.ElevatedButton(icon=ft.Icons.ARROW_LEFT, text="HOME")

    navbar = ft.Row([btn_home])
    body = ft.Row([dropdownTema, dropdownPorta, txtfield_nome_device], spacing=50)
    finestra = ft.Column([navbar,body], spacing=100)

    # Layout principale
    layout = ft.Column(
        [navbar, body],
        alignment=ft.MainAxisAlignment.START, # allinea gli elementi in colonna dall'inizio in verticale
        horizontal_alignment=ft.CrossAxisAlignment.START, # allinea gli elementi in colonna al centro orizzontalmente
        expand=True,  #  importantissimo: riempie tutta la finestra
    )

    init_settings()
    init_settings_fields()
    page.add(layout)
    page.update()
