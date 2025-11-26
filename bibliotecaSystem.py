import pandas as pd
import csv
from pathlib import Path 

dados = []  

colunas = ['codigo', 'titulo', 'autor', 'ano_publicacao', 'status']

#Vai basicamente esperar uma resposta do usuário para continuar o código
def pause():
    import os
    os.system('cls')

#Apenas o programador vai poder usar. Basicamente todo o banco de dados será resetado
def reset():
    pd.DataFrame(dados, columns=colunas).to_csv('biblioteca.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

#Adiciona um novo item ao banco de dados
def cadastrar():
    titulo = input("Digite o título do livro: ").strip().title()
    autor = input("Digite o autor do livro: ").strip().title()
    ano = input("Digite o ano de publicação: ").strip()

    status = 'naoValido'

    df = pd.read_csv('biblioteca.csv')

    if titulo == '' or autor == '' or ano=='':
        print("Não é permitido valores vázios! Tente novamente.")
    else:
        if titulo in df['titulo'].values:
            print("O livro já está cadastrado no sistema!")
        else:
            while status == 'naoValido':
                status = int(input("Digite o status do livro (1 - Disponível || 0 - Emprestado): "))
                if status == 1:
                    status = 'Disponível'
                elif status == 0:
                    status = 'Emprestado'
                else:
                    print('Status inválido!')
                    print('Tente novamente.')


            

            #Sempre vai adiconar o próximo código com base no maior código existente
            if df.empty:
                codigo = 1
            else:
                codigo = df['codigo'].max() + 1

            bookNew = pd.DataFrame([[codigo, titulo, autor, ano, status]], columns=colunas)

            pd.concat([df, bookNew], ignore_index=True).to_csv('biblioteca.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

            print("Livro cadastrado com sucesso!")
    

def listar():
    for _, row in pd.read_csv('biblioteca.csv').iterrows():
        print(f"{row['titulo']} - {row['autor']}, ({row['ano_publicacao']}) || Status: {row['status']}")

def buscar():
    search = input("Digite o título ou autor do livro que deseja buscar: ").lower().strip()
    encontrados = False

    for _, row in pd.read_csv('biblioteca.csv').iterrows():
        if search in row['titulo'].lower() or search in row['autor'].lower():
            print(f"{row['titulo']} - {row['autor']}, ({row['ano_publicacao']}) || Status: {row['status']}")
            encontrados = True

    if not encontrados:
        print("Nenhum livro encontrado com esse título ou autor.")

def atualizar():
    df = pd.read_csv('biblioteca.csv')

    bookAtt = input("Qual livro deseja atualizar? ").lower().strip()

    if df['titulo'].str.lower().str.contains(bookAtt).any():
        for _, row in df.iterrows():
            if bookAtt in row['titulo'].lower():
                print(f'({row['codigo']}) - {row['titulo']}')

        try:
            bookAtt = int(input('Digite o ID do livro que deseja atualizar: '))
        except:
            print("Valor inválido!")
            return


        if bookAtt not in df['codigo'].values:
            print('Codigo inválido! Tente novamente.')
            return

        option = int(input('O que deseja atualizar?\n1. Titulo\n2. Autor\n3. Ano\n4. Alterar o Status\n5. Sair\n'))

        match option:
            case 1:
                option = 'titulo'
            case 2:
                option = 'autor'
            case 3:
                option = 'ano_publicacao'
            case 4:
                option = 'status'
            case 5:
                return
            case _:
                print('Número inválido!')

        if option == 'status':

            statusAtual = df.loc[df['codigo']==bookAtt, option].values[0]

            if statusAtual=='Emprestado':
                df.loc[df['codigo']==bookAtt, option]='Disponível'
                print("O livro foi devolvido com sucesso!")
            else:
                df.loc[df['codigo']==bookAtt, option]='Emprestado'
                print('O livro foi pego com sucesso!')
        else:
            newInfo = str(input(f"Digite a nova informação: ")).strip()
    
            df.loc[df['codigo']==bookAtt, option] = newInfo

        df.to_csv('biblioteca.csv', index=False)
    else:
        print("Livro não encontrado!")
        

def remover():
    df = pd.read_csv('biblioteca.csv')

    bookDelet = input("Qual livro acabou?").lower().strip()

    if df['titulo'].str.lower().str.contains(bookDelet).any():
        for _, row in df.iterrows():
            if bookDelet in row['titulo'].lower():
                print(f"({row['codigo']}) - {row['titulo']}")
        bookDelet = int(input("Digite o ID do livro correspodente: "))
        conf = int(input(f"Você tem certeza que deseja deletar '{df.loc[df['codigo']==bookDelet, 'titulo'].values[0]}'? (1 - Sim | 2 - Não)\n"))
        if bookDelet not in df['codigo'].values:
            print("Livro não encontrado!")
        else:
            if conf == 1:
                df = df[df['codigo'] != bookDelet]
                df.reset_index(drop=True, inplace=True)
                df.to_csv("biblioteca.csv", index=False)                
                print("Livro Deletado com sucesso")
            elif conf == 2:
                print('Ok, o livro não foi deletado!')
    else:
        print("Livro não encontrado!")


def ordenar(collumInfo):
    df = pd.read_csv("biblioteca.csv")

    dfOrdenado = df.sort_values(by=[collumInfo], ascending=[True])

    return dfOrdenado

def gerarRelatorio():
    option = int(input('Escolha uma das opções:\n1. Organizar por Título\n2. Organizar por Autor\n3. Organizar por data de publicação\n4. Organizar por status\n5. Sair\n'))

    match option:
        case 1:
            option = 'titulo'
        case 2:
            option = 'autor'
        case 3:
            option = 'ano_publicacao'
        case 4:
            option = 'status'
        case 5:
            return
        case _:
            print('Número inválido!')
    
    relatorio = ordenar(option)

    if option == 'status':
        opt = int(input("Escolha entre livros disponíveis e livros emprestados (1 - 2) "))
        if opt == 1:
            relatorio = relatorio[relatorio['status'] == 'Disponível']

        elif opt == 2:
            relatorio = relatorio[relatorio['status'] == 'Emprestado']
        else:
            print("Valor inválido!")

        for _, row in relatorio.iterrows():
            print(f"{row['titulo']} - {row['autor']}, ({row['ano_publicacao']}) || Status: {row['status']}")
    else:
        for _, row in relatorio.iterrows():
            print(f"{row['titulo']} - {row['autor']}, ({row['ano_publicacao']}) || Status: {row['status']}")

def menu():
    while True:
        pause()
        print(f'{'='*10}Sistema da Biblioteca{'='*10}')
        print("\nMenu de Opções:")
        print("1. Cadastrar Livro")
        print("2. Listar Livros")
        print("3. Buscar Livro")
        print("4. Atualizar Livro")
        print("5. Remover Livro")
        print("6. Gerar Relátorio")
        print("7. Sair")

        try:
            escolha = int(input("Escolha uma opção (1-7): "))
        except:
            pause()
            print("Valor inválido!")
            continue

        match escolha:
            case 1:
                pause()
                cadastrar()
                input('Aperte ENTER para continuar...')
            case 2:
                pause()
                listar()
                input('Aperte ENTER para continuar...')
            case 3:
                pause()
                buscar()
                input('Aperte ENTER para continuar...')
            case 4:
                pause()
                atualizar()
                input('Aperte ENTER para continuar...')
            case 5:
                pause()
                remover()
                input('Aperte ENTER para continuar...')
            case 6:
                pause()
                gerarRelatorio()
                input('Aperte ENTER para continuar...')
            case 7:
                print("Saindo do programa...")
                break
            case _:
                print("Opção inválida. Tente novamente.")

def main():
    dfBiblioteca = Path('./biblioteca.csv')
    if not dfBiblioteca.exists():
        pd.DataFrame(dados, columns=colunas).to_csv('biblioteca.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)

    menu()

main()