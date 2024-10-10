from data_pipeline.src.classes.ETL_source.Output.OutputCsv import OutputCsv
from data_pipeline.src.classes.ETL_source.Output.OutputJson import OutputJson
from data_pipeline.src.classes.ETL_source.Columns.ColumnsCsv import ColumnsCsv
from data_pipeline.src.classes.ETL_source.Columns.ColumnsJson import ColumnsJson
from data_pipeline.src.classes.api_intagrations.ControllerCsv import APIClientCsv
from data_pipeline.src.classes.api_intagrations.ControllerJson import APIClientJson
from time import sleep

outputcsv = OutputCsv()
outputjson = OutputJson()
getcolumncsv = ColumnsCsv()
getcolumnsjson = ColumnsJson()
controllercsv = APIClientCsv()
controllerjson = APIClientJson()

while format not in [1,2]: 
    print('''
        Antes de começar a busca por arquivos
        em qual formato você prefere o data frame?
        
        [1] CSV
        [2] JSON   
    ''')
    format = int(input('Resposta: '))
    table_name_input = str(input("Nome da tabela que será criada: "))
    try:
        if format == 1:
            output = outputcsv.check_and_transforme_csv() #Busca arquivos e armazena em csv
            getcolumncsv.check_and_post_csv(table_name_input) #Manda as colunas e tipos para api
            controllercsv.create_and_populate_json(table_name_input)

        elif format == 2:
            outputjson.check_and_transforme_json()
            getcolumnsjson.check_and_post_json(table_name_input)
            controllerjson.create_and_populate_json(table_name_input)
        else:
            print('Resposta inválida, tente novamente')
    except Exception as e:
        print(f'An error occurred while reading the file:', e)
