from io import BytesIO
import json
import pickle
import pandas as pd
from azure.storage.blob import BlobServiceClient


def read_blob_as_stream(connection_string, container_name, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name, snapshot=None)

    download_stream = blob_client.download_blob()
    return download_stream


def read_blob_as_df(connection_string, container_name, blob_name):
    download_stream = read_blob_as_stream(connection_string, container_name, blob_name)
    csv_file = download_stream.content_as_text(encoding='utf-8-sig')
    file = BytesIO(csv_file.encode())
    df = pd.read_csv(file)

    return df


def read_blob_as_json_object(connection_string, container_name, blob_name):
    download_stream = read_blob_as_stream(connection_string, container_name, blob_name).readall()
    json_data = json.loads(download_stream)
    
    return json_data


def read_blob_as_pickle_object(connection_string, container_name, blob_name):
    download_stream = read_blob_as_stream(connection_string, container_name, blob_name).readall()
    json_data = pickle.loads(download_stream)
    
    return json_data


def save_df_to_blob(connection_string, container_name, blob_name, df):
    """
    We assume dfs is a list of dataframes
    """

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_client.upload_blob(data=df.to_csv(), blob_type='BlockBlob')
    
    return True

