from tdm.abstract.datamodel import AbstractDirective
from tdm.datamodel.directives import CreateAccountDirective, CreateConceptDirective, CreatePlatformDirective
from tdm.v0.json_schema.directive import AbstractDirectiveModel, CreateAccountDirectiveModel, CreateConceptDirectiveModel, \
    CreatePlatformDirectiveModel


def convert_directive(directive: AbstractDirectiveModel) -> AbstractDirective:
    if isinstance(directive, CreateConceptDirectiveModel):
        return CreateConceptDirective(
            name=directive.name,
            concept_type=directive.concept_type,
            filters=directive.filters,
            notes=directive.notes,
            markers=directive.markers,
            access_level=directive.access_level,
            id=directive.id
        )
    elif isinstance(directive, CreateAccountDirectiveModel):
        return CreateAccountDirective(
            key=directive.key,
            platform_key=directive.platform_key,
            name=directive.name,
            url=directive.url
        )
    elif isinstance(directive, CreatePlatformDirectiveModel):
        return CreatePlatformDirective(
            key=directive.key,
            name=directive.name,
            platform_type=directive.platform_type,
            url=directive.url
        )
