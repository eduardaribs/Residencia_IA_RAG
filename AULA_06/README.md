# Atividade 06 — Arquitetura RAG

Esta atividade apresenta o planejamento de duas aplicações utilizando RAG (Retrieval-Augmented Generation).

A proposta foi pensar em dois cenários diferentes e definir como os documentos seriam organizados, processados e recuperados para auxiliar um modelo de linguagem na geração das respostas.

## Cenários escolhidos

### Cenário 1 — Biblioteca Científica Pessoal

O primeiro cenário é uma biblioteca científica pessoal para ajudar estudantes e pesquisadores a consultar artigos que já possuem.

A ideia é permitir perguntas sobre os trabalhos armazenados e recuperar os trechos mais relacionados à consulta, mantendo também informações como título, autores, ano, página e DOI.

[Ver Cenário 1](./cenario1.md)

### Cenário 2 — Assistente Interno para Suporte Técnico de Software

O segundo cenário é um assistente para equipes de desenvolvimento e suporte técnico.

Nesse caso, a base é formada por documentos internos, como documentação de sistemas, manuais, runbooks, documentação de APIs e registros de problemas já resolvidos. O objetivo é facilitar a busca por informações que normalmente ficam espalhadas em diferentes documentos.

[Ver Cenário 2](./cenario2.md)

## Estrutura do projeto

```text
AULA_06/
├── README.md
├── cenario1.md
└── cenario2.md
```

Cada cenário foi desenvolvido separadamente e contém:

- identificação do problema;
- justificativa para o uso de RAG;
- limitações do uso de RAG;
- organização dos documentos;
- pipeline de ingestão;
- metadados;
- estratégia de chunking;
- escolha e comparação dos modelos de embeddings;
- diagrama da arquitetura;
- tabela de decisões;
- riscos e limitações.

## Comparação entre os cenários

Os dois cenários usam RAG para recuperar informações de documentos, mas possuem necessidades diferentes.

Na biblioteca científica, a preocupação principal é encontrar informações nos artigos e conseguir mostrar de onde cada informação foi retirada.

No suporte técnico, além da recuperação da informação, existe uma preocupação maior com atualização, controle de acesso e versão dos documentos, já que uma documentação antiga pode levar a uma orientação errada.

Algumas decisões são parecidas nos dois projetos, como o uso de metadados, divisão dos documentos em chunks e armazenamento dos embeddings em um banco vetorial. Isso acontece porque essas etapas fazem parte da estrutura básica de uma aplicação RAG.

As principais diferenças aparecem na forma de organizar os documentos, nos metadados utilizados e na frequência de atualização da base.

Se eu tivesse que construir apenas um dos dois, escolheria a biblioteca científica pessoal. É um cenário que faz parte da minha realidade acadêmica e poderia ser útil para consultar uma quantidade maior de artigos durante pesquisas e trabalhos.

## Uso de IA na atividade

## Uso de IA

Utilizei o ChatGPT como apoio para organizar as ideias e revisar a estrutura da atividade. Também usei a ferramenta para auxiliar na comparação dos modelos de embeddings. As informações técnicas foram conferidas nas páginas dos próprios modelos, principalmente no Hugging Face, e nas páginas dos provedores para verificar os custos das APIs.

## Autora

Maria Eduarda Ribeiro da Silva