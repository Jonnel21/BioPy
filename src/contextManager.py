from device.instrument import InstrumentStrategy
class ContextManager:

    """
        This class is responsible for creating a new
        strategy based on the three options given to
        the user.
    """
    
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set(self, new_strategy: InstrumentStrategy):
        self.strategy = new_strategy

    def get(self):
        return self.strategy
    