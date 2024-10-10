from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import schema.schema_metadata as schema_metadata, models.models_metadata as models_metadata, database
router_metadata = APIRouter()

#INSERT no banco metadata_tables
@router_metadata.post("/create_table_metadata/", response_model=schema_metadata.ResponseModel)
async def create_table(table: schema_metadata.TableSchema, db: Session = Depends(database.get_metadata_db)):
    try:
        # Verifica se o nome da tabela já existe
        table_exists = db.query(models_metadata.TableDefinition).filter_by(table_name=table.table_name).first()
        if table_exists:
            raise HTTPException(status_code=400, detail="Tabela com este nome já existe.")

        # Serializa a lista de colunas como JSON
        columns_json = models_metadata.TableDefinition.serialize_columns(table.columns)

        # Cria uma nova definição de tabela no banco de dados
        new_table = models_metadata.TableDefinition(
            table_name=table.table_name,
            columns=columns_json,
        )

        # Adiciona a nova entrada ao banco de dados
        db.add(new_table)
        db.commit()
        db.refresh(new_table)

        columns = models_metadata.TableDefinition.deserialize_columns(new_table.columns)

        return {
            "message": "Tabela criada com sucesso!",
            "table_name": new_table.table_name,
            "columns": columns 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#GET no banco metadata_tables
@router_metadata.get("/get_table_metadata/{table_name}",response_model=schema_metadata.ResponseModel)
async def get_table(table_name: str, db: Session = Depends(database.get_metadata_db)):
    # Consulta a tabela pelo nome
    table_entry = db.query(models_metadata.TableDefinition).filter_by(table_name=table_name).first()

    if table_entry:
        # Desserializa as colunas de volta para lista de dicionários
        columns = models_metadata.TableDefinition.deserialize_columns(table_entry.columns)
        return {"table_name": table_entry.table_name, "columns": columns}

    raise HTTPException(status_code=404, detail="Tabela não encontrada")
