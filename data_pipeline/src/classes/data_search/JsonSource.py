import json
from operator import index
import os
import pandas as pd
from data_pipeline.src.classes.data_search.FilesSources import FilesSources

class JsonSource(FilesSources):
    def create_path(self):
        current_directory = os.getcwd()
        self.folder_path = os.path.join(current_directory, 'data', 'json_files')
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def check_for_new_files(self):
        current_files = os.listdir(self.folder_path)
        new_files = [file for file in current_files if file not in self.previous_files and file.endswith('.json')]

        if new_files:
            print("New files detected:", new_files)
            self.previous_files = current_files
        else:
            print("No new JSON files detected.")
            self.get_data()

    def get_data(self):
        data_frame = []
        for file_path in self.previous_files:
            try:
                path = f'{self.folder_path}/{file_path}'
                data = pd.read_json(path)

                # Flatten nested JSON structure if necessary
                if isinstance(data, list):
                    data = pd.json_normalize(data)
                
                data_frame.append(data)
            except Exception as e:
                print("An error occurred while reading the JSON file:", e)
        if data_frame:
            self.combined_data = pd.concat(data_frame, ignore_index=True)
            return self.combined_data
        else:
            return None
