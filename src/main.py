import flet as ft
from config import *
import config
from seriale import start_ascolto


def main(page: ft.Page):

    #impostazioni pagina
    page.title = "HOME"
    page.padding = 30
    page.spacing = 20
    page.theme_mode = tema
    page.window.maximized = True
    page.window.focused = True
       

    start_ascolto()# avvio l'ascolto sulla porta seriale

    # Testi coordinate
    c_cupola_testo = ft.Text(f"coordinata Cupola: {c_cupola}", size=16)
    c_telescopio_testo = ft.Text(f"coordinata Telescopio: {c_telescopio}", size=16)

    #funzioni dei pulsanti per aggiornare le coordinate e la pagina
    def sposta_c_destra(sposta: int):
        sposta_cupola_destra(sposta)
        c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
        page.update()
    def sposta_c_sinistra(sposta: int):
        sposta_cupola_sinistra(sposta)
        c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
        page.update()
    def r_posizioni():
        reset_posizioni()
        c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
        c_telescopio_testo.value = f"coordinata Telescopio: {config.c_telescopio}"
        page.update()
    
    #textField per input coordinate
    input_destra = ft.TextField(label="Input destra", value=str(c_cupola), width=100)
    input_sinistra = ft.TextField(label="Input sinistra", value=str(c_telescopio) , width=100)

    # Pulsanti
    p_destra = ft.ElevatedButton(text=" ", icon=ft.Icons.ARROW_RIGHT, on_click=lambda e: sposta_c_destra(input_destra.value and int(input_destra.value) or 0))
    p_sinistra = ft.ElevatedButton(text=" ", icon=ft.Icons.ARROW_LEFT, on_click=lambda e: sposta_c_sinistra(input_sinistra.value and int(input_sinistra.value) or 0))
    p_stop = ft.ElevatedButton(text="Pulsante Stop", icon=ft.Icons.STOP, on_click=lambda e: stop_movimento())
    p_reset = ft.ElevatedButton(text="Pulsante Reset", icon=ft.Icons.REFRESH, on_click=lambda e: r_posizioni())

    

    # Navbar e centro
    navbar = ft.Row(
        [c_cupola_testo, c_telescopio_testo], #aggiunti i testi delle coordinate
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # allinea gli elementi in modo EVENLY orizzontalmente
        vertical_alignment=ft.CrossAxisAlignment.CENTER, # allinea gli elementi al centro verticalmente
        height=60,
    )

    centro = ft.Container(
        ft.Text("CONTENUTO CENTRALE", size=18),
        alignment=ft.alignment.center,
        expand=True,  # si espande verticalmente e spinge il footer in basso
    )

    # Footer
    r_frecce = ft.Row( # righe per i pulsanti delle frecce destra e sinistra
        [p_sinistra,input_sinistra,  input_destra, p_destra],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50,
    )
    r_stop_reset = ft.Row( # righe per i pulsanti di stop e reset
        [p_stop, p_reset],
        alignment=ft.MainAxisAlignment.CENTER, 
        spacing=50,
    )
    footer = ft.Container( 
        ft.Column(
            [r_frecce, r_stop_reset],
            alignment=ft.MainAxisAlignment.CENTER, #centro il contenuto della colonna orizzontalmente
            spacing=50, # so uno spazio di 50px tra le righe
        ),
        alignment=ft.alignment.center,
        expand=False,
    )

    log_list = ft.Column()

    def show_list (e):
        log_list.visible = not log_list.visible
        page.update()

    switch_show = ft.Switch(
        thumb_icon=ft.Icons.LIST_OUTLINED,
        value=True,
        label="Log",
        label_position=ft.LabelPosition.RIGHT,
        on_change=show_list,
    )

    log_list.controls.append(
            ft.Row(
                [config.new_lista_log(page, "src/fileLog/spostamenti.log")],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )
    

    # Layout principale
    layout = ft.Column(
        [navbar, centro, footer],
        alignment=ft.MainAxisAlignment.START, # allinea gli elementi in colonna dall'inizio in verticale
        horizontal_alignment=ft.CrossAxisAlignment.START, # allinea gli elementi in colonna al centro orizzontalmente
        expand=True,  #  importantissimo: riempie tutta la finestra
    )

    log_layout = ft.Row(
        [log_list,switch_show],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(
        ft.Row(
            [log_layout,layout],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,),
    )

ft.app(main)
