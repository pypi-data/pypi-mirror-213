import os
from importlib.metadata import version as get_version

from typer.testing import CliRunner

from thipstercli.cli import app

AUTH_FILE_PATH = "tests/credentials.json"

runner = CliRunner(mix_stderr=False)


def auth_test(func):
    def wrapper(*args, **kwargs):
        delete_credentials = False
        if (
            not os.path.exists(
                os.path.join(
                    os.getenv('HOME'),
                    '.config/gcloud/application_default_credentials.json',
                ),
            )
            and (
                os.getenv('GOOGLE_APPLICATION_CREDENTIALS') is not None
                or os.getenv('GOOGLE_APPLICATION_CREDENTIALS') != ''
            )
        ):

            delete_credentials = True
            if os.getenv('GOOGLE_APPLICATION_CREDENTIALS_CONTENT') is None:
                raise Exception("No credentials available")

            with open(AUTH_FILE_PATH, "w") as auth_file:
                auth_file.write(
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS_CONTENT"],
                )
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = AUTH_FILE_PATH

        res = func(*args, **kwargs)

        if delete_credentials:
            os.remove(AUTH_FILE_PATH)

        return res
    return wrapper


def test_version():
    result = runner.invoke(app, ["version"])
    version = get_version("thipstercli")
    assert result.exit_code == 0
    assert "THipster-cli" and version in result.output


def test_version_thipster():
    result = runner.invoke(app, ["version", "--thipster"])
    version = get_version("thipstercli")
    assert result.exit_code == 0
    assert "THipster-cli" and version in result.output
    version = get_version("thipster")
    assert "THipster" and version in result.output


def test_run_wrong_local_repository():
    result = runner.invoke(
        app, ["run", "tests/resources/bucket.thips", "--local", "wrong_path"],
    )
    assert result.exit_code != 0
    assert "Error : No such file or directory :" \
        in result.stderr
    assert "wrong_path" in result.stderr


def test_run_wrong_file_path():
    result = runner.invoke(app, ["run", "wrong_path"])
    assert result.exit_code != 0
    assert "Error : Path not found :" in result.stderr
    assert "wrong_path" in result.stderr


@auth_test
def test_run_bucket():

    result = runner.invoke(
        app, [
            "run", "tests/resources/bucket.thips",
            "-l", "tests/resources/models",
        ],
    )

    assert result.exit_code == 0
    assert "thipster_cli_test_bucket" in result.output
    assert "Terraform will perform the following actions" in result.output
