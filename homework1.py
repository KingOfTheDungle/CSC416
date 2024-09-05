
"""
hamburger
"""

class world:

    def __init__(self):
        pass


    def ask(self, sentence):
        pass

class player:

    def __init__(self, kb):
        self.kb  = kb

    def interface(self, query):
        return false

    if __name__ == '__main__':
        kb = 
        [
            ('NOT', 'P11'),
            ('NOT', 'W11'),
            ('NOT', 'B11'),
            ('NOT', 'S11'),
            ('IFF', 'BII', ('OR', 'P12', 'P21'))

        ]
        query = 'P21'
        player = player(kb = kb)
        