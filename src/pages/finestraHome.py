import flet as ft # type: ignore
import config
from seriale import start_ascolto
from flet_video import Video, VideoMedia
from pages import router
from settings import settings

def home(page: ft.Page):
    bLog = ft.ElevatedButton(text="Mostra Log", on_click=lambda e: router.go("log",page), icon_color=ft.Colors.WHITE)
    bSetting = ft.IconButton(icon=ft.Icons.SETTINGS, on_click=lambda e: router.go("settings",page), icon_color=ft.Colors.WHITE, icon_size=35, alignment=ft.alignment.top_right)
    bClear = ft.IconButton(icon=ft.CupertinoIcons.TRASH_CIRCLE, on_click=lambda e: clear_log(), icon_color=ft.Colors.WHITE, icon_size=35)
    
    page.window.width = 1400#page_width
    page.window.height = 700#page_height

    #impostazioni pagina
    page.title = "HOME"
    page.padding = 30
    page.spacing = 20
    global settings
    page.theme_mode = settings.page.theme
    page.bgcolor = "#222222"
    
    
    start_ascolto()# avvio l'ascolto sulla porta seriale
    
    # per la cronologia
    def add_log(messaggio: str):
        log_entry = ft.Text(messaggio, size=12, color=ft.Colors.GREY_400)
        log_list.controls.insert(0, log_entry)  # aggiunge in cima
        page.update()
        
    # per il clear della cronologia
    def clear_log():
        log_list.controls.clear()
        page.update()
        
    # Testi coordinate
    c_cupola_testo = ft.Text(f"coordinata Cupola: {config.c_cupola}", size=16)
    c_telescopio_testo = ft.Text(f"coordinata Telescopio: {config.c_telescopio}", size=16)

    #funzioni dei pulsanti per aggiornare le coordinate e la pagina
    def sposta_c_destra(sposta: int):
        msg = config.sposta_cupola_destra(sposta)
        if msg:
            add_log(msg)
            c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
            page.update()
    def sposta_c_sinistra(sposta: int):
        msg = config.sposta_cupola_sinistra(sposta)
        if msg:
            add_log(msg)
            c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
            page.update()
    def r_posizioni():
        config.reset_posizioni()
        c_cupola_testo.value = f"coordinata Cupola: {config.c_cupola}"
        c_telescopio_testo.value = f"coordinata Telescopio: {config.c_telescopio}"
        page.update()
    
    #textField per input coordinate
    input_destra = ft.TextField(label="Input destra", value=str(config.c_cupola), width=100, bgcolor=ft.Colors.WHITE)
    input_sinistra = ft.TextField(label="Input sinistra", value=str(config.c_telescopio) , width=100, bgcolor=ft.Colors.WHITE)

    # Pulsanti
    p_destra = ft.ElevatedButton(text=" ", icon=ft.Icons.ARROW_RIGHT, on_click=lambda e: sposta_c_destra(input_destra.value and int(input_destra.value) or 0))
    p_sinistra = ft.ElevatedButton(text=" ", icon=ft.Icons.ARROW_LEFT, on_click=lambda e: sposta_c_sinistra(input_sinistra.value and int(input_sinistra.value) or 0))
    p_stop = ft.ElevatedButton(text="Pulsante Stop", icon=ft.Icons.STOP, on_click=lambda e: config.stop_movimento())
    p_reset = ft.ElevatedButton(text="Pulsante Reset", icon=ft.Icons.REFRESH, on_click=lambda e: r_posizioni())

    

    # Navbar e centro
    navbar = ft.Row(
        [c_cupola_testo, c_telescopio_testo, bSetting], #aggiunti i testi delle coordinate
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


    # Layout principale
    layout = ft.Column(
        [navbar, centro, footer],
        alignment=ft.MainAxisAlignment.START, # allinea gli elementi in colonna dall'inizio in verticale
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # allinea gli elementi in colonna al centro orizzontalmente
        expand=True,  #  importantissimo: riempie tutta la finestra
    )
    
    log_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=5,
    )

    
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=4,
            track_color="#111111",
            thumb_color="#444444",
        )
    )
    
    roba_log = ft.Column( #scusa menghi per il nome
        [switch_show, bLog, bClear],
        spacing=10,
    )
    
    log_layout = ft.Row(
        [log_list, roba_log],  # usa log_container invece di log_list
        expand=False,
        width=200,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )
    

    
    layout = ft.Row(
            [log_layout,layout],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,)
    video_bg = Video(
        
        playlist=[VideoMedia("src/assets/Composizione1.mp4")],
        autoplay=True,
        muted=True,
        expand=True,
        fit="COVER"
    )

    pagina = ft.Stack(
            [
                video_bg,
                ft.Container(
                    content=layout,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            expand=True,
            fit="COVER"
        )
    return pagina

