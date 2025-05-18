from navPoint import *
from navSegment import *
from navAirport import *

class AirSpace:
    def __init__(self):
        self.navPoints = {}
        self.navSegments = []
        self.navAirports = {}

    def load_points(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number, name, lat, lon = parts[0], parts[1], parts[2], parts[3]
                    self.navPoints[int(number)] = NavPoint(number, name, lat, lon)

    def load_segments(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    origin, dest, dist = parts[0], parts[1], parts[2]
                    self.navSegments.append(NavSegment(origin, dest, dist))

    def load_airports(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    name, type_, point_id = parts[0], parts[1], int(parts[2])
                    if name not in self.navAirports:
                        self.navAirports[name] = NavAirport(name)
                    if point_id in self.navPoints:
                        point = self.navPoints[point_id]
                        if 'SID' in type_ or type_.endswith('.D'):
                            self.navAirports[name].add_sid(point)
                        elif 'STAR' in type_ or type_.endswith('.A'):
                            self.navAirports[name].add_star(point)

    def get_neighbors(self, point_id):
        neighbors = []
        for seg in self.navSegments:
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
    for navpoint in airspace.navPoints.values():
        plt.plot(navpoint.longitude, navpoint.latitude, 'o', color='gray')
        plt.text(navpoint.longitude + 0.02, navpoint.latitude + 0.02, navpoint.name, fontsize=8)

    for segment in airspace.navSegments:
        origin = airspace.navPoints.get(segment.origin_number)
        dest = airspace.navPoints.get(segment.destination_number)
        if origin and dest:
            x = [origin.longitude, dest.longitude]
            y = [origin.latitude, dest.latitude]
            plt.plot(x, y, 'black', linewidth=1)
            mid_x = (x[0] + x[1]) / 2
            mid_y = (y[0] + y[1]) / 2
            plt.text(mid_x, mid_y, f"{segment.distance:.1f}", fontsize=7, color='red')

    plt.title("AirSpace Navigation Map")
    plt.axis('equal')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()
