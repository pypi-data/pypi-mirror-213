import os
import sys
import click
import importlib

from pathlib import Path
from threading import Thread

from .exploits import launchAttack

with open(Path(Path(__file__).parent, "template.py")) as fs:
    temp = fs.read()


@click.group()
@click.option("--logs-dir", "logs", type=click.STRING, envvar="MOREL_LOGS_DIR")
@click.option(
    "--flag-regex",
    "regex",
    type=click.STRING,
    envvar="FLAG_REGEX",
)
def app(logs, regex):
    """Simple program to aid in the development and testing of exploits."""
    if "MOREL_LOGS_DIR" not in os.environ and logs is None:
        os.environ["MOREL_LOGS_DIR"] = "None"
    if "FLAG_REGEX" not in os.environ and regex is None:
        os.environ["FLAG_REGEX"] = "None"
        click.echo("You may want to set the environment variable FLAG_REGEX")


@app.command()
@click.argument("filename", required=False, type=click.Path())
def template(filename):
    """Generate a template for your exploit that is compatible with M1lkman"""
    confirmed = True

    if not filename:
        click.echo("No filename specified")
        filename = "exploit_template.py"

    if Path(filename).exists():
        confirmed = click.confirm(
            f"File {filename} already exists. Do you want to overwrite it?",
            default=False,
            show_default=True,
        )

    if confirmed:
        click.echo(f"Generating file {filename} from template")
        with open(filename, "w") as fs:
            fs.write(temp)


@app.command()
@click.option(
    "--target",
    "-t",
    type=click.STRING,
    default="0.0.0.0",
    show_default=True,
    prompt="Target IP",
)
@click.argument("filename", required=True, type=click.Path(exists=True))
def test(target, filename):
    """Test your exploit against a target ip"""
    if os.system("ping -c 1 " + target + " > /dev/null") != 0:
        click.echo(f"Host {target} is unreachable")
        return
    click.echo(f"Testing {filename} on {target}")
    filename = Path(filename)
    name = filename.stem

    try:
        spec = importlib.util.spec_from_file_location(name, filename.resolve())
        module = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules[name] = module
        spec.loader.exec_module(module)  # type: ignore
        exploitfun = getattr(sys.modules[name], "main")
    except Exception as e:
        click.echo("There was an error import your exploit. Please check the syntax.")
        return

    t = Thread(
        target=launchAttack,
        args=(
            exploitfun,
            target,
        ),
        name=f"{exploitfun.__module__}_{target}",
    )
    t.start()
    t.join()
