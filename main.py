import services as s
import persistence as p
import os



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
        arquivo_bruto = s.LerArquivo(s.SelecionarArquivo())
        header = s.ExtrairHeader(arquivo_bruto)
        arquivo_bruto.pop(0)
        trailler = s.ExtrairTrailler(arquivo_bruto)
        arquivo_bruto.pop()
        titulos = s.TratarArquivo(arquivo_bruto, header['id_transacao'])
        validacao, mensagem = s.validar_arquivo(titulos, header, trailler)
        print(mensagem)
        if validacao:
            p.GravaDados()
        print('Pressione qualquer tecla para continuar...')
        input()