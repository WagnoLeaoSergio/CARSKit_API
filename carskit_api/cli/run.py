import logging
import os
import glob
import datetime
import pathlib as pl
from cliff.command import Command

from ..runner import Runner
from ..editors import Settings_Editor
from ..managers import Model_Statistics_Manager, Recommendations_Manager


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

    def latest_execution_data(self, app_path, dataset_path, results_foldername):
        data_filenames = glob.glob(
            os.path.join(
                app_path,
                os.path.dirname(dataset_path),
                f"{results_foldername}/*",
            )
        )

        data_filenames.sort(key=os.path.getctime, reverse=True)
        # return list(map(os.path.basename, data_filenames))
        return data_filenames

    def extract_stat_data(self, stats_mngr, stats_filepath):
        stats_file = open(stats_filepath)
        execution_stats = stats_mngr.generate_statistic_data(
            stats_file
        )
        stats_file.close()

        return execution_stats

    def extract_recommendations(self, recs_mngr, recs_filepath):
        recommendations_file = open(recs_filepath)
        recommendations = recs_mngr.generate_recommendations_data(
            recommendations_file
        )
        recommendations_file.close()

        return recommendations

    def take_action(self, parsed_args):
        """RunEngine action"""
        #output = "Is Running!"

        app_path = pl.Path(os.path.dirname(os.path.abspath(__file__))).parent
        engine_folder_path = os.path.join(app_path, "carskit/")
        conf_file_path = os.path.join(app_path, "carskit/test.conf")

        settings_editor = Settings_Editor(conf_file_path)
        runner = Runner(engine_folder_path)

        current_time = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

        stats_filename = f"execution@{current_time}.json"
        recs_filename = f"recomendations@{current_time}.json"

        stats_mgn = Model_Statistics_Manager(
            settings_editor.get_results_foldername(),
            stats_filename,
        )

        recs_mgn = Recommendations_Manager(
            settings_editor.get_results_foldername(),
            recs_filename
        )

        status = settings_editor.generate_file()

        if status == "The settings file was generated!":

            runner.run_engine()

            execution_datafiles = self.latest_execution_data(
                app_path,
                settings_editor.get_dataset_path(),
                settings_editor.get_results_foldername()
            )

            target_path = pl.Path(execution_datafiles[0]).parent.parent

            execution_stats = self.extract_stat_data(
                stats_mgn,
                execution_datafiles[0]
            )

            recommendations = self.extract_recommendations(
                recs_mgn,
                execution_datafiles[1]
            )

            stats_mgn.save_statistics(
                execution_stats,
                os.path.join(target_path, stats_filename)
            )
            recs_mgn.save_recommendations(
                recommendations,
                os.path.join(target_path, recs_filename)
            )

            return
        else:
            output = "An error has occured, execution canceled."

        return
