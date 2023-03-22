import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("arg")
def one(arg):
    click.echo(arg)


@cli.command()
@click.argument("arg")
def two(arg):
    click.echo(arg)


if __name__ == "__main__":
    cli()
