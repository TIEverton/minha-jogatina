import argparse
import json
from pathlib import Path
from .src.minha_jogatina.models.jogo import JogoPC, JogoConsole, JogoMobile
from .src.minha_jogatina.models.status import StatusJogo
from .src.minha_jogatina.colecoes.colecao import Colecao
from .src.minha_jogatina.dados import RepositorioDados
from .src.minha_jogatina.models.relatorio import Relatorio


class CLI:
    def __init__(self):
        self.repo = RepositorioDados("json", "jogos.json")
        self.jogos = self.repo.carregar_jogos()
        self.colecoes = {}

    def run(self):
        parser = argparse.ArgumentParser(
            description="Catálogo de Jogos Digitais")
        subparsers = parser.add_subparsers(dest="comando")

        # Subcomando: cadastrar
        cadastrar_parser = subparsers.add_parser(
            "cadastrar", help="Cadastrar novo jogo")
        cadastrar_parser.add_argument("titulo", help="Título do jogo")
        cadastrar_parser.add_argument("genero", help="Gênero")
        cadastrar_parser.add_argument(
            "plataforma", choices=["PC", "Console", "Mobile"])

        # Subcomando: atualizar
        atualizar_parser = subparsers.add_parser(
            "atualizar", help="Atualizar jogo")
        atualizar_parser.add_argument("titulo", help="Título do jogo")
        atualizar_parser.add_argument(
            "--horas", type=float, help="Horas jogadas")
        atualizar_parser.add_argument("--status", help="Novo status")

        # Subcomando: relatorio
        subparsers.add_parser("relatorio", help="Gerar relatório")

        args = parser.parse_args()

        if args.comando == "cadastrar":
            self.cadastrar_jogo(args.titulo, args.genero, args.plataforma)
        elif args.comando == "atualizar":
            self.atualizar_jogo(args.titulo, args.horas, args.status)
        elif args.comando == "relatorio":
            self.gerar_relatorio()

    def cadastrar_jogo(self, titulo: str, genero: str, plataforma: str):
        if plataforma == "PC":
            jogo = JogoPC(titulo, genero)
        elif plataforma == "Console":
            jogo = JogoConsole(titulo, genero)
        else:
            jogo = JogoMobile(titulo, genero)

        self.jogos.append(jogo)
        self.repo.salvar_jogos(self.jogos)
        print(f"Jogo '{titulo}' cadastrado com sucesso!")

    def atualizar_jogo(self, titulo: str, horas: float = None, status: str = None):
        for jogo in self.jogos:
            if jogo.titulo.lower() == titulo.lower():
                if horas is not None:
                    jogo.horas_jogadas = horas
                if status:
                    jogo.status = StatusJogo[status.upper()]
                self.repo.salvar_jogos(self.jogos)
                print(f"Jogo '{titulo}' atualizado!")
                return
        print(f"Jogo '{titulo}' não encontrado!")

    def gerar_relatorio(self):
        relatorio = Relatorio(self.jogos)
        print(f"\n--- RELATÓRIO ---")
        print(f"Total de horas: {relatorio.total_horas():.1f}h")
        print(
            f"Média de avaliação: {relatorio.media_avaliacao_finalizados():.1f}")
        print(f"Top 5: {[j.titulo for j in relatorio.top_5_mais_jogados()]}")
