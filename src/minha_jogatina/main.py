import argparse
import json
import os
from typing import Dict, Any, List

from src.minha_jogatina import (
    StatusJogo,
    JogoPC,
    JogoConsole,
    JogoMobile,
    Colecao,
)

CAMINHO_ARMAZENAMENTO = os.path.expanduser("~/.minha_jogatina_colecoes.json")


def carregar_armazenamento() -> Dict[str, Any]:
    if not os.path.exists(CAMINHO_ARMAZENAMENTO):
        return {"collections": {}}
    with open(CAMINHO_ARMAZENAMENTO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_armazenamento(armazenamento: Dict[str, Any]):
    with open(CAMINHO_ARMAZENAMENTO, "w", encoding="utf-8") as f:
        json.dump(armazenamento, f, indent=2, ensure_ascii=False)


def _status_de_str(s: str) -> StatusJogo:
    for st in StatusJogo:
        if s == st.name or s == st.value:
            return st
    return StatusJogo.NAO_INICIADO


def _jogo_de_dict(d: Dict[str, Any]):
    platform = (d.get("platform") or "").lower()
    titulo = d.get("title") or ""
    genero = d.get("genero") or ""

    if "pc" in platform:
        g = JogoPC(titulo, genero)
    elif "console" in platform:
        g = JogoConsole(titulo, genero)
    else:
        g = JogoMobile(titulo, genero)

    g.horas_jogadas = float(d.get("horas_jogadas", 0))
    g.status = _status_de_str(d.get("status", ""))

    if d.get("avaliacao") is not None:
        g.avaliacao = float(d.get("avaliacao"))

    return g


def _jogo_para_dict(g) -> Dict[str, Any]:
    return {
        "title": g.titulo,
        "genero": g.genero,
        "platform": g.plataforma,
        "status": g.status.value,
        "horas_jogadas": g.horas_jogadas,
        "avaliacao": g.avaliacao,
    }


def validar_avaliacao(valor):
    return 0 <= valor <= 10


def main():
    parser = argparse.ArgumentParser(prog="minha-jogatina")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("listar-colecoes")

    p_criar = sub.add_parser("criar-colecao")
    p_criar.add_argument("nome")

    p_deletar = sub.add_parser("deletar-colecao")
    p_deletar.add_argument("nome")

    p_listar = sub.add_parser("listar-jogos")
    p_listar.add_argument("colecao")

    p_add = sub.add_parser("adicionar-jogo")
    p_add.add_argument("colecao")
    p_add.add_argument("--titulo", required=True)
    p_add.add_argument("--genero", required=True)
    p_add.add_argument("--plataforma", required=True, choices=["PC", "Console", "Mobile"])
    p_add.add_argument("--status", required=True)
    p_add.add_argument("--horas", type=float, default=0)
    p_add.add_argument("--avaliacao", type=float)

    p_up = sub.add_parser("atualizar-jogo")
    p_up.add_argument("colecao")
    p_up.add_argument("titulo")
    p_up.add_argument("--novo-titulo")
    p_up.add_argument("--genero")
    p_up.add_argument("--plataforma", choices=["PC", "Console", "Mobile"])
    p_up.add_argument("--status")
    p_up.add_argument("--horas", type=float)
    p_up.add_argument("--avaliacao", type=float)

    p_rm = sub.add_parser("remover-jogo")
    p_rm.add_argument("colecao")
    p_rm.add_argument("titulo")

    args = parser.parse_args()
    armazenamento = carregar_armazenamento()

    if args.cmd == "listar-colecoes":
        for c in armazenamento["collections"]:
            print(c)
        return

    if args.cmd == "criar-colecao":
        armazenamento["collections"][args.nome] = {"games": []}
        salvar_armazenamento(armazenamento)
        print("Coleção criada.")
        return

    if args.cmd == "deletar-colecao":
        armazenamento["collections"].pop(args.nome, None)
        salvar_armazenamento(armazenamento)
        print("Coleção deletada.")
        return

    if args.cmd == "listar-jogos":
        for g in armazenamento["collections"].get(args.colecao, {}).get("games", []):
            print(g)
        return

    if args.cmd == "adicionar-jogo":
        if args.avaliacao is not None and not validar_avaliacao(args.avaliacao):
            print("Avaliação deve ser entre 0 e 10.")
            return

        if args.avaliacao is not None and _status_de_str(args.status) != StatusJogo.FINALIZADO:
            print("Só é possível avaliar jogos finalizados.")
            return

        jogo = _jogo_para_dict(_jogo_de_dict(vars(args)))
        armazenamento["collections"][args.colecao]["games"].append(jogo)
        salvar_armazenamento(armazenamento)
        print("Jogo adicionado.")
        return

    if args.cmd == "remover-jogo":
        col = armazenamento["collections"][args.colecao]
        col["games"] = [g for g in col["games"] if g["title"].lower() != args.titulo.lower()]
        salvar_armazenamento(armazenamento)
        print("Jogo removido.")
        return

    if args.cmd == "atualizar-jogo":
        col = armazenamento["collections"][args.colecao]

        for i, g in enumerate(col["games"]):
            if g["title"].lower() == args.titulo.lower():

                novo = dict(g)

                if args.horas is not None and args.horas < g["horas_jogadas"]:
                    print("Horas não podem ser reduzidas.")
                    return

                if args.status:
                    novo["status"] = _status_de_str(args.status).value

                if args.avaliacao is not None:
                    if novo["status"] != StatusJogo.FINALIZADO.value:
                        print("Só é possível avaliar jogos finalizados.")
                        return
                    if not validar_avaliacao(args.avaliacao):
                        print("Avaliação deve ser entre 0 e 10.")
                        return
                    novo["avaliacao"] = args.avaliacao

                if args.horas is not None:
                    novo["horas_jogadas"] = args.horas

                if args.genero:
                    novo["genero"] = args.genero

                if args.plataforma:
                    novo["platform"] = args.plataforma

                if args.novo_titulo:
                    novo["title"] = args.novo_titulo

                col["games"][i] = _jogo_para_dict(_jogo_de_dict(novo))
                salvar_armazenamento(armazenamento)
                print("Jogo atualizado.")
                return

        print("Jogo não encontrado.")
        return


if __name__ == "__main__":
    main()