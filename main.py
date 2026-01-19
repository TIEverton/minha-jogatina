"""
Módulo principal da aplicação 'minha-jogatina'.
Implementa uma CLI (Command Line Interface) para gerenciar coleções de jogos.
"""

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
from src.minha_jogatina.models.relatorio import Relatorio
from src.minha_jogatina.dados import RepositorioDados

# Caminho onde os dados das coleções serão armazenados no sistema de arquivos do usuário
CAMINHO_ARMAZENAMENTO = os.path.expanduser("~/.minha_jogatina_colecoes.json")


def carregar_armazenamento() -> Dict[str, Any]:
    """
    Carrega o arquivo JSON com as coleções de jogos do sistema.
    
    Se o arquivo não existir, retorna um dicionário vazio com estrutura padrão.
    Isso garante que sempre teremos a estrutura esperada mesmo na primeira execução.
    """
    if not os.path.exists(CAMINHO_ARMAZENAMENTO):
        return {"collections": {}}
    with open(CAMINHO_ARMAZENAMENTO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_armazenamento(armazenamento: Dict[str, Any]):
    """
    Persiste o armazenamento em memória para o arquivo JSON.
    
    Garante que todas as alterações feitas nas coleções e jogos sejam salvos permanentemente.
    """
    with open(CAMINHO_ARMAZENAMENTO, "w", encoding="utf-8") as f:
        json.dump(armazenamento, f, indent=2, ensure_ascii=False)


def _status_de_str(s: str) -> StatusJogo:
    """
    Converte uma string em um objeto StatusJogo.
    
    Busca correspondência pelo nome (ex: "NAO_INICIADO") ou valor (ex: "Não Iniciado").
    Se nenhuma correspondência for encontrada, retorna o status padrão NAO_INICIADO.
    """
    for st in StatusJogo:
        if s == st.name or s == st.value:
            return st
    return StatusJogo.NAO_INICIADO


def _jogo_de_dict(d: Dict[str, Any]):
    """
    Reconstrói um objeto Jogo a partir de um dicionário JSON.
    
    Este processo é necessário porque o JSON armazena dados simples (strings, números),
    mas precisamos de objetos Jogo com validações e comportamentos específicos.
    
    Processo:
    1. Extrai a plataforma do dicionário e cria a subclasse apropriada (JogoPC, JogoConsole ou JogoMobile)
    2. Popula as propriedades usando os setters, que garantem as validações
    3. Retorna o objeto Jogo completamente inicializado
    """
    platform = (d.get("platform") or "").lower()
    titulo = d.get("title") or ""
    genero = d.get("genero") or ""

    # Cria a subclasse correta baseado na plataforma
    if "pc" in platform:
        g = JogoPC(titulo, genero)
    elif "console" in platform:
        g = JogoConsole(titulo, genero)
    else:
        g = JogoMobile(titulo, genero)

    # Usa os setters das properties para garantir validações
    g.horas_jogadas = float(d.get("horas_jogadas", 0))
    g.status = _status_de_str(d.get("status", ""))

    # Só atribui avaliação se ela existir no dicionário
    if d.get("avaliacao") is not None:
        g.avaliacao = float(d.get("avaliacao"))

    return g


def _jogo_para_dict(g) -> Dict[str, Any]:
    """
    Converte um objeto Jogo em um dicionário JSON.
    
    Operação inversa de _jogo_de_dict().
    Extrai as propriedades do objeto Jogo e as organiza em um formato que pode ser 
    serializado como JSON para armazenamento persistente.
    """
    return {
        "title": g.titulo,
        "genero": g.genero,
        "platform": g.plataforma,
        "status": g.status.value,
        "horas_jogadas": g.horas_jogadas,
        "avaliacao": g.avaliacao,
    }


def validar_avaliacao(valor):
    """
    Verifica se uma avaliação está dentro do intervalo permitido (0 a 10).
    
    Retorna True se válida, False caso contrário.
    """
    return 0 <= valor <= 10


def _construir_jogos_de_armazenamento(armazenamento: Dict[str, Any], colecao_nome: str = None) -> List:
    """
    Reconstrói lista de objetos Jogo a partir do armazenamento JSON.
    
    Parâmetros:
        armazenamento: O dicionário com todas as coleções
        colecao_nome: Nome da coleção específica. Se None, retorna TODOS os jogos de todas as coleções
    
    Retorna:
        Lista de objetos Jogo completos (com validações e comportamentos)
    """
    jogos = []
    if colecao_nome:
        # Se uma coleção específica foi solicitada, busca apenas seus jogos
        col = armazenamento["collections"].get(colecao_nome, {})
        for g_dict in col.get("games", []):
            jogos.append(_jogo_de_dict(g_dict))
    else:
        # Se nenhuma coleção foi especificada, busca jogos de TODAS as coleções
        for col_name, col_data in armazenamento["collections"].items():
            for g_dict in col_data.get("games", []):
                jogos.append(_jogo_de_dict(g_dict))
    return jogos


def main():
    """
    Função principal que coordena toda a interface CLI da aplicação.
    
    O fluxo funciona assim:
    1. Define todos os subcomandos disponíveis e seus argumentos
    2. Carrega os dados do armazenamento JSON
    3. Processa o comando passado pelo usuário
    4. Executa a ação correspondente (CRUD de coleções/jogos, relatórios, etc)
    5. Persiste as mudanças no armazenamento
    """
    # Criador do parser de linha de comando
    parser = argparse.ArgumentParser(prog="minha-jogatina")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # ===== COMANDOS PARA GERENCIAR COLEÇÕES =====
    sub.add_parser("listar-colecoes")

    p_criar = sub.add_parser("criar-colecao")
    p_criar.add_argument("nome")

    p_deletar = sub.add_parser("deletar-colecao")
    p_deletar.add_argument("nome")

    # ===== COMANDOS PARA GERENCIAR JOGOS =====
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

    # ===== COMANDO ESPECIAL =====
    p_reiniciar = sub.add_parser("reiniciar-jogo")
    p_reiniciar.add_argument("colecao")
    p_reiniciar.add_argument("titulo")

    # ===== COMANDOS DE RELATÓRIOS =====
    p_total_horas = sub.add_parser("total-horas")
    p_total_horas.add_argument("--colecao")

    p_media_aval = sub.add_parser("media-avaliacao")
    p_media_aval.add_argument("--colecao")

    p_percent = sub.add_parser("percentual-status")
    p_percent.add_argument("--colecao")

    p_top5 = sub.add_parser("top-5-jogos")
    p_top5.add_argument("--colecao")

    p_filtro_genero = sub.add_parser("filtrar-por-genero")
    p_filtro_genero.add_argument("genero")
    p_filtro_genero.add_argument("--colecao")

    p_filtro_plat = sub.add_parser("filtrar-por-plataforma")
    p_filtro_plat.add_argument("plataforma", choices=["PC", "Console", "Mobile"])
    p_filtro_plat.add_argument("--colecao")

    p_filtro_status = sub.add_parser("filtrar-por-status")
    p_filtro_status.add_argument("status")
    p_filtro_status.add_argument("--colecao")

    p_buscar = sub.add_parser("buscar-por-titulo")
    p_buscar.add_argument("titulo")
    p_buscar.add_argument("--colecao")

    p_ordem_horas = sub.add_parser("ordenar-por-horas")
    p_ordem_horas.add_argument("--colecao")

    p_ordem_aval = sub.add_parser("ordenar-por-avaliacao")
    p_ordem_aval.add_argument("--colecao")

    # ===== COMANDOS PARA USAR MÉTODOS ESPECIAIS DAS CLASSES JOGO =====
    p_exibir = sub.add_parser("exibir-jogo")
    p_exibir.add_argument("colecao")
    p_exibir.add_argument("titulo")

    p_exibir_det = sub.add_parser("exibir-jogo-detalhes")
    p_exibir_det.add_argument("colecao")
    p_exibir_det.add_argument("titulo")

    p_comparar = sub.add_parser("comparar-jogos")
    p_comparar.add_argument("colecao")
    p_comparar.add_argument("titulo1")
    p_comparar.add_argument("titulo2")

    # ===== COMANDOS DE PERSISTÊNCIA DE DADOS =====
    p_salvar_dados = sub.add_parser("salvar-dados")
    p_salvar_dados.add_argument("--arquivo", default="dados.json")
    p_salvar_dados.add_argument("--formato", default="json", choices=["json", "sqlite"])
    p_salvar_dados.add_argument("--colecao")

    p_carregar_dados = sub.add_parser("carregar-dados")
    p_carregar_dados.add_argument("--arquivo", default="dados.json")
    p_carregar_dados.add_argument("--formato", default="json", choices=["json", "sqlite"])

    # Faz o parse dos argumentos da linha de comando
    args = parser.parse_args()
    
    # Carrega os dados do armazenamento
    armazenamento = carregar_armazenamento()

    # ===== EXECUÇÃO DO COMANDO: LISTAR COLEÇÕES =====
    if args.cmd == "listar-colecoes":
        for c in armazenamento["collections"]:
            print(c)
        return

    # ===== EXECUÇÃO DO COMANDO: CRIAR COLEÇÃO =====
    if args.cmd == "criar-colecao":
        # Cria uma nova entrada no dicionário de coleções com lista vazia de jogos
        armazenamento["collections"][args.nome] = {"games": []}
        salvar_armazenamento(armazenamento)
        print("Coleção criada.")
        return

    # ===== EXECUÇÃO DO COMANDO: DELETAR COLEÇÃO =====
    if args.cmd == "deletar-colecao":
        # Remove a coleção do dicionário (pop retorna None se não existir)
        armazenamento["collections"].pop(args.nome, None)
        salvar_armazenamento(armazenamento)
        print("Coleção deletada.")
        return

    # ===== EXECUÇÃO DO COMANDO: LISTAR JOGOS DE UMA COLEÇÃO =====
    if args.cmd == "listar-jogos":
        # Busca a coleção, extrai os jogos e exibe cada um
        for g in armazenamento["collections"].get(args.colecao, {}).get("games", []):
            print(g)
        return

    # ===== EXECUÇÃO DO COMANDO: ADICIONAR JOGO A UMA COLEÇÃO =====
    if args.cmd == "adicionar-jogo":
        # Valida se a avaliação (se fornecida) está no intervalo 0-10
        if args.avaliacao is not None and not validar_avaliacao(args.avaliacao):
            print("Avaliação deve ser entre 0 e 10.")
            return

        # Valida se está tentando avaliar um jogo que não foi finalizado
        if args.avaliacao is not None and _status_de_str(args.status) != StatusJogo.FINALIZADO:
            print("Só é possível avaliar jogos finalizados.")
            return

        # Cria o objeto Jogo com validações, depois converte para dicionário
        jogo = _jogo_para_dict(_jogo_de_dict(vars(args)))
        # Adiciona o jogo na lista de jogos da coleção
        armazenamento["collections"][args.colecao]["games"].append(jogo)
        salvar_armazenamento(armazenamento)
        print("Jogo adicionado.")
        return

    # ===== EXECUÇÃO DO COMANDO: REMOVER JOGO DE UMA COLEÇÃO =====
    if args.cmd == "remover-jogo":
        col = armazenamento["collections"][args.colecao]
        # Filtra a lista de jogos removendo o que tem o título procurado
        col["games"] = [g for g in col["games"] if g["title"].lower() != args.titulo.lower()]
        salvar_armazenamento(armazenamento)
        print("Jogo removido.")
        return

    # ===== EXECUÇÃO DO COMANDO: ATUALIZAR JOGO =====
    if args.cmd == "atualizar-jogo":
        col = armazenamento["collections"][args.colecao]

        # Procura pelo jogo na coleção
        for i, g in enumerate(col["games"]):
            if g["title"].lower() == args.titulo.lower():
                # Cria uma cópia do jogo para poder modificá-la
                novo = dict(g)

                # Valida que as horas não podem diminuir (apenas aumentar)
                if args.horas is not None and args.horas < g["horas_jogadas"]:
                    print("Horas não podem ser reduzidas.")
                    return

                # Atualiza o status se foi fornecido
                if args.status:
                    novo["status"] = _status_de_str(args.status).value

                # Atualiza a avaliação se foi fornecida (com validações)
                if args.avaliacao is not None:
                    if novo["status"] != StatusJogo.FINALIZADO.value:
                        print("Só é possível avaliar jogos finalizados.")
                        return
                    if not validar_avaliacao(args.avaliacao):
                        print("Avaliação deve ser entre 0 e 10.")
                        return
                    novo["avaliacao"] = args.avaliacao

                # Atualiza os campos opcionais se foram fornecidos
                if args.horas is not None:
                    novo["horas_jogadas"] = args.horas

                if args.genero:
                    novo["genero"] = args.genero

                if args.plataforma:
                    novo["platform"] = args.plataforma

                if args.novo_titulo:
                    novo["title"] = args.novo_titulo

                # Reconstrói o objeto Jogo (com validações) e salva novamente
                col["games"][i] = _jogo_para_dict(_jogo_de_dict(novo))
                salvar_armazenamento(armazenamento)
                print("Jogo atualizado.")
                return

        print("Jogo não encontrado.")
        return

    # ===== EXECUÇÃO DO COMANDO: REINICIAR JOGO =====
    if args.cmd == "reiniciar-jogo":
        col = armazenamento["collections"].get(args.colecao)
        if not col:
            print("Coleção não encontrada.")
            return

        for i, g in enumerate(col["games"]):
            if g["title"].lower() == args.titulo.lower():
                # Reconstrói o objeto Jogo a partir do dicionário
                jogo_obj = _jogo_de_dict(g)
                
                # Valida se pode reiniciar (não está NAO_INICIADO)
                if jogo_obj.status == StatusJogo.NAO_INICIADO:
                    print("Não é possível reiniciar um jogo que não foi iniciado.")
                    return

                # Reinicia o jogo: volta ao status JOGANDO, zera horas e remove avaliação
                jogo_obj._horas_jogadas = 0.0
                jogo_obj._status = StatusJogo.JOGANDO
                jogo_obj._avaliacao = None

                # Salva o jogo reiniciado
                col["games"][i] = _jogo_para_dict(jogo_obj)
                salvar_armazenamento(armazenamento)
                print("Jogo reiniciado.")
                return

        print("Jogo não encontrado.")
        return

    # ===== COMANDOS DE RELATÓRIOS =====
    # Todos os comandos de relatório seguem o mesmo padrão:
    # 1. Reconstrói a lista de objetos Jogo (da coleção específica ou de todas)
    # 2. Cria uma instância de Relatorio passando a lista
    # 3. Chama o método correspondente do Relatorio
    # 4. Exibe o resultado

    # --- RELATÓRIO: Total de horas jogadas ---
    if args.cmd == "total-horas":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        print(f"Total de horas: {relatorio.total_horas()}")
        return

    # --- RELATÓRIO: Média de avaliação dos jogos finalizados ---
    if args.cmd == "media-avaliacao":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        print(f"Média de avaliação (finalizados): {relatorio.media_avaliacao_finalizados()}")
        return

    # --- RELATÓRIO: Percentual de jogos por status ---
    if args.cmd == "percentual-status":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        percentuais = relatorio.percentual_por_status()
        for status, percent in percentuais.items():
            print(f"{status}: {percent:.2f}%")
        return

    # --- RELATÓRIO: Top 5 jogos mais jogados ---
    if args.cmd == "top-5-jogos":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        top5 = relatorio.top_5_mais_jogados()
        for jogo in top5:
            print(f"{jogo.titulo} - {jogo.horas_jogadas}h")
        return

    # --- RELATÓRIO: Filtrar por gênero ---
    if args.cmd == "filtrar-por-genero":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        filtrados = relatorio.filtrar_por_genero(args.genero)
        for jogo in filtrados:
            print(f"{jogo.titulo} ({jogo.genero})")
        return

    # --- RELATÓRIO: Filtrar por plataforma ---
    if args.cmd == "filtrar-por-plataforma":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        filtrados = relatorio.filtrar_por_plataforma(args.plataforma)
        for jogo in filtrados:
            print(f"{jogo.titulo} ({jogo.plataforma})")
        return

    # --- RELATÓRIO: Filtrar por status ---
    if args.cmd == "filtrar-por-status":
        status_obj = _status_de_str(args.status)
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        filtrados = relatorio.filtrar_por_status(status_obj)
        for jogo in filtrados:
            print(f"{jogo.titulo} ({jogo.status.value})")
        return

    # --- RELATÓRIO: Buscar por título (substring) ---
    if args.cmd == "buscar-por-titulo":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        encontrados = relatorio.buscar_por_titulo(args.titulo)
        for jogo in encontrados:
            print(f"{jogo.titulo}")
        return

    # --- RELATÓRIO: Ordenar por horas jogadas ---
    if args.cmd == "ordenar-por-horas":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        ordenados = relatorio.ordenar_por_horas()
        for jogo in ordenados:
            print(f"{jogo.titulo} - {jogo.horas_jogadas}h")
        return

    # --- RELATÓRIO: Ordenar por avaliação ---
    if args.cmd == "ordenar-por-avaliacao":
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        relatorio = Relatorio(jogos)
        ordenados = relatorio.ordenar_por_avaliacao()
        for jogo in ordenados:
            print(f"{jogo.titulo} - nota {jogo.avaliacao}")
        return

    # ===== COMANDOS DE PERSISTÊNCIA DE DADOS =====
    
    # --- COMANDO: Salvar dados em arquivo (JSON ou SQLite) ---
    if args.cmd == "salvar-dados":
        # Reconstrói os objetos Jogo (da coleção específica ou todas)
        jogos = _construir_jogos_de_armazenamento(armazenamento, args.colecao if hasattr(args, 'colecao') and args.colecao else None)
        # Cria repositório e salva no formato especificado
        repo = RepositorioDados(formato=args.formato, arquivo=args.arquivo)
        repo.salvar_jogos(jogos)
        print(f"Dados salvos em {args.arquivo}")
        return

    # --- COMANDO: Carregar dados de arquivo (JSON ou SQLite) ---
    if args.cmd == "carregar-dados":
        # Cria repositório e carrega jogos do arquivo
        repo = RepositorioDados(formato=args.formato, arquivo=args.arquivo)
        jogos = repo.carregar_jogos()
        print(f"Jogos carregados: {len(jogos)}")
        for jogo in jogos:
            print(f"  - {jogo.titulo} ({jogo.plataforma})")
        return

    # ===== COMANDOS PARA USAR MÉTODOS ESPECIAIS DAS CLASSES JOGO =====
    # Estes comandos demonstram o uso dos métodos especiais (__str__, __repr__, __eq__, __lt__)

    # --- COMANDO: Exibir jogo (usa __str__()) ---
    if args.cmd == "exibir-jogo":
        col = armazenamento["collections"].get(args.colecao)
        if not col:
            print("Coleção não encontrada.")
            return

        for g_dict in col["games"]:
            if g_dict["title"].lower() == args.titulo.lower():
                jogo_obj = _jogo_de_dict(g_dict)
                # __str__() retorna: "{titulo} ({plataforma}) - {status}"
                print(jogo_obj)
                return

        print("Jogo não encontrado.")
        return

    # --- COMANDO: Exibir jogo com detalhes (usa __repr__()) ---
    if args.cmd == "exibir-jogo-detalhes":
        col = armazenamento["collections"].get(args.colecao)
        if not col:
            print("Coleção não encontrada.")
            return

        for g_dict in col["games"]:
            if g_dict["title"].lower() == args.titulo.lower():
                jogo_obj = _jogo_de_dict(g_dict)
                # __repr__() retorna representação detalhada: Jogo(titulo='...', plataforma='...', status='...', horas=...)
                print(repr(jogo_obj))
                return

        print("Jogo não encontrado.")
        return

    # --- COMANDO: Comparar dois jogos (usa __eq__() e __lt__()) ---
    if args.cmd == "comparar-jogos":
        col = armazenamento["collections"].get(args.colecao)
        if not col:
            print("Coleção não encontrada.")
            return

        jogo1 = None
        jogo2 = None

        # Busca os dois jogos na coleção
        for g_dict in col["games"]:
            if g_dict["title"].lower() == args.titulo1.lower():
                jogo1 = _jogo_de_dict(g_dict)
            if g_dict["title"].lower() == args.titulo2.lower():
                jogo2 = _jogo_de_dict(g_dict)

        if not jogo1 or not jogo2:
            print("Um ou ambos os jogos não foram encontrados.")
            return

        # __eq__() compara título e plataforma (retorna True se são iguais)
        if jogo1 == jogo2:
            print(f"Os jogos '{args.titulo1}' e '{args.titulo2}' são iguais (mesmo título e plataforma).")
        else:
            print(f"Os jogos '{args.titulo1}' e '{args.titulo2}' são diferentes.")
            # __lt__() compara por horas jogadas (retorna True se jogo1 tem menos horas)
            if jogo1 < jogo2:
                print(f"  {jogo1.titulo} tem MENOS horas ({jogo1.horas_jogadas}h) que {jogo2.titulo} ({jogo2.horas_jogadas}h)")
            elif jogo2 < jogo1:
                print(f"  {jogo2.titulo} tem MENOS horas ({jogo2.horas_jogadas}h) que {jogo1.titulo} ({jogo1.horas_jogadas}h)")
            else:
                print(f"  Ambos têm o mesmo número de horas: {jogo1.horas_jogadas}h")
        return

    # Se nenhum comando foi reconhecido, exibe a ajuda
    parser.print_help()


if __name__ == "__main__":
    main()