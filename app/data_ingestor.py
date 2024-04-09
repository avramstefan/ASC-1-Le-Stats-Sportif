"""
    DataIngestor class is responsible for reading data from a csv file and storing
    it in a dictionary for easy access.
"""

import csv

class DataIngestor:
    """
        DataIngestor class is responsible for reading data from a csv file and storing
        it in a dictionary for easy access.
    """

    def __init__(self, csv_path: str):
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity\
 aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic\
 activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity\
 aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic\
 physical activity and engage in muscle-strengthening activities on 2 or more\
 days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity\
 aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic\
 activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days\
 a week',
        ]

        self.process_csv_data(csv_path)

    def select_import_features(self, entry: dict) -> dict:
        """
            Select the important features from the entry and return them as a dictionary
        """

        return {
            "YearStart": entry["YearStart"],
            "YearEnd": entry["YearEnd"],
            "DataValue": entry["Data_Value"],
            "LocationAbbr": entry["LocationAbbr"],
            "LocationDesc": entry["LocationDesc"],
            "StratificationCategory1": entry["StratificationCategory1"],
            "Stratification1": entry["Stratification1"],
        }

    def process_csv_data(self, csv_path:str):
        """
            Read data from the given csv and store the important features in the data dictionary
        """
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)

        self.data = {q: {} for q in self.questions_best_is_max + self.questions_best_is_min}

        for entry in csv_data:
            important_data = self.select_import_features(entry)

            loc_d = entry["LocationDesc"]

            if loc_d not in self.data[entry["Question"]]:
                self.data[entry["Question"]][loc_d] = [important_data]
            else:
                self.data[entry["Question"]][loc_d].append(important_data)
