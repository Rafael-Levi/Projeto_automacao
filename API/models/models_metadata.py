from sqlalchemy import Column, Integer, String, MetaData
from database import Base,metadata_engine 
import json 

metadata = MetaData()

# Modelo SQLAlchemy para armazenar as definições da tabela
class TableDefinition(Base):
    __tablename__ = "table_definitions"
    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, unique=True, index=True)
    columns = Column(String)  # Aqui armazenamos as colunas em formato JSON ou string serializada
    
    # Serialização: converte a lista de colunas para string JSON
    @staticmethod
    def serialize_columns(columns):
        return json.dumps(columns)

    # Desserialização: converte a string JSON de volta para uma lista de dicionários
    @staticmethod
    def deserialize_columns(columns_json):
        return json.loads(columns_json)

# Criação da tabela no banco
Base.metadata.create_all(bind=metadata_engine)