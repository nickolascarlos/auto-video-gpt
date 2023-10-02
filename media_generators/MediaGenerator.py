from abc import abstractmethod

class MediaGenerator:

    @abstractmethod
    def generate(self, options):
        pass