import flet as ft


def main(page: ft.Page):
   
    p_destra = ft.Button(text="Pulsante Destra")
    p_sinistra = ft.Button(text="Pulsante Sinistra")
    p_stop = ft.Button(text="Pulsante Stop")
    p_reset = ft.Button(text="Pulsante Reset")

    navbar = ft.Row()
    centro = ft.Row()
    footer = ft.Row()
    centro.controls.append(p_sinistra)
    centro.controls.append(p_destra)
    centro.controls.append(p_stop)
    centro.controls.append(p_reset)
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    navbar,
                    ft.Column(
                        centro,
                        expand=True,
                    ),
                    footer,
                ],
            expand=True,
            )
        )
    )


ft.app(main)
