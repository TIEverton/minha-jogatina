import json
import sqlite3
from typing import List
from pathlib import Path
from .models.jogo import Jogo, JogoPC, JogoConsole, JogoMobile
from .colecoes.colecao import Colecao


class RepositorioDados:
    def __init__(self, formato="json", arquivo="dados.json"):
        self.formato = formato
        self.arquivo = arquivo
        self.caminho = Path(arquivo)

    def salvar_jogos(self, jogos: List[Jogo]) -> None:
        if self.formato == "json":
            self._salvar_json(jogos)
        elif self.formato == "sqlite":
            self._salvar_sqlite(jogos)

    def carregar_jogos(self) -> List[Jogo]:
        if self.formato == "json":
            return self._carregar_json()
        elif self.formato == "sqlite":
            return self._carregar_sqlite()
        return []

    def _salvar_json(self, jogos: List[Jogo]) -> None:
        dados = []
        for jogo in jogos:
            dados.append({
                'titulo': jogo.titulo,
                'genero': jogo.genero,
                'plataforma': jogo.plataforma,
                'horas_jogadas': jogo.horas_jogadas,
                'status': jogo.status.value,
                'avaliacao': jogo.avaliacao,
                'tipo': type(jogo).__name__
            })
        with open(self.caminho, 'w') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def _carregar_json(self) -> List[Jogo]:
        if not self.caminho.exists():
            return []
        with open(self.caminho, 'r') as f:
            dados = json.load(f)

        jogos = []
        for item in dados:
            tipo = item['tipo']
            if tipo == 'JogoPC':
                jogo = JogoPC(item['titulo'], item['genero'])
            elif tipo == 'JogoConsole':
                jogo = JogoConsole(item['titulo'], item['genero'])
            else:
                jogo = JogoMobile(item['titulo'], item['genero'])

            jogo.horas_jogadas = item['horas_jogadas']
            jogo._status = item['status']  # Carrega status sem validar
            if item['avaliacao']:
                jogo._avaliacao = item['avaliacao']
            jogos.append(jogo)
        return jogos
