from glamcheck.models.composition.domain import ComponentModel
from glamcheck.services.abstract_component_service import AbstractComponentService


class ComponentStorageService(AbstractComponentService):
    def find_component(self, title: str) -> ComponentModel:
        pass
