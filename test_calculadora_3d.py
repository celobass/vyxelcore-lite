import pytest

from calculadora_3d import (
    calcular_custo_energia,
    calcular_custo_filamento,
    calcular_custo_perdas,
    calcular_custo_total,
    calcular_lucro,
    calcular_preco_venda,
    criar_resumo_orcamento,
    validar_numero_positivo,
)


def test_calcular_custo_filamento():
    resultado = calcular_custo_filamento(200, 100)
    assert resultado == pytest.approx(20)


def test_calcular_custo_energia():
    resultado = calcular_custo_energia(10, 200, 1)
    assert resultado == pytest.approx(2)


def test_calcular_custo_perdas():
    resultado = calcular_custo_perdas(50, 10)
    assert resultado == pytest.approx(5)


def test_calcular_custo_total():
    resultado = calcular_custo_total(20, 2, 5, 2.7)
    assert resultado == pytest.approx(29.7)


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


def test_criar_resumo_orcamento():
    resumo = criar_resumo_orcamento(
        "Suporte",
        20,
        2,
        2.7,
        29.7,
        14.85,
        44.55
    )

    assert "ORÇAMENTO: Suporte" in resumo
    assert "Preço sugerido: R$ 44.55" in resumo
