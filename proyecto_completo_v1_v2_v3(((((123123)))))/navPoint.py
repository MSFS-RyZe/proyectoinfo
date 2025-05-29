class NavPoint:
    def __init__(self, id, name, latitude, longitude): #Se utiliza para clasificar y reconocer los puntos de los documentos especificados. ID es el número, Name es el nombre que se le da, y luego aparecen las coordenadas. 
        self.number = int(id)
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

    def __hash__(self): #Permite que los NavPoints se puedan utilizar en estructuras hash (Listas largas de documentos como la de las coordenadas de los Waypoints de Europa para el Airspace)
        return hash(self.number)