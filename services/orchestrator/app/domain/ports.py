from abc import ABC, abstractmethod

class RecorderPort(ABC):
    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...
