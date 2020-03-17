#! /usr/bin/env python
#  Copyright (c) 2020 Zero A.E., LLC
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import json
import os

import click

from chalicelib import db


def _get_chalice_stages():
    config = _get_chalice_config()
    stages: dict = config["stages"]
    return list(stages.keys())


def _get_chalice_config():
    with open(".chalice/config.json") as f:
        config = json.load(f)
    return config


def _apply_chalice_stage(stage):
    config = _get_chalice_config()
    stage_config: dict = config["stages"][stage]
    env_vars: dict = stage_config.get("environment_variables", {})
    for k, v in env_vars.items():
        if k not in os.environ:
            os.environ[k] = v


@click.group()
@click.option(
    "--stage",
    help="The Chalice stage",
    type=click.Choice(_get_chalice_stages()),
    default=_get_chalice_stages()[0],
    show_default=True,
)
def go(stage) -> None:
    """
    The Terraform Registry Management CLI
    """
    _apply_chalice_stage(stage)


@go.group()
def db():
    """
    Manage the DynamoDB backend (init, destroy, backup, restore).
    """


@db.command(name="init")
def db_init():
    """Initializes the backend."""
    return db.db_init()


@db.command(name="destroy")
def db_destroy():
    """Destroys the backend."""
    click.confirm(
        "There is no coming back from this... are you sure you want to continue?",
        abort=True,
    )
    return db.db_destroy()


@db.command(name="backup")
@click.argument("filename", type=click.Path(dir_okay=False, writable=True))
def db_backup(filename):
    """Backups the backend content."""
    db.db_dump(filename)


@db.command(name="restore")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def db_restore(filename):
    """Restores the backend content."""
    db.db_load(filename)


if __name__ == "__main__":
    go()
