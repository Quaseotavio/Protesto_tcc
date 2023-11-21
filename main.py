from services import ler_arquivo, selecionar_arquivo, extrair_header, extrair_trailler, tratar_arquivo, validar_arquivo

while True:

    print('=' * 50)
    print(f"{'CONTROLE DE PROTESTO':^50}")
    print('=' * 50)
    print('''\nInforme a opção desejada:
     
    1 - TRATAR ARQUIVO
    2 - INSERIR TÍTULO NA REMESSA
    3 - LISTAR TITULOS
    0 - SAIR''')

    opt = int(input('\n>: '))
    while opt not in [1, 2, 3, 0]:
        opt = int(input('Opção inválida. Digite sua opção: '))
    if opt == 0:
        print('Encerrando aplicação.')
        break
    elif opt == 1:
        arquivo_bruto = ler_arquivo(selecionar_arquivo())
        header = extrair_header(arquivo_bruto)
        arquivo_bruto.pop(0)
        trailler = extrair_trailler(arquivo_bruto)
        arquivo_bruto.pop()
        titulos = tratar_arquivo(arquivo_bruto, header['id_transacao'])
        validacao, mensagem = validar_arquivo(titulos, header, trailler)
        print(mensagem)