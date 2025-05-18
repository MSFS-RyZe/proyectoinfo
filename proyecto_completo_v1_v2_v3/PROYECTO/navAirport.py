class NavAirport:
    def __init__(self, name):
        self.name = name
        self.SIDs = []
        self.STARs = []

    def add_sid(self, navpoint):
        self.SIDs.append(navpoint)

    def add_star(self, navpoint):
        self.STARs.append(navpoint)

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs: {len(self.SIDs)}, STARs: {len(self.STARs)})"
