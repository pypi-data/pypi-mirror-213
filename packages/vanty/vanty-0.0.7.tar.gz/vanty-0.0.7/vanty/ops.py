from subprocess import call, run

import environ
import rich
import sh
import typer

from vanty.config import logger

app = typer.Typer(
    name="ops",
    help="Operations commands for interacting with providers such as fly.io. "
    "\n this will be moved to plugins in the future.",
    no_args_is_help=True,
)


@app.command()
def set_secrets(platform="fly"):
    """
    Set secrets for the platform.
    Supported platforms:
    - fly.io
    """
    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False),
    )

    # Set the project base directory
    environ.Env.read_env(".env")

    export_envs = [
        "DJANGO_AWS_SECRET_ACCESS_KEY",
        "DJANGO_SECRET_KEY",
        "STRIPE_LIVE_SECRET_KEY",
        "REDIS_URL",
        "DATABASE_URL",
    ]

    for e in export_envs:
        rich.print(f"exporting {e}={env(e)}")

    call(["fly", "secrets", "set", f"{e}={env(e)}"])


@app.command()
def app_status(app_name=None):
    """Check the app status on fly.io"""
    logger.info("Checking app status")
    if app_name is None:
        return sh.fly("status")
    sh.fly("status", app=app_name)


@app.command()
def fly_deploy(skip_tests: bool = False):
    """Run tests and deploy to fly.io"""
    logger.info("Running tests")
    run(["make", "tests"])
    run(["flyctl", "deploy"])


@app.command()
def fly_proxy_db(app_name="demo-app", bg=True):
    """
    Connect to the database
    """
    logger.info("Connecting to the database")
    return sh.fly("proxy", "5433:5432", app=app_name, _out=logger.info, _bg=bg)
