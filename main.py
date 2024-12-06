import os
import akeyless
from akeyless.rest import ApiException
import urllib3
import pyodbc

def obter_uid_token(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f'O arquivo {caminho_arquivo} não foi encontrado.')
    
    with open(caminho_arquivo, 'r', encoding='utf-16') as arquivo:
        uid_token = arquivo.read().strip()
    return uid_token

# Caminho do arquivo que contém o UID Token
caminho_arquivo = r'C:\Users\adm_azure\.vault-token'  

try:
    uid_token = obter_uid_token(caminho_arquivo)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    configuration = akeyless.Configuration(
            host = "https://10.0.1.13/akeyless-api/v2/"
    )

    configuration.verify_ssl = False

    api_client = akeyless.ApiClient(configuration)
    api = akeyless.V2Api(api_client)

    body = akeyless.GetSecretValue(names=['/demo/zero-secret-sql'], uid_token=uid_token)

    res = api.get_secret_value(body)
    connection_string = res['/demo/zero-secret-sql']

    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tb_pessoa")

        rows = cursor.fetchall()
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

    except pyodbc.Error as db_err:
        print(f"Erro no banco de dados: {db_err}")

except FileNotFoundError as e:
    print(e)
except ApiException as e:
    print(f'Erro na API: {e}')
except Exception as e:
    print(f'Ocorreu um erro: {e}')
