# Aula 03 - Embeddings e Busca Semântica

Nesta aula foram explorados conceitos de **embeddings**, medidas de distância e similaridade entre vetores e busca semântica utilizando modelos de embeddings por meio da API do OpenRouter.

## Objetivos

- Gerar embeddings para palavras e frases;
- Compreender a representação vetorial de textos;
- Implementar a Distância Euclidiana;
- Implementar a Similaridade de Cosseno;
- Implementar a Distância de Cosseno;
- Comparar semanticamente diferentes palavras e frases;
- Visualizar embeddings em um espaço tridimensional;
- Implementar uma busca semântica simples;
- Avaliar diferentes estratégias de divisão de documentos em chunks.

## Termos analisados

Foram gerados embeddings para os seguintes termos:

- gato
- felino
- cachorro
- carro
- caminhão
- moto
- banana
- maçã
- goiaba

Os vetores gerados pelo modelo utilizado possuem **2048 dimensões**.

## Distâncias e similaridade

Foram implementadas funções para calcular:

### Distância Euclidiana

Mede a distância entre dois vetores no espaço vetorial. Quanto menor a distância, maior a proximidade entre os embeddings.

### Similaridade de Cosseno

Mede a similaridade entre dois vetores considerando o ângulo entre eles. Valores maiores indicam maior similaridade.

### Distância de Cosseno

Calculada a partir de:

`Distância de Cosseno = 1 - Similaridade de Cosseno`

Quanto menor a distância, maior a similaridade entre os embeddings.

## Comparação de palavras

Foram realizadas comparações entre termos semanticamente relacionados e não relacionados.

Os experimentos mostraram, por exemplo, maior proximidade entre termos pertencentes ao mesmo contexto, como:

- carro, caminhão e moto;
- banana, maçã e goiaba;
- gato, felino e cachorro.

## Visualização 3D

Para permitir a visualização dos embeddings, os vetores originalmente compostos por 2048 dimensões foram reduzidos para três dimensões utilizando **PCA (Principal Component Analysis)**.

A representação 3D permitiu observar a distribuição espacial dos termos e a proximidade entre alguns conceitos semanticamente relacionados.

A redução dimensional provoca perda de informação, portanto o gráfico representa apenas uma aproximação das relações existentes no espaço original dos embeddings.

## Comparação de frases

Também foram comparadas frases com diferentes relações semânticas:

- mesmo sentido com palavras diferentes;
- mesmo contexto;
- contexto diferente;
- oposição ou negação.

Os resultados mostraram que frases semanticamente semelhantes apresentam maior similaridade de cosseno.

Também foi possível observar que frases com sentidos opostos podem manter certa proximidade semântica quando compartilham conceitos e palavras relacionadas.

## Busca Semântica

Foi implementada uma busca semântica manual utilizando os documentos Markdown gerados na Aula 02.

O processo utilizado foi:

1. Leitura dos arquivos Markdown;
2. Divisão dos documentos em trechos;
3. Geração do embedding de cada trecho;
4. Geração do embedding da consulta;
5. Cálculo da Similaridade de Cosseno;
6. Ordenação dos resultados;
7. Retorno dos três trechos mais semelhantes (TOP 3).

Uma das consultas utilizadas foi:

`O que é autonomia e opacidade algorítmica?`

## Estratégias de Chunking

A busca semântica foi testada utilizando três formas diferentes de divisão dos documentos:

### Linhas

Apresentou alta precisão na localização de termos específicos, porém alguns resultados possuíam pouco contexto.

### Parágrafos

Apresentou melhor equilíbrio entre similaridade e quantidade de informação disponível no trecho recuperado.

### Seções

Recuperou trechos maiores e com mais contexto, permitindo obter informações mais completas sobre o assunto pesquisado.

## Conclusão

Os experimentos demonstraram que embeddings permitem representar semanticamente palavras, frases e documentos por meio de vetores numéricos.

Também foi possível observar que o tamanho dos chunks influencia diretamente os resultados da busca semântica. Um score de similaridade maior não significa necessariamente que o trecho recuperado seja o mais útil.

A escolha da estratégia de chunking representa um equilíbrio entre precisão e quantidade de contexto, sendo uma etapa importante no desenvolvimento de sistemas de busca semântica e aplicações de RAG.

## Arquivo

- `Aula_03_Embeddings.ipynb` - notebook contendo os experimentos, cálculos, visualizações e implementação da busca semântica.