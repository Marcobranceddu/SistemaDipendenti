
import pyodbc

host = 'localhost'
bd = 'sistema'
user = 'sa'
password = '123456789'

try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + host+';DATABASE='+bd+';UID='+user+';PWD=' + password)
    # OK! 
    print("Connessione andata a buon fine: ")
except Exception as e:
    # Errore
    print("Si è verificato un errore durante la connessione a SQL Server:: ", e)