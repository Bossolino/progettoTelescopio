import flet as ft


def main(page: ft.Page):
   
    navbar = ft.Row()
    centro = ft.Row()
    footer = ft.Row()

    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    navbar,
                    ft.Container(
                        centro,
                        expand=True,
                    ),
                    footer,
                ],
            expand=True,
        )
    )


ft.app(main)
