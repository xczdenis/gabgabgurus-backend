from abc import ABC, abstractmethod


class DataInitializer(ABC):
    @abstractmethod
    def initialize(self):
        pass
