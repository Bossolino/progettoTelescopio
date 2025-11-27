import flet as ft
from pages import router

def main(page: ft.Page):
    router.go("home", page)

ft.app(target=main)