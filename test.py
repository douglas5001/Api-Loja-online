from utils.sqlServerConnector import extract_data
from utils.config import GET_QUERIES

print(extract_data(GET_QUERIES['produto']))
