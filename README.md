# Justificativa do projeto
 - Diante da necessidade do dia a dia de manipular grande quantidade de arquivos e de diferentes formatos (CSV,JSON,TXT...) surgiu a ideia de automatizar o processo usando
   Poo e Bibliotecas python ( fastapi,pandas,sqlalchemy, etc).
   - Construi então um sistema de busca de arquivos que detecta todos os arquivos presentes na pasta *data* e concatena tudo na pasta *data_frames*.
   - Com os dados concatenados eu coleto todas as colunas do arquivo e o tipo de dados de cada uma e mando para um banco de dados que serve para armazenar as informações básicas de cada tabela que sera gerada.
   - Por fim crio um banco de dados com as respectivas colunas e tipos e apartir dai o usuário consegue manipular todos os dados (fazer operações CRUD) de maneira fácil e rápida.


```graphql
projeto_automacao/
│
├── API/
│   ├── models/
│   │   └── models_metadata.py          # Arquivo que define os metadados dos modelos utilizados na aplicação
│   │
│   ├── routers/
│   │   ├── router_data.py               # Rota para manipulação e gerenciamento de dados
│   │   └── router_metadata.py           # Rota responsável por manipular e gerenciar metadados
│   │
│   ├── schema/
│   │   ├── schema_data.py               # Define o esquema para os dados manipulados na aplicação
│   │   ├── schema_metadata.py           # Define o esquema para os metadados
│   │   ├── database.py                  # Configura a conexão e interação com o banco de dados
│   │   └── start.py                     # Script de inicialização do schema e setup inicial da aplicação
│   │
│   └── data/
│       ├── csv_files/                   # Diretório onde são armazenados arquivos CSV
│       ├── data_frames/                 # Diretório para armazenamento de frames de dados
│       ├── json_files/                  # Diretório para arquivos JSON
│       └── txt_files/                   # Diretório para arquivos de texto (TXT)
│
└── data_pipeline/
    ├── src/
    │   └── classes/
            ├── api_integrations/
    │       │   ├── __init__.py              # Inicializa o módulo de integrações com APIs
    │       │   └── controller.py            # Controlador responsável por lidar com integrações de APIs
    │       │
    │       ├── data_search/
    │       │   ├── AbstractDataSource.py # Classe abstrata para definir fontes de dados
    │       │   ├── CsvSource.py          # Classe que define a manipulação de dados CSV
    │       │   ├── FilesSources.py       # Classe para manipulação de diferentes fontes de arquivos
    │       │   ├── JsonSource.py         # Classe que gerencia a integração com arquivos JSON
    │       │   └── TxtSource.py          # Classe para trabalhar com arquivos de texto (TXT)
    │       │
    │       └── ETL_source/
    │           ├── AbstractEtlSource.py  # Classe abstrata que define a estrutura de processos ETL (Extract, Transform, Load)
    │           ├── Columns.py             # Classe que define e gerencia as colunas para o processo ETL
    │           ├── EtlSource.py           # Implementação da lógica para o processo ETL
    │           ├── Output.py              # Define as operações de saída para os dados transformados
    │           ├── OutputCsv.py           # Manipula a saída dos dados no formato CSV
    │           ├── OutputJson.py          # Manipula a saída dos dados no formato JSON
    │           └── __init__.py            # Inicializa o módulo de fontes ETL
```

# Como rodar o projeto

```bash
git clone github.com/Rafael-Levi/projeto_automacao
```
```bash
pip install poetry
```
```bash
poetry install
```
```bash
task api 
```
```bash
task run
```

## Índice de Arquivos

## 1. **models/**
   - `models_metadata.py` — Arquivo que define os metadados dos modelos utilizados na aplicação.

## 2. **routers/**
   - `router_data.py` — Rota para manipulação e gerenciamento de dados.
   - `router_metadata.py` — Rota responsável por manipular e gerenciar metadados.

## 3. **schema/**
   - `schema_data.py` — Define o esquema para os dados manipulados na aplicação.
   - `schema_metadata.py` — Define o esquema para os metadados.
   - `database.py` — Configura a conexão e interação com o banco de dados.
   - `start.py` — Script de inicialização do schema e setup inicial da aplicação.

## 4. **data/**
   - `csv_files/` — Diretório onde são armazenados arquivos CSV.
   - `data_frames/` — Diretório para armazenamento de frames de dados.
   - `json_files/` — Diretório para arquivos JSON.
   - `txt_files/` — Diretório para arquivos de texto (TXT).

## 5. **data_pipeline/**
   - **src/**
     - `api_integrations/`
       - `__init__.py` — Inicializa o módulo de integrações com APIs.
       - `controller.py` — Controlador responsável por lidar com integrações de APIs.
     
   - **classes/**
     - `data_search/`
       - `AbstractDataSource.py` — Classe abstrata para definir fontes de dados.
       - `CsvSource.py` — Classe que define a manipulação de dados CSV.
       - `FilesSources.py` — Classe para manipulação de diferentes fontes de arquivos.
       - `JsonSource.py` — Classe que gerencia a integração com arquivos JSON.
       - `TxtSource.py` — Classe para trabalhar com arquivos de texto (TXT).

     - `ETL_source/`
       - `AbstractEtlSource.py` — Classe abstrata que define a estrutura de processos ETL (Extract, Transform, Load).
       - `Columns.py` — Classe que define e gerencia as colunas para o processo ETL.
       - `EtlSource.py` — Implementação da lógica para o processo ETL.
       - `Output.py` — Define as operações de saída para os dados transformados.
       - `OutputCsv.py` — Manipula a saída dos dados no formato CSV.
       - `OutputJson.py` — Manipula a saída dos dados no formato JSON.
       - `__init__.py` — Inicializa o módulo de fontes ETL.
