from bs4 import BeautifulSoup
import pytest
import requests

from climatempo import raspagem


CIDADES = [
    ('pouso alegre', 'mg', '455986'),
    ('Bom Jesus', 'RN', '425471'),
    ('Bom Jesus', 'PI', '456838'),
]
IDS = [cidade[2] for cidade in CIDADES]


def sopa():
    url = (
        'https://console.hgbrasil.com/documentation/weather/tools?stats=455986'
    )
    pagina = requests.get(url)
    minha_sopa = BeautifulSoup(pagina.text, 'lxml')
    yield minha_sopa


@pytest.mark.parametrize('cidade, estado, esperado', CIDADES)
def test_cidade_id(cidade: str, estado: str, esperado: str) -> None:
    assert raspagem.cidade_id(cidade, estado) == esperado


@pytest.mark.parametrize('cidade_id', IDS)
def test_requisitar_api(cidade_id: str) -> None:
    resposta_api = raspagem.requisitar_api(cidade_id)
    assert resposta_api.get('nome')
    assert resposta_api.get('nascer')
    assert resposta_api.get('por')
    assert resposta_api.get('temperatura')
    assert resposta_api.get('descricao')
