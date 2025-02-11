from abc import ABC, abstractmethod

from glamcheck.models.composition.domain import ComponentModel


class AbstractComponentService(ABC):
    @abstractmethod
    def find_component(self, title: str) -> ComponentModel:
        ...
