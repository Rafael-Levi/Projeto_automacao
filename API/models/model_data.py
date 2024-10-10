from sqlalchemy import Column, Integer, String, MetaData, Table, Date, Float, Boolean,DateTime
from database import data_engine
metadata = MetaData()

def create_table_value(table_name: str, columns: list):
    columns_list = []
    
    # Itera sobre a lista de dicionários de colunas
    for column in columns:
        column_name = column['name']
        column_type = column['type']
        
        if column_type == "int":
            columns_list.append(Column(column_name, Integer))
        elif column_type == "string":
            columns_list.append(Column(column_name, String))
        elif column_type == "bool":
            columns_list.append(Column(column_name, Boolean))
        elif column_type == "date":
            columns_list.append(Column(column_name,String))
        elif column_type == "hora":
            columns_list.append(Column(column_name,String))
        elif column_type == "float":
            columns_list.append(Column(column_name, Float))
        else:
            raise ValueError(f"Invalid column type: {column_type}")
        
    # Cria a tabela no banco de dados
    if table_name in metadata.tables:
        raise ValueError(f"Tabela '{table_name}' já existe.")
    else:
        new_table = Table(table_name, metadata, *columns_list)
        metadata.create_all(data_engine)
        return f"Tabela '{table_name}' criada com sucesso."
