import click
import pytest
from dotenv import load_dotenv


@click.group()
def adolf():
    pass


@adolf.command(help='Start Adolf bot')
def run():
    click.echo('Starting Adolf bot')
    import app


@adolf.command(help='Run all tests')
def test():
    click.echo('Starting tests')
    pytest.main('--rootdir=tests -v'.split())


if __name__ == '__main__':
    load_dotenv()
    adolf()
