import click
from colorama import Fore, Back, Style

@click.command()
@click.pass_context
def create(ctx: click.Context) -> None: 
   config = ctx.obj["config"]

   print(config)

