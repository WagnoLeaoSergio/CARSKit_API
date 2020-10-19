import logging
import os
import glob
import datetime
import pathlib as pl
import pickledb
import pymongo
from cliff.command import Command


class Database(Command):
    """Controls the connection with the MongoDB server"""
    def get_parser(self, prog_name):
        parser = super(Database, self).get_parser(prog_name)

        parser.add_argument(
            "--url",
            help="Especifies the MongoDB server URL to create a connection",
            action="store")

        return parser

    def test_connection(self, mdb_url, maxServDelay=2000):
        try:
            testClient = pymongo.MongoClient(
                mdb_url, serverSelectionTimeoutMS=maxServDelay)
            testClient.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print(err)
            return 0

        return 1

    def take_action(self, parsed_args):

        if not self.test_connection(parsed_args.url):
            return "ERROR! Could not connect to the server"

        app_path = pl.Path(os.path.dirname(os.path.abspath(__file__))).parent
        configs_db = pickledb.load(os.path.join(app_path, "configs.json"),
                                   False)

        configs_db.set("mongoDB_URL", parsed_args.url)
        configs_db.dump()
        return "MongoDB url saved."