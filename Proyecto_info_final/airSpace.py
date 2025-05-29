from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.navPoints = {}
        self.segments = []
        self.airports = {}

    def load_points(self, filename, color='blue'):
        print(f"Cargando puntos desde: {filename}")
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number, name, lat, lon = parts[0], parts[1], parts[2], parts[3]
                    navpoint = NavPoint(number, name, lat, lon)
                    navpoint.color = color  # For KML styling
                    self.navPoints[int(number)] = navpoint
        print(f"Cargados {len(self.navPoints)} NavPoints")

    def load_segments(self, filename):
        print(f"Cargando segmentos desde: {filename}")
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    origin, dest, dist = parts[0], parts[1], parts[2]
                    self.segments.append(NavSegment(origin, dest, dist))
        print(f"Cargados {len(self.segments)} segmentos")

    def load_airports(self, filename):
        print(f"Cargando aeropuertos desde: {filename}")
        with open(filename, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or not line.endswith('.A'):
                continue  # Ignora las listas que no sean aeropuertos

            airport_code = line[:-2]  #Quita la A   
            navpoint = self.get_navpoint_by_name(airport_code)
            if navpoint:
                airport_id = navpoint.number
                airport = NavAirport(airport_code)
                self.airports[airport_id] = airport
                navpoint.name = airport_code  # Label navpoint with the 3-letter airport code
                navpoint.color = 'red'
                print(f"✓ Aeropuerto registrado: {airport_code} (ID {airport_id})")
            else:
                print(f"⚠️ Punto de aeropuerto '{airport_code}' no encontrado en navPoints")

        print(f"Total aeropuertos cargados: {len(self.airports)}")

    def get_neighbors(self, point_id):
        neighbors = []
        for seg in self.segments:
            if seg.origin_number == point_id:
                neighbors.append(seg.destination_number)
        return neighbors

    def get_navpoint_by_name(self, name):
        for p in self.navPoints.values():
            if p.name.startswith(name):  # matches BZR, BZR.A, etc.
             return p
        return None
