import logging
import os
import glob
import datetime
import pathlib as pl
import pickledb
import pymongo
from cliff.command import Command
from ..controllers.mongo_connection import test_connection


class Database(Command):
    """Controls the connection with the MongoDB server"""
    def get_parser(self, prog_name):
        parser = super(Database, self).get_parser(prog_name)

        parser.add_argument(
            "--url",
            help="Especifies the MongoDB server URL to create a connection",
            action="store")

        return parser

    def take_action(self, parsed_args):

        if not test_connection(parsed_args.url):
            return "ERROR! Could not connect to the server"

        app_path = pl.Path(os.path.dirname(os.path.abspath(__file__))).parent
        configs_db = pickledb.load(os.path.join(app_path, "configs.json"),
                                   False)

        configs_db.set("mongoDB_URL", parsed_args.url)
        configs_db.dump()
        return "MongoDB url saved."
