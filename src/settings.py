import json
import flet as ft


class Settings:
    def __init__(self):
        self.page = self.Page()
        self.seriale = self.Seriale()
        self.init_settings()

    class Page:
        def __init__(self):
            self.theme = ft.ThemeMode.SYSTEM
            self.pageFullscreen = False
            self.windowWidth = 1400
            self.windowHeight = 800
             #IMPOSTARE I CODICI COLORE PRIMA DI USARE LE FUNZIONI

        def self.setColorsDark(self, page:ft.Page):
            page.dark_theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                brightness=ft.Brightness.DARK,
                primary="#90caf9",
                secondary="#ffd54f",
                background="#121212",
                surface="#1e1e1e",
                on_primary="black",
                on_surface="#e0e0e0",
            )
        )
    
        def self.setColorsLight(self, page:ft.Page):
            page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.colors.BLUE_500,
                secondary=ft.colors.AMBER,
                background="#ffffff",
                surface="#f2f2f2",
                on_primary="white",
                on_surface="#333333",
            )
        )
    
    class Seriale:
        def __init__(self):
            self.porta_seriale = ""
            self.nome_device = ""
        
    def init_settings(self): #print(data["application"]["tema"])
        with open("src/assets/settings.json", "r") as f:
            data = json.load(f)
        self.page.theme = data["page"]["tema"]
        self.seriale.porta_seriale = data["seriale"]["portaSeriale"]
        self.seriale.nome_device = data["seriale"]["nomeDevice"]
    
    def setSetting(self, oggetto:str, setting: str, new_value):
        with open("src/assets/settings.json", "r") as f:
            data = json.load(f)
        data[oggetto][setting] = new_value
        with open("src/assets/settings.json", "w") as f:
            json.dump(data, f, indent=4)
        return
    
class Colors:
    # bgColor = ""
    # btnColor = ""
    # txtColor = ""
    # color1 = ""

    # darkColors = {
    #     bgColor : "",
    #     btnColor : "",
    #     txtColor : "",
    #     color1 : ""
    # }

    # lightColors = {
    #     bgColor : "",
    #     btnColor : "",
    #     txtColor : "",
    #     color1 : ""
    # }


   


settings = Settings()
