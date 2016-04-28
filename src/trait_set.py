class TraitError(RuntimeError):
    pass

class TraitSet(object):
    def __init__(self):
        self.traits = []

    def add_trait(self, trait):
        self.traits += [trait]

    def check(self, ec, nothrow = False):
        for pred, msg in self.traits:
            if not pred(ec):
                if nothrow: return False
                else:       raise TraitError(msg)

        return True
