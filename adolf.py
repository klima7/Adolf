from dotenv import load_dotenv
import click
import pytest


@click.group()
def adolf():
    pass


@adolf.command(help='Start Adolf bot')
def run():
    from app.bot import start_bot
    click.echo('Starting Adolf bot')
    start_bot()


@adolf.command(help='Run all tests')
def test():
    click.echo('Starting tests')
    pytest.main('--rootdir=tests -v'.split())


if __name__ == '__main__':
    load_dotenv()
    adolf()
