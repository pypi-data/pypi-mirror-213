"""
- Title:            Utils GCP. Wrapper on top of google.cloud for common GCP tasks
- Project/Topic:    Utils Tabular Data. Practical functions for Data Science  (internal project)
- Author/s:         Angel Martinez-Tenor
- Dev Date:         2020 - 2022

- Status:           Planning
- Required (pip / poetry):  google.cloud.aiplatform
"""

from pathlib import Path
from typing import Dict

import pandas as pd
from google.cloud import aiplatform  # pylint: disable=import-error, no-name-in-module
from google.cloud import bigquery, storage  # type: ignore # pylint: disable=import-error, no-name-in-module
from google.protobuf import json_format  # pylint: disable=import-error, no-name-in-module
from google.protobuf.json_format import MessageToDict
from google.protobuf.struct_pb2 import Value  # pylint: disable=import-error, no-name-in-module

from smart_data_science import logger

log = logger.get_logger(__name__)

global_client_storage = None
global_client_bigquery = None
global_source_bucket = None
global_normalized_bucket = None


# GOOGLE CLOUD STORAGE ---------------------------------------------------------


def get_client_storage(project: str = None):  # redundant, could e
    """Update and Return a GCP storage client
    Args:
        project (str, optional): GCP project. Defaults to None (uses default project)
    Returns:
        storage.Client: GCP Storage client
    """
    global global_client_storage  # pylint: disable=global-statement
    if global_client_storage is None:
        global_client_storage = storage.Client(project)
    return global_client_storage


def get_client_bigquery(project: str = None):  # redundant, could e
    """Update and Return a GCP storage client
    Args:
        project (str, optional): GCP project. Defaults to None (uses default project)
    Returns:
        storage.Client: GCP Storage client
    """
    global global_client_bigquery  # pylint: disable=global-statement
    if global_client_bigquery is None:
        global_client_bigquery = bigquery.Client(project, location="EU")
    return global_client_bigquery


def copy_from_bucket(bucket_name: str, local_folder: Path | str, blob_name=None, force_replace: bool = False) -> None:
    """Copy all files (blob_name=None) or a single file defined by 'blob_name' from a GCP bucket to a local filepath
    Args:
        bucket_name (str): GCP bucket name
        local_folder (str|Path): Local path
        blob_name (str, optional): Blob name. Defaults to None (all blobs)
        force_replace (bool, optional): Force replace local file if exists. Defaults to False.
    """
    local_folder = Path(local_folder)
    local_folder.mkdir(parents=True, exist_ok=True)

    client_storage = get_client_storage()
    # log.debug(f"Copying files from {bucket_name} to {local_folder}")

    bucket = client_storage.get_bucket(bucket_name)
    blobs = [bucket.get_blob(blob_name)] if blob_name else bucket.list_blobs()
    for item in blobs:
        blob = bucket.get_blob(item.name)
        destination_path = local_folder / item.name
        if not destination_path.exists() or force_replace:
            log.debug(f"copying \t {item.name} \t {round(blob.size/(1024**2),2)}Mb to {destination_path}")
            blob.download_to_filename(destination_path)
        else:
            log.debug(f"{item.name} \t {round(blob.size/(1024**2),2)}Mb \t already in folder '{local_folder}'")


def copy_file_to_bucket(datapath: str | Path, bucket_name: str) -> None:
    """Copy a file from local to a GCP bucket
    Args:
        datapath (str|Path): Local file path
        bucket_name (str): GCP bucket name
    """
    client_storage = get_client_storage()
    bucket = storage.Bucket(client_storage, bucket_name)
    # if not bucket_normalized.exists():   # better to create manually the bucket with the required permissions
    #     bucket_normalized = client.create_bucket(bucket_name, location='europe-west1')
    # bucket_normalized = client.get_bucket(bucket_name)
    blob = bucket.blob(Path(datapath).name)
    blob.upload_from_filename(datapath)
    log.debug(
        f"{blob.name} ({round(blob.size/(1024**2),2)}MB) copied from {Path(datapath).parent} "
        f"to the bucket '{bucket_name}'"
    )

    # blob = client_storage.bucket(BUCKET_NAME).blob(datapath)
    # blob.download_to_filename(localpath)
    # log.debug(f"{blob.name} copied from {bucket_name} to {localpath}")


def setup_default(project: str = None, source_bucket: str = None, normalized_bucket: str = None) -> None:
    # sourcery skip: extract-duplicate-method
    """Setup default parameters for GCP services
    Args:
    """
    # global client_bigquery
    # client_bigquery = bigquery.Client(location="EU", project=project)
    global global_client_storage  # pylint: disable=global-statement
    global_client_storage = storage.Client(project=project)
    log.debug(f"GCP Project: {global_client_storage.project}")

    if source_bucket:
        global global_source_bucket  # pylint: disable=global-statement
        global_source_bucket = global_client_storage.get_bucket(source_bucket)
        log.debug(f"Global Source bucket set to: {global_source_bucket.name}")

    if normalized_bucket:
        global global_normalized_bucket  # pylint: disable=global-statement
        global_normalized_bucket = global_client_storage.get_bucket(normalized_bucket)
        log.debug(f"Global Normalized bucket set to: {global_normalized_bucket.name}")


# BIGQUERY --------------------------------------------------------------------------------------------


def load_to_bigquery(df: pd.DataFrame, dataset_id: str, table_id: str) -> None:
    """Upload the normalized dataframe to BigQuery & remove duplicated samples
    Args:
        df (pd.DataFrame): Normalized dataframe
        database_id (str): BigQuery database name
        dataset_id (str): BigQuery dataset name
        table_id (str): BigQuery table name
    """
    df = df.copy()
    client_bigquery = get_client_bigquery()
    dataset = client_bigquery.create_dataset(dataset_id, exists_ok=True)
    table_ref = dataset.table(table_id)
    log.debug(table_ref)

    job = client_bigquery.load_table_from_dataframe(df, table_ref, location="EU")
    log.debug(f"Loading data to Bigquery:\n{table_ref.path}")
    job.result()  # waits until the upload is completed
    log.debug("OK")

    # # Remove duplicated rows:
    # query = f"""
    #     CREATE OR REPLACE TABLE `{table_id}`
    #     AS
    #     SELECT DISTINCT * FROM `{table_id}`
    #     """
    # query_job = client_bigquery.query(query, location="EU")
    # query_job.result()

    # df.to_gbq(
    #     f"{PROJECT_ID}.{table_name}",
    #     if_exists="replace",
    #     project_id=PROJECT_ID,
    #     credentials=credentials,
    #     location="EU",
    # )

    # log.info(f"BigQuery table '{table_name}' created")


def predict_tabular_classification_sample(
    instance_dict: Dict,
    project: str = "PROJECT_ID",
    endpoint_id: str = "ENDPOINT_ID",
    location: str = "europe-west1",
    api_endpoint: str = "europe-west1-aiplatform.googleapis.com",
):
    """
        source: https://github.com/googleapis/python-aiplatform/blob/main/samples/snippets/prediction_service/predict_tabular_classification_sample.py # noqa: E501 # pylint: disable=line-too-long

        Example usage:
        prediction = predict_tabular_classification_sample(sample)
        print(
            f"Predicted Prediction: {prediction['value']:.2f}\n95% prediction interval:"
            f"{prediction['lower_bound']:.2f} - {prediction['upper_bound']:.2f}"
    )
    """
    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    instance = json_format.ParseDict(instance_dict, Value())
    instances = [instance]
    parameters_dict: dict = {}
    parameters = json_format.ParseDict(parameters_dict, Value())
    endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    predictions = response.predictions
    return MessageToDict(predictions[0])  # dict(predictions[0])  # Only one prediction is returned


# def get_from_bigquery() -> pd.DataFrame:
#     """Get the normalized dataframe from BigQuery
#     Returns:
#         pd.DataFrame: Normalized dataframe
#     """
#     query = f"""
#     SELECT DISTINCT *
#     FROM `{BIGQUERY_TABLE_REF}`
#     """
#     query_job = client_bigquery.query(query, location="EU")

#     df = query_job.to_dataframe()

#     log.debug(f"Normalized data loaded from BigQuery: {BIGQUERY_TABLE_REF}")
#     df = df.set_index("CustomerId")
#     log.debug(f"{df.shape[0]} Rows \n{df.shape[1]} Columns")

#     return df


# def load_pipeline_from_bucket(filepath):
#     """ Return a pipeline object loaded form the gcs bucket defined in BUCKET_NAME. It solves appengine issues
# (avoid copying file) """
#     blob = bucket.blob(filepath)

#     from tempfile import TemporaryFile

#     with TemporaryFile() as temp_file:
#         #download blob into temp file
#         blob.download_to_file(temp_file)
#         temp_file.seek(0)
#         #load into joblib
#         pipeline=joblib.load(temp_file)
#     log.debug(f'Pipeline Loaded from: {blob}')

#     return pipeline

# AUTOML TABLES  --------------------------------------------


# def predict_sample(
#     project_id: str,
#     compute_region: str,
#     model_display_name: str,
#     inputs: pd.Series,
# ):
#     """Make a single prediction with Auto ML
#     Args:
#         project_id (str): GCP Project ID
#         compute_region (str): GCP Compute Region
#         model_display_name (str): AutoML Model Display Name
#         inputs (pd.Series): Input data to be predicted
#     """
#     # [START automl_tables_predict]
#     # project_id = 'PROJECT_ID_HERE'
#     # compute_region = 'COMPUTE_REGION_HERE'
#     # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
#     # inputs = {'value': 3, ...}

#     if inputs.empty:
#         log.debug("EMPTY SAMPLE")
#         return None, None

#     inputs = inputs.to_dict(orient="records")[0]

#     client = automl.TablesClient(project=project_id, region=compute_region)
#     response = client.predict(model_display_name=model_display_name, inputs=inputs)

#     results = {}
#     for result in response.payload:
#         results[result.tables.value.string_value] = result.tables.score

#     max_key = max(results, key=results.get)
#     max_value = max(results.values())

#     return (max_key, max_value)


# def batch_predict(
#     project_id: str,
#     compute_region: str,
#     model_display_name: str,
#     gcs_input_uris: str | Path,
#     gcs_output_uri: str | Path,
# ):
#     """Make a batch prediction with Auto ML
#     Args:
#         project_id (str): GCP Project ID
#         compute_region (str): GCP Compute Region
#         model_display_name (str): AutoML Model Display Name
#         gcs_input_uris (str|Path): GCS Input URI
#         gcs_output_uri (str|Path): GCS Output URI

#     """
#     # [START automl_tables_batch_predict]
#     # project_id = 'PROJECT_ID_HERE'
#     # compute_region = 'COMPUTE_REGION_HERE'
#     # model_display_name = 'MODEL_DISPLAY_NAME_HERE'
#     # gcs_input_uris = ['gs://path/to/file.csv]
#     # gcs_output_uri = 'gs://path'

#     client = automl.TablesClient(project=project_id, region=compute_region)

#     # Query model
#     response = client.batch_predict(
#         gcs_input_uris=gcs_input_uris, gcs_output_uri_prefix=gcs_output_uri, model_display_name=model_display_name
#     )
#     log.debug("Making batch prediction... ")
#     response.result()
#     log.debug(f"Batch prediction complete.\n{response.metadata}")


# def copy_file_from_bucket(
#     bucket_name: str, blob_name: str | Path, localpath: str | Path, force_replace: bool = False
# ) -> None:
#     """Copy a single  file from a GCP bucket to a local filepath
#     Args:
#         bucket_name (str): GCP bucket name
#         blob_name (str): GCP blob name
#         localpath (Path): Local path
#         force_replace (bool, optional): Force replace local file if exists. Defaults to False.
#     """
#     localpath.parent.mkdir(parents=True, exist_ok=True)
#     storage_client = get_client_storage()
#     bucket = storage_client.get_bucket(bucket_name)
#     blob = bucket.get_blob(blob_name)
#     if not localpath.exists() or force_replace:
#         log.debug(f"copying \t {blob.name} \t {round(blob.size/(1024**2),2)}Mb to {localpath}")
#         blob.download_to_filename(localpath)
#     else:
#         log.debug(f"{blob.name} \t {round(blob.size/(1024**2),2)}Mb \t already in folder '{localpath.parent}'")
