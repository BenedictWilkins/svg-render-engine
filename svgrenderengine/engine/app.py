from abc import abstractmethod, ABC


class Application(ABC):
    @abstractmethod
    def query(self, query):
        raise NotImplementedError()
