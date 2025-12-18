from .jogo import Jogo

class JogoPC(Jogo):
    def __init__(self, titulo: str, genero: str):
        super().__init__(titulo, genero, "PC")

class JogoConsole(Jogo):
    def __init__(self, titulo: str, genero: str):
        super().__init__(titulo, genero, "Console")

class JogoMobile(Jogo):
    def __init__(self, titulo: str, genero: str):
        super().__init__(titulo, genero, "Mobile")
