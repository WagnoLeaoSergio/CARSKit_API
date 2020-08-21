import re
import json
import os

"""
    Dependendo do quão parecido essas classes ficarem
        uma super classe Data_Manager talvez seja criada...

    class DataSet_Manager(object):
        def __init__(self):
            coisas....
"""

class Recommendations_Manager(object):
    def __init__(self):
        self.result_filename = "CAMF_CU-top-10-items fold [1]"

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
        rec_strings = re.findall("\(.*?\)", line)
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

    def save_recommendations(self):

        current_path = os.path.abspath(os.getcwd())
        results_folder = os.path.join(current_path, "source/datasets/results/")
        results_file_path = os.path.join(results_folder, self.result_filename + ".txt")

        recommendations_file = open(results_file_path, "r")
        if recommendations_file:

            header = recommendations_file.readline()
            results_data = self.generate_recommendations_data(recommendations_file)
            # json_results = json.dump(results_data)
            recommendations_file.close()

            with open(os.path.join(results_folder, self.result_filename + ".json"), 'w') as outfile:
                json.dump(results_data, outfile)

            return f"The file {self.result_filename + '.json'} was successfully created!"

        return f"ERROR! The file {self.result_filename + '.txt'} could not be opened."
