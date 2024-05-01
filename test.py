from utils.sqlServerConnector import extract_data
from utils.config import SELECT_QUERIES

print(extract_data(SELECT_QUERIES['produto']))
