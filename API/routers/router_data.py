from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData
import schema.schema_data
import schema.schema_metadata
import logger,logging,models.model_data,schema
from database import get_data_db
from sqlalchemy.exc import SQLAlchemyError
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
router_data = APIRouter()

@router_data.post("/create_table/{table_name}",response_model = None)
async def create_table(table_schema: schema.schema_metadata.TableSchema):
        models.model_data.create_table_value(table_schema.table_name, table_schema.columns)
        return {"message": f"Table '{table_schema.table_name}' created successfully. {table_schema.columns}"}

#INSERT no banco tables
@router_data.post("/populate_table/{table_name}",response_model=schema.schema_data.ResponseModel)
async def populate_table(schema_tables: schema.schema_data.PopulateTable, db: Session = Depends(get_data_db)):
    try:
        # Refletir a tabela do banco de dados
        metadata = MetaData()
        table = Table(schema_tables.table_name, metadata, autoload_with=db.bind) 

        # Validação dos dados
        for entry in schema_tables.data:
            for column in table.columns:
                if column.name not in entry:
                    raise HTTPException(status_code=400, detail=f"Missing column '{column.name}' in entry {entry}.")

        # Inserir dados
        logger.info(f"Inserindo dados na tabela {schema_tables.table_name}: {schema_tables.data}")
        result = db.execute(table.insert(), schema_tables.data)
        
        db.flush()
        db.commit()

        # Contar quantos registros foram inseridos
        count = result.rowcount
        logger.info(f"Número de registros inseridos: {count}")
        return {"message": "Table populated successfully!", "rows_inserted": count}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro durante a inserção: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        db.rollback()
        logger.error(f"Erro geral: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")