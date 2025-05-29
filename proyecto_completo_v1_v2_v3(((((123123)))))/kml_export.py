from tkinter import messagebox, filedialog

def generate_kml_header(): # Genera el encabezado del KML ajustando los colores de los iconos
    return '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
<Style id="blue"><IconStyle><color>ff0000ff</color><scale>1.2</scale></IconStyle></Style>
<Style id="green"><IconStyle><color>ff00ff00</color><scale>1.2</scale></IconStyle></Style>
<Style id="red"><IconStyle><color>ff0000aa</color><scale>1.2</scale></IconStyle></Style>
<Style id="airport">
  <IconStyle>
    <scale>1.5</scale>
    <Icon>
      <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
    </Icon>
  </IconStyle>
</Style>
'''

def generate_kml_footer(): # Genera el pie del KML
    return '''</Document>
</kml>'''

def kml_placemark_point(name, lon, lat, style_id=None): # Genera un punto en el KML
    style_tag = f"<styleUrl>#{style_id}</styleUrl>" if style_id else "" # Si se proporciona un estilo, se añade al punto
    return f'''
<Placemark>
    <name>{name}</name> # Nombre del punto
    {style_tag} # Estilo del punto
    <Point>
        <coordinates>{lon},{lat},0</coordinates> # Coordenadas del punto
    </Point>
</Placemark>
'''

def kml_placemark_path(name, coords): # Genera una ruta en el KML
    coord_text = ' '.join([f"{lon},{lat},0" for lon, lat in coords]) # Formatea las coordenadas de la ruta
    return f'''
<Placemark>
    <name>{name}</name> # Nombre de la ruta
    <LineString> # Genera una línea en el KML
        <coordinates>{coord_text}</coordinates> # Coordenadas de la ruta
    </LineString>
</Placemark>
'''

def export_airspace_to_kml(airspace, filename): # Exporta el espacio aéreo a un archivo KML
    with open(filename, 'w', encoding='utf-8') as f: # Abre el archivo para escribir
        f.write(generate_kml_header()) # Escribe el encabezado del KML

        for navpoint in airspace.navPoints.values(): # Recorre todos los puntos de navegación
            if navpoint.number in airspace.airports: # Si el punto es un aeropuerto
                f.write(kml_placemark_point(f"✈ {navpoint.name}", navpoint.longitude, navpoint.latitude, "airport")) # Añade el estilo de aeropuerto
            else:
                style = getattr(navpoint, 'color', 'blue') # Obtiene el color del punto, por defecto azul
                f.write(kml_placemark_point(navpoint.name, navpoint.longitude, navpoint.latitude, style))

        # Exportar segmentos
        for seg in airspace.segments: # Recorre todos los segmentos
            origin = airspace.navPoints.get(seg.origin_number)
            dest = airspace.navPoints.get(seg.destination_number)
            if origin and dest: # Si ambos puntos existen
                coords = [(origin.longitude, origin.latitude), (dest.longitude, dest.latitude)] # Formatea las coordenadas del segmento
                f.write(kml_placemark_path(f"{origin.name}-{dest.name}", coords))

        f.write(generate_kml_footer()) # Escribe el pie del KML

def export_path_to_kml(path, filename): # Exporta un camino a un archivo KML
    with open(filename, 'w', encoding='utf-8') as f: # Abre el archivo para escribir
        f.write(generate_kml_header()) # Escribe el encabezado del KML

        # Exportar todos los nodos del path
        for node in path.nodes:
            f.write(kml_placemark_point(node.name, node.x, node.y, "green"))

        # Exportar el path como una linea
        coords = [(node.x, node.y) for node in path.nodes]
        f.write(kml_placemark_path("Ruta", coords))

        f.write(generate_kml_footer()) # Escribe el pie del KML
