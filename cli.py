import sqlite3
from typing import Optional
import typer
from clarc import ERRORS, __app_name__, __version__, clarc, __DB_NAME__
import json

app = typer.Typer()


def get_operations() -> clarc.Operations:
    conn = sqlite3.connect(__DB_NAME__)
    if clarc.DatabaseHandler(conn).is_db():
        return clarc.Operations(conn)
    else:
        typer.secho(
            'database not found. Please, run "clarc init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def init() -> None:
    """initialize the database."""
    app_init_error = get_operations().init_app()
    if app_init_error:
        typer.secho(
            f'database creation failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"database is created successfully!", fg=typer.colors.GREEN)


@app.command()
def fetch(key: str = None, all: bool = False) -> None:
    """fetch the archived entries '--all' or by '--key' ${key}"""
    if all:
        fetch_list = get_operations().fetch_all()
        if isinstance(fetch_list, int):
            typer.secho(
                f'execution failed with {ERRORS[fetch_list]}',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        if len(fetch_list) == 0:
            typer.secho(
                "no entries in db yet", fg=typer.colors.YELLOW
            )
            raise typer.Exit()
        data = _response(fetch_list)
        typer.secho(
                data,
                fg=typer.colors.BLUE,
        )
    if key is not None:
        fetch_key = get_operations().fetch_key(key)
        if len(fetch_key) == 0:
            typer.secho(
                "no entries found for key search: " + key, fg=typer.colors.YELLOW
            )
            raise typer.Exit()
        data = _response(fetch_key)
        typer.secho(
            data,
            fg=typer.colors.BLUE,
        )


@app.command()
def upsert(
        key: str = typer.Argument(...),
        value: str = typer.Argument(...)
) -> None:
    """update on duplicate key else insert a new entry to db """
    get_operations().upsert(key, value)
    typer.secho("entry is successfully archived with key: " + key, fg=typer.colors.GREEN, bold=True)


@app.command()
def remove(
        key: str = typer.Argument(...)
) -> None:
    """remove an archived entry by specefic --key' ${key}"""
    fetch_key = get_operations().fetch_key_strict(key)
    if len(fetch_key) == 0:
        typer.secho(
            "no entries found for key search: " + key, fg=typer.colors.YELLOW
        )
        raise typer.Exit()
    get_operations().delete(key)
    typer.secho("entry is removed for key: " + key, fg=typer.colors.GREEN, bold=True)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def _response(results):
    res_dict = {"total": len(results),
                "archives": []}
    for index, element in enumerate(results):
        arch = {"id": index, "key": element[0], "value": element[1]}
        res_dict["archives"].append(arch)
    return json.dumps(res_dict, indent=4)


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show the application's version and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return
