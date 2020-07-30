class Player :

    def __init__(self, id):
        self.id = id
        self.statistics = []
    
    def __repr__(self):
        return("Player of id " + str(self.id))