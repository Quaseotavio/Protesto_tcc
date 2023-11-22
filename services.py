import tkinter as tk
from tkinter import filedialog
from datetime import datetime


def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    local_arquivo = filedialog.askopenfilename(
        title="Selecione um arquivo para tratamento: ",
        filetypes=[('Arquivos Mensagem', '.ARQ'), ('Arquivos CNAB600', '*.23*'), ('Todos os arquivos', '*.*')]
    )
    return local_arquivo


def ler_arquivo(local):
    try:
        with open(local, 'r') as arquivo:
            lines = arquivo.readlines()
            lines = [linha.strip() for linha in lines]
            return lines
    except FileNotFoundError:
        print(f'O arquivo selecionado não foi encontrado no seguinte caminho:\n{local}')
    except Exception as e:
        print(f'Ocorreu o erro {e}')


def extrair_header(arquivo):
    extracted_header = arquivo[0]
    if extracted_header[0] != '0':
        return Exception
    else:
        split_header = {
            'data_mov': datetime.strptime(extracted_header[44:52], "%d%m%Y").date().strftime("%d-%m-%Y"),
            'id_remetente': extracted_header[52:55],
            'id_destinatario': extracted_header[55:58],
            'id_transacao': extracted_header[58:61],
            'sequencial': extracted_header[61:67],
            'qtd_registros': int(extracted_header[67:71]),
            'qtd_titulos': int(extracted_header[71:75]),
            'qtd_indicacoes': int(extracted_header[75:79]),
            'qtd_originais': int(extracted_header[79:83]),
        }
        return split_header


def extrair_trailler(arquivo):
    extracted_trailler = arquivo[-1]
    if extracted_trailler[0] != '9':
        return Exception
    else:
        split_trailler = {
            'data_mov': datetime.strptime(extracted_trailler[44:52], "%d%m%Y").date().strftime("%d-%m-%Y"),
            'checksum_qtd': int(extracted_trailler[52:57]),
            'checksum_valor': float(int(extracted_trailler[57:75])/100)
        }
        return split_trailler


def tratar_arquivo(arquivo, id_transacao):
    lista_titulos = []
    if id_transacao == 'TPR':  # Remessa para protesto
        for transacao in arquivo:
            titulo = {
                'cod_agencia': transacao[4:8],
                'cod_cedente': transacao[8:19],
                'nome_cedente': transacao[19:64].strip(),
                'nome_sacador': transacao[64:109].strip(),
                'doc_sacador': transacao[109:123],
                'end_sacador': transacao[123:168].strip(),
                'cep_sacador': transacao[168:176],
                'cidade_sacador': transacao[176:196].strip(),
                'uf_sacador': transacao[196:198],
                'nosso_numero': transacao[198:213],
                'especie_titulo': transacao[213:216],
                'num_titulo': transacao[216:227],
                'data_emissao': datetime.strptime(transacao[227:235], "%d%m%Y").date().strftime("%d-%m-%Y"),
                'data_vecimento': datetime.strptime(transacao[235:243], "%d%m%Y").date().strftime("%d-%m-%Y"),
                'valor_titulo': float(int(transacao[246:260])/100),
                'saldo_titulo': float(int(transacao[260:274])/100),
                'endosso': transacao[294:295],
                'aceite': transacao[295:296],
                'nome_devedor': transacao[297:342].strip(),
                'tipo_doc_devedor': int(transacao[342:345]),
                'doc_devedor': transacao[345:359],
                'doc_devedor_pf': transacao[359:370],
                'endereco_devedor': transacao[370:415].strip(),
                'cep_devedor': transacao[415:423],
                'cidade_devedor': transacao[423:443].strip(),
                'uf_devedor': transacao[443:445],
                'bairro_devedor': transacao[487:507].strip()
            }
            lista_titulos.append(titulo)
    elif id_transacao == 'CRT':  # Confirmacao da remessa
        for transacao in arquivo:
            titulo = {
                'cod_cedente': transacao[8:19],
                'nosso_numero': transacao[198:213],
                'protocolo': transacao[447:457].strip(),
                'ocorrencia': transacao[457:458],
                'data_protocolo': datetime.strptime(transacao[458:466], "%d%m%Y").date().strftime("%d-%m-%Y"),
                'custas_cartorio': float(int(transacao[466:476])/100),
                'custas_distribuicao': float(int(transacao[507:517])/100),
                'compl_cod_irregularidade': transacao[557:565]
            }
            if transacao[485:487] != "  ":
                titulo['data_ocorrencia'] = datetime.strptime(transacao[477:485], "%d%m%Y").date().strftime("%d-%m-%Y")
                titulo['cod_irregularidade'] = int(transacao[485:487])
            lista_titulos.append(titulo)
    elif id_transacao == 'RTP':  # Retorno da remessa
        for transacao in arquivo:
            titulo = {
                'cod_cedente': transacao[8:19],
                'nosso_numero': transacao[198:213],
                'saldo_titulo': float(int(transacao[260:274])/100),
                'ocorrencia': transacao[457:458],
                'custas_cartorio': float(int(transacao[466:476]) / 100),
                'compl_cod_irregularidade': transacao[557:565]
            }
            if transacao[485:487] != "  ":
                titulo['data_ocorrencia'] = datetime.strptime(transacao[477:485], "%d%m%Y").date().strftime("%d-%m-%Y")
                titulo['cod_irregularidade'] = int(transacao[485:487])
            lista_titulos.append(titulo)
    return lista_titulos


def validar_arquivo(arquivo, header, trailler):
    flag_quantidade = flag_valor = validacao = False
    message = ''
    if header['id_transacao'] in ['TPR', 'CRT']:  # Remessa para protesto e confirmação de remessa
        qtd_geral = qtd_indicacoes = qtd_originais = soma = 0
        for transacao in arquivo:
            qtd_geral += 1
            soma += transacao['saldo_titulo']
            if transacao['especie_titulo'] in ['DMI', 'DRI', 'CBI']:
                qtd_indicacoes += 1
            else:
                qtd_originais += 1
        if qtd_geral * 2 + qtd_indicacoes + qtd_originais == trailler['checksum_qtd']:
            flag_quantidade = True
        if round(soma, 2) == trailler['checksum_valor']:
            flag_valor = True
    elif header['id_transacao'] == 'RTP':  # Retorno de protesto
        soma = quantidade = 0
        for transacao in arquivo:
            quantidade += 1
            soma += transacao['saldo_titulo']
        if quantidade == trailler['checksum_qtd']:
            flag_quantidade = True
        if soma == trailler['checksum_valor']:
            flag_valor = True
    else:
        print('Tipo de arquivo não definido.')
    if not flag_quantidade or not flag_valor:
        message = 'Arquivo não validado! Verifique a soma da quantidade de títulos ou do saldo dos títulos'
    if flag_valor and flag_quantidade:
        message = 'Arquivo validado com sucesso.'
        validacao = True
    return validacao, message
