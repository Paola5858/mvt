import logging
from io import TextIOWrapper
from django.db import transaction
from api_telemetria.models import MedicaoVeiculo
from api_telemetria.csv_import_service import processar_csv_para_medicoes

logger = logging.getLogger(__name__)

def processar_upload_csv_medicoes(arquivo_csv_upload):
    """
    Processa o arquivo CSV de medições recebido via upload.
    Utiliza o csv_import_service para realizar a importação direta para MedicaoVeiculo.
    """
    try:
        # Decodifica o arquivo para texto para ser lido pelo csv.DictReader
        arquivo_texto = TextIOWrapper(arquivo_csv_upload.file, encoding=\'utf-8-sig\')
        
        resultado_importacao = processar_csv_para_medicoes(arquivo_texto)
        
        logger.info(f"Importação CSV concluída. Total de linhas no arquivo: {resultado_importacao[\'total_linhas_arquivo\']}, "
                    f"Total de linhas importadas: {resultado_importacao[\'total_linhas_importadas\']}")
        
        if resultado_importacao[\'erros\']:
            logger.warning(f"{len(resultado_importacao[\'erros\'])} erros encontrados durante a importação CSV.")

        return {
            "status": "sucesso",
            "mensagem": "Importação CSV processada com sucesso.",
            "total_linhas_arquivo": resultado_importacao[\'total_linhas_arquivo\'],
            "total_linhas_importadas": resultado_importacao[\'total_linhas_importadas\'],
            "erros": resultado_importacao[\'erros\']
        }

    except ValueError as e:
        logger.error(f"Erro de validação na importação CSV: {e}")
        return {"status": "erro", "mensagem": str(e), "erros": []}
    except Exception as e:
        logger.critical(f"Erro inesperado ao processar upload CSV: {e}")
        return {"status": "erro", "mensagem": "Erro interno do servidor ao processar o CSV.", "erros": []}
