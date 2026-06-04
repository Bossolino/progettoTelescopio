"""
theme.py  –  palette e temi condivisi tra home.py e finestraSettings.py
Importare con:  from theme import DARK, LIGHT, P
"""
import flet as ft

# ── Palette dark ─────────────────────────────────────────────────────────────
class _Dark:
    BG       = "#0d0f14"
    SURFACE  = "#13161e"
    SURFACE2 = "#1c2030"
    BORDER   = "#2a3045"
    ACCENT   = "#4f8ef7"
    ACCENT2  = "#7dd3fc"
    SUCCESS  = "#34d399"
    DANGER   = "#f87171"
    WARNING  = "#fbbf24"
    TEXT_PRI = "#e8eaf2"
    TEXT_SEC = "#8892aa"
    TEXT_DIM = "#4a5268"

# ── Palette light ─────────────────────────────────────────────────────────────
class _Light:
    BG       = "#f0f2f8"
    SURFACE  = "#ffffff"
    SURFACE2 = "#e8eaf2"
    BORDER   = "#d0d4e4"
    ACCENT   = "#2563eb"
    ACCENT2  = "#0284c7"
    SUCCESS  = "#059669"
    DANGER   = "#dc2626"
    WARNING  = "#d97706"
    TEXT_PRI = "#111827"
    TEXT_SEC = "#4b5563"
    TEXT_DIM = "#9ca3af"

DARK  = _Dark()
LIGHT = _Light()

# ── ft.Theme objects ───────────────────────────────────────────────────────────
def _make_theme(p) -> ft.Theme:
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=p.ACCENT,
            background=p.BG,
            surface=p.SURFACE,
            on_surface=p.TEXT_PRI,
            on_background=p.TEXT_PRI,
            outline=p.BORDER,
        ),
        scaffold_bgcolor=p.BG,
        scrollbar_theme=ft.ScrollbarTheme(
            thickness=3,
            track_color=p.SURFACE2,
            thumb_color=p.BORDER,
        ),
    )

THEME_DARK  = _make_theme(DARK)
THEME_LIGHT = _make_theme(LIGHT)


def apply_theme(page: ft.Page, mode: ft.ThemeMode):
    """Applica tema chiaro o scuro alla pagina."""
    page.theme      = THEME_LIGHT
    page.dark_theme = THEME_DARK
    page.theme_mode = mode
    page.bgcolor    = DARK.BG if mode == ft.ThemeMode.DARK else LIGHT.BG
    page.update()


def palette(page: ft.Page):
    """Ritorna la palette corrente in base al tema attivo."""
    if page.theme_mode == ft.ThemeMode.DARK:
        return DARK
    elif page.theme_mode == ft.ThemeMode.LIGHT:
        return LIGHT
    # SYSTEM: usa platform_brightness
    if page.platform_brightness == ft.Brightness.DARK:
        return DARK
    return LIGHT