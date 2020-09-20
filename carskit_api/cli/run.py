import logging
import os
import pathlib as pl
from cliff.command import Command
from ..runner import Runner
from ..editors import Settings_Editor


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

        conf_file_path = os.path.join(engine_folder_path, "test.conf")

        settings_editor = Settings_Editor(conf_file_path)
        runner = Runner(engine_folder_path)

        status = settings_editor.generate_file()
        if status == "The settings file was generated!":
            output = runner.run_engine()
        else:
            output = "An error has occured, execution canceled."

        return output
