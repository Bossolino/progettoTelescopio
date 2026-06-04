import flet as ft  # type: ignore
import config
from seriale import start_ascolto
from flet_video import Video, VideoMedia
from pages import router
from settings import settings
from pages.theme import apply_theme, palette

# ── Helpers ───────────────────────────────────────────────────────────────────
def _card(content, p, padding=16, expand=False, width=None, height=None):
    return ft.Container(
        content=content,
        bgcolor=p.SURFACE,
        border=ft.border.all(1, p.BORDER),
        border_radius=10,
        padding=padding,
        expand=expand,
        width=width,
        height=height,
    )

def _label(text, p, size=11):
    return ft.Text(
        text.upper(),
        size=size,
        color=p.TEXT_DIM,
        weight=ft.FontWeight.W_600,
        style=ft.TextStyle(letter_spacing=1.5),
    )

def _divider(p):
    return ft.Container(height=1, bgcolor=p.BORDER, margin=ft.margin.symmetric(vertical=6))


# ── Page ──────────────────────────────────────────────────────────────────────
def home(page: ft.Page):
    global settings

    page.window.width  = settings.page.windowWidth
    page.window.height = settings.page.windowHeight
    page.window.center()
    page.title   = "Observatory Control"
    page.padding = 0
    page.spacing = 0

    apply_theme(page, settings.page.theme)
    p = palette(page)

    # ── Serial init ───────────────────────────────────────────────────────
    if not settings.seriale.inAscolto:
        try:
            from seriale import setPorta
            setPorta()
            start_ascolto(settings.seriale.porta_seriale)
        except Exception as exc:
            print("ERRORE: Ascolto non avviato!", exc)

    # ── Log ───────────────────────────────────────────────────────────────
    log_list = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=2, expand=True)

    def add_log(msg: str):
        dot_color = p.SUCCESS if ("←" in msg or "→" in msg) else p.ACCENT
        row = ft.Row(
            [
                ft.Container(width=6, height=6, bgcolor=dot_color, border_radius=3),
                ft.Text(msg, size=11, color=p.TEXT_SEC, expand=True),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        log_list.controls.insert(0, row)
        if len(log_list.controls) > 80:
            log_list.controls.pop()
        page.update()

    def clear_log():
        log_list.controls.clear()
        page.update()

    # ── Coordinate values ─────────────────────────────────────────────────
    val_cupola = ft.Text(
        f"{config.c_cupola}°", size=28, color=p.ACCENT2, weight=ft.FontWeight.W_300,
    )
    val_telescopio = ft.Text(
        f"{config.c_telescopio}°", size=28, color=p.SUCCESS, weight=ft.FontWeight.W_300,
    )

    def _refresh_coords():
        val_cupola.value     = f"{config.c_cupola}°"
        val_telescopio.value = f"{config.c_telescopio}°"
        page.update()

    # ── Movement callbacks ────────────────────────────────────────────────
    def sposta_destra(sposta: int):
        msg = config.sposta_cupola_destra(sposta)
        if msg:
            add_log(f"→ {msg}")
        _refresh_coords()

    def sposta_sinistra(sposta: int):
        msg = config.sposta_cupola_sinistra(sposta)
        if msg:
            add_log(f"← {msg}")
        _refresh_coords()

    def reset_posizioni():
        config.reset_posizioni()
        add_log("Posizioni resettate")
        _refresh_coords()

    # ── Input fields ──────────────────────────────────────────────────────
    def _input(label, value):
        return ft.TextField(
            label=label,
            value=str(value),
            width=90,
            height=48,
            text_size=14,
            color=p.TEXT_PRI,
            label_style=ft.TextStyle(color=p.TEXT_DIM, size=11),
            border_color=p.BORDER,
            focused_border_color=p.ACCENT,
            bgcolor=p.SURFACE2,
            border_radius=6,
            text_align=ft.TextAlign.CENTER,
        )

    input_destra   = _input("Step destra",   config.c_cupola)
    input_sinistra = _input("Step sinistra", config.c_telescopio)

    # ── Buttons ───────────────────────────────────────────────────────────
    def _ctrl_btn(icon, label, color, on_click, width=110):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Icon(icon, color=color, size=16),
                    ft.Text(label, color=color, size=13, weight=ft.FontWeight.W_500),
                ],
                spacing=6,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            bgcolor=ft.Colors.with_opacity(0.08, color),
            border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
            border_radius=8,
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            width=width,
            on_click=on_click,
            on_hover=lambda e, c=color: _btn_hover(e, c),
        )

    def _btn_hover(e, color):
        e.control.bgcolor = ft.Colors.with_opacity(
            0.18 if e.data == "true" else 0.08, color
        )
        page.update()

    btn_left  = _ctrl_btn(ft.Icons.CHEVRON_LEFT,  "Sinistra", p.ACCENT,  lambda e: sposta_sinistra(int(input_sinistra.value or 0)))
    btn_right = _ctrl_btn(ft.Icons.CHEVRON_RIGHT, "Destra",   p.ACCENT,  lambda e: sposta_destra(int(input_destra.value or 0)))
    btn_stop  = _ctrl_btn(ft.Icons.STOP_CIRCLE,   "Stop",     p.DANGER,  lambda e: config.stop_movimento(), width=90)
    btn_reset = _ctrl_btn(ft.Icons.REFRESH,       "Reset",    p.WARNING, lambda e: reset_posizioni(), width=90)

    btn_set = ft.IconButton(
        icon=ft.Icons.TUNE,
        icon_color=p.TEXT_SEC,
        icon_size=22,
        tooltip="Impostazioni",
        on_click=lambda e: router.go("settings", page),
    )

    # ── Log panel ─────────────────────────────────────────────────────────
    def toggle_log(e):
        log_panel.visible = not log_panel.visible
        page.update()

    log_toggle_btn = ft.IconButton(
        icon=ft.Icons.RECEIPT_LONG,
        icon_color=p.ACCENT,
        icon_size=18,
        tooltip="Mostra/nascondi log",
        on_click=toggle_log,
    )
    clear_btn = ft.IconButton(
        icon=ft.Icons.DELETE_SWEEP_OUTLINED,
        icon_color=p.TEXT_DIM,
        icon_size=18,
        tooltip="Pulisci log",
        on_click=lambda e: clear_log(),
    )

    log_panel = _card(
        ft.Column(
            [
                ft.Row(
                    [
                        _label("Event Log", p),
                        ft.Row([log_toggle_btn, clear_btn], spacing=0),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                _divider(p),
                ft.Container(content=log_list, height=260),
            ],
            spacing=0,
        ),
        p,
        padding=14,
        width=280,
    )

    # ── Coordinate cards ──────────────────────────────────────────────────
    def _coord_card(label, value_widget, color):
        return _card(
            ft.Column(
                [
                    _label(label, p),
                    ft.Container(height=4),
                    ft.Row(
                        [
                            ft.Container(width=3, height=32, bgcolor=color, border_radius=2),
                            ft.Container(width=8),
                            value_widget,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
            ),
            p,
            padding=16,
            width=180,
        )

    card_cupola     = _coord_card("Cupola",     val_cupola,     p.ACCENT2)
    card_telescopio = _coord_card("Telescopio", val_telescopio, p.SUCCESS)

    # ── Movement panel ────────────────────────────────────────────────────
    movement_panel = _card(
        ft.Column(
            [
                _label("Controllo Movimento", p),
                _divider(p),
                ft.Row(
                    [btn_left, input_sinistra, input_destra, btn_right],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=10),
                ft.Row(
                    [btn_stop, btn_reset],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        p,
        padding=20,
    )

    # ── Top bar ───────────────────────────────────────────────────────────
    status_dot = ft.Container(
        width=8, height=8, bgcolor=p.SUCCESS, border_radius=4,
        animate=ft.Animation(1200, ft.AnimationCurve.EASE_IN_OUT),
    )

    topbar = ft.Container(
        content=ft.Row(
            [
                ft.Row(
                    [
                        ft.Text("OBSERVATORY", size=14, color=p.TEXT_PRI,
                                weight=ft.FontWeight.W_600),
                        ft.Text("CONTROL", size=14, color=p.ACCENT,
                                weight=ft.FontWeight.W_300),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        status_dot,
                        ft.Text("Sistema attivo", size=12, color=p.SUCCESS),
                        ft.Container(width=12),
                        log_toggle_btn,
                        clear_btn,
                        btn_set,
                    ],
                    spacing=4,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.85, p.SURFACE),
        border=ft.border.only(bottom=ft.border.BorderSide(1, p.BORDER)),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        height=56,
    )

    # ── Crosshair decorativo ──────────────────────────────────────────────
    crosshair = ft.Stack(
        [
            ft.Container(
                width=160, height=160,
                border=ft.border.all(1, ft.Colors.with_opacity(0.15, p.ACCENT2)),
                border_radius=80,
            ),
            ft.Container(
                width=80, height=80,
                border=ft.border.all(1, ft.Colors.with_opacity(0.25, p.ACCENT2)),
                border_radius=40,
            ),
            ft.Container(width=10, height=10, bgcolor=p.ACCENT2, border_radius=5),
        ],
        alignment=ft.alignment.center,
        width=160,
        height=160,
    )

    # ── Center area ───────────────────────────────────────────────────────
    center_area = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [card_cupola, card_telescopio],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                ),
                ft.Container(height=30),
                ft.Row([crosshair], alignment=ft.MainAxisAlignment.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.top_center,
        padding=ft.padding.only(top=30),
    )

    # ── Bottom strip ──────────────────────────────────────────────────────
    bottom_strip = ft.Container(
        content=movement_panel,
        padding=ft.padding.symmetric(horizontal=24, vertical=16),
        bgcolor=ft.Colors.with_opacity(0.70, p.BG),
        border=ft.border.only(top=ft.border.BorderSide(1, p.BORDER)),
    )

    sidebar = ft.Container(
        content=log_panel,
        padding=ft.padding.only(top=16, right=16, bottom=16),
    )

    main_row = ft.Row(
        [
            ft.Container(content=center_area, expand=True),
            sidebar,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    layout = ft.Column(
        [topbar, main_row, bottom_strip],
        expand=True,
        spacing=0,
    )

    # ── Video background ──────────────────────────────────────────────────
    video_bg = Video(
        playlist=[VideoMedia("src/assets/Composizione1.mp4")],
        autoplay=True,
        muted=True,
        expand=True,
        fit="COVER",
    )

    overlay = ft.Container(
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.72, p.BG),
    )

    pagina = ft.Stack(
        [
            video_bg,
            overlay,
            ft.Container(content=layout, expand=True),
        ],
        expand=True,
        fit="COVER",
    )

    return pagina