from .SixFactsVideoCoordinator import *

_coordinators = {
    'SixFacts': SixFactsVideoCoordinator
}

def get_coordinator_class_by_name(name):
    return _coordinators[name]

