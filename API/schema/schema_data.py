from pydantic import BaseModel
from typing import List,Dict,Optional

class PopulateTable(BaseModel):
    table_name:str
    data: List[Dict[str,Optional[int|str|float]]]

    class Config:
        from_attributes = True

class ResponseModel(BaseModel):
    msg:str
    table_name:Optional[str]
    count:Optional[int]
    item_name:Optional[str]

class UpdateRequest(BaseModel):
    table_name:str
    column_name: str
    new_value: str|int|float
    condition: str

class DeleteItem(BaseModel):
    table_name:str
    condition:str

class InsertData(BaseModel):
    table_name:str
    data:List[Dict[str,int|str|float]]