"""
Código para finalidade de estudo.
site: https://hgbrasil.com/status/weather/
"""
# python
import typing

# 3rd
import requests
from bs4 import BeautifulSoup

# local
from climatempo import excecoes


# HEADERS = {
#     'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
# }
HEADERS = {}


def nome_cidade(sopa: BeautifulSoup) -> str:
    """
    Procura pelo nome da cidade.

    :param sopa: Onde sera realizado a busca.
    :type sopa: BeautifulSoup.

    :return: Nome da cidade.
    :rtpe: str.
    """
    try:
        div = sopa.find('div', {'class': 'col col-md-4 city-data'})
        header = div.find('h4')

    except AttributeError:
        raise excecoes.ErroRaspagem('Erro ao realizar a raspagem de dados.')

    else:
        return header.text


def nascer_sol(sopa: BeautifulSoup) -> str:
    """
    Procura pelo horario do nascer do sol.

    :param sopa: Onde sera realizado a busca.
    :type sopa: BeautifulSoup.

    :return: Horario do nascer do sol.
    :rtype: str.
    """
    try:
        div = sopa.find('div', {'class': 'col col-md-4 city-data'})
        paragraph = div.find('p')
        nascer = [string for string in paragraph.strings][1]

    except AttributeError:
        raise excecoes.ErroRaspagem('Erro ao realizar a raspagem de dados.')

    else:
        return nascer.replace('\n', '').strip()


def por_sol(sopa: BeautifulSoup) -> str:
    """
    Procura pelo horario do por do sol.

    :param sopa: Onde sera realizado a busca.
    :type sopa: BeautifulSoup.

    :return: Horario do por do sol.
    :rtype: str.
    """
    try:
        div = sopa.find('div', {'class': 'col col-md-4 city-data'})
        paragraph = div.find('p')
        por = [string for string in paragraph.strings][-1]

    except AttributeError:
        raise excecoes.ErroRaspagem('Erro ao realizar a raspagem de dados.')

    else:
        return por.replace('\n', '').strip()


def temperatura(sopa: BeautifulSoup) -> str:
    """
    Procura pela temperatura atual.

    :param sopa: Onde sera realizado a busca.
    :type sopa: BeautifulSoup.

    :return: Temperatura atual.
    :rtype: str.
    """
    try:
        div = sopa.find('div', {'class': 'col col-md-4 current-description'})
        header = div.find('h4')

    except AttributeError:
        raise excecoes.ErroRaspagem('Erro ao realizar a raspagem de dados.')

    else:
        return header.text


def descricao(sopa: BeautifulSoup) -> str:
    """
    Procura pela descricao do clima.

    :param sopa: Onde sera realizado a busca.
    :type sopa: BeautifulSoup.

    :return: Descricao atual.
    :rtype: str.
    """
    try:
        div = sopa.find('div', {'class': 'col col-md-4 current-description'})
        paragraph = div.find('p')

    except AttributeError:
        raise excecoes.ErroRaspagem('Erro ao realizar a raspagem de dados.')

    else:
        return paragraph.text


def cidade_id(cidade: str, estado: str) -> str:
    """
    Obtem o id da cidade apartir de seu nome.

    :param cidade: Nome da cidade.
    :type cidade: str.

    :param estado: Sigla do estado.
    :type estado: str.

    :return: Id da cidade.
    :rtype: str.
    """
    try:
        endpoint = 'https://console.hgbrasil.com/search?utf8=%E2%9C%93&q={}'
        estado = estado.upper()
        id_ = None
        cidade_formatado = cidade.lower().replace(' ', '+')

        url = endpoint.format(cidade_formatado)
        pagina = requests.get(url, headers=HEADERS)
        sopa = BeautifulSoup(pagina.text, 'lxml')

        divs = sopa.find_all('div', {'search-item mt-3'})
        for div in divs:
            if div.find('h4').text.endswith(estado):
                anchor = div.find('a')
                id_ = anchor.text.split('=')[-1]
                break

        if id_ is None:
            raise excecoes.CidadeNaoEncontrada(
                f'A cidade {cidade} nao foi encontrada.'
            )

    except AttributeError as error:
        raise excecoes.ErroRaspagem(f'Erro ao realizar a raspagem de dados.')

    except Exception as error:
        raise error

    else:
        return id_


def requisitar_api(cidade_id: str) -> typing.Optional[typing.Dict]:
    """
    Responsavel por obter os dados do clima de uma cidade.

    :param cidade_id: Id da cidade.
    :type cidade_id: str.

    :return: Dicionario com as informacoes.
    :rtype: dict.
    """
    try:
        # endpoint = 'https://api.hgbrasil.com/weather?woeid={}'
        endpoint = (
            'https://console.hgbrasil.com/documentation/weather/tools?stats={}'
        )
        url = endpoint.format(cidade_id)
        pagina = requests.get(url, headers=HEADERS)
        sopa = BeautifulSoup(pagina.text, 'lxml')
        nome = nome_cidade(sopa)
        nascer = nascer_sol(sopa)
        por = por_sol(sopa)
        temp = temperatura(sopa)
        desc = descricao(sopa)

    except Exception as error:
        raise error

    else:
        return {
            'nome': nome,
            'nascer': nascer,
            'por': por,
            'temperatura': temp,
            'descricao': desc,
        }


def pesquisar(cidade: str, estado: str) -> typing.Optional[typing.Dict]:
    """
    Pesquisa pelas informacoes de clima de uma cicade.

    :param cidade: Nome da cidade.
    :type cidade: str.

    :param estado: Sigla do estado.
    :type estado: str.

    :return: Informacoes de clima.
    :rtype: dict.
    """
    identificador_cidade = cidade_id(cidade, estado)
    resposta = requisitar_api(identificador_cidade)

    return resposta
