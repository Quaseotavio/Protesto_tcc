import mysql.connector

conexao_bd = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="protesto_tcc"
)

cursor = conexao_bd.cursor()
cursor.execute("SHOW TABLES LIKE 'transacao'")
tabela_existe = cursor.fetchone()
if tabela_existe:
    print('deu certo')
