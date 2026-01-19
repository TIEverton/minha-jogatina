from typing import List
from models.jogo import Jogo
from models.status import StatusJogo


class Relatorio:
    def __init__(self, jogos: List[Jogo]):
        self.jogos = jogos

    def total_horas(self) -> float:
        """Total de horas jogadas no catálogo."""
        return sum(j.horas_jogadas for j in self.jogos)

    def media_avaliacao_finalizados(self) -> float:
        """Média de avaliação dos jogos finalizados."""
        finalizados = [j for j in self.jogos if j.status ==
                       StatusJogo.FINALIZADO and j.avaliacao]
        if not finalizados:
            return 0.0
        return sum(j.avaliacao for j in finalizados) / len(finalizados)

    def percentual_por_status(self) -> dict:
        """Percentual de jogos por status."""
        if not self.jogos:
            return {}
        total = len(self.jogos)
        resultado = {}
        for status in StatusJogo:
            count = len([j for j in self.jogos if j.status == status])
            resultado[status.value] = (count / total) * 100
        return resultado

    def top_5_mais_jogados(self) -> List[Jogo]:
        """Top 5 jogos mais jogados."""
        return sorted(self.jogos, key=lambda j: j.horas_jogadas, reverse=True)[:5]

    def filtrar_por_genero(self, genero: str) -> List[Jogo]:
        """Filtrar jogos por gênero."""
        return [j for j in self.jogos if j.genero.lower() == genero.lower()]

    def filtrar_por_plataforma(self, plataforma: str) -> List[Jogo]:
        """Filtrar jogos por plataforma."""
        return [j for j in self.jogos if j.plataforma.lower() == plataforma.lower()]

    def filtrar_por_status(self, status: StatusJogo) -> List[Jogo]:
        """Filtrar jogos por status."""
        return [j for j in self.jogos if j.status == status]

    def buscar_por_titulo(self, titulo: str) -> List[Jogo]:
        """Buscar jogos por parte do título."""
        return [j for j in self.jogos if titulo.lower() in j.titulo.lower()]

    def ordenar_por_horas(self) -> List[Jogo]:
        """Ordenar lista por tempo jogado."""
        return sorted(self.jogos, key=lambda j: j.horas_jogadas, reverse=True)

    def ordenar_por_avaliacao(self) -> List[Jogo]:
        """Ordenar lista por avaliação."""
        return sorted([j for j in self.jogos if j.avaliacao],
                      key=lambda j: j.avaliacao, reverse=True)
