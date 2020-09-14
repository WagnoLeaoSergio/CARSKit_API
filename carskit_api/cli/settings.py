import logging
from cliff.command import Command
from ..editors import Settings_Editor


class Settings(Command):
    """Edit the Engine's Settings"""

    def get_parser(self, prog_name):
        """Settings argument parsing."""
        parser = super(Settings, self).get_parser(prog_name)
        group = parser.add_mutually_exclusive_group()

        group.add_argument(
            "--set",
            help="set a new value for a specific configuration",
            action="store_true",
        )

        group.add_argument(
            "--get",
            help="get the value of the configuration specified",
            action="store_true",
        )

        parser.add_argument(
            "field", help="The name of the cofiguration field", action="store"
        )

        return parser

    def take_action(self, parsed_args):
        """Settings action"""
        output = "test"

        settings_editor = Settings_Editor(
            "/home/wagno/Documents/Pesquisa_de_bolsa/CARSKit_Interface/carskit_api/test.conf"
        )

        if parsed_args.get:
            param = settings_editor.get_parameter(parsed_args.field)
            return str(param)

        if parsed_args.set:
            value = input("Select the value for the configuration: ")
            result = settings_editor.set_parameter(parsed_args.field, value)
            return result

        return output
