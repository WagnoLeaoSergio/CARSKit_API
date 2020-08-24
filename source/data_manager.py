import re
import json
import os
import datetime

"""
    Dependendo do quão parecido essas classes ficarem
        uma super classe Data_Manager talvez seja criada...

    class DataSet_Manager(object):
        def __init__(self):
            coisas....
"""

class Model_Statistics_Manager(object):
    def __init__(self, statistics_filename="sample@statistics"):
        self.statistics_filename = statistics_filename

    def generate_statistic_data(self, statistic_file):

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
                        stats_data[field[0]]["value"] = re.sub(" ", "", field[1])
                        fields_founded = True
        except KeyError as e:
            return e.data

        if not fields_founded:
            return "ERROR! stats file not suporrted"

        labeled_data = {}
        for field in stats_data.items():
            labeled_data[field[1]['field_name']] = field[1]['value']

        return labeled_data

    def format_stats(self, stats_data):

        if "average_ratings" in stats_data and "median_ratings" in stats_data \
            and "mode_ratings" in stats_data and "standard_deviation_ratings" in stats_data \
            and "scale_distributions" in stats_data:

            stats_data["average_ratings"] = re.sub(",", ".", stats_data["average_ratings"])
            stats_data["median_ratings"] = re.sub(",", ".", stats_data["median_ratings"])
            stats_data["mode_ratings"] = re.sub(",", ".", stats_data["mode_ratings"])
            stats_data["standard_deviation_ratings"] = re.sub(",", ".", stats_data["standard_deviation_ratings"])

            stats_data["scale_distributions"] = re.split(",",  stats_data["scale_distributions"])

            stats_data["scale_distributions"][0] = re.sub(r"\[|\]", "", stats_data["scale_distributions"][0])
            stats_data["scale_distributions"][len(stats_data["scale_distributions"]) - 1] = re.sub(
                r"\[|\]", "", stats_data["scale_distributions"][len(stats_data["scale_distributions"]) - 1]
            )

            return "statistics data successfully formatted!"
        
        return "ERROR! statistics data dict not supported"

    def save_statistics(self, stats_file_path_=None):

        current_path = os.path.abspath(os.getcwd())
        results_folder = os.path.join(current_path, "source/datasets/results/")

        if stats_file_path_ is None:
            stats_file_path = os.path.join(results_folder, self.statistics_filename + ".txt")
        else:
            stats_file_path = stats_file_path_

        
        file_name = os.path.basename(stats_file_path)
        file_name = re.split("@|.txt", file_name)[1]
        file_name = re.sub(" ", "_", file_name)
        file_name = "execution_" + file_name

        try:
            statistics_file = open(stats_file_path, "r")
        except FileNotFoundError:
            return f"ERROR! The file {stats_file_path} could not be opened."

        if statistics_file.readable():
            
            stats_data = self.generate_statistic_data(statistics_file)
            self.format_stats(stats_data)
            statistics_file.close()

            with open(os.path.join(results_folder, file_name + ".json"), 'w') as outfile:
                json.dump(stats_data, outfile)

            return f"The file {file_name + '.json'} was successfully created!"

        return f"ERROR! The file {stats_file_path} is not readable."


class Recommendations_Manager(object):
    def __init__(self, result_filename="sample_recommendations"):
        self.result_filename = result_filename

    def get_line_header(self, line):
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


    def get_line_recommendations(self, line) -> list:
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

    def create_context_combinations(self, contexts:list):
        ctx = ""
        for i in range(len(contexts) - 1):
            ctx = ctx + contexts[i][1] + ", "
        ctx = ctx + contexts[-1][1]

        return ctx


    def generate_recommendations_data(self, results_file):
        results_data = {
            "users": {}
        }

        for line in results_file:

            user, contexts = self.get_line_header(line)
            recommendations = self.get_line_recommendations(line)
            context_combination = self.create_context_combinations(contexts)

            if user not in results_data["users"]:
                results_data["users"][user] = {}
            if context_combination not in results_data["users"][user]:
                results_data["users"][user][context_combination] = []

            results_data["users"][user][context_combination] = recommendations

        return results_data

    def save_recommendations(self, results_file_path_=None):

        current_path = os.path.abspath(os.getcwd())
        results_folder = os.path.join(current_path, "source/datasets/results/")

        if results_file_path_ is None:
            results_file_path = os.path.join(results_folder, self.result_filename + ".txt")
        else:
            results_file_path = results_file_path_

        results_filename = os.path.basename(results_file_path)
        results_filename = re.split(".txt", results_filename)[0]

        try:
            recommendations_file = open(results_file_path, "r")
        except FileNotFoundError:
            return f"ERROR! The file {results_file_path} could not be opened."

        if recommendations_file.readable():
            header = recommendations_file.readline()
            results_data = self.generate_recommendations_data(recommendations_file)
            recommendations_file.close()

            with open(os.path.join(results_folder, self.result_filename + ".json"), 'w') as outfile:
                json.dump(results_data, outfile)

            return f"The file {results_filename + '.json'} was successfully created!"

        return f"ERROR! The file {results_file_path} is not readable."
