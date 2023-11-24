import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os

HOJE = datetime.now().strftime("%d%m%Y")


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
                'data_emissao': datetime.strptime(transacao[227:235], "%d%m%Y").date().strftime("%d%m%Y"),
                'data_vencimento': datetime.strptime(transacao[235:243], "%d%m%Y").date().strftime("%d%m%Y"),
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


def montar_remessa(arquivo, header):
    while True:
        os.system('cls')
        print('=' * 150)
        print(f"{'MONTAGEM DE NOVA REMESSA':^150}")
        print('=' * 150)
        quantidade = soma = c = 0
        print(f"SEQ {'COD CEDENTE':<15}{'NOSSO NUMERO':<20}{'CEDENTE':<45}{'SACADO':<45}{'DT VENC':<10}{'VALOR'}")
        for titulo in arquivo:
            print(f"{c+1}   {titulo['cod_cedente']:.<15}{titulo['nosso_numero']:.<20}", end='')
            print(f"{titulo['nome_cedente']:.<45}{titulo['nome_devedor']:.<45}{titulo['data_vencimento']}", end='')
            print(f" R$ {titulo['saldo_titulo']:.2f}")
            quantidade += 1
            c += 1
            soma += round(titulo['saldo_titulo'], 2)
        print(f"QUANTIDADE: {quantidade}         VALOR: R$ {soma}")
        print('''\nEssa é a remessa atual. Escolha o que deseja fazer:
        1 - INSERIR NOVO TITULO
        2 - REMOVER TITULO DA REMESSA
        3 - FECHAR REMESSA
        0 - CANCELAR E VOLTAR PARA O MENU ANTERIOR''')
        opt = int(input('>>: '))
        while opt not in [0, 1, 2, 3]:
            opt = int(input('Opção inválida. Informe sua opção: '))
        if opt == 0:
            print('A remessa atual será perdida e o arquivo deverá ser lido novamente.')
            conf = str(input('Deseja continuar? [S/N] ')).strip().upper()[0]
            if conf == 'S':
                break
        elif opt == 1:
            arquivo.append(inserir_titulo())
        elif opt == 2:
            tit_rem = int(input('Informe o SEQ do título que deseja remover: '))
            while tit_rem not in range(1, len(arquivo)+1):
                tit_rem = int(input('Opção inválida. Informe o SEQ do título que deseja remover: '))
            arquivo.pop(tit_rem-1)
        elif opt == 3:
            gerar_remessa(arquivo, header)
            break
    return


def inserir_titulo():
    novo_titulo = {
        'cod_agencia': str(input('Código da agência: ')).strip()[:4],
        'cod_cedente': str(input('Código do cedente: ')).strip()[:11],
        'nome_cedente': str(input('Nome do cedente: ')).upper().strip()[:45],
        'nome_sacador': str(input('Nome do sacador: ')).upper().strip()[:45],
        'tipo_doc_devedor': int(input('Tipo de documento do sacador (001 - CPF  002 - CNPJ): ')),
        'doc_sacador': str(input("CPF ou CNPJ do sacador: ")).strip()[:14],
        'end_sacador': str(input('Endereço do sacador: ')).strip()[:45],
        'bairro_devedor': str(input('Bairro do sacador: ')).upper().strip()[:20],
        'cep_sacador': str(input('CEP do sacador: ')).strip()[:8],
        'cidade_sacador': str(input('Cidade do sacador: ')).upper().strip()[:20],
        'uf_sacador': str(input('UF do sacador: ')).upper().strip()[:2],
        'nosso_numero': str(input('Nosso número: '))[:15],
        'especie_titulo': str(input('Espécie do título: ')).upper().strip()[:3],
        'num_titulo': str(input('Número do título (cadastrado pelo cedente): ')).strip()[:11],
        'data_emissao': datetime.strptime(input('Data de emissão (dd-mm-yyyy): '), "%d-%m-%Y").date(),
        'data_vencimento': datetime.strptime(input('Data de vencimento (dd-mm-yyyy): '), "%d-%m-%Y").date(),
        'valor_titulo': float(input('Valor do título: R$ ')),
        'endosso': str(input('Endosso (M - Mandato, T - Translativo, Branco - Sem endosso): ')).upper().strip()[0],
        'aceite': str(input('Aceite pelo devedor (N - Não Aceito, A - Aceito): ')).upper().strip()[0],
        'nome_devedor': '', 'doc_devedor': '', 'endereco_devedor': '', 'cep_devedor': '', 'cidade_devedor': '',
        'uf_devedor': '', 'doc_devedor_pf': '',
        'saldo_titulo': 0
    }
    novo_titulo['saldo_titulo'] = novo_titulo['valor_titulo']
    q = str(input('Sacado e devedor são o mesmo? [S/N]')).upper().strip()[0]
    while q not in 'SN':
        q = str(input('Opção inválida. Sacado e devedor são o mesmo? [S/N]')).upper().strip()[0]
    if q == 'S':
        novo_titulo['nome_devedor'] = novo_titulo['nome_sacador']
        novo_titulo['doc_devedor'] = novo_titulo['doc_sacador']
        novo_titulo['endereco_devedor'] = novo_titulo['end_sacador']
        novo_titulo['cep_devedor'] = novo_titulo['cep_sacador']
        novo_titulo['uf_devedor'] = novo_titulo['uf_sacador']
    elif q == 'N':
        novo_titulo['nome_devedor'] = str(input('Nome do devedor: ')).upper().strip()[45]
        novo_titulo['doc_devedor'] = str(input("CPF ou CNPJ do devedor: ")).strip()[14]
        novo_titulo['endereco_devedor'] = str(input('Endereço do devedor: ')).strip()[45]
        novo_titulo['cep_devedor'] = str(input('CEP do devedor: ')).strip()[8]
        novo_titulo['uf_devedor'] = str(input('UF do devedor: ')).upper().strip()[2]
    return novo_titulo


def gerar_remessa(arq, head):
    arquivo_final = list()
    quant_geral = quant_indicacoes = quant_originais = checksum_valor = 0
    count = 1
    for t in arq:
        quant_geral += 1
        if t['especie_titulo'] in ['DMI', 'DRI', 'CBI']:
            quant_indicacoes += 1
        else:
            quant_originais += 1
    checksum_qtd = quant_geral * 2 + quant_indicacoes + quant_originais
    quant_geral = str(quant_geral)
    quant_indicacoes = str(quant_indicacoes)
    quant_originais = str(quant_originais)
    checksum_qtd = '{:0>5}'.format(str(checksum_qtd))
    header = ('0104' + '{: <40}'.format('BANCO EXEMPLO') + HOJE + "BFOSDTTPR" + head['sequencial'] +
              '{:0>4}'.format(quant_geral) * 2 + '{:0>4}'.format(quant_indicacoes) + '{:0>4}'.format(quant_originais) +
              "0099990434127106" + " " * 497 + '0001') + "\n"
    arquivo_final.append(header)
    for t in arq:
        count += 1
        registro = ("1104" + t['cod_agencia'] +
                    t['cod_cedente'] +
                    '{: <45}'.format(t['nome_cedente']) +
                    '{: <45}'.format(t['nome_sacador']) +
                    t['doc_sacador'] +
                    '{: <45}'.format(t['end_sacador']) +
                    t['cep_sacador'] +
                    '{: <20}'.format(t['cidade_sacador']) +
                    t['uf_sacador'] + t['nosso_numero'] +
                    t['especie_titulo'] +
                    t['num_titulo'] +
                    str(t['data_emissao']) +
                    str(t['data_vencimento'])
                    + '001' + '{:0>14}'.format(str(int(t['valor_titulo'] * 100))) +
                    '{:0>14}'.format(str(int(t['saldo_titulo'] * 100))) +
                    '{: <20}'.format('CIDADE EXEMPLO') + t['endosso'] +
                    t['aceite'] +
                    '1' + '{: <45}'.format(t['nome_devedor']) +
                    '{:0>3}'.format(str(t['tipo_doc_devedor'])) +
                    t['doc_devedor'] +
                    t['doc_devedor_pf'] +
                    '{: <45}'.format(t['endereco_devedor']) +
                    t['cep_devedor'] +
                    '{: <20}'.format(t['cidade_devedor']) +
                    t['uf_devedor'] +
                    "00           000000000000000000 00000000  " + '{: <20}'.format(t['bairro_devedor']) +
                    "0" * 49 + " " * 11 + "0" * 10 + " " * 19 + '{:0>4}'.format(str(count)) + "\n"
                    )
        arquivo_final.append(registro)
        checksum_valor += t['saldo_titulo']
    checksum_valor = '{:0>18}'.format(str(int(checksum_valor * 100)))
    trailler = ('9104' + '{: <40}'.format('BANCO EXEMPLO') + HOJE + checksum_qtd + checksum_valor +
                " " * 521 + '{:0>4}'.format(str(count+1)) + "\n")
    arquivo_final.append(trailler)

    # Salvando o arquivo em .txt
    caminho = filedialog.asksaveasfilename(defaultextension='.231', filetypes=[("Arquivos de Protesto", "*.231")])
    if caminho:
        with open(caminho, 'w') as remessa:
            for registro in arquivo_final:
                remessa.write(registro)
            print('Remessa gerada com sucesso!')
    else:
        print('Operação cancelada pelo usuário.')
