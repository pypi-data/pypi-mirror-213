#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import click
import requests

from reddit2pdf import __version__
from reddit2pdf.configuration import Configuration
from reddit2pdf.reddit2pdf import reddit2pdf

logger = logging.getLogger(__name__)


def _check_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    current = __version__
    latest = requests.get("https://pypi.org/pypi/reddit2pdf/json").json()["info"][
        "version"
    ]
    print(f"You are currently using v{current} the latest is v{latest}")
    context.exit()


@click.group()
@click.help_option("-h", "--help")
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_check_version,
    help="Check version and exit.",
)
def cli():
    """reddit2pdf is used to download and archive content from Reddit."""
    pass


@cli.command("pdf")
@click.option("-o", "--outdir", type=str, required=True, help="")
@click.option("-l", "--link", default=None, type=str, required=True, help="")
@click.option("-v", "--verbose", default=None, count=True, help="")
@click.option("-u", "--unclean", is_flag=True, default=None, help="")
@click.option("--move-media", is_flag=True, default=None, help="")
@click.option("--move-html", is_flag=True, default=None, help="")
@click.help_option("-h", "--help")
@click.pass_context
def cli_pdf(context: click.Context, **_):
    """Archives a reddit thread as a pdf"""
    config = Configuration()
    config.process_click_arguments(context)
    reddit2pdf(config)


@cli.command("authenticate")
@click.help_option("-h", "--help")
def cli_authenticate(context: click.Context, **_):
    """Passthrough to bdfr authentication"""


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    cli()
