import json
import os
import re
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# CAMINHOS DO PROJETO
# =========================================================

# Pasta em que este arquivo extrair_metadados.py está.
PASTA_AULA_02 = Path(__file__).resolve().parent

# Pasta AULA_01, que contém o .env.
PASTA_RAIZ = PASTA_AULA_02.parent

PASTA_MARKDOWN = PASTA_AULA_02 / "markdown"
PASTA_METADADOS = PASTA_AULA_02 / "metadados"
CAMINHO_ENV = PASTA_RAIZ / ".env"


# =========================================================
# VARIÁVEIS DE AMBIENTE
# =========================================================

load_dotenv(CAMINHO_ENV)

API_KEY = os.getenv("OPENROUTER_API_KEY")

BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)

MODELO = os.getenv("OPENROUTER_MODEL")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY não foi encontrada no arquivo .env."
    )

if not MODELO:
    raise ValueError(
        "OPENROUTER_MODEL não foi encontrado no arquivo .env."
    )


# =========================================================
# CLIENTE OPENROUTER
# =========================================================

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


# =========================================================
# JSON SCHEMA
# =========================================================

SCHEMA_METADADOS: dict[str, Any] = {
    "name": "metadados_artigo",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "titulo": {
                "type": "string",
                "description": (
                    "Título oficial e completo do artigo ou trabalho."
                )
            },
            "autores": {
                "type": "array",
                "description": (
                    "Lista somente com os nomes dos autores do trabalho."
                ),
                "items": {
                    "type": "string"
                }
            },
            "ano": {
                "type": "integer",
                "description": (
                    "Ano oficial de publicação do próprio trabalho."
                )
            }
        },
        "required": [
            "titulo",
            "autores",
            "ano"
        ],
        "additionalProperties": False
    }
}


# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================

def limpar_resposta_json(resposta: str) -> str:
    """
    Remove possíveis blocos ```json ... ``` da resposta.
    """

    resposta = resposta.strip()

    resposta = re.sub(
        r"^```(?:json)?\s*",
        "",
        resposta,
        flags=re.IGNORECASE
    )

    resposta = re.sub(
        r"\s*```$",
        "",
        resposta
    )

    return resposta.strip()


def validar_metadados(
    metadados: dict[str, Any]
) -> dict[str, Any]:
    """
    Confere se o objeto retornado possui os campos e
    os tipos definidos na tarefa.
    """

    campos_esperados = {
        "titulo",
        "autores",
        "ano"
    }

    if set(metadados.keys()) != campos_esperados:
        raise ValueError(
            "O JSON retornado não possui exatamente os campos "
            "'titulo', 'autores' e 'ano'."
        )

    if not isinstance(metadados["titulo"], str):
        raise TypeError(
            "O campo 'titulo' precisa ser uma string."
        )

    if not metadados["titulo"].strip():
        raise ValueError(
            "O campo 'titulo' está vazio."
        )

    if not isinstance(metadados["autores"], list):
        raise TypeError(
            "O campo 'autores' precisa ser uma lista."
        )

    if not metadados["autores"]:
        raise ValueError(
            "A lista de autores está vazia."
        )

    if not all(
        isinstance(autor, str) and autor.strip()
        for autor in metadados["autores"]
    ):
        raise TypeError(
            "Todos os autores precisam ser strings válidas."
        )

    if not isinstance(metadados["ano"], int):
        raise TypeError(
            "O campo 'ano' precisa ser um número inteiro."
        )

    if not 1800 <= metadados["ano"] <= 2100:
        raise ValueError(
            f"Ano de publicação inválido: {metadados['ano']}"
        )

    # Remove espaços extras.
    metadados["titulo"] = metadados["titulo"].strip()

    metadados["autores"] = [
        autor.strip()
        for autor in metadados["autores"]
    ]

    return metadados


# =========================================================
# FUNÇÃO PRINCIPAL SOLICITADA NA TAREFA
# =========================================================

def extrair_metadados(
    caminho_md: Path,
    tentativas: int = 3
) -> dict[str, Any]:
    """
    Recebe o caminho de um arquivo Markdown e retorna
    seus metadados em um dicionário Python estruturado.

    Campos retornados:
    - titulo
    - autores
    - ano
    """

    if not caminho_md.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho_md}"
        )

    if caminho_md.suffix.lower() != ".md":
        raise ValueError(
            f"O arquivo precisa ser .md: {caminho_md.name}"
        )

    conteudo = caminho_md.read_text(
        encoding="utf-8"
    )

    if not conteudo.strip():
        raise ValueError(
            f"O arquivo está vazio: {caminho_md.name}"
        )

    # Os metadados normalmente ficam nas primeiras páginas.
    # Usar apenas o início também evita que anos das referências
    # bibliográficas confundam o modelo.
    trecho_inicial = conteudo[:18000]

    prompt = f"""
Extraia os metadados bibliográficos do artigo acadêmico abaixo.

REGRAS OBRIGATÓRIAS:

1. "titulo" deve conter o título principal e oficial do trabalho.
2. "autores" deve conter somente os autores do próprio trabalho.
3. Não inclua editores, instituições ou autores das referências.
4. "ano" deve ser o ano oficial de publicação do próprio trabalho.
5. Procure o ano no cabeçalho, rodapé, identificação da revista,
   DOI, informações de recebimento/publicação ou primeira página.
6. Não use anos mencionados no resumo, corpo do texto ou referências.
7. Não invente dados.
8. Retorne apenas o objeto definido no JSON Schema.

Nome do arquivo:
{caminho_md.name}

INÍCIO DO DOCUMENTO EM MARKDOWN:

{trecho_inicial}
"""

    ultimo_erro: Exception | None = None

    for tentativa in range(1, tentativas + 1):
        try:
            print(
                f"  Consultando o modelo "
                f"(tentativa {tentativa}/{tentativas})..."
            )

            resposta = client.chat.completions.create(
                model=MODELO,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é especialista em catalogação "
                            "bibliográfica e identificação de metadados "
                            "de artigos científicos. Analise principalmente "
                            "a primeira página e nunca confunda anos das "
                            "referências com o ano de publicação."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": SCHEMA_METADADOS
                },
                temperature=0,
                max_tokens=500,
                stream=False,
                extra_body={
                    "provider": {
                        "require_parameters": True
                    },
                    "plugins": [
                        {
                            "id": "response-healing"
                        }
                    ]
                }
            )

            mensagem = resposta.choices[0].message
            conteudo_resposta = mensagem.content

            if conteudo_resposta is None:
                raise ValueError(
                    "O modelo não devolveu conteúdo."
                )

            conteudo_resposta = limpar_resposta_json(
                conteudo_resposta
            )

            if not conteudo_resposta:
                raise ValueError(
                    "O modelo devolveu uma resposta vazia."
                )

            print(
                f"  Resposta recebida: "
                f"{conteudo_resposta}"
            )

            metadados = json.loads(
                conteudo_resposta
            )

            metadados = validar_metadados(
                metadados
            )

            return metadados

        except Exception as erro:
            ultimo_erro = erro

            print(
                f"  Falha na tentativa {tentativa}: {erro}"
            )

            if tentativa < tentativas:
                time.sleep(2)

    raise RuntimeError(
        f"Não foi possível extrair os metadados de "
        f"{caminho_md.name} após {tentativas} tentativas. "
        f"Último erro: {ultimo_erro}"
    )


# =========================================================
# PROCESSAMENTO DE TODOS OS MARKDOWNS
# =========================================================

def processar_todos_os_markdowns() -> None:
    """
    Processa todos os arquivos .md da pasta markdown
    e salva um arquivo .json para cada documento.
    """

    PASTA_METADADOS.mkdir(
        parents=True,
        exist_ok=True
    )

    arquivos_md = sorted(
        PASTA_MARKDOWN.glob("*.md")
    )

    if not arquivos_md:
        print(
            "Nenhum arquivo .md foi encontrado na pasta markdown."
        )
        return

    print("=" * 60)
    print("EXTRAÇÃO DE METADADOS DOS ARQUIVOS MARKDOWN")
    print(f"Modelo utilizado: {MODELO}")
    print("=" * 60)

    quantidade_sucessos = 0
    quantidade_erros = 0

    for caminho_md in arquivos_md:
        print(f"\nProcessando: {caminho_md.name}")

        try:
            metadados = extrair_metadados(
                caminho_md
            )

            caminho_json = (
                PASTA_METADADOS
                / f"{caminho_md.stem}.json"
            )

            caminho_json.write_text(
                json.dumps(
                    metadados,
                    ensure_ascii=False,
                    indent=2
                ),
                encoding="utf-8"
            )

            quantidade_sucessos += 1

            print("  Metadados extraídos com sucesso:")
            print(
                json.dumps(
                    metadados,
                    ensure_ascii=False,
                    indent=2
                )
            )
            print(
                f"  JSON salvo em: {caminho_json}"
            )

        except Exception as erro:
            quantidade_erros += 1

            print(
                f"  Erro ao processar "
                f"{caminho_md.name}: {erro}"
            )

    print("\n" + "=" * 60)
    print("PROCESSAMENTO FINALIZADO")
    print(f"Arquivos processados com sucesso: {quantidade_sucessos}")
    print(f"Arquivos com erro: {quantidade_erros}")
    print("=" * 60)


# =========================================================
# EXECUÇÃO
# =========================================================

if __name__ == "__main__":
    processar_todos_os_markdowns()