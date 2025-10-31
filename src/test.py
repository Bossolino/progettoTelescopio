import flet as ft

from config import *

def main(page: ft.Page):
    # 🔹 imposta la pagina a espandere completamente la finestra
    page.title = "Footer fisso in fondo"
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    def sposta_c_destra(sposta: int):
        sposta_cupola_destra(sposta)
    def sposta_c_sinistra(sposta: int):
        sposta_cupola_sinistra(sposta)


    # Navbar
    navbar = ft.Container(
        ft.Text("NAVBAR", size=20, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        height=60,
        expand=False,
    )

    # Contenuto centrale
    centro = ft.Container(
        ft.Text("CONTENUTO CENTRALE", size=18),
        alignment=ft.alignment.center,
        expand=True,  # 🔹 si espande verticalmente e spinge il footer in basso
    )

    # Footer (può essere Row o Column)
    footer = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton("Sinistra"),
                ft.ElevatedButton("Destra"),
                ft.ElevatedButton("Stop"),
                ft.ElevatedButton("Reset"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        height=80,
        bgcolor=ft.Colors.BLUE_50,
        alignment=ft.alignment.center,
        expand=False,  # 🔹 il footer NON deve espandersi
    )

    # Layout principale
    layout = ft.Column(
        [navbar, centro, footer],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,  # 🔹 importantissimo: riempie tutta la finestra
    )

    page.add(layout)

ft.app(main)
