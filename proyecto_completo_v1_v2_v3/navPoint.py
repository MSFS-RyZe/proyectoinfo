class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = int(number)
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        
        # Compatibilidad con el sistema de grafos
        self.x = self.longitude
        self.y = self.latitude
        self.neighbors = []

    def __repr__(self):
        return f"NavPoint({self.number}, {self.name}, {self.latitude}, {self.longitude})"

    def __eq__(self, other):
        if isinstance(other, NavPoint):
            return self.number == other.number
        return False

    def __hash__(self):
        return hash(self.number)
