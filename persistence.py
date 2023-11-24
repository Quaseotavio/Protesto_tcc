import mysql.connector


def bd_connect():
    conexao_bd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="protesto_tcc"
    )
    cursor = conexao_bd.cursor()
    if valida_bd(cursor):
        return cursor
    else:
        return


def valida_bd(cursor):
    validacao = True
    tabelas = ["arquivo_remessa", "transacao_remessa", "transacao", "arquivo_retorno", "transacao_retorno",
               "codigos_ocorrencia", "especies_titulos", "codigos_irregularidade"]
    for tabela in tabelas:
        cursor.execute(f"SHOW TABLES LIKE '{tabela}'")
        if cursor.fetchone() is None:
            validacao = False
    if not validacao:
        print('Não foi possível estabelecer conexão com o banco de dados. Verifique e tente novamente.')
    return validacao


def grava_dados():
    cursor = bd_connect()
    return


def gravar_header(header):

    return