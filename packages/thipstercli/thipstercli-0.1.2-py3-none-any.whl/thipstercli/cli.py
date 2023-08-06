import typer
from rich import print
from thipster import Engine as ThipsterEngine
from thipster.auth import Google
from thipster.parser import ParserFactory
from thipster.repository import GithubRepo, LocalRepo
from thipster.terraform import Terraform
from thipster.engine.exceptions import THipsterException

from thipstercli import providers
from thipstercli.helpers import (
    error,
    print_if_verbose,
)
from thipstercli.state import init_state, state

init_state()
app = typer.Typer(name=state["app_name"], no_args_is_help=True)
app.add_typer(providers.app, name="providers")


@app.callback()
def _callback(
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Prints more information about the execution of the THipster CLI",
    ),
):
    """THipster CLI

    THipster is a tool that allows you to generate Terraform code 
from a simple DSL or yaml file.
    """
    state["verbose"] = verbose


@app.command("version")
def _version(
    thipster: bool = typer.Option(
        False,
        "--thipster", "-t",
        help="Prints the version of the THipster tool",
    ),
):
    """Prints the version of the THipster CLI
    """
    print(f"{state['app_name']}")

    if thipster:
        print(
            f":bookmark: THipster [green]v{state['thipster_version']}[/green]",
        )


@app.command("run")
def _run(
    path: str = typer.Argument(
        ".",
        help="Path to the file or directory to run",
    ),
    local: str = typer.Option(
        None,
        "--local", "-l",
        help="Runs the THipster Tool locally, importing models from the given path",
    ),
    provider: str = typer.Option(
        None,
        "--provider", "-p",
        help="Runs the THipster Tool using the given provider",
    ),
    apply: bool = typer.Option(
        False,
        "--apply", "-a",
        help="Applies the generated Terraform code",
    ),
):
    """Runs the THipster Tool on the given path
    """
    print_if_verbose(f"Running THipster on {path}")

    authentification_provider = providers.get_provider_class(
        providers.check_provider_exists(provider),
    ) if provider else Google

    print_if_verbose(
        f"Provider Auth set to [green]{authentification_provider.__name__}[/green]",
    )

    repo = LocalRepo(local) if local else GithubRepo(
        state["github_repo"], state["github_repo_branch"],
    )
    print_if_verbose("Repo set-up successful! :memo:")

    engine = ThipsterEngine(
        ParserFactory(),
        repo,
        authentification_provider,
        Terraform(),
    )
    print_if_verbose("Engine start-up successful! :rocket:")

    print_if_verbose("Parsing files...")

    try:
        parsed_file = engine._parse_files(path)
        print_if_verbose("Parsing successful! :white_check_mark:")

        models = engine._get_models(parsed_file)
        print_if_verbose("Models retrieved! :white_check_mark:")

        engine._generate_tf_files(parsed_file, models)
        print_if_verbose("Terraform files generated! :white_check_mark:")

        engine._init_terraform()
        print_if_verbose("Terraform initialized! :white_check_mark:")

        print(engine._plan_terraform())

        if apply:
            print("Type 'yes' to apply the changes : ")
            print(engine._apply_terraform())

        print_if_verbose("Done! :tada:")

    except THipsterException as e:
        error(e.message)
    except FileNotFoundError as e:
        error(
            f'No such file or directory : [bold][red]{e.filename}[/red][/bold]',
        )
    except Exception as e:
        error(*e.args)


if __name__ == "__main__":
    app()
