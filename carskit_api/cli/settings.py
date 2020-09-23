import logging
import os
import pathlib as pl
from cliff.command import Command
from ..editors import Settings_Editor


class Settings(Command):
    """Edit the Engine's Settings"""

    def get_parser(self, prog_name):
        """Settings argument parsing."""
        parser = super(Settings, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "-s", "--set",
            help="set a new value for a specific configuration",
            action="store_true",
        )
        group.add_argument(
            "-g", "--get",
            help="get the value of the configuration specified",
            action="store_true",
        )

        parser.add_argument(
            "field",
            help="The name of the configuration field",
            action="store"
        )

        parser.add_argument(
            "--value",
            help="The new value for the configuration field specified. When the --get flag is setted this argument is disabled.",
            action="store"
        )

        return parser

    def take_action(self, parsed_args):
        """Settings action"""
        output = "test"

        conf_file_path = pl.Path(
            os.path.dirname(os.path.abspath(__file__)))

        conf_file_path = os.path.join(
            conf_file_path.parent, "carskit/test.conf")

        settings_editor = Settings_Editor(conf_file_path)

        if parsed_args.get:
            param = settings_editor.get_parameter(parsed_args.field)
            return str(param)

        if parsed_args.set:
            if not parsed_args.value:
                return "No value setted. Operation canceled."

            value = parsed_args.value
            result = settings_editor.set_parameter(parsed_args.field, value)
            return result

        return output
