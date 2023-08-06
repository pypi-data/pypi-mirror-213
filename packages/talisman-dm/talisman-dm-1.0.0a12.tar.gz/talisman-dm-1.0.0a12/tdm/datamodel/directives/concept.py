from dataclasses import dataclass
from typing import Mapping, Optional, Tuple

from tdm.abstract.datamodel import AbstractDirective, Identifiable
from tdm.abstract.json_schema import generate_model
from tdm.helper import freeze_sequence


@dataclass(frozen=True)
class _CreateConceptDirective(AbstractDirective):
    name: str
    concept_type: str
    filters: Tuple[Mapping[str, object], ...]
    notes: Optional[str] = None
    markers: Optional[str] = None
    access_level: Optional[str] = None

    def __post_init__(self):
        filters = freeze_sequence(self.filters)
        object.__setattr__(self, 'filters', filters)


@generate_model(label='create_concept')
@dataclass(frozen=True)
class CreateConceptDirective(Identifiable, _CreateConceptDirective):
    pass
