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
            self.windowHeight = 700
    
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

settings = Settings()