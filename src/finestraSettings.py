import flet as ft
import config

def finestraSettings():
    
    body = ft.Row(
        [ft.Dropdown([
            ft.DropdownOption(key=f"{ft.ThemeMode.DARK}", text="Scuro"),
            ft.DropdownOption(key=f"{ft.ThemeMode.LIGHT}", text="Chiaro"),
            ft.DropdownOption(key=f"{ft.ThemeMode.SYSTEM}", text="Sistema")       
        ])]
    )

    finestra = ft.Container(
        [body]
    )