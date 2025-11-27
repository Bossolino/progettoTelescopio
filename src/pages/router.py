import flet as ft
from pages.finestraHome import home
from pages.finestraSettings import finestraSettings
from pages.finestraLog import finestraLog

pages = {
    "home": home,
    "settings": finestraSettings,
    "log": finestraLog
}

def go(dest: str, page: ft.Page):
    print("vado a ", dest)
    page.clean()
    nuova_vista = pages[dest](page)
    page.add(nuova_vista)
    page.update()

def main(page: ft.Page):
    go("home", page)
