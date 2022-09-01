from datetime import datetime
import pathlib


def get_filename():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    filename = dt_string + ".md"
    filepath = pathlib.Path(__file__).parent.resolve()
    final = str(filepath) + "/" + filename

    return final


def data_sub_names():
    names = [
        "DataScience",
        #        "DataEngineering",
        "MachineLearning",
        #        "LearnMachineLearning",
        "AskStatistics",
        "LatestInML",
        #        "MLQuestions",
    ]

    return names
