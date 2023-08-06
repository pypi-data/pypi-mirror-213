# 
#   AutoFunction
#   Copyright © 2023 NatML Inc. All Rights Reserved.
#

from dataclasses import asdict
from fxn import Acceleration, AccessMode, PredictorType
from fxn.cli.auth import get_access_key # CHECK # This is not a stable API
from rich import print_json
from typer import Argument, Exit, Option, Typer
from typing import List
from webbrowser import open as open_browser

from .create import create
from .version import __version__

# Define CLI
app = Typer(
    name=f"AutoFunction CLI {__version__}",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_short=True,
    add_completion=False
)

@app.command(name="create", help="Create an AI prediction function by describing what it does.")
def create_predictor (
    tag: str=Argument(..., help="Predictor tag."),
    description: str=Argument(..., help="Describe what you want the predictor to do. Be as detailed as possible."),
    type: PredictorType=Option(None, case_sensitive=False, help="Predictor type. This defaults to `CLOUD`."),
    access: AccessMode=Option(None, case_sensitive=False, help="Predictor access mode. This defaults to `PRIVATE`."),
    acceleration: Acceleration=Option(None, case_sensitive=False, help="Cloud predictor acceleration. This defaults to `CPU`."),
    env: List[str]=Option([], help="Specify a predictor environment variable."),
    overwrite: bool=Option(None, "--overwrite", help="Overwrite any existing predictor with the same tag.")
):
    environment = { e.split("=")[0].strip(): e.split("=")[1].strip() for e in env }
    predictor = create(
        tag=tag,
        description=description,
        type=type,
        access=access,
        acceleration=acceleration,
        env=environment,
        overwrite=overwrite,
        access_key=get_access_key()
    )
    predictor = asdict(predictor)
    print_json(data=predictor)

def _learn_callback (value: bool):
    if value:
        open_browser("https://docs.fxn.ai")
        raise Exit()

def _version_callback (value: bool):
    if value:
        print(__version__)
        raise Exit()

def cli_options (
    learn: bool = Option(None, "--learn", callback=_learn_callback, help="Learn about Function."),
    version: bool = Option(None, "--version", callback=_version_callback, help="Get the AutoFunction CLI version.")
):
    pass

# Add top level options
app.callback()(cli_options)

# Run
if __name__ == "__main__":
    app()