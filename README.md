# Minha Jogatina 🎮

Aplicação CLI para gerenciar coleções de jogos. Projeto desenvolvido para a disciplina de Programação Orientada a Objetos (UFCA).

**Observação para o professor/tutor:** Os commits da conta edgarestevam contém código tanto da parte do aluno Edgar quanto da parte do aluno Petrus.

## Instalação

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

### Gerenciamento de Coleções

**Listar todas as coleções:**
```bash
minha-jogatina listar-colecoes
```

**Criar uma coleção:**
```bash
minha-jogatina criar-colecao "Meus Favoritos"
```

**Excluir uma coleção:**
```bash
minha-jogatina excluir-colecao "Meus Favoritos"
```

### Gerenciamento de Jogos

**Adicionar um jogo:**
```bash
minha-jogatina adicionar-jogo "Meus Favoritos" \
  --titulo "The Witcher 3" \
  --genero "RPG" \
  --plataforma PC \
  --status "JOGANDO" \
  --horas 50
```

**Listar jogos de uma coleção:**
```bash
minha-jogatina listar-jogos "Meus Favoritos"
```

**Exibir detalhes de um jogo:**
```bash
minha-jogatina exibir-jogo-detalhes "Meus Favoritos" "The Witcher 3"
```

**Atualizar um jogo:**
```bash
minha-jogatina atualizar-jogo "Meus Favoritos" "The Witcher 3" \
  --status "FINALIZADO" \
  --horas 80 \
  --avaliacao 9
```

**Excluir um jogo:**
```bash
minha-jogatina excluir-jogo "Meus Favoritos" "The Witcher 3"
```

### Relatórios e Estatísticas

**Total de horas jogadas:**
```bash
minha-jogatina total-horas
```

**Top 5 jogos mais bem avaliados:**
```bash
minha-jogatina top-5-jogos
```

**Média de avaliação:**
```bash
minha-jogatina media-avaliacao
```

### Status Disponíveis

- `NÃO INICIADO` - Jogo ainda não iniciado
- `JOGANDO` - Jogo em progresso
- `FINALIZADO` - Jogo completado

### Ajuda

**Ver ajuda completa:**
```bash
minha-jogatina -h
```

**Ver ajuda de um comando específico:**
```bash
minha-jogatina adicionar-jogo -h
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
