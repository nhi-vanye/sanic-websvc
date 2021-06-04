#! /usr/bin/env python3

import json

import click
import sanic
from sanic_openapi import openapi3_blueprint

import websvc.views
from websvc import Config as thisApp

app = None


@click.command()
@click.option(
    "--rules", default="rules.json", type=click.Path(exists=True), envvar="RULES", help="Tax rules"
)
@click.option("--listen", default="127.0.0.1", envvar="LISTEN", help="Only listen on this address")
@click.option("--port", default=8888, type=int, envvar="PORT", help="Listen on this port")
@click.option(
    "--access-log/--no-access-log",
    default=False,
    type=bool,
    envvar="ACCESS_LOG",
    help="Log access requests",
)
@click.option("--workers", default=1, envvar="WORKERS", help="Number of worker processes")
@click.option("--debug", default=False, type=bool, envvar="DEBUG", help="Enable debug output")
def server(rules, listen, port, access_log, workers, debug):

    app = sanic.Sanic("Test")
    app.blueprint(openapi3_blueprint)

    thisApp.app = app

    app.config.FALLBACK_ERROR_FORMAT = "json"

    # TODO expose an endpoint to reload rules as needed...
    with open(rules, "r") as fp:
        thisApp.RULES = json.load(fp)

    app.add_route(websvc.views.CalculateTax.as_view(), "/calc")

    app.run(host=listen, port=port, access_log=access_log, workers=workers, debug=debug)


if __name__ == "__main__":

    server()
