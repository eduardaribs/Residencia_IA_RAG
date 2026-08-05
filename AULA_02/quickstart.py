import os
from pathlib import Path

# Evita que o PyTorch tente usar o compilador C++ do Windows.
os.environ["TORCH_COMPILE_DISABLE"] = "1"

# Limita o uso simultâneo de processamento para consumir menos memória.
os.environ["OMP_NUM_THREADS"] = "1"

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption


# Pasta onde estão os arquivos PDF.
pasta_artigos = Path("artigos")

# Pasta onde serão salvos os arquivos Markdown.
pasta_markdown = Path("markdown")

# Cria a pasta markdown caso ela ainda não exista.
pasta_markdown.mkdir(exist_ok=True)


# Configuração do processamento dos PDFs.
pipeline_options = PdfPipelineOptions()

# Os artigos já possuem texto digital, então o OCR não é necessário.
pipeline_options.do_ocr = False

# Mantém o reconhecimento de tabelas.
pipeline_options.do_table_structure = True

# Processa uma página por vez para reduzir o uso de memória RAM.
pipeline_options.layout_batch_size = 1
pipeline_options.ocr_batch_size = 1
pipeline_options.table_batch_size = 1


# Cria o conversor do Docling com as configurações definidas acima.
converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)


# Procura todos os arquivos PDF dentro da pasta artigos.
arquivos_pdf = list(pasta_artigos.glob("*.pdf"))

if not arquivos_pdf:
    print("Nenhum arquivo PDF foi encontrado na pasta artigos.")

else:
    # Percorre cada PDF encontrado.
    for arquivo_pdf in arquivos_pdf:
        try:
            print(f"Convertendo: {arquivo_pdf.name}")

            # Converte o PDF para o formato interno do Docling.
            resultado = converter.convert(arquivo_pdf)

            # Transforma o documento em Markdown.
            conteudo_markdown = resultado.document.export_to_markdown()

            # Cria o nome do arquivo de saída com a extensão .md.
            arquivo_saida = pasta_markdown / f"{arquivo_pdf.stem}.md"

            # Salva o conteúdo Markdown.
            arquivo_saida.write_text(
                conteudo_markdown,
                encoding="utf-8"
            )

            print(f"Arquivo criado: {arquivo_saida}")

        except Exception as erro:
            print(f"Erro ao converter {arquivo_pdf.name}: {erro}")

    print("Processamento finalizado.")