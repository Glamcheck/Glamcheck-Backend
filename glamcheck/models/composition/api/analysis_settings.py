from pydantic import BaseModel

from .not_found_components_policy import NotFoundComponentsPolicy
from .set_policy import SetPolicy


class AnalysisSettingsModel(BaseModel):
    skin_type_policy: SetPolicy
    cosmetic_properties_policy: SetPolicy
    additional_properties_policy: SetPolicy
    not_found_components_policy: NotFoundComponentsPolicy
