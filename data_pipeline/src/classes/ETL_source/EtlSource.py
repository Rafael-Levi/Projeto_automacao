from data_pipeline.src.classes.ETL_source.AbstractEtlSource import AbstractETLSource
from data_pipeline.src.classes.data_search.CsvSource import CsvSource
from data_pipeline.src.classes.data_search.JsonSource import JsonSource
from data_pipeline.src.classes.data_search.TxtSource import TxtSource

class ETL_source(AbstractETLSource):
    
    def __init__(self):
        self.csv_source = CsvSource
        self.txt_source = TxtSource
        self.json_source = JsonSource

    def get_all_data_fremes(self):
        return self.get_all_data_fremes
    
    def escolher_formato_saida(self):
        return super().escolher_formato_saida()