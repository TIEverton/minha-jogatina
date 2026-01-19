# Minha Jogatina 🎮

Aplicação CLI para gerenciar coleções de jogos. Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (UFCA).

## Instalação

### Método 1: Instalação Local (Recomendado)

Clone ou baixe o repositório e instale em modo desenvolvimento:

```bash
git clone https://github.com/TIEverton/minha-jogatina/
cd minha-jogatina
pip install -e .
```

Após a instalação, você pode usar em qualquer lugar:

```bash
minha-jogatina listar-colecoes
minha_jogatina criar-colecao "Meus Jogos"
```

## Como Usar

**Listar coleções:**
```bash
minha-jogatina listar-colecoes
```

**Criar uma coleção:**
```bash
minha-jogatina criar-colecao "Meus Favoritos"
```

**Adicionar um jogo:**
```bash
minha-jogatina adicionar-jogo "Meus Favoritos" \
  --titulo "The Witcher 3" \
  --genero "RPG" \
  --plataforma PC \
  --status "Jogando" \
  --horas 50
```

**Listar jogos:**
```bash
minha-jogatina listar-jogos "Meus Favoritos"
```

**Ver detalhes de um jogo:**
```bash
minha-jogatina exibir-jogo-detalhes "Meus Favoritos" "The Witcher 3"
```

**Gerar relatórios:**
```bash
minha-jogatina total-horas
minha-jogatina top-5-jogos
minha-jogatina media-avaliacao
```

**Ver ajuda completa:**
```bash
minha-jogatina -h
```

## Conceitos de POO Implementados

- **Herança:** Classe base `Jogo` e subclasses `JogoPC`, `JogoConsole` e `JogoMobile`
- **Encapsulamento:** Uso de `@property` para validar dados (título não vazio, horas não negativas, avaliação 0-10)
- **Regras de Negócio:** Sistema impede jogo finalizado com <1h, avaliação só após finalização
- **Métodos Especiais:** `__str__()`, `__repr__()`, `__eq__()`, `__lt__()` para exibição e ordenação

## Armazenamento de Dados

Os dados são salvos em: `~/.minha_jogatina_colecoes.json`

## Requisitos

- Python 3.8+
