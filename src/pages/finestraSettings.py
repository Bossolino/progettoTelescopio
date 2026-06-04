import flet as ft
from seriale import getPorteDisponibili
from pages import router
from settings import settings
from pages.theme import apply_theme, palette

# ── Helpers ───────────────────────────────────────────────────────────────────
def _card(content, p, padding=20, width=None):
    return ft.Container(
        content=content,
        bgcolor=p.SURFACE,
        border=ft.border.all(1, p.BORDER),
        border_radius=10,
        padding=padding,
        width=width,
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
    return ft.Container(height=1, bgcolor=p.BORDER, margin=ft.margin.symmetric(vertical=8))

def _section_title(text, p):
    return ft.Column([_label(text, p), _divider(p)], spacing=0)


# ── Page ──────────────────────────────────────────────────────────────────────
def finestraSettings(page: ft.Page):
    global settings

    page.title     = "Impostazioni"
    page.window.width  = settings.page.windowWidth
    page.window.height = settings.page.windowHeight
    page.padding   = 0

    apply_theme(page, settings.page.theme)
    p = palette(page)

    # ── Dropdown stile comune ─────────────────────────────────────────────
    def _style_dd(dd: ft.Dropdown):
        dd.bgcolor              = p.SURFACE2
        dd.border_color         = p.BORDER
        dd.focused_border_color = p.ACCENT
        dd.color                = p.TEXT_PRI
        dd.label_style          = ft.TextStyle(color=p.TEXT_DIM, size=12)
        dd.text_size            = 14
        dd.border_radius        = 8
        dd.width                = 260
        return dd

    # ── Dropdown Tema ─────────────────────────────────────────────────────
    dropdownTema = _style_dd(ft.Dropdown(
        options=[
            ft.DropdownOption(key="DARK",   text="Scuro",   leading_icon=ft.Icons.DARK_MODE),
            ft.DropdownOption(key="LIGHT",  text="Chiaro",  leading_icon=ft.Icons.LIGHT_MODE),
            ft.DropdownOption(key="SYSTEM", text="Sistema", leading_icon=ft.Icons.COMPUTER),
        ],
        label="Tema dell'applicazione",
    ))

    # ── Dropdown Porta ────────────────────────────────────────────────────
    dropdownPorta = _style_dd(ft.Dropdown(
        options=[ft.DropdownOption(key=" ", text="Seleziona...", disabled=True)],
        label="Porta seriale",
        on_change=settings.seriale.savePorta,
    ))

    # ── Callbacks ─────────────────────────────────────────────────────────
    def getSelectionTheme(e):
        global settings
        selezione = e.data
        mode_map = {
            "DARK":   ft.ThemeMode.DARK,
            "LIGHT":  ft.ThemeMode.LIGHT,
            "SYSTEM": ft.ThemeMode.SYSTEM,
        }
        icon_map = {
            "DARK":   ft.Icons.DARK_MODE,
            "LIGHT":  ft.Icons.LIGHT_MODE,
            "SYSTEM": ft.Icons.COMPUTER,
        }
        settings.page.theme       = mode_map[selezione]
        dropdownTema.leading_icon = icon_map[selezione]
        settings.setSetting("page", "tema", selezione)

        # Applica il nuovo tema e ricostruisce la pagina
        apply_theme(page, settings.page.theme)
        page.controls.clear()
        page.add(finestraSettings.__wrapped__(page))

    dropdownTema.on_change = getSelectionTheme

    def init_settings_fields():
        global settings
        # Tema
        theme_str = {
            ft.ThemeMode.LIGHT:  "LIGHT",
            ft.ThemeMode.DARK:   "DARK",
            ft.ThemeMode.SYSTEM: "SYSTEM",
            "LIGHT": "LIGHT", "DARK": "DARK", "SYSTEM": "SYSTEM",
        }.get(settings.page.theme, "DARK")

        icon_map = {
            "LIGHT": ft.Icons.LIGHT_MODE,
            "DARK":  ft.Icons.DARK_MODE,
            "SYSTEM": ft.Icons.COMPUTER,
        }
        dropdownTema.value        = theme_str
        dropdownTema.leading_icon = icon_map.get(theme_str, ft.Icons.DARK_MODE)

        # Porta
        porte_disp = getPorteDisponibili()
        if porte_disp:
            for porta, nome in porte_disp.items():
                dropdownPorta.options.append(
                    ft.DropdownOption(key=porta, text=f"{porta} : {nome}")
                )
            dropdownPorta.value = settings.seriale.porta_seriale or " "
        else:
            dropdownPorta.options.append(
                ft.DropdownOption(key="none", text="Nessun device trovato")
            )
            dropdownPorta.value    = "none"
            dropdownPorta.disabled = True

        page.update()

    # ── Hover helper ─────────────────────────────────────────────────────
    def _hover(e):
        e.control.bgcolor = ft.Colors.with_opacity(
            0.16 if e.data == "true" else 0.08, p.TEXT_SEC
        )
        page.update()

    # ── Top bar ───────────────────────────────────────────────────────────
    btn_home = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.ARROW_BACK, color=p.TEXT_SEC, size=18),
                ft.Text("Home", color=p.TEXT_SEC, size=13, weight=ft.FontWeight.W_500),
            ],
            spacing=6,
        ),
        bgcolor=ft.Colors.with_opacity(0.08, p.TEXT_SEC),
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, p.TEXT_SEC)),
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=14, vertical=9),
        on_click=lambda e: router.go("home", page),
        on_hover=_hover,
    )

    topbar = ft.Container(
        content=ft.Row(
            [
                ft.Text("IMPOSTAZIONI", size=14, color=p.TEXT_PRI,
                        weight=ft.FontWeight.W_600),
                btn_home,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=ft.Colors.with_opacity(0.85, p.SURFACE),
        border=ft.border.only(bottom=ft.border.BorderSide(1, p.BORDER)),
        padding=ft.padding.symmetric(horizontal=24, vertical=12),
        height=56,
    )

    # ── Cards ─────────────────────────────────────────────────────────────
    card_tema = _card(
        ft.Column(
            [
                _section_title("Aspetto", p),
                ft.Container(height=8),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.PALETTE_OUTLINED, color=p.ACCENT, size=20),
                        ft.Text("Tema dell'applicazione", color=p.TEXT_SEC, size=13),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=12),
                dropdownTema,
            ],
            spacing=4,
        ),
        p,
        width=340,
    )

    card_porta = _card(
        ft.Column(
            [
                _section_title("Connessione", p),
                ft.Container(height=8),
                ft.Row(
                    [
                        ft.Icon(ft.Icons.USB_OUTLINED, color=p.ACCENT, size=20),
                        ft.Text("Porta seriale del device", color=p.TEXT_SEC, size=13),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=12),
                dropdownPorta,
            ],
            spacing=4,
        ),
        p,
        width=340,
    )

    body = ft.Container(
        content=ft.Column(
            [
                ft.Row([card_tema, card_porta], spacing=20, wrap=True),
            ],
            spacing=20,
        ),
        padding=ft.padding.all(30),
        expand=True,
    )

    layout = ft.Column([topbar, body], spacing=0, expand=True)

    init_settings_fields()
    return layout


# alias usato internamente per il rebuild al cambio tema
finestraSettings.__wrapped__ = finestraSettings