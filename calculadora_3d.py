'''
VyxelCore Lite
Calculadora de custos para impressão 3D.

Projeto final desenvolvido por Marcelo Alves de Lima.
'''


def calcular_custo_filamento(peso_gramas, preco_quilo):
    '''Calcula o custo do filamento utilizado na impressão.'''
    peso_quilos = peso_gramas / 1000
    return peso_quilos * preco_quilo


def calcular_custo_energia(tempo_horas, potencia_watts, preco_kwh):
    '''Calcula o custo da energia elétrica consumida.'''
    potencia_kw = potencia_watts / 1000
    consumo_kwh = potencia_kw * tempo_horas
    return consumo_kwh * preco_kwh


def calcular_custo_perdas(custo_parcial, percentual_perdas):
    '''Calcula o valor reservado para falhas e desperdícios.'''
    return custo_parcial * percentual_perdas / 100


def calcular_custo_total(
        custo_filamento,
        custo_energia,
        custo_acabamento,
        custo_perdas):
    '''Soma todos os custos de produção.'''
    return (
        custo_filamento
        + custo_energia
        + custo_acabamento
        + custo_perdas
    )


def calcular_preco_venda(custo_total, margem_lucro):
    '''Calcula o preço de venda usando uma margem sobre o custo.'''
    valor_lucro = custo_total * margem_lucro / 100
    return custo_total + valor_lucro


def calcular_lucro(preco_venda, custo_total):
    '''Calcula o lucro estimado da venda.'''
    return preco_venda - custo_total


def validar_numero_positivo(valor):
    '''Retorna True quando o valor é maior ou igual a zero.'''
    return valor >= 0


def criar_resumo_orcamento(
        nome_peca,
        custo_filamento,
        custo_energia,
        custo_perdas,
        custo_total,
        lucro,
        preco_venda):
    '''Cria um resumo formatado do orçamento.'''
    return (
        f'\nORÇAMENTO: {nome_peca}\n'
        f'Custo do filamento: R$ {custo_filamento:.2f}\n'
        f'Custo de energia: R$ {custo_energia:.2f}\n'
        f'Reserva para perdas: R$ {custo_perdas:.2f}\n'
        f'Custo total: R$ {custo_total:.2f}\n'
        f'Lucro estimado: R$ {lucro:.2f}\n'
        f'Preço sugerido: R$ {preco_venda:.2f}'
    )


def solicitar_numero(mensagem):
    '''Solicita um número não negativo ao usuário.'''
    while True:
        try:
            valor = float(input(mensagem))

            if validar_numero_positivo(valor):
                return valor

            print('Digite um valor maior ou igual a zero.')

        except ValueError:
            print('Entrada inválida. Digite apenas números.')


def main():
    '''Controla a execução principal do programa.'''
    print('=' * 45)
    print('VYXELCORE LITE')
    print('Calculadora de custos para impressão 3D')
    print('=' * 45)

    nome_peca = input('Nome da peça: ')

    peso_gramas = solicitar_numero(
        'Peso da peça em gramas: '
    )
    preco_quilo = solicitar_numero(
        'Preço do quilo do filamento: R$ '
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
        preco_quilo
    )

    custo_energia = calcular_custo_energia(
        tempo_horas,
        potencia_watts,
        preco_kwh
    )

    custo_parcial = (
        custo_filamento
        + custo_energia
        + custo_acabamento
    )

    custo_perdas = calcular_custo_perdas(
        custo_parcial,
        percentual_perdas
    )

    custo_total = calcular_custo_total(
        custo_filamento,
        custo_energia,
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

    resumo = criar_resumo_orcamento(
        nome_peca,
        custo_filamento,
        custo_energia,
        custo_perdas,
        custo_total,
        lucro,
        preco_venda
    )

    print(resumo)


if __name__ == '__main__':
    main()
