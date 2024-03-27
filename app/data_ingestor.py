import json
import csv
import os

class DataIngestor:
    def __init__(self, csv_path: str):
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

        self.process_csv_data(csv_path)

        

    def process_csv_data(self, csv_path:str):
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)

        self.data = {q: {} for q in self.questions_best_is_max + self.questions_best_is_min}

        for entry in csv_data:
            important_data = {
                "YearStart": entry["YearStart"],
                "YearEnd": entry["YearEnd"],
                "DataValue": entry["Data_Value"] if entry["Data_Value"] != "" else None,
                "LocationAbbr": entry["LocationAbbr"],
                "LocationDesc": entry["LocationDesc"],
                "StratificationCategory1": entry["StratificationCategory1"],
            }

            # Can't use this data as we don't know the Data_Value
            if important_data["DataValue"] is None:
                continue
            
            locD = entry["LocationDesc"]
            
            if locD not in self.data[entry["Question"]]:
                self.data[entry["Question"]][locD] = [important_data]
            else:
                self.data[entry["Question"]][locD].append(important_data)
