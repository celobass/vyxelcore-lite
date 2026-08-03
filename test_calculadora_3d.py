import csv
import pytest

from calculadora_3d import (
    calcular_custo_energia,
    calcular_custo_filamento,
    calcular_custo_perdas,
    calcular_custo_tempo,
    calcular_custo_total,
    calcular_lucro,
    calcular_preco_venda,
    gerar_relatorio,
    ler_materiais,
    salvar_orcamento,
    validar_numero_positivo,
)
def test_ler_materiais(tmp_path):
    arquivo = tmp_path / 'materiais.csv'

    arquivo.write_text(
        'nome,tipo,preco_quilo\n'
        'PLA Preto,PLA,100.00\n'
        'TPU Preto,TPU,130.00\n',
        encoding='utf-8'
    )

    materiais = ler_materiais(arquivo)

    assert len(materiais) == 2
    assert materiais[0]['nome'] == 'PLA Preto'
    assert materiais[0]['tipo'] == 'PLA'
    assert materiais[0]['preco_quilo'] == pytest.approx(100)

    assert materiais[1]['nome'] == 'TPU Preto'
    assert materiais[1]['preco_quilo'] == pytest.approx(130)

def test_salvar_orcamento(tmp_path):
    arquivo = tmp_path / 'orcamentos.csv'

    dados_orcamento = {
        'data': '02/08/2026 22:00:00',
        'nome_peca': 'Suporte',
        'material': 'PLA Preto',
        'peso_gramas': '200.00',
        'tempo_horas': '5.00',
        'custo_filamento': '20.00',
        'custo_energia': '1.00',
        'custo_tempo': '10.00',
        'custo_acabamento': '5.00',
        'custo_perdas': '3.60',
        'custo_total': '39.60',
        'lucro': '19.80',
        'preco_venda': '59.40'
    }

    salvar_orcamento(
        dados_orcamento,
        arquivo
    )

    assert arquivo.exists()

    with open(
            arquivo,
            'rt',
            newline='',
            encoding='utf-8') as arquivo_csv:

        leitor = csv.DictReader(arquivo_csv)
        orcamentos = list(leitor)

    assert len(orcamentos) == 1
    assert orcamentos[0]['nome_peca'] == 'Suporte'
    assert orcamentos[0]['material'] == 'PLA Preto'
    assert orcamentos[0]['preco_venda'] == '59.40'

def test_salvar_orcamento_nao_repete_cabecalho(
        tmp_path):
    arquivo = tmp_path / 'orcamentos.csv'

    dados_orcamento = {
        'data': '02/08/2026 22:00:00',
        'nome_peca': 'Suporte',
        'material': 'PLA Preto',
        'peso_gramas': '200.00',
        'tempo_horas': '5.00',
        'custo_filamento': '20.00',
        'custo_energia': '1.00',
        'custo_tempo': '10.00',
        'custo_acabamento': '5.00',
        'custo_perdas': '3.60',
        'custo_total': '39.60',
        'lucro': '19.80',
        'preco_venda': '59.40'
    }

    salvar_orcamento(
        dados_orcamento,
        arquivo
    )

    salvar_orcamento(
        dados_orcamento,
        arquivo
    )

    with open(
            arquivo,
            'rt',
            encoding='utf-8') as arquivo_csv:

        linhas = arquivo_csv.readlines()

    assert len(linhas) == 3


def test_calcular_custo_filamento():
    resultado = calcular_custo_filamento(200, 100)

    assert resultado == pytest.approx(20)


def test_calcular_custo_energia():
    resultado = calcular_custo_energia(10, 200, 1)

    assert resultado == pytest.approx(2)


def test_calcular_custo_tempo():
    resultado = calcular_custo_tempo(8, 2.50)

    assert resultado == pytest.approx(20)


def test_calcular_custo_perdas():
    resultado = calcular_custo_perdas(50, 10)

    assert resultado == pytest.approx(5)


def test_calcular_custo_total():
    resultado = calcular_custo_total(
        20,
        2,
        10,
        5,
        3.7
    )

    assert resultado == pytest.approx(40.7)


def test_calcular_preco_venda():
    resultado = calcular_preco_venda(100, 50)

    assert resultado == pytest.approx(150)


def test_calcular_lucro():
    resultado = calcular_lucro(150, 100)

    assert resultado == pytest.approx(50)


def test_validar_numero_positivo():
    assert validar_numero_positivo(10) is True
    assert validar_numero_positivo(0) is True
    assert validar_numero_positivo(-1) is False


def test_gerar_relatorio():
    relatorio = gerar_relatorio(
        'Suporte',
        'PLA Preto',
        20,
        2,
        10,
        5,
        3,
        40,
        20,
        60
    )

    assert 'ORÇAMENTO: Suporte' in relatorio
    assert 'Material: PLA Preto' in relatorio
    assert 'Preço sugerido: R$ 60.00' in relatorio