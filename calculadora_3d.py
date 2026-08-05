'''
VyxelCore Lite
Calculadora de custos para impressão 3D.

Projeto final desenvolvido por Marcelo Alves de Lima.
'''

import csv
import os
from datetime import datetime


ARQUIVO_MATERIAIS = os.path.join('dados', 'materiais.csv')
ARQUIVO_ORCAMENTOS = os.path.join('dados', 'orcamentos.csv')


def ler_materiais(nome_arquivo=ARQUIVO_MATERIAIS):
    '''Lê os materiais de um arquivo CSV e retorna uma lista.'''

    materiais = []

    try:
        with open(
                nome_arquivo,
                'rt',
                encoding='utf-8') as arquivo:

            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                material = {
                    'nome': linha['nome'],
                    'tipo': linha['tipo'],
                    'preco_quilo': float(
                        linha['preco_quilo']
                    )
                }

                materiais.append(material)

    except FileNotFoundError:
        print(
            f'Erro: o arquivo {nome_arquivo} '
            'não foi encontrado.'
        )

    except (KeyError, ValueError):
        print(
            'Erro: o arquivo de materiais '
            'possui dados inválidos.'
        )

    return materiais


def calcular_custo_filamento(
        peso_gramas,
        preco_quilo):
    '''Calcula o custo do filamento utilizado.'''

    peso_quilos = peso_gramas / 1000
    return peso_quilos * preco_quilo


def calcular_custo_energia(
        tempo_horas,
        potencia_watts,
        preco_kwh):
    '''Calcula o custo da energia elétrica.'''

    potencia_kw = potencia_watts / 1000
    consumo_kwh = potencia_kw * tempo_horas

    return consumo_kwh * preco_kwh


def calcular_custo_tempo(
        tempo_horas,
        custo_hora_impressora):
    '''Calcula o custo de uso da impressora.'''

    return tempo_horas * custo_hora_impressora


def calcular_custo_perdas(
        custo_parcial,
        percentual_perdas):
    '''Calcula o custo estimado de perdas.'''

    return custo_parcial * percentual_perdas / 100


def calcular_custo_total(
        custo_filamento,
        custo_energia,
        custo_tempo,
        custo_acabamento,
        custo_perdas):
    '''Soma todos os custos de produção.'''

    return (
        custo_filamento
        + custo_energia
        + custo_tempo
        + custo_acabamento
        + custo_perdas
    )


def calcular_preco_venda(
        custo_total,
        margem_lucro):
    '''Calcula o preço de venda sugerido.'''

    valor_lucro = custo_total * margem_lucro / 100
    return custo_total + valor_lucro


def calcular_lucro(
        preco_venda,
        custo_total):
    '''Calcula o lucro estimado da venda.'''

    return preco_venda - custo_total


def validar_numero_positivo(valor):
    '''Verifica se o valor é maior ou igual a zero.'''

    return valor >= 0


def gerar_relatorio(
        nome_peca,
        nome_material,
        custo_filamento,
        custo_energia,
        custo_tempo,
        custo_acabamento,
        custo_perdas,
        custo_total,
        lucro,
        preco_venda):
    '''Gera o relatório detalhado do orçamento.'''

    return (
        '\n' + '=' * 45
        + f'\nORÇAMENTO: {nome_peca}'
        + f'\nMaterial: {nome_material}'
        + f'\nCusto do filamento: R$ {custo_filamento:.2f}'
        + f'\nCusto de energia: R$ {custo_energia:.2f}'
        + f'\nCusto de tempo: R$ {custo_tempo:.2f}'
        + f'\nCusto de acabamento: R$ {custo_acabamento:.2f}'
        + f'\nReserva para perdas: R$ {custo_perdas:.2f}'
        + f'\nCusto total: R$ {custo_total:.2f}'
        + f'\nLucro estimado: R$ {lucro:.2f}'
        + f'\nPreço sugerido: R$ {preco_venda:.2f}'
        + '\n' + '=' * 45
    )


def salvar_orcamento(
        dados_orcamento,
        nome_arquivo=ARQUIVO_ORCAMENTOS):
    '''Salva um orçamento em um arquivo CSV.'''

    pasta = os.path.dirname(nome_arquivo)

    if pasta:
        os.makedirs(
            pasta,
            exist_ok=True
        )

    arquivo_novo = (
        not os.path.exists(nome_arquivo)
        or os.path.getsize(nome_arquivo) == 0
    )

    cabecalho = [
        'data',
        'nome_peca',
        'material',
        'peso_gramas',
        'tempo_horas',
        'custo_filamento',
        'custo_energia',
        'custo_tempo',
        'custo_acabamento',
        'custo_perdas',
        'custo_total',
        'lucro',
        'preco_venda'
    ]

    with open(
            nome_arquivo,
            'at',
            newline='',
            encoding='utf-8') as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=cabecalho
        )

        if arquivo_novo:
            escritor.writeheader()

        escritor.writerow(dados_orcamento)


def solicitar_numero(mensagem):
    '''Solicita um número maior ou igual a zero.'''

    while True:
        try:
            valor = float(input(mensagem))

            if validar_numero_positivo(valor):
                return valor

            print(
                'Digite um valor maior '
                'ou igual a zero.'
            )

        except ValueError:
            print(
                'Entrada inválida. '
                'Digite apenas números.'
            )


def escolher_material(materiais):
    '''Exibe os materiais e retorna o escolhido.'''

    print('\nMateriais disponíveis:')

    for indice, material in enumerate(
            materiais,
            start=1):

        print(
            f'{indice}. '
            f'{material['nome']} '
            f'({material['tipo']}) - '
            f'R$ {material['preco_quilo']:.2f}/kg'
        )

    while True:
        try:
            escolha = int(
                input(
                    'Escolha o número do material: '
                )
            )

            if 1 <= escolha <= len(materiais):
                return materiais[escolha - 1]

            print('Escolha uma opção válida.')

        except ValueError:
            print(
                'Entrada inválida. '
                'Digite apenas o número da opção.'
            )


def main():
    '''Controla a execução principal.'''

    print('=' * 45)
    print('VYXELCORE LITE')
    print('Calculadora de custos para impressão 3D')
    print('=' * 45)

    materiais = ler_materiais()

    if not materiais:
        print(
            'Não foi possível carregar '
            'os materiais.'
        )
        return

    material = escolher_material(materiais)

    nome_peca = input('\nNome da peça: ')

    peso_gramas = solicitar_numero(
        'Peso da peça em gramas: '
    )

    tempo_horas = solicitar_numero(
        'Tempo de impressão em horas: '
    )

    potencia_watts = solicitar_numero(
        'Potência da impressora em watts: '
    )

    preco_kwh = solicitar_numero(
        'Preço da energia por kWh: R$ '
    )

    custo_hora_impressora = solicitar_numero(
        'Custo por hora da impressora: R$ '
    )

    custo_acabamento = solicitar_numero(
        'Custo de acabamento: R$ '
    )

    percentual_perdas = solicitar_numero(
        'Percentual para perdas: '
    )

    margem_lucro = solicitar_numero(
        'Margem de lucro desejada: '
    )

    custo_filamento = calcular_custo_filamento(
        peso_gramas,
        material['preco_quilo']
    )

    custo_energia = calcular_custo_energia(
        tempo_horas,
        potencia_watts,
        preco_kwh
    )

    custo_tempo = calcular_custo_tempo(
        tempo_horas,
        custo_hora_impressora
    )

    custo_parcial = (
        custo_filamento
        + custo_energia
        + custo_tempo
        + custo_acabamento
    )

    custo_perdas = calcular_custo_perdas(
        custo_parcial,
        percentual_perdas
    )

    custo_total = calcular_custo_total(
        custo_filamento,
        custo_energia,
        custo_tempo,
        custo_acabamento,
        custo_perdas
    )

    preco_venda = calcular_preco_venda(
        custo_total,
        margem_lucro
    )

    lucro = calcular_lucro(
        preco_venda,
        custo_total
    )

    relatorio = gerar_relatorio(
        nome_peca,
        material['nome'],
        custo_filamento,
        custo_energia,
        custo_tempo,
        custo_acabamento,
        custo_perdas,
        custo_total,
        lucro,
        preco_venda
    )

    print(relatorio)

    dados_orcamento = {
        'data': datetime.now().strftime(
            '%d/%m/%Y %H:%M:%S'
        ),
        'nome_peca': nome_peca,
        'material': material['nome'],
        'peso_gramas': f'{peso_gramas:.2f}',
        'tempo_horas': f'{tempo_horas:.2f}',
        'custo_filamento': f'{custo_filamento:.2f}',
        'custo_energia': f'{custo_energia:.2f}',
        'custo_tempo': f'{custo_tempo:.2f}',
        'custo_acabamento': f'{custo_acabamento:.2f}',
        'custo_perdas': f'{custo_perdas:.2f}',
        'custo_total': f'{custo_total:.2f}',
        'lucro': f'{lucro:.2f}',
        'preco_venda': f'{preco_venda:.2f}'
    }

    try:
        salvar_orcamento(dados_orcamento)

        print(
            '\nOrçamento salvo em '
            'dados/orcamentos.csv'
        )

    except OSError as erro:
        print(
            f'\nErro ao salvar o orçamento: '
            f'{erro}'
        )


if __name__ == '__main__':
    main()