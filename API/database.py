from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexão para o banco de metadados (repo_tables.db)
METADATA_DATABASE_URL = "sqlite:///./metadata_tables.db"
metadata_engine = create_engine(METADATA_DATABASE_URL, connect_args={"check_same_thread": False})
MetadataSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=metadata_engine)

# Conexão para o banco de dados real (tables.db ou outro arquivo do client)
DATA_DATABASE_URL = "sqlite:///./tables.db"
data_engine = create_engine(DATA_DATABASE_URL, connect_args={"check_same_thread": False})
DataSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=data_engine)

Base = declarative_base()

# Função para obter sessão do banco de metadados
def get_metadata_db():
    db = MetadataSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para obter sessão do banco de dados real
def get_data_db():
    db = DataSessionLocal()
    try:
        yield db
    finally:
        db.close()
