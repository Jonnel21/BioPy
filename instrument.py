from abc import ABC, abstractmethod

class InstrumentStrategy(ABC):

    @abstractmethod
    def convert_pdf(pdf_tuples: tuple):
       pass

    @abstractmethod
    def rename_unknown(table: list):
        pass

    @abstractmethod
    def wrapper_decode(array: list):
        pass

    @abstractmethod
    def to_nested(_list: list):
        pass

    @abstractmethod
    def parse_text(text_path: str):
        pass

    @abstractmethod
    def sort_headers(x: str):
        pass

    @abstractmethod
    def map_to_dictionary(nested_list: list):
        pass

    @abstractmethod
    def build_csv(save_location: str):
        pass