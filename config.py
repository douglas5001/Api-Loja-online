import mysql.connector
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Configurações do banco de dados
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

# Conexão com o banco de dados
mysql = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
