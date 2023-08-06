import click
from werkzeug.serving import is_running_from_reloader


def show_server_banner(debug, app_import_path):
    """Show extra startup messages the first time the server is run,
    ignoring the reloader.

    this overrides original flask.cli's show_server_banner function.
    """
    if is_running_from_reloader():
        return

    if app_import_path is not None:
        click.echo(f" * Serving Flask project: '{app_import_path}'")
        click.echo(f" * Loaded blueprints: '{app_import_path}'")

    if debug is not None:
        click.echo(f" * Debug mode: {'on' if debug else 'off'}")
