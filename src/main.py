import flet as ft
from pages import router
from settings import settings

def main(page: ft.Page):
    router.go("home", page)
    settings.init_settings()

ft.app(target=main)