import re
import json
import os
import pathlib as pl
import datetime

"""
    Dependendo do quão parecido essas classes ficarem
        uma super classe Data_Manager talvez seja criada...

    class DataSet_Manager(object):
        def __init__(self):
            coisas....
"""


class Model_Statistics_Manager(object):
    """
    Class responsible for managing the statistics created after
    an execution of the engine. Requires the name of the statistics file.

    Parameters:
    ----------
        output_folder: str
            The name of the folder where the engine will create the
            next execution's statistics.

        statistics_filename: str
            The name of the next execution's statistics file.
    """

    # OS PARAMETROS NAO ESTAO SENDO USADOS

    def __init__(self, output_folder: str, statistics_filename="sample@statistics"):
        self.statistics_filename = statistics_filename
        self.output_folder = output_folder
        self.current_path = pl.Path(
            os.path.dirname(os.path.abspath(__file__)))

    def generate_statistic_data(self, statistic_file) -> dict:
        """
        Extracts the essencial data from the statistics file specified and
        returns it as an dictionary.

        Parameters:
        ----------
            statistic_file: IO
                The statistics file from which the data will be extracted.

        The variables that will be extracted from the file are:
            User amount
            Item amount
            Rate amount
            Context dimensions
            Context conditions
            Context situations
            Data density
            Scale distribution
            Average value of all ratings
            Standard deviation of all ratings
            Mode of all rating values
            Median of all rating values

        Returns:
        --------
            A dictionary with the extrated data.
        """

        fields_founded = False
        stats_data = {
            " * User amount": {
                "field_name": "user_amount",
                "value": 0
            },
            " * Item amount": {
                "field_name": "item_mount",
                "value": 0
            },
            " * Rate amount": {
                "field_name": "rate_amount",
                "value": 0
            },
            " * Context dimensions": {
                "field_name": "context_dimensions",
                "value": 0
            },
            " * Context conditions": {
                "field_name": "context_conditions",
                "value": 0
            },
            " * Context situations": {
                "field_name": "context_situations",
                "value": 0
            },
            " * Data density": {
                "field_name": "data_density",
                "value": 0
            },
            " * Scale distribution": {
                "field_name": "scale_distributions",
                "value": ""
            },
            " * Average value of all ratings": {
                "field_name": "average_ratings",
                "value": 0
            },
            " * Standard deviation of all ratings": {
                "field_name": "standard_deviation_ratings",
                "value": 0
            },
            " * Mode of all rating values": {
                "field_name": "mode_ratings",
                "value": 0
            },
            " * Median of all rating values": {
                "field_name": "median_ratings",
                "value": 0
            }
        }

        try:
            for line in statistic_file:
                field = re.findall(" [*]? .*", line)
                if field != []:
                    field = field[0]
                    field = re.split(":", field, 1)

                    if field[0] in stats_data:
                        stats_data[field[0]]["value"] = re.sub(
                            " ", "", field[1])
                        fields_founded = True
        except KeyError as e:
            return e

        if not fields_founded:
            return "ERROR! stats file not suporrted"

        labeled_data = {}
        for field in stats_data.items():
            labeled_data[field[1]['field_name']] = field[1]['value']

        return labeled_data

    def format_stats(self, stats_data: dict) -> str:
        """
        Format the dictionary of statistical data specified.

        Parameters:
        ----------
            stats_data: dict
                The extracted data from the statistics file.

        Returns:
            A message about the success of the operation.
        """

        if "average_ratings" in stats_data and "median_ratings" in stats_data \
                and "mode_ratings" in stats_data and "standard_deviation_ratings" in stats_data \
                and "scale_distributions" in stats_data:

            stats_data["average_ratings"] = re.sub(
                ",", ".", stats_data["average_ratings"])
            stats_data["median_ratings"] = re.sub(
                ",", ".", stats_data["median_ratings"])
            stats_data["mode_ratings"] = re.sub(
                ",", ".", stats_data["mode_ratings"])
            stats_data["standard_deviation_ratings"] = re.sub(
                ",", ".", stats_data["standard_deviation_ratings"])

            stats_data["scale_distributions"] = re.split(
                ",",  stats_data["scale_distributions"])

            stats_data["scale_distributions"][0] = re.sub(
                r"\[|\]", "", stats_data["scale_distributions"][0])
            stats_data["scale_distributions"][len(stats_data["scale_distributions"]) - 1] = re.sub(
                r"\[|\]", "", stats_data["scale_distributions"][len(
                    stats_data["scale_distributions"]) - 1]
            )

            return "statistics data successfully formatted!"

        return "ERROR! statistics data dict not supported"

    def save_statistics(self, stats_data, stats_file_path: str = None) -> str:
        """
        Generate and save the data extracted from the statistic file specified.

        Parameters:
        ----------
            stats_data: dict
                The extracted data from the statistics file.
            stats_file_path: str
                The path where the statitics file is going the be saved.

        Returns:
            A message about the success of the operation.
        """

        results_folder = pl.Path(os.path.dirname(stats_file_path)).parent

        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        file_name = os.path.basename(stats_file_path)

        try:
            statistics_file = open(stats_file_path, "w+")
        except FileNotFoundError:
            return f"ERROR! The file {stats_file_path} could not be opened."

        if statistics_file.writable():

            self.format_stats(stats_data)
            json.dump(stats_data, statistics_file)
            statistics_file.close()

            return f"The file {file_name + '.json'} was successfully created!"

        return f"ERROR! The file {stats_file_path} is not readable."


class Recommendations_Manager(object):
    """
    Class responsible for managing the recommendations generated after
    an execution of the engine. Requires the name of the recommendation file.

    Parameters:
    ----------
        output_folder: str
            The name of the folder where the engine will create the
            next execution's recommendations.

        result_filename: str
            The name of the next execution's recommendations file.
    """

    # OS PARAMETROS NAO ESTAO SENDO USADOS

    def __init__(self, output_folder: str, result_filename="sample_recommendations"):

        self.current_path = pl.Path(
            os.path.dirname(os.path.abspath(__file__)))
        self.output_folder = output_folder
        self.result_filename = result_filename

    def get_line_header(self, line: str):
        """
        Returns the user's id and 
        a list of his contexts from the specified line.
        """

        contexts = []

        s_line = line.split(sep=',')
        user = s_line[0]
        context_str = s_line[1]
        context_list = re.findall(".*?;|.*?: ", context_str)

        for context in context_list:
            s_context = context.split(sep=":")
            context_name = s_context[0]
            context_value = s_context[1]

            context_name = re.sub(" ", "", context_name)
            context_value = re.sub(" ", "", context_value)
            context_value = re.sub(";", "", context_value)

            contexts.append((context_name, context_value))

        return user, contexts

    def get_line_recommendations(self, line: str) -> list:
        """
        Returns a list of items and ratings from the
        specified line.
        """

        rec_strings = re.findall(r"\(.*?\)", line)
        rec_data = []
        for rec in rec_strings:

            s_rec = re.sub("[(]|[)]", "", rec)
            s_rec = re.sub(" ", "", s_rec)
            s_rec = s_rec.split(sep=',')
            item = s_rec[0]
            rating = s_rec[1]

            rec_data.append((item, rating))

        return rec_data

    def create_context_combinations(self, contexts: list) -> str:
        """
        Returns the context combination string from a 
        specified list of contexts.
        """

        ctx = ""
        for i in range(len(contexts) - 1):
            ctx = ctx + contexts[i][1] + ", "
        ctx = ctx + contexts[-1][1]

        return ctx

    def generate_recommendations_data(self, recs_file) -> dict:
        """
        Returns a dictionary of items recommendations for each user
        for each combination  for context(s) from a specified file.

        Parameters:
            recs_file: IO
                The recommendations file loaded.
        """

        results_data = {
            "users": {}
        }

        header = recs_file.readline()
        for line in recs_file:

            user, contexts = self.get_line_header(line)
            recommendations = self.get_line_recommendations(line)
            context_combination = self.create_context_combinations(contexts)

            if user not in results_data["users"]:
                results_data["users"][user] = {}
            if context_combination not in results_data["users"][user]:
                results_data["users"][user][context_combination] = []

            results_data["users"][user][context_combination] = recommendations

        return results_data

    def save_recommendations(self, recs_data, recs_file_path: str = None) -> str:
        """
        Extract the recommendations from a file which his path need to be specified,
        saves them as a JSON file and returns a message about the operations success.

        Parameters:
        ----------
            recs_data: dict
                The recommendation that was extrated from the engine's file.

            recs_file_path: 
                The path where the recommendations will be saved.
        """

        results_folder = pl.Path(os.path.dirname(recs_file_path)).parent

        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        file_name = os.path.basename(recs_file_path)

        try:
            recommendations_file = open(recs_file_path, "w+")
        except FileNotFoundError:
            return f"ERROR! The file {recs_file_path} could not be opened."

        if recommendations_file.writable():

            json.dump(recs_data, recommendations_file)
            recommendations_file.close()

            return f"The file {file_name + '.json'} was successfully created!"

        return f"ERROR! The file {recs_file_path} is not readable."
