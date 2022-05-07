from typer.testing import CliRunner
from clarc import __app_name__, __version__, cli

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_init():
    result = runner.invoke(cli.app, ["init"])
    assert result.exit_code == 0
    assert f"successfully!" in result.stdout
