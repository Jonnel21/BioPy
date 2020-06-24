from abc import ABC, abstractmethod

class CreateDictionary(ABC):

    @abstractmethod
    def create_dictionary(self, txt_file_path):
        pass