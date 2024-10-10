from data_pipeline.src.classes.ETL_source.Columns.ColumnsSource import Columns 
import requests
import pandas as pd

class ColumnsCsv(Columns):   
    def get_columns(self):
        #Pega apenas as colunas para criar o banco metadata
        data = pd.read_csv(self.file_path_csv)
        self.columns_name = data.columns.tolist()
        return self.columns_name
    
    def check_and_post_csv(self,table_name_input:str):
        get_columns_data_frame = self.get_columns()
        return self.create_table(get_columns_data_frame,table_name_input)
    
    #INSERT no banco metadata_tables
    def create_table(self,columns_name,table_name:str):
        self.table_data ={
            "table_name": table_name, 
            "columns": []
            }
        
        for name in columns_name:
            column_type = input(f"Enter the type for column '{name}' (default is 'string'): ")
            if not column_type:
                column_type = "string"
            self.table_data["columns"].append({"name": name, "type": column_type})
                
        response = requests.post("http://127.0.0.1:8000/create_table_metadata/", json=self.table_data)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)