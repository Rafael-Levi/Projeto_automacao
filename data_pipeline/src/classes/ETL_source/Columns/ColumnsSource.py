from data_pipeline.src.classes.ETL_source.Output.Output import Output
import requests
import pandas as pd
import os

class Columns(Output):
    def __init__(self):
        self.current_directory = os.getcwd()
        self.file_path_csv = os.path.join(self.current_directory,'data','data_frames','data_frame_csv','combined_data.csv')
        self.file_path_json = os.path.join(self.current_directory,'data','data_frames','data_frame_json','combined_data.json')

    def get_columns(self):
        raise NotImplementedError("Método não implementado")
    
    def check_and_post_csv(self,table_name_input:str):
        raise NotImplementedError("Método não implementado")
    
    #INSERT no banco metadata_tables
    def create_table(self,columns_name,table_name:str):
        raise NotImplementedError("Método não implementado")