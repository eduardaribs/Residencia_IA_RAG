# Aula 02 – Conversão de PDFs e Extração de Metadados

## Objetivo

Esta atividade tem como objetivo converter artigos científicos em PDF para o formato Markdown utilizando o Docling e, posteriormente, extrair metadados estruturados utilizando Structured Outputs por meio da API do OpenRouter.

---

## Estrutura do projeto

```
AULA_02/
│
├── artigos/
│   ├── bioetica_e_ia.pdf
│   ├── escrita_academica_ia.pdf
│   └── twitter_algoritmo.pdf
│
├── markdown/
│   ├── bioetica_e_ia.md
│   ├── escrita_academica_ia.md
│   └── twitter_algoritmo.md
│
├── metadados/
│   ├── bioetica_e_ia.json
│   ├── escrita_academica_ia.json
│   └── twitter_algoritmo.json
│
├── quickstart.py
├── extrair_metadados.py
└── README.md
```

---

## Tecnologias utilizadas

- Python 3
- Docling
- OpenRouter
- OpenAI SDK
- python-dotenv

---

## Conversão dos PDFs

O arquivo `quickstart.py` percorre todos os arquivos PDF presentes na pasta `artigos`, realiza a conversão para Markdown utilizando o Docling e salva os arquivos gerados na pasta `markdown`.

---

## Extração dos metadados

O arquivo `extrair_metadados.py` realiza a leitura dos arquivos Markdown e utiliza Structured Outputs para extrair automaticamente:

- Título do trabalho;
- Autores;
- Ano de publicação.

Os resultados são armazenados em arquivos JSON na pasta `metadados`.

---

## Formato dos metadados

Exemplo:

```json
{
  "titulo": "Título do trabalho",
  "autores": [
    "Autor 1",
    "Autor 2"
  ],
  "ano": 2024
}
```

---

## Como executar

### 1. Ativar o ambiente virtual

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Converter os PDFs

```powershell
python quickstart.py
```

### 3. Extrair os metadados

```powershell
python extrair_metadados.py
```

---

## Autor

Maria Eduarda Ribeiro da Silva