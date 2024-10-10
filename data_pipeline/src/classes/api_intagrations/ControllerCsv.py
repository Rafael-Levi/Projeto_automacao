import requests,json
from datetime import datetime,date
import pandas as pd
from data_pipeline.src.classes.api_intagrations.ControllerSource import APIClient

#SELECT no banco metadata_tables
class APIClientCsv(APIClient):
    def get_table_info(self,table_name: str):
        request = requests.get(f"http://127.0.0.1:8000/get_table_metadata/{table_name}")
        if request.status_code == 200:
            data = request.json()
            print(f"Table Name:{data['table_name']}\nColumns: {data}")
            return data
        else:
            return None

    def create_table(self,table_name:str):
        metadata = self.get_table_info(table_name)
        response = requests.post(f"http://127.0.0.1:8000/create_table/{table_name}:",json=metadata)
        return response

    def custom_json_serializer(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()  # Converte para string no formato ISO (YYYY-MM-DD)
        raise TypeError(f"Type {type(obj)} not serializable")

    def populate_table(self,table_name: str):
        try:
            # Carregar o CSV
            data_frame = pd.read_csv(self.file_path_csv)

            # Converter o DataFrame para uma lista de dicionários
            data = data_frame.to_dict(orient='records')
            '''
            # Iterar sobre os registros e converter datas no campo 'data' para objeto datetime.date
            for entry in data:
                if 'data' in entry and isinstance(entry['data'], str):
                    try:
                        # Converter string para objeto datetime.date
                        entry['data'] = datetime.strptime(entry['data'], '%Y-%m-%d').date()
                    except ValueError:
                        print(f"Erro ao converter data: {entry['data']}")
            '''
            # Serializar os dados para JSON usando o custom serializer
            payload = json.dumps({"table_name": table_name, "data": data})

            # Enviar para a API
            response = requests.post(f"http://127.0.0.1:8000/populate_table/{table_name}", data=payload)

            if response.status_code == 200:
                print("Table populated successfully.")
            else:
                print(f"Failed to populate table. Error: {response.json()}")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def create_and_populate_json(self,table_name_input:str):
        self.create_table(table_name_input)
        self.populate_table(table_name_input)  