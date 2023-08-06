import importlib
import importlib.util
import os
from typing import Optional

import click

from unitelabs import Connector, utils


def default_app():
    """Compose"""
    src_dir = os.path.join(os.getcwd(), "src")
    package_dir = next(os.scandir(src_dir), None)
    package_name = getattr(package_dir, "name", None)

    return f"{package_name}:create_app"


@click.group()
def cli() -> None:
    """Base cli"""


@cli.command()
@click.option(
    "--app",
    type=str,
    metavar="IMPORT",
    default=default_app,
    help="The application factory function to load, in the form 'module:name'.",
)
@utils.coroutine
async def start(app):
    """Application Entrypoint"""
    app = await load_app(app)
    if app:
        await app.start()


async def load_app(location: str) -> Optional[Connector]:
    """Dynamically import application factory"""
    module_name, _, factory_name = location.partition(":")

    try:
        module = importlib.import_module(module_name)
        factory = getattr(module, factory_name)
        app = await factory()

        return app
    except ImportError as exc:
        print(exc)
    except AttributeError as exc:
        print(exc)

    return None


if __name__ == "__main__":
    cli()
