from abc import ABC, abstractmethod

class IToken(ABC):

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass


class ITokenProvider(ABC):

    @abstractmethod
    def new_token(self):
        pass

    @abstractmethod
    def get_tokens(self):
        pass

    @abstractmethod
    def new_single_operation_token():
        pass

    @abstractmethod
    def new_double_operation_token():
        pass

    @abstractmethod
    def new_tripple_operation_token():
        pass