from .templates import (
    Template,
    TemplateAny,
    TemplateDict,
    TemplateList,
    Optional,
)

from .validate import (
    Validate,
    ValidateFromJSON,
    ValidateFromYAML,
    ValidateFromTOML,
)

__all__ = [
    'Template',
    'TemplateAny',
    'TemplateDict',
    'TemplateList',
    'Optional',
    'Validate',
    'ValidateFromJSON',
    'ValidateFromYAML',
    'ValidateFromTOML',
]

__version__ = '1.2.0'
__author__ = 'Alon Krymgand Osovsky'
