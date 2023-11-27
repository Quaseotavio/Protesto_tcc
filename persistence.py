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
        return cursor, conexao_bd
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


def gravar_header(header):
    cursor, conexao = bd_connect()
    query = "INSERT INTO arquivo_remessa (sequencial_remessa, data_remessa) VALUES (%s, %s)"
    param = (header['sequencial'], header['data_mov'])
    cursor.execute(query, param)
    conexao.commit()
    conexao.close()
    return


def gravar_registros(arq, seq):
    cursor, conexao = bd_connect()
    # Inserindo os registros na tabela 'transacao'
    query = '''INSERT INTO transacao
    (cod_agencia_cedente, cod_cedente, nome_cedente, nome_sacador, doc_sacador, end_sacador, cep_sacador,
    cidade_sacador, uf_sacador, nosso_numero, especie_titulo, num_titulo, data_emissao, data_vencimento,
    valor_titulo, saldo_titulo, endosso, aceite, nome_devedor, tipo_doc_devedor, doc_devedor, doc_devedor_pf,
    endereco_devedor, cep_devedor, cidade_devedor, uf_devedor, bairro_devedor, sequencial_remessa, ocorrencia)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Z')'''
    for reg in arq:
        reg['sequencial'] = seq
        param = tuple(reg.values())
        cursor.execute(query, param)
    conexao.commit()
    # Vinculando todos os registros a um arquivo remessa na tabela transacao_remessa
    query = "INSERT INTO transacao_remessa VALUES (%s, %s, %s)"
    for reg in arq:
        param = (seq, reg['cod_cedente'], reg['nosso_numero'])
        cursor.execute(query, param)
    conexao.commit()
    conexao.close()
    print('Os registros foram gravados no banco de dados.')
    return


def checar_remessa(header):
    cursor, conexao = bd_connect()
    seq = header['sequencial']
    query = f'SELECT * FROM arquivo_remessa WHERE sequencial_remessa = {seq}'
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexao.close()
    if resultado:
        return True
    else:
        return False


def distribuir_titulos(arq, header):
    cursor, conexao = bd_connect()
    query = 'UPDATE transacao SET protocolo = %s, data_protocolo = %s, ocorrencia = 0 WHERE nosso_numero = %s'
    for reg in arq:
        param = (reg['protocolo'], header['data_mov'], reg['nosso_numero'])
        cursor.execute(query, param)
    conexao.commit()
    query = f"UPDATE arquivo_remessa SET confirmacao = True WHERE sequencial_remessa = {header['sequencial']}"
    cursor.execute(query)
    conexao.commit()
    conexao.close()
    return


def consulta_titulos_com_arq_e_tipo(arq, tipo):
    resultado = list()
    cursor, conexao = bd_connect()
    query = '''SELECT cod_cedente, nome_cedente, nome_devedor, nosso_numero, protocolo, descricao_ocorrencia   
    FROM transacao AS t, codigos_ocorrencia AS c
    WHERE t.ocorrencia = %s AND t.ocorrencia = c.cod_ocorrencia AND t.nosso_numero = %s'''
    for reg in arq:
        param = (tipo, reg['nosso_numero'],)
        cursor.execute(query, param)
        resultado.append(cursor.fetchall())
    conexao.close()
    return resultado


def consulta_titulos_arq(arq):
    resultado = list()
    cursor, conexao = bd_connect()
    query = '''SELECT cod_cedente, nome_cedente, nome_devedor, nosso_numero, protocolo, descricao_ocorrencia   
    FROM transacao AS t, codigos_ocorrencia AS c
    WHERE t.nosso_numero = %s AND t.ocorrencia = c.cod_ocorrencia'''
    for reg in arq:
        param = (reg['nosso_numero'],)
        cursor.execute(query, param)
        resultado.append(cursor.fetchall())
    conexao.close()
    return resultado


def consulta_titulos_geral(tipo):
    resultado = list()
    cursor, conexao = bd_connect()
    if not tipo:
        query = '''SELECT cod_cedente, nome_cedente, nome_devedor, nosso_numero, protocolo, descricao_ocorrencia   
        FROM transacao AS t, codigos_ocorrencia AS c
        WHERE t.ocorrencia = c.cod_ocorrencia
        ORDER BY t.protocolo'''
    else:
        query = f'''SELECT cod_cedente, nome_cedente, nome_devedor, nosso_numero, protocolo, descricao_ocorrencia   
        FROM transacao AS t, codigos_ocorrencia AS c
        WHERE t.ocorrencia = {tipo} AND t.ocorrencia = c.cod_ocorrencia
        ORDER BY t.protocolo'''
    cursor.execute(query)
    resultado.append(cursor.fetchall())
    conexao.close()
    return resultado


def checar_retorno(arq):
    validacao = True
    cursor, conexao = bd_connect()
    query = '''SELECT nosso_numero FROM transacao WHERE nosso_numero = %s'''
    for reg in arq:
        param = (reg['nosso_numero'], )
        cursor.execute(query, param)
        response = cursor.fetchone()
        if response is None:
            validacao = False
    conexao.close()
    return validacao


def retornar_titulos(arq, header):
    cursor, conexao = bd_connect()
    query = '''UPDATE transacao SET saldo_titulo = %s, ocorrencia = %s, custas_cartorio = %s, 
                compl_cod_irregularidade = %s, data_ocorrencia = %s WHERE nosso_numero = %s'''
    for tit in arq:
        param = (tit['saldo_titulo'], tit['ocorrencia'], tit['custas_cartorio'], tit['compl_cod_irregularidade'],
                 tit['data_ocorrencia'], tit['nosso_numero'])
        cursor.execute(query, param)
    query = '''INSERT INTO arquivo_retorno VALUES (%s, %s)'''
    param = (header['data_mov'], header['qtd_registros'])
    cursor.execute(query, param)
    query = '''INSERT INTO transacao_retorno VALUES (%s, %s, %s)'''
    for tit in arq:
        param = (header['data_mov'], tit['cod_cedente'], tit['nosso_numero'])
        cursor.execute(query, param)
    conexao.commit()
    conexao.close()
    print('Dados gravados com sucesso!')
    return
