import json
import os
import requests
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import boto3
import base64
from botocore.exceptions import ClientError


def sqlConnector():

    server = json.loads(get_secret("prod/BancoSQLServer"))['host']
    database = json.loads(get_secret("prod/BancoSQLServer"))['dbname']
    username = json.loads(get_secret("prod/BancoSQLServer"))['username']
    password = json.loads(get_secret("prod/BancoSQLServer"))['password']
    conn = ('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='
            + password)
    quoted = quote_plus(conn)
    new_con = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)

    return create_engine(new_con, fast_executemany=True, use_insertmanyvalues=False)


def get_secret(secret):
    secret_name = secret
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        aws_access_key_id=json.loads(os.environ.get('aws_token'))['Access Key Id'],
        aws_secret_access_key=json.loads(os.environ.get('aws_token'))['Secret Access Key']
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


def fetch_data_from_api(endpoint,page=1):
    url = f"http://127.0.0.1:5000/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def pushToSqlServer(df_data, table):
    engine = sqlConnector()
    schema = 'db_lojavirtual'
    inserted_at = 'inserted_at'

    try:
        print('Realizando inserção do dataframe')
        #df_data.to_csv(f'buffer_{endpoint}.csv')
        df_data.to_sql(name=table, index=False, con=engine, schema=schema, if_exists='append', chunksize=10000)
        print(f'inserted into {schema}.{table}')

    except Exception as e:
        print('Erro ao inserir')
        print(e)
