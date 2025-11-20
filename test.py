import flet as ft
from flet_video import Video, VideoMedia

def main(page: ft.Page):
    page.title = "App con Video di Sfondo"
    page.window_width = 800
    page.window_height = 600

    # Video di sfondo
    video_bg = Video(
        playlist=[VideoMedia("src/assets/Composizione1.mp4")],
        autoplay=True,
        
        muted=True,
        expand=True,
        fit=ft.ImageFit.COVER
    )

    # Contenuto sopra il video
    content = ft.Column(
        [
            ft.Text("Contenuto sopra il video", size=24, color=ft.Colors.WHITE),
            ft.ElevatedButton("Cliccami!", on_click=lambda e: print("Bottone premuto"))
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Stack per mettere il video dietro il contenuto
    page.add(
        ft.Stack(
            [
                video_bg,
                ft.Container(
                    content=content,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            expand=True
        )
    )

ft.app(target=main)
