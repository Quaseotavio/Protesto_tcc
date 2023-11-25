import services as s
import persistence as p
import os


def main():
    while True:
        os.system('cls')
        print('=' * 50)
        print(f"{'CONTROLE DE PROTESTO':^50}")
        print('=' * 50)
        print('''\nInforme a opção desejada:
         
        1 - TRATAR ARQUIVO
        2 - CONSULTAR REMESSA ATUAL
        3 - LISTAR TODOS OS TITULOS
        0 - SAIR''')

        opt = int(input('\n>: '))
        while opt not in [1, 2, 3, 0]:
            opt = int(input('Opção inválida. Digite sua opção: '))
        if opt == 0:
            print('Encerrando aplicação.')
            break
        elif opt == 1:
            arquivo_bruto = s.ler_arquivo(s.selecionar_arquivo())
            header = s.extrair_header(arquivo_bruto)
            arquivo_bruto.pop(0)
            trailler = s.extrair_trailler(arquivo_bruto)
            arquivo_bruto.pop()
            titulos = s.tratar_arquivo(arquivo_bruto, header['id_transacao'])
            validacao, mensagem = s.validar_arquivo(titulos, header, trailler)
            print(mensagem)
            if header['id_transacao'] == 'TPR':
                print('Você enviou um arquivo de nova remessa.')
                print('Pressione qualquer tecla para continuar a montagem da remessa.')
                input()
                montar_remessa(titulos, header)
            elif header['id_transacao'] == 'CRT':
                validacao = p.checar_remessa(header)
                if validacao:
                    print('Você enviou um arquivo de confirmação de distribuição.')
                    print('Pressione qualquer tecla para verificar os títulos distribuídos.')
                    p.distribuir_titulos(titulos, header)
                    resultado = p.consulta_distribuicao(titulos)
                    print(resultado)
                    input()
                else:
                    print('Você enviou um arquivo de confirmação de uma remessa que não consta no banco de dados.')
                    print('O arquivo não será tratado. Pressione qualquer tecla para continuar.')
                    input()


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
        print(f"QUANTIDADE: {quantidade}         VALOR: R$ {soma:.2f}")
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
            arquivo.append(s.inserir_titulo())
        elif opt == 2:
            tit_rem = int(input('Informe o SEQ do título que deseja remover: '))
            while tit_rem not in range(1, len(arquivo)+1):
                tit_rem = int(input('Opção inválida. Informe o SEQ do título que deseja remover: '))
            arquivo.pop(tit_rem-1)
        elif opt == 3:
            s.gerar_remessa(arquivo, header)
            p.gravar_header(header)
            arquivo = s.converte_datas(arquivo)
            p.gravar_registros(arquivo, header['sequencial'])
            break
    return


main()
