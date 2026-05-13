class BasicAgent:
    def __init__(self, name, metadata):
        self.name = name
        self.metadata = metadata
    def perform(self, **kwargs):
        raise NotImplementedError
