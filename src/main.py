import flet as ft
from pages import router
from settings import settings

def main(page: ft.Page):
    settings.init_settings()
    from seriale import stop_ascolto
    page.on_close = stop_ascolto
    router.go("home", page)
    

ft.app(target=main)