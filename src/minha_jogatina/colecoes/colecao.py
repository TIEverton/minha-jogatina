from typing import List
from ..models.jogo import Jogo


class Colecao:    
    def __init__(self, nome: str):
        self.nome = nome
        self._jogos: List[Jogo] = []

    def adicionar_jogo(self, jogo: Jogo):
        # Não permite duplicatas
        if jogo in self._jogos:
            raise ValueError(f"O jogo '{jogo.titulo}' já está na coleção '{self.nome}'.")
        self._jogos.append(jogo)

    def remover_jogo(self, titulo: str):
        self._jogos = [j for j in self._jogos if j.titulo.lower() != titulo.lower()]

    def listar_jogos(self) -> List[Jogo]:
        return self._jogos

    def __str__(self):
        return f"Coleção '{self.nome}' com {len(self._jogos)} jogos."
