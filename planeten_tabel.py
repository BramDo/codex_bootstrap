import xml.etree.ElementTree as ET
import urllib.request
import gzip
import io

URL = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"


def fetch_planets(limit=10, url=URL):
    """Download and parse planet data from the Open Exoplanet Catalogue."""
    with urllib.request.urlopen(url) as response:
        data = response.read()
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
        tree = ET.parse(gz)

    planets = []
    for planet in tree.findall(".//planet")[:limit]:
        name = planet.findtext("name")
        mass = planet.findtext("mass")
        radius = planet.findtext("radius")
        planets.append((name, mass, radius))
    return planets


def print_table(rows):
    """Print rows as a simple table."""
    headers = ["Name", "Mass", "Radius"]
    data = [headers] + [list(r) for r in rows]
    widths = [max(len(str(row[i] or "")) for row in data) for i in range(3)]

    header_line = " | ".join(headers[i].ljust(widths[i]) for i in range(3))
    separator = "-+-".join("-" * widths[i] for i in range(3))
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join((str(row[i] or "").ljust(widths[i]) for i in range(3))))


def main():
    planets = fetch_planets()
    print_table(planets)


if __name__ == "__main__":
    main()
