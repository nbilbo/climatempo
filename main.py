# 3rd
import click

# local
from climatempo import excecoes, raspagem
from climatempo.view.app import App


@click.group()
def cli():
    pass


@cli.command()
def gui():
    """Interface grafica de usuario.
    """
    App().mainloop()


@cli.command()
@click.option(
    '--cidade',
    '-c',
    required=True,
    help='Nome da cidade',
)
@click.option(
    '--estado',
    '-e',
    required=True,
    help='Sigla do estado',
)
def clima(cidade: str, estado: str) -> None:
    """Conferir temperatura diretamente pela linha de comando.
    """
    try:
        resultado = raspagem.pesquisar(cidade, estado)
        nome = resultado.get('nome')
        nascer = resultado.get('nascer')
        por = resultado.get('por')
        temperatura = resultado.get('temperatura')
        descricao = resultado.get('descricao')

        click.echo('*' * 10)
        click.echo(f'{"Cidade":<20} {nome}')
        click.echo(f'{"Nascer do sol":<20} {nascer}')
        click.echo(f'{"Por do sol":<20} {por}')
        click.echo(f'{"Temperaratura":<20} {temperatura}')
        click.echo(f'{"Descricao":<20} {descricao}')
        click.echo('*' * 10)

    except excecoes.CidadeNaoEncontrada as error:
        click.echo(str(error))

    except excecoes.ErroRaspagem as error:
        click.echo(str(error))


if __name__ == '__main__':
    cli()
