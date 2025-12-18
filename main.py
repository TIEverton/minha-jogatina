from src.minha_jogatina import (
    StatusJogo,
    JogoPC,
    JogoConsole,
    Colecao
)

def main():
    # PARA TESTES INICIAIS
    jogo1 = JogoPC("The Witcher 3", "RPG")
    jogo1.horas_jogadas = 50.5
    jogo1.status = StatusJogo.JOGANDO
    
    jogo2 = JogoConsole("God of War", "Ação")
    jogo2.horas_jogadas = 25.0
    jogo2.status = StatusJogo.FINALIZADO
    jogo2.avaliacao = 9.5
    
    colecao = Colecao("Meus Jogos")
    colecao.adicionar_jogo(jogo1)
    colecao.adicionar_jogo(jogo2)
    
    print(colecao)
    for jogo in colecao.listar_jogos():
        print(f"  - {jogo}")


if __name__ == "__main__":
    main()