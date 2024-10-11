from data_pipeline.src.classes.ETL_source.Output.OutputCsv import OutputCsv
from data_pipeline.src.classes.ETL_source.Output.OutputJson import OutputJson
from data_pipeline.src.classes.ETL_source.Columns.ColumnsCsv import ColumnsCsv
from data_pipeline.src.classes.ETL_source.Columns.ColumnsJson import ColumnsJson
from data_pipeline.src.classes.api_intagrations.ControllerCsv import APIClientCsv
from data_pipeline.src.classes.api_intagrations.ControllerJson import APIClientJson
from data_pipeline.src.classes.api_intagrations.ControllerSource import APIClient
from time import sleep

outputcsv = OutputCsv()
outputjson = OutputJson()
getcolumncsv = ColumnsCsv()
getcolumnsjson = ColumnsJson()
controllercsv = APIClientCsv()
controllerjson = APIClientJson()
controller = APIClient()
"""
while True: 
    print('''
        Antes de começar a busca por arquivos
        em qual formato você prefere o data frame?
        
        [1] CSV
        [2] JSON
        [3] SAIR
    ''')
    start_input = int(input('Resposta: '))
    table_name_input = str(input("Nome da tabela que será criada: "))
    try:
        if start_input == 1:
            output = outputcsv.check_and_transforme_csv() #Busca arquivos e armazena em csv
            getcolumncsv.check_and_post_csv(table_name_input) #Manda as colunas e tipos para api
            controllercsv.create_and_populate_json(table_name_input)

        elif start_input == 2:
            outputjson.check_and_transforme_json()
            getcolumnsjson.check_and_post_json(table_name_input)
            controllerjson.create_and_populate_json(table_name_input)

        elif start_input == 3:
            break

        else:
            print('Resposta inválida, tente novamente')
    except Exception as e:
        print(f'An error occurred while reading the file:', e)
    sleep(2)
"""

query_input =int(input("""
-------------------------------------
    Sistema de CRUD do banco
-------------------------------------
\nQual operação você deseja fazer?
[1] CONSULTAR DB\n
[2] INSERIR NOVO REGISTRO\n
[3] ALTERAR UM REGISTRO\n
[4]DELETAR UM REGISTRO\n
[5]SAIR
"""))
table_name_input = str(input("Nome da tabela que será criada: "))
if query_input == 1:
    teste = controller.get_table_data(table_name_input)
    print(teste)

elif query_input == 2:
    print("Operação em desenvolvimento... por favor aguarde")
elif query_input ==3:
    controller.update_table_value(table_name_input)
elif query_input == 4:
    item_name = str(input("Nome do item"))
    controller.delete_item(item_name)
else:
    print("Resposta inválida, tente novamente!")
    
