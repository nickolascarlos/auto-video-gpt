from .StdInputContentFactory import StdInputContentFactory
from .G4FContentFactory import G4FContentFactory
from .OpenAIContentFactory import OpenAIContentFactory

_factories = {
    'G4F': G4FContentFactory,
    'OpenAI': OpenAIContentFactory,
    'StdInput': StdInputContentFactory
}

def get_factory_class_by_name(name):
    return _factories[name]