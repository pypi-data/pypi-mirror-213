from importlib.metadata import version as get_version

state = {
    "verbose": False,
    "github_repo": "THipster/models",
    "github_repo_branch": "main",
    "local_repo_path": "models",
    "provider": None,
    "providers": [],
}


def init_state() -> None:
    """Initializes the state
    """
    state["thipstercli_version"] = get_version("thipstercli")
    state["thipster_version"] = get_version("thipster")
    state["app_name"] = f":bookmark: THipster-cli \
[green]v{state['thipstercli_version']}[/green]"
