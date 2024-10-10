from abc import ABC, abstractmethod

class AbstractETLSource(ABC):
    def __init__():
        pass
    
    @abstractmethod
    def add_data_source(self):
        raise NotImplementedError("Método não implementado")
    
    @abstractmethod 
    def combine_data(self):
        raise NotImplementedError("Método não implementado")