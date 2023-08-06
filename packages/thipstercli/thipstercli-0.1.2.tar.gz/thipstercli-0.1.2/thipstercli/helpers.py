import sys

import typer
from rich import print
from thipstercli.state import state


def error(*args, **kwargs):
    print('[bold][red]Error :[/red][/bold]', *args, file=sys.stderr, **kwargs)
    sys.stderr.flush()
    raise typer.Exit(1)


def print_if_verbose(text: str):
    print(text) if state["verbose"] else None
