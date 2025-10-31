import flet as ft


def main(page: ft.Page):
   
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Text("PROVA FILE COLLEGAMENTO GIT"),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
