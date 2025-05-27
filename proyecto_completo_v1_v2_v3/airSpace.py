from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.navPoints = {}
        self.segments = []
        self.airports = {}

    def load_points(self, filename):
        print(f"Cargando puntos desde: {filename}")
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number, name, lat, lon = parts[0], parts[1], parts[2], parts[3]
                    self.navPoints[int(number)] = NavPoint(number, name, lat, lon)
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
        
        current_airport = None
        airport_counter = 1  # Contador simple para IDs
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Si es un código ICAO de aeropuerto (4 letras que empiezan por L)
            if len(line) == 4 and line.startswith('L'):
                current_airport = line
                
                # Buscar un NavPoint que pueda estar relacionado con este aeropuerto
                # Usar el primer NavPoint disponible como referencia
                if self.navPoints:
                    # Usar el ID del primer NavPoint como base + contador
                    first_nav_id = list(self.navPoints.keys())[0]
                    airport_id = first_nav_id + airport_counter * 10000
                else:
                    airport_id = airport_counter
                
                self.airports[airport_id] = NavAirport(current_airport)
                airport_counter += 1
                print(f"Aeropuerto creado: {current_airport} con ID {airport_id}")
                
            # Si es un procedimiento SID/STAR (termina en .D o .A)
            elif line.endswith('.D') or line.endswith('.A'):
                if current_airport:
                    # Buscar el NavPoint correspondiente
                    base_name = line.replace('.D', '').replace('.A', '')
                    for nav_id, nav_point in self.navPoints.items():
                        if nav_point.name == base_name:
                            # Encontrar el aeropuerto correspondiente
                            for airport_id, airport in self.airports.items():
                                if airport.name == current_airport:
                                    if line.endswith('.D'):
                                        airport.add_sid(nav_point)
                                        print(f"SID añadido: {line} al aeropuerto {current_airport}")
                                    elif line.endswith('.A'):
                                        airport.add_star(nav_point)
                                        print(f"STAR añadido: {line} al aeropuerto {current_airport}")
                                    break
                            break
            
            # Si es "VGO VON" (caso especial)
            elif line == "VGO VON":
                print(f"Elemento especial ignorado: {line}")
                current_airport = None
            
            # Otros elementos no reconocidos
            else:
                print(f"Elemento ignorado: {line}")
                current_airport = None
        
        print(f"Total aeropuertos cargados: {len(self.airports)}")

    def get_neighbors(self, point_id):
        neighbors = []
        for seg in self.segments:
            if seg.origin_number == point_id:
                neighbors.append(seg.destination_number)
        return neighbors

    def get_navpoint_by_name(self, name):
        for p in self.navPoints.values():
            if p.name == name:
                return p
        return None

def PlotAirSpace(airspace):
    import matplotlib.pyplot as plt
    
    # Dibujar NavPoints
    for navpoint in airspace.navPoints.values():
        plt.plot(navpoint.longitude, navpoint.latitude, 'o', color='blue', markersize=3)
        plt.text(navpoint.longitude + 0.02, navpoint.latitude + 0.02, navpoint.name, fontsize=6)

    # Dibujar aeropuertos usando una estrategia diferente
    for airport_id, airport in airspace.airports.items():
        # Buscar NavPoints que contengan el código del aeropuerto
        airport_code = airport.name[:3]  # Primeras 3 letras del código ICAO
        
        for nav_id, nav_point in airspace.navPoints.items():
            if airport_code in nav_point.name or nav_point.name.startswith(airport_code):
                plt.plot(nav_point.longitude, nav_point.latitude, 's', color='red', markersize=8)
                plt.text(nav_point.longitude + 0.02, nav_point.latitude + 0.02, 
                        airport.name, fontsize=8, fontweight='bold', color='red')
                break  # Solo mostrar el primer match

    # Dibujar segmentos
    for segment in airspace.segments:
        origin = airspace.navPoints.get(segment.origin_number)
        dest = airspace.navPoints.get(segment.destination_number)
        if origin and dest:
            x = [origin.longitude, dest.longitude]
            y = [origin.latitude, dest.latitude]
            plt.plot(x, y, 'gray', linewidth=0.5, alpha=0.7)

    plt.title("AirSpace Navigation Map")
    plt.axis('equal')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
