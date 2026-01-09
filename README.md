# Catálogo de Jogos Digitais

Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (UFCA).

## O que foi feito até agora (Entrega 2)
Nesta etapa, foquei na estruturação das classes principais usando os conceitos de POO:
- **Herança:** Criei a classe base Jogo e as subclasses JogoPC, JogoConsole e JogoMobile.
- **Encapsulamento:** Usei @property para validar se o título está vazio, se as horas são negativas e para controlar a nota (0 a 10).
- **Regras de Negócio:** O sistema agora impede que um jogo seja finalizado com menos de 1h e só permite dar nota para jogos terminados.
- **Métodos Especiais:** Implementei __str__, __repr__, __eq__ e __lt__ para facilitar a exibição e ordenação dos jogos.

## Como testar
O arquivo main.py contém alguns testes iniciais para validar as travas de segurança e a criação dos objetos.
