from abc import ABC, abstractmethod

class IOperation(ABC):

    @abstractmethod
    def evaluate():
        pass

    @abstractmethod
    def set_successor():
        pass

    @abstractmethod
    def set_error_handler():
        pass

    @abstractmethod
    def set_recorder(self,recorder):
            pass

class IFunction(ABC):

    @abstractmethod
    def evaluate():
        pass

    @abstractmethod
    def set_successor():
        pass

    @abstractmethod
    def set_error_handler():
        pass


class IErrorHandler(ABC):

    @abstractmethod
    def set_error():
        pass
    @abstractmethod
    def get_error():
        pass
    @abstractmethod
    def set_expression():
        pass

    @abstractmethod
    def get_errors():
        pass

    @abstractmethod
    def clean_errors():
        pass

class IValidation(ABC):


    @abstractmethod
    def check_error():
        pass

    @abstractmethod
    def set_successor():
        pass

class IRecorder(ABC):


    @abstractmethod
    def record():
        pass

    @abstractmethod
    def get_record():
        pass

    @abstractmethod
    def set_expression():
        pass

class IProcess(ABC):


    @abstractmethod
    def process():
        pass

    @abstractmethod
    def set_successor():
        pass


