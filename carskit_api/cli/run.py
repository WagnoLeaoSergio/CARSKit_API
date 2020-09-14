import logging
from cliff.command import Command
from ..runner import Runner


class RunEngine(Command):
    """Run the CARSKit engine"""

    def get_parser(self, prog_name):
        """RunEngine argument parsing."""
        parser = super(RunEngine, self).get_parser(prog_name)
        # group = parser.add_mutually_exclusive_group()

        #     group.add_argument(
        #         "--lowercase",
        #         help="print result in lower case",
        #         action="store_true",
        #     )

        return parser

    def take_action(self, parsed_args):

        """RunEngine action"""
        output = "Is Running!"

        runner = Runner(
            "/home/wagno/Documents/Pesquisa_de_bolsa/CARSKit_Interface/carskit_api/CARSKit"
        )

        output = runner.run_engine()

        return "output: " + output
