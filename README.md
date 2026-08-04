# Introdução à IA - Aula 01

Este projeto contém o código inicial para interação com modelos de linguagem (LLMs) utilizando Python e OpenRouter.

## Tecnologias

- Python 3
- OpenRouter
- SDK OpenAI
- python-dotenv

## Estrutura do projeto

```
.
├── hello_llm.py
├── hello_llm.ipynb
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalação

Crie o ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env`:

```env
OPENROUTER_API_KEY=sua_chave
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
```

## Executar

```bash
python hello_llm.py
```