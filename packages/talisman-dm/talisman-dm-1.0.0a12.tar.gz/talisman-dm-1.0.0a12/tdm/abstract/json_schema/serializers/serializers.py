from typing import Collection, Mapping, Sequence, Tuple, Type, TypeVar

from tdm.abstract.datamodel import AbstractDomainType, AbstractFact, AbstractMarkup, AbstractNode, AbstractNodeMention, AbstractValue, \
    BaseNodeMetadata
from tdm.helper import uniform_collection
from .abstract import AbstractElementSerializer
from .dataclass import DataclassSerializer
from .domain import DomainTypeSerializer
from .identifiable import IdSerializer
from .identity import IdentitySerializer
from .markup import MarkupSerializer
from .mention import NodeMentionSerializer
from .type_ import TypeSerializer
from .value import ValueSerializer
from .wrap import MappingElementSerializer, SequenceElementSerializer

_BASE_SERIALIZERS = {
    AbstractNode: IdSerializer(AbstractNode),
    AbstractFact: IdSerializer(AbstractFact),
    AbstractNodeMention: NodeMentionSerializer(),
    BaseNodeMetadata: DataclassSerializer(),
    AbstractValue: ValueSerializer(),
    AbstractMarkup: MarkupSerializer(),
    AbstractDomainType: DomainTypeSerializer()
}

_E = TypeVar('_E')
_S = TypeVar('_S')


def _prepare(serializer: AbstractElementSerializer[_E, _S], arg: Type[_E]) -> Tuple[Type[_S], _E]:
    return serializer.field_type(arg), serializer


def get_serializer(t: Type) -> Tuple[type, AbstractElementSerializer]:
    real_type, arg = uniform_collection(t)
    if real_type is type:
        return _prepare(TypeSerializer(), arg)
    if real_type is not None:
        if issubclass(real_type, Collection):
            wrapped_type, serializer = get_serializer(arg)
            if issubclass(real_type, Mapping):
                serializer = MappingElementSerializer(real_type, serializer)
            elif issubclass(real_type, Sequence):
                serializer = SequenceElementSerializer(real_type, serializer)
            else:
                raise TypeError
            return _prepare(serializer, wrapped_type)
        raise TypeError
    possible_types = set(arg.mro()).intersection(_BASE_SERIALIZERS)
    if len(possible_types) == 1:
        return _prepare(_BASE_SERIALIZERS[possible_types.pop()], arg)
    if hasattr(arg, '__dataclass_fields__'):
        return _prepare(DataclassSerializer(), arg)
    return _prepare(IdentitySerializer(arg), arg)
