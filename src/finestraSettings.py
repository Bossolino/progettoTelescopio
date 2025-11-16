import flet as ft
from config import tema

def finestraSettings(page: ft.Page):

    page.title = "Ïmpostazioni"
    page.theme_mode = tema

    def init_setting():
        dropdown.value = "ThemeMode.DARK"
        dropdown.leading_icon=ft.Icons.DARK_MODE
        page.update()

    def getSelection(e):
        global tema
        selezione = e.control.value
        print(selezione)
        if "DARK" in selezione:
            tema = ft.ThemeMode.DARK
            dropdown.leading_icon=ft.Icons.DARK_MODE
        elif "LIGHT" in selezione:
            tema = ft.ThemeMode.LIGHT
            dropdown.leading_icon=ft.Icons.LIGHT_MODE
        else:
            tema = ft.ThemeMode.SYSTEM
            dropdown.leading_icon=ft.Icons.COMPUTER
        page.theme_mode = tema
        page.update()

    dropdown = ft.Dropdown(
        options=[
            ft.DropdownOption(key="DARK", text="Scuro", leading_icon=ft.Icons.DARK_MODE), 
            ft.DropdownOption(key="LIGHT", text="Chiaro", leading_icon=ft.Icons.LIGHT_MODE), 
            ft.DropdownOption(key="SYSTEM", text="Sistema", leading_icon=ft.Icons.COMPUTER)
        ], on_change= getSelection, leading_icon=""
        
    )

    body = ft.Row([dropdown])

    page.add(body)
    init_setting()

ft.app(target=finestraSettings)
