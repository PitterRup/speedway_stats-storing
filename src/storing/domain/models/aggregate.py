class AggregateRoot:
    def __init__(self, version_number: int = 0):
        self.events = []
        self.version_number = version_number
