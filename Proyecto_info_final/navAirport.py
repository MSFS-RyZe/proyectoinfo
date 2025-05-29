class NavAirport: #Esta clase representa un aeropuerto (SID: Salida, STAR: Llegada)
    def __init__(self, name):
        self.name = name #Nombre del aeropuerto
        self.SIDs = [] #Lista de puntos de salida
        self.STARs = [] #Lista de puntos de llegada

    def add_sid(self, navpoint): #Agrega un punto de salida
        self.SIDs.append(navpoint)

    def add_star(self, navpoint): #Agrega un punto de llegada, en formato NavPoint
        self.STARs.append(navpoint)

    def __repr__(self): #Cuando se imprime el aeropuerto, aparece una lista con el número de rutas de salida y de llegada. 
        return f"NavAirport({self.name}, SIDs: {len(self.SIDs)}, STARs: {len(self.STARs)})"
