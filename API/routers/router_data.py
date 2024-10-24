from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData,select,update,text,insert
import models.models_metadata
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
        metadata = MetaData()
        table = Table(schema_tables.table_name, metadata, autoload_with=db.bind) 

        # Validação dos dados
        for entry in schema_tables.data:
            for column in table.columns:
                if column.name not in entry:
                    raise HTTPException(status_code=400, detail=f"Missing column '{column.name}' in entry {entry}.")

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

@router_data.get("/get_table_data/{table_name}", response_model=None)
async def get_table_data(table_name:str, db: Session = Depends(get_data_db)):
    try:
        metadata = MetaData()

        logger.info(f"Refletindo o banco de dados para buscar a tabela {table_name}...")
        metadata.reflect(bind=db.bind)

        if table_name not in metadata.tables:
            logger.error(f"Tabela '{table_name}' não encontrada no banco de dados.")
            raise HTTPException(status_code=404, detail=f"Tabela '{table_name}' não encontrada.")

        table = metadata.tables.get(table_name)
        logger.info(f"Tabela {table_name} encontrada com sucesso!")

        query = select(table)
        logger.info(f"Executando query: SELECT * FROM {table_name}")
        result = db.execute(query).fetchall()

        if result:
            columns = table.columns.keys()
            rows = [dict(zip(columns, row)) for row in result]
            return rows
        else:
            return []

    except SQLAlchemyError as e:
        logger.error(f"Erro de SQLAlchemy: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        logger.error(f"Erro geral: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados da tabela: {str(e)}")

@router_data.delete("/delete_register/")
async def delete_register_router(schema_delete: schema.schema_data.DeleteItem, db: Session = Depends(get_data_db)):
    try:
        # Refletir a tabela existente no banco de dados
        metadata = MetaData()
        table = Table(schema_delete.table_name, metadata, autoload_with=db.bind)
        
        # Montar a query de delete com base na condição
        delete_query = table.delete().where(text(schema_delete.condition))
        
        # Executar a query
        result = db.execute(delete_query)
        db.commit()

        # Verificar quantas linhas foram afetadas
        rows_deleted = result.rowcount

        if rows_deleted == 0:
            return {"message": "Nenhuma linha foi deletada."}
        
        return {"message": "Linhas deletadas com sucesso.", "rows_deleted": rows_deleted}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar dados da tabela: {str(e)}")

@router_data.put("/update_table_column/")
async def update_table_column(schema_data: schema.schema_data.UpdateRequest, db: Session = Depends(get_data_db)):
    try:
        metadata = MetaData()
        table = Table(schema_data.table_name, metadata, autoload_with=db.bind)

        stmt = (
            update(table)
            .where(text(schema_data.condition))  
            .values({schema_data.column_name: schema_data.new_value})
        )

        result = db.execute(stmt)
        db.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Nenhum registro encontrado para atualizar.")
        
        return {"msg": "Coluna atualizada com sucesso.", "rows_updated": result.rowcount}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

@router_data.post("/insert_data")
async def insert_data(schema_insert: schema.schema_data.InsertData, db: Session = Depends(get_data_db)):
    try:
        # Refletir a tabela do banco de dados
        metadata = MetaData()
        table = Table(schema_insert.table_name, metadata, autoload_with=db.bind)
        
        # Realizar a inserção
        insert_stmt = insert(table).values(schema_insert.data)
        result = db.execute(insert_stmt)
        
        db.commit()

        return {"message": "Dados inseridos com sucesso", "rowcount": result.rowcount}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")