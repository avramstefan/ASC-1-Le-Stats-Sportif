import unittest
import csv
from app.tasks import *

class TestWebserver(unittest.TestCase):
    
    def setUp(self):
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
        
        with open("unittests/unittest_nutrition_activity_obesity_usa_subset.csv", 'r') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)

        self.data = {q: {} for q in self.questions_best_is_max + self.questions_best_is_min}

        for entry in csv_data:
            important_data = {
                "YearStart": entry["YearStart"],
                "YearEnd": entry["YearEnd"],
                "DataValue": entry["Data_Value"],
                "LocationAbbr": entry["LocationAbbr"],
                "LocationDesc": entry["LocationDesc"],
                "StratificationCategory1": entry["StratificationCategory1"],
                "Stratification1": entry["Stratification1"],
            }

            locD = entry["LocationDesc"]
            
            if locD not in self.data[entry["Question"]]:
                self.data[entry["Question"]][locD] = [important_data]
            else:
                self.data[entry["Question"]][locD].append(important_data)
                
    def test_states_mean(self):
        data = {
            "question": "Percent of adults who engage in no leisure-time physical activity"
        }
        
        self.assertEqual(states_mean(self, 1, data), {"Kentucky": 22.9, "New Hampshire": 23.4, "Louisiana": 24.9, "Iowa": 25.2, "Massachusetts": 26.5, "Arkansas": 31.9, "North Carolina": 42.7})
        
    def test_state_mean(self):
        data = {
            "question": "Percent of adults who engage in no leisure-time physical activity",
            "state": "Kentucky"
        }
        
        self.assertEqual(state_mean(self, 1, data), {"Kentucky": 22.9})
        
    def test_best5(self):
        data = {
            "question": "Percent of adults who engage in no leisure-time physical activity"
        }
        
        self.assertEqual(best5(self, 1, data), {"Kentucky": 22.9, "New Hampshire": 23.4, "Louisiana": 24.9, "Iowa": 25.2, "Massachusetts": 26.5})
        
    def test_worst5(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        
        self.assertEqual(worst5(self, 1, data), {"Idaho": 46.4, "Connecticut": 55.2})
        
    def test_global_mean(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        
        self.assertEqual(global_mean(self, 1, data), {"global_mean": 50.8})
        
    def test_diff_from_mean(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        
        self.assertEqual(diff_from_mean(self, 1, data), {"Idaho": 4.399999999999999, "Connecticut": -4.400000000000006})
        
    def test_state_diff_from_mean(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "state": "Idaho"
        }
        
        self.assertEqual(state_diff_from_mean(self, 1, data), {"Idaho": 4.399999999999999})
        
    def test_mean_by_category(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)"
        }
        
        self.assertEqual(mean_by_category(self, 1, data), {"('Connecticut', 'Race/Ethnicity', 'Non-Hispanic White')": 55.2, "('Idaho', 'Education', 'Less than high school')": 46.4})
        
    def test_state_mean_by_category(self):
        data = {
            "question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)",
            "state": "Connecticut"
        }
        
        self.assertEqual(state_mean_by_category(self, 1, data), {"Connecticut": {"('Race/Ethnicity', 'Non-Hispanic White')": 55.2}})
        
from app import webserver
webserver.tasks_runner.graceful_shutdown()