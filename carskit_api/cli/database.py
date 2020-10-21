import logging
import os
import glob
import datetime
import pathlib as pl
import pickledb
import pymongo
from cliff.command import Command
from cryptography.fernet import Fernet

from ..controllers.mongo_connection import test_connection
from ..controllers.data_processing import get_app_path, encrypt, decrypt


class Database(Command):
    """Controls the connection with the MongoDB server"""

    def get_parser(self, prog_name):
        parser = super(Database, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "--url",
            help="Especifies the MongoDB server URL to create a connection",
            dest="url",
            action="store",
        )

        group.add_argument(
            "--secrets-path",
            help="Especifies the path for the file '.secrets.key'",
            dest="path",
            action="store",
        )

        return parser

    def take_action(self, parsed_args):

        if parsed_args.path:
            if os.path.exists(parsed_args.path):
                app_path = get_app_path()
                configs_db = pickledb.load(
                    os.path.join(app_path, "configs.json"), False
                )
                configs_db.set("skpath", parsed_args.path)
                configs_db.dump()

                return "'.secrets.key' path saved."
            return "The path specified do not exists."

        if parsed_args.url:
            if not test_connection(parsed_args.url):
                return "ERROR! Could not connect to the server"

            # Getting where the package is in the computer
            app_path = get_app_path()
            configs_db = pickledb.load(os.path.join(app_path, "configs.json"), False)

            # Opening the '.secrets.key' file previously specified
            secrets_path = configs_db.get("skpath")
            secrets_file = open(secrets_path, mode="w+")

            # Generating a new key to encrypt the URL
            new_key = Fernet.generate_key()
            url_encripted = encrypt(parsed_args.url.encode(), new_key)

            # Saving the key in the file
            secrets_file.write(new_key.decode())

            # Saving the encripted url in the configs_db
            configs_db.set("mdburl", url_encripted.decode())
            configs_db.dump()
            return "MongoDB url saved."
