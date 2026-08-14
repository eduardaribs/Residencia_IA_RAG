# Aula 05 — Documents e Metadados com LangChain

## Objetivo

Esta atividade tem como objetivo compreender a estrutura `Document` utilizada pelo ecossistema LangChain e projetar metadados adequados para representar os chunks produzidos anteriormente.

Na Aula 04, os chunks foram representados manualmente por estruturas contendo texto, identificadores, embeddings e metadados. Nesta aula, essa representação é adaptada para o formato padrão `Document` do LangChain.

Um `Document` possui dois componentes principais:

- `page_content`: conteúdo textual do documento;
- `metadata`: informações adicionais utilizadas para identificação, rastreamento e filtragem.

Os embeddings não fazem parte diretamente do objeto `Document`, sendo responsabilidade da vector store.

---

## Exercício 1 — Criando Documents manualmente

Foram criados manualmente cinco objetos `Document` abordando diferentes temas relacionados ao curso:

- embeddings;
- similaridade de cosseno;
- chunking;
- RAG;
- tokenização.

Cada objeto foi construído utilizando a estrutura:

```python
Document(
    page_content="Conteúdo do documento",
    metadata={
        "fonte": "arquivo.md",
        "pagina": 1,
        "tipo": "teoria",
        "tema": "embeddings",
        "autor": "Maria Eduarda Ribeiro da Silva"
    }
)
```

Foram exibidos o `page_content` e os metadados de cada documento e verificada a quantidade total de objetos utilizando `len(documentos)`.

### Tipos de dados em metadata

Durante os testes, foram utilizados diferentes tipos de dados dentro de `metadata`, incluindo:

- strings;
- números;
- valores booleanos;
- listas;
- dicionários aninhados.

O objeto `Document` permite armazenar essas estruturas. Entretanto, determinadas vector stores podem impor restrições aos tipos de metadados utilizados para indexação e filtragem.

### Document sem metadata

Também foi criado um `Document` sem informar explicitamente o campo `metadata`.

Nesse caso, o LangChain utiliza automaticamente um dicionário vazio:

```python
{}
```

Portanto, não é obrigatório fornecer metadados para criar um objeto `Document`.

---

## Exercício 2 — Projetando o schema de metadados

Foi definido um schema para organizar os metadados dos chunks produzidos na Aula 04.

| Campo | Tipo | Descrição |
|---|---|---|
| `fonte` | string | Nome do arquivo `.md` de origem |
| `documento_id` | string | Identificador do documento |
| `chunk_index` | int | Posição do chunk dentro do documento |
| `estrategia` | string | Estratégia de chunking utilizada |
| `chunk_size` | int ou null | Tamanho configurado para o chunk |
| `chunk_overlap` | int | Sobreposição configurada |
| `n_caracteres` | int | Quantidade real de caracteres do chunk |
| `secao` | string ou null | Seção do documento de origem |
| `subdividido` | bool | Indica se o chunk precisou ser subdividido |
| `idioma` | string | Idioma predominante do conteúdo |

### Campos adicionais

Além dos campos obrigatórios, foram adicionados três campos ao schema.

**`secao`**

Permite identificar em qual parte do documento o chunk estava localizado, facilitando a localização da informação original e possibilitando filtros por seção.

**`subdividido`**

Permite identificar chunks que precisaram passar por uma subdivisão adicional durante o processamento, auxiliando na rastreabilidade das transformações realizadas.

**`idioma`**

Permite identificar o idioma predominante do conteúdo e possibilita futuras buscas ou filtros em corpora multilíngues.

---

## Exemplo de metadados

Um exemplo da estrutura definida é:

```json
{
  "fonte": "bioetica_e_ia.md",
  "documento_id": "doc03",
  "chunk_index": 12,
  "estrategia": "recursive",
  "chunk_size": 1000,
  "chunk_overlap": 100,
  "n_caracteres": 823,
  "secao": "Autonomia e opacidade algorítmica",
  "subdividido": false,
  "idioma": "pt"
}
```

---

## Metadados para citação em RAG

Para permitir que um sistema RAG informe ao usuário de onde uma informação foi recuperada, são especialmente importantes os campos:

- `fonte`;
- `secao`;
- `pagina`, quando essa informação estiver disponível.

O campo `fonte` identifica o documento original, enquanto `secao` e `pagina` permitem localizar a informação com maior precisão.

---

## Importância do chunk_index

O campo `chunk_index` registra a posição do chunk dentro do documento original.

Essa informação é especialmente útil quando um trecho recuperado termina no meio de uma explicação. Conhecendo sua posição, é possível recuperar o chunk anterior (`chunk_index - 1`) ou o seguinte (`chunk_index + 1`) para obter contexto adicional.

Assim, o sistema pode ampliar o contexto de uma informação recuperada sem precisar processar novamente todo o documento.

---

## Estrutura da atividade

```text
AULA_05/
├── aula_05_documents_vectorstore.ipynb
└── README.md
```

O notebook contém a implementação dos exercícios, os testes realizados e as respostas às questões propostas.