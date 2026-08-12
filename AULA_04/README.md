# Aula 04 — Estratégias de Chunking e Embeddings

## 1. Objetivo

Esta atividade tem como objetivo experimentar e comparar diferentes estratégias de segmentação de documentos (chunking), analisando como o tamanho, a sobreposição e a estrutura dos chunks influenciam a geração de embeddings e a recuperação semântica de informações.

A atividade foi desenvolvida em duas etapas principais. Inicialmente, diferentes configurações de chunking foram testadas em um documento de referência. Posteriormente, estratégias selecionadas foram aplicadas a um corpus composto por 12 documentos relacionados à Inteligência Artificial, modelos de linguagem, Transformers, RAG e aplicações de IA.

Os embeddings foram gerados utilizando o modelo:

`nvidia/llama-nemotron-embed-vl-1b-v2:free`

A dimensão dos vetores gerados foi de **2048**.

---

## 2. Estrutura da atividade

O desenvolvimento foi organizado nas seguintes etapas:

1. Conversão dos documentos PDF para Markdown;
2. Experimentação de diferentes configurações de chunking;
3. Comparação quantitativa dos chunks;
4. Seleção de estratégias para aplicação ao corpus;
5. Processamento dos 12 documentos;
6. Geração de embeddings;
7. Tratamento de chunks que excederam o limite suportado pelo modelo;
8. Validação dos arquivos gerados;
9. Implementação de busca semântica;
10. Comparação dos resultados de recuperação entre as estratégias.

---

## 3. Corpus utilizado

O corpus final é composto por 12 documentos:

- `attention_is_all_you_need.md`
- `bert_pretraining.md`
- `bioetica_e_ia.md`
- `escrita_academica_ia.md`
- `gpt3_language_models.md`
- `gpt4_technical_report.md`
- `instruct_gpt.md`
- `llama_foundation_models.md`
- `lora_low_rank_adaptation.md`
- `retrieval_augmented_generation.md`
- `scaling_laws_llm.md`
- `twitter_algoritmo.md`

Os arquivos PDF foram convertidos para Markdown antes da realização dos experimentos de chunking.

---

## 4. Experimentos iniciais de chunking

Os experimentos iniciais foram realizados utilizando o documento `bioetica_e_ia.md`.

Foram avaliadas 10 configurações diferentes, incluindo segmentação fixa, segmentação com overlap, divisão por parágrafos, sentenças, divisão recursiva e estrutura Markdown.

| Teste | Estratégia | Chunk Size | Overlap | Nº de Chunks | Média | Mínimo | Máximo |
|------:|------------|-----------:|--------:|-------------:|------:|-------:|-------:|
| 1 | Fixed | 200 | 0 | 222 | 199.42 | 146 | 200 |
| 2 | Fixed | 500 | 0 | 89 | 497.92 | 347 | 500 |
| 3 | Fixed | 1000 | 0 | 45 | 985.13 | 347 | 1000 |
| 4 | Fixed | 2000 | 0 | 23 | 1927.87 | 347 | 2000 |
| 5 | Fixed com overlap | 500 | 50 | 99 | 497.13 | 246 | 500 |
| 6 | Fixed com overlap | 500 | 200 | 148 | 497.91 | 246 | 500 |
| 7 | Paragraph | 1000 | 0 | 57 | 776.33 | 195 | 1360 |
| 8 | Sentence | — | 0 | 86 | 513.50 | 56 | 1088 |
| 9 | Recursive | 1000 | 100 | 65 | 695.02 | 102 | 999 |
| 10 | Markdown | — | 0 | 19 | 2283.53 | 20 | 6946 |

Os resultados completos dessa etapa estão armazenados em:

`results/summary.json`

---

## 5. Estratégias selecionadas para o corpus

Após os experimentos iniciais, foram utilizadas três estratégias para o processamento dos 12 documentos:

### Recursive

Utiliza divisão recursiva do texto, buscando respeitar limites de tamanho e mantendo uma pequena sobreposição entre chunks.

Essa abordagem apresentou tamanhos mais controlados e relativamente uniformes.

### Paragraph

Utiliza a estrutura de parágrafos do documento como unidade de segmentação.

Essa abordagem tende a preservar unidades textuais semanticamente completas, embora possa produzir chunks de tamanhos bastante diferentes.

### Markdown

Utiliza a estrutura do próprio documento Markdown, como títulos e seções, para realizar a segmentação.

Essa abordagem preserva melhor a organização estrutural do documento, mas pode gerar chunks muito grandes quando uma seção contém grande quantidade de texto.

---

## 6. Processamento do corpus

As três estratégias foram aplicadas aos 12 documentos.

Dessa forma, foram produzidas:

**12 documentos × 3 estratégias = 36 combinações de processamento.**

Para cada combinação foram armazenados os chunks e posteriormente seus respectivos embeddings.

Os resultados consolidados estão disponíveis em:

`results/summary_corpus.json`

---

## 7. Geração de embeddings

Os chunks produzidos foram transformados em representações vetoriais utilizando o modelo:

`nvidia/llama-nemotron-embed-vl-1b-v2:free`

Cada embedding possui:

**2048 dimensões**

Os embeddings foram processados em lotes e armazenados juntamente com os respectivos textos e metadados nos arquivos:

`chunks_embeddings.json`

---

## 8. Tratamento de chunks muito grandes

Durante a geração dos embeddings, alguns chunks ultrapassaram o limite máximo aceito pelo modelo.

O erro observado indicava entradas superiores ao limite de **8192 tokens**.

O problema ocorreu principalmente em documentos extensos e em estratégias que preservavam grandes blocos estruturais.

Foram identificados casos problemáticos em:

- `gpt3_language_models` — Paragraph;
- `gpt3_language_models` — Markdown;
- `gpt4_technical_report` — Markdown.

Para evitar a perda de contexto e permitir a geração dos embeddings, os chunks excessivamente grandes foram subdivididos utilizando `RecursiveCharacterTextSplitter`.

Foi utilizada a configuração:

- `chunk_size = 6000`
- `chunk_overlap = 300`

Após o tratamento, o maior chunk corrigido apresentou **5999 caracteres**.

Os resultados finais foram:

| Documento | Estratégia | Chunks finais | Chunks subdivididos | Maior chunk |
|------------|------------|--------------:|--------------------:|------------:|
| GPT-3 | Paragraph | 599 | 10 | 5999 |
| GPT-3 | Markdown | 88 | 49 | 5999 |
| GPT-4 Technical Report | Markdown | 211 | 24 | 5999 |

Esse tratamento permitiu concluir a geração dos embeddings sem exceder o limite do modelo.

---

## 9. Validação dos embeddings

Após o processamento, foi realizada uma verificação automática dos arquivos gerados.

Resultado:

- Arquivos esperados: **36**
- Arquivos encontrados: **36**
- Dimensão esperada: **2048**
- Problemas encontrados: **0**

Portanto, todas as combinações documento/estratégia possuem embeddings válidos.

---

## 10. Busca semântica

Após a geração dos embeddings, foi implementada uma busca semântica utilizando similaridade de cosseno.

A consulta é transformada em um embedding utilizando o mesmo modelo empregado nos chunks.

Em seguida, o vetor da consulta é comparado com os embeddings armazenados.

A similaridade de cosseno permite ordenar os chunks de acordo com sua proximidade semântica com a consulta.

Foram utilizadas três consultas:

1. **Como os modelos de linguagem utilizam mecanismos de atenção?**
2. **Como o aprendizado por reforço com feedback humano é utilizado para alinhar modelos de linguagem?**
3. **Como a recuperação de documentos externos pode melhorar as respostas de modelos de linguagem?**

Para cada pergunta foram comparados os três primeiros resultados das estratégias Recursive, Paragraph e Markdown.

---

## 11. Comparação da recuperação semântica

### Pergunta 1

**Como os modelos de linguagem utilizam mecanismos de atenção?**

| Estratégia | TOP 1 | Score | TOP 2 | Score | TOP 3 | Score |
|------------|-------|------:|-------|------:|-------|------:|
| Recursive | llama_foundation_models | 0.3416 | gpt3_language_models | 0.3411 | instruct_gpt | 0.3276 |
| Paragraph | escrita_academica_ia | 0.4275 | gpt3_language_models | 0.4126 | attention_is_all_you_need | 0.3739 |
| Markdown | llama_foundation_models | 0.3052 | llama_foundation_models | 0.3039 | attention_is_all_you_need | 0.3025 |

Embora `attention_is_all_you_need` seja o documento diretamente relacionado ao tema da consulta, ele não apareceu na primeira posição. Entretanto, foi recuperado entre os três primeiros resultados pelas estratégias Paragraph e Markdown.

Isso demonstra que um maior valor de similaridade não necessariamente corresponde ao resultado qualitativamente mais adequado.

---

### Pergunta 2

**Como o aprendizado por reforço com feedback humano é utilizado para alinhar modelos de linguagem?**

| Estratégia | TOP 1 | Score | TOP 2 | Score | TOP 3 | Score |
|------------|-------|------:|-------|------:|-------|------:|
| Recursive | gpt4_technical_report | 0.5314 | instruct_gpt | 0.5179 | instruct_gpt | 0.4435 |
| Paragraph | instruct_gpt | 0.5282 | gpt4_technical_report | 0.5257 | instruct_gpt | 0.5131 |
| Markdown | instruct_gpt | 0.4312 | instruct_gpt | 0.4103 | gpt4_technical_report | 0.3819 |

Para essa consulta, as três estratégias apresentaram resultados relacionados ao tema.

A estratégia Paragraph recuperou `instruct_gpt` diretamente na primeira posição, enquanto Recursive apresentou o relatório técnico do GPT-4 na primeira posição e `instruct_gpt` logo em seguida.

---

### Pergunta 3

**Como a recuperação de documentos externos pode melhorar as respostas de modelos de linguagem?**

| Estratégia | TOP 1 | Score | TOP 2 | Score | TOP 3 | Score |
|------------|-------|------:|-------|------:|-------|------:|
| Recursive | retrieval_augmented_generation | 0.3621 | retrieval_augmented_generation | 0.3532 | gpt3_language_models | 0.3251 |
| Paragraph | retrieval_augmented_generation | 0.3620 | retrieval_augmented_generation | 0.3592 | escrita_academica_ia | 0.3465 |
| Markdown | retrieval_augmented_generation | 0.3524 | retrieval_augmented_generation | 0.3308 | retrieval_augmented_generation | 0.3305 |

Essa consulta apresentou os resultados mais consistentes.

As três estratégias recuperaram `retrieval_augmented_generation` na primeira posição, demonstrando forte correspondência entre a consulta e o documento relacionado a RAG.

---

## 12. Análise comparativa

Os experimentos demonstraram que a estratégia de chunking interfere diretamente na representação vetorial e, consequentemente, nos resultados da recuperação semântica.

A estratégia **Recursive** apresentou maior controle sobre o tamanho dos chunks. Com `chunk_size` próximo de 1000 caracteres, os segmentos permaneceram relativamente uniformes, facilitando o processamento e reduzindo problemas relacionados a entradas excessivamente grandes.

A estratégia **Paragraph** produziu chunks de tamanhos mais variados, mas apresentou bons resultados qualitativos nas consultas semânticas. Na consulta relacionada a RLHF, por exemplo, recuperou `instruct_gpt` diretamente na primeira posição.

A estratégia **Markdown** apresentou a vantagem de preservar a estrutura lógica dos documentos, respeitando títulos e seções. Entretanto, essa característica também resultou em chunks significativamente maiores em determinados artigos, exigindo uma etapa adicional de subdivisão antes da geração dos embeddings.

Os testes de busca também mostraram que o maior score de similaridade não necessariamente representa o resultado mais relevante do ponto de vista qualitativo. Por esse motivo, a avaliação de sistemas de recuperação deve considerar tanto métricas quantitativas quanto a pertinência semântica dos conteúdos recuperados.

---

## 13. Conclusão

A atividade permitiu observar experimentalmente como diferentes estratégias de chunking influenciam a quantidade, o tamanho e a organização dos segmentos de texto utilizados na geração de embeddings.

Não foi identificada uma única estratégia superior em todos os cenários.

A estratégia Recursive apresentou maior regularidade e controle de tamanho. Paragraph demonstrou bom desempenho em diferentes consultas semânticas, enquanto Markdown preservou melhor a estrutura dos documentos, mas apresentou maior risco de produzir chunks excessivamente grandes.

Também foi possível verificar a importância do tratamento de limites impostos pelos modelos de embeddings. A subdivisão dos chunks que excediam o limite permitiu preservar o processamento do corpus sem descartar documentos ou estratégias.

Por fim, os experimentos de recuperação demonstraram que a escolha da estratégia de chunking influencia diretamente os resultados de busca semântica. Dessa forma, a definição do método de segmentação deve considerar o tipo de documento, a estrutura textual e o objetivo do sistema de recuperação.

---

## 14. Estrutura dos resultados

A organização principal dos arquivos produzidos é:

```text
AULA_04/
│
├── artigos/
│   └── arquivos PDF
│
├── markdown/
│   └── documentos convertidos para Markdown
│
├── results/
│   ├── summary.json
│   ├── summary_corpus.json
│   │
│   ├── attention_is_all_you_need/
│   ├── bert_pretraining/
│   ├── bioetica_e_ia/
│   ├── escrita_academica_ia/
│   ├── gpt3_language_models/
│   ├── gpt4_technical_report/
│   ├── instruct_gpt/
│   ├── llama_foundation_models/
│   ├── lora_low_rank_adaptation/
│   ├── retrieval_augmented_generation/
│   ├── scaling_laws_llm/
│   └── twitter_algoritmo/
│
├── aula_04_chunking.ipynb
│
└── README.md