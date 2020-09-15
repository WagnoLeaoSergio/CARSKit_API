import logging
import os
import pathlib as pl
from cliff.command import Command
from ..runner import Runner


class RunEngine(Command):
    """Run the CARSKit engine"""

    # CRIAR UMA FLAG PARA MEDIR O TEMPO DE EXECUCAO DA ENGINE
    # CRIAR UMA FLAG PARA ESPECIFICAR O TIPO DE SAIDA DA ENGINE

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

        engine_folder_path = pl.Path(
            os.path.dirname(os.path.abspath(__file__)))

        engine_folder_path = os.path.join(
            engine_folder_path.parent, "CARSKit/")

        runner = Runner(
            engine_folder_path
        )

        output = runner.run_engine()

        return "output: " + output
