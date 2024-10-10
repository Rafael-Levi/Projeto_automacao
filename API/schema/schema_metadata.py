from pydantic import BaseModel
from typing import List,Dict

#Schema para metadata_tables
class ColumnSchema(BaseModel):
    name: str
    type: str

class TableSchema(BaseModel):
    table_name: str
    columns: List[Dict[str,str]]

    class Config:
        from_attributes = True

class ResponseModel(BaseModel):
    table_name:str
    columns: List[Dict]

    class Config:
        from_attributes = True
