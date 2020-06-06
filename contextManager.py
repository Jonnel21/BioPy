from instrument import InstrumentStrategy

'''
This class is responsible for creating a new
strategy based on the three options given to
the user
'''
class ContextManager:
    def __init__(self, strat=None):
        self.strat = strat

    def set(self, newStrat: InstrumentStrategy):
        self.strat = newStrat

    def get(self):
        return self.strat
    