import pandas as pd
import os
from data_pipeline.src.classes.ETL_source.EtlSource import AbstractETLSource
from data_pipeline.src.classes.data_search.CsvSource import CsvSource
from data_pipeline.src.classes.data_search.JsonSource import JsonSource
from data_pipeline.src.classes.data_search.TxtSource import TxtSource

class Output(AbstractETLSource):
    def __init__(self):
        self.data_sources = []
        self.output_file_csv = 'combined_data.csv'
        self.output_file_json = 'combined_data.json'
        self.file_path_csv = f'data/data_frames/data_frame_csv/{self.output_file_csv}'
        self.file_path_json = f'data/data_frames/data_frame_json/{self.output_file_json}'
        self.csv_source = CsvSource()
        self.txt_source = TxtSource()
        self.json_source = JsonSource()

    def add_data_source(self, data_source):
        self.data_sources.append(data_source)

    def combine_data(self):
        combined_data = pd.DataFrame()
        for source in self.data_sources:
            source.create_path()
            source.check_for_new_files()
            data = source.get_data() 
            if data is not None:
                combined_data = pd.concat([combined_data, data], ignore_index=True)
        return combined_data

    def create_folder_path_data_frames(self,file:str):
        if file.endswith('.csv'):
            self.folder_path = os.path.join('data','data_frames','data_frame_csv')
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
        elif file.endswith('.json'):
            self.folder_path = os.path.join('data','data_frames','data_frame_json')
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
