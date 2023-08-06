#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from argparse import Namespace
from pathlib import Path
from typing import Optional

import click
import yaml

logger = logging.getLogger(__name__)


class Configuration(Namespace):
    def __init__(self):
        super(Configuration, self).__init__()
        self.opts: Optional[str] = None

        self.outdir: str = None
        self.link: str = None

        self.verbose: int = 0
        self.unclean: bool = False
        self.move_media: bool = False
        self.move_html: bool = False

    def process_click_arguments(self, context: click.Context):
        if context.params.get("opts") is not None:
            self.parse_yaml_options(context.params["opts"])
        for arg_key in context.params.keys():
            if not hasattr(self, arg_key):
                logger.warning(f"Ignoring an unknown CLI argument: {arg_key}")
                continue
            val = context.params[arg_key]
            if val is None or val == ():
                # don't overwrite with an empty value
                continue
            setattr(self, arg_key, val)

    def parse_yaml_options(self, file_path: str):
        yaml_file_loc = Path(file_path)
        if not yaml_file_loc.exists():
            logger.error(f"No YAML file found at {yaml_file_loc}")
            return
        with yaml_file_loc.open() as file:
            try:
                opts = yaml.safe_load(file)
            except yaml.YAMLError as e:
                logger.error(f"Could not parse YAML options file: {e}")
                return
        for arg_key, val in opts.items():
            if not hasattr(self, arg_key):
                logger.warning(f"Ignoring an unknown YAML argument: {arg_key}")
                continue
            setattr(self, arg_key, val)
