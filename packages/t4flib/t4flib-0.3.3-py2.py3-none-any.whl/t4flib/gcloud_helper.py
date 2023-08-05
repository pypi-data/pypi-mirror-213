import shutil
from pydantic import BaseModel, Field, ValidationError
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud import storage
from google.api_core import exceptions as gcloud_ex
import pandas as pd
from .log_helper import logger
from .config import GCP_ACCOUNT_SERVICE_FILE, ENVIRONEMENT, PROXY_AUCHAN, BQ_PROJECT_ID
import os

# Modèle de validation pour une requête BigQuery
class QueryModel(BaseModel):
    query: str = Field(..., min_length=1)

def run_bq_query(query) -> pd.DataFrame:
    """
    Cette fonction exécute une requête BigQuery et retourne un DataFrame sans les en-têtes.
    """
    # Vérification de la validité de la requête
    try:
        valid_query = QueryModel(query=query)
    except ValidationError as e:
        logger('ERROR', f"La requête est invalide : {e}")
        return None

    ENVIRONEMENT='dev'
    credentials = service_account.Credentials.from_service_account_file(GCP_ACCOUNT_SERVICE_FILE)
    if ENVIRONEMENT == 'dev':
        os.environ["HTTPS_PROXY"] = PROXY_AUCHAN

    try:
        client = bigquery.Client(credentials=credentials)
        # Exécution de la requête BigQuery
	
        logger('DEBUG', f'Query => {query}')
	
        query_job = client.query(valid_query.query, location='EU')

        # Attente de la fin de l'exécution de la requête et récupération des résultats
        results = query_job.result()

        # Conversion des résultats en DataFrame
        df = results.to_dataframe()

        logger('INFO', f"La requête a été exécutée avec succès.")

        return df

    except Exception as e:
        logger('ERROR', f"Une erreur est survenue lors de l'exécution de la requête : {e}")
        return None


def upload_file_to_gcs(file_path, bucket_name, path_bucket):
    logger('INFO', f'Début de l\'upload du fichier {file_path} vers le bucket {bucket_name}')
    try:
        if ENVIRONEMENT == 'dev':
            os.environ["HTTPS_PROXY"] = PROXY_AUCHAN

        credentials = service_account.Credentials.from_service_account_file(GCP_ACCOUNT_SERVICE_FILE)
        client = storage.Client(credentials=credentials)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path_bucket)
        blob.upload_from_filename(file_path)

        logger('INFO', f'Le fichier {file_path} a été envoyé à gs://{os.path.join(bucket_name,path_bucket)} avec succès' )
        return 0

    except FileNotFoundError as e:
        logger('ERROR',f'Le fichier {file_path} est introuvable : {e}')
        return 1
    except Exception as e:
        logger('ERROR',f'Une erreur inattendue s\'est produite : {e}')
        return 1
