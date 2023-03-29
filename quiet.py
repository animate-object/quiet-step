from datetime import datetime
from typing import List, Tuple
import gpxpy
from gpxpy.gpx import GPX, GPXTrackPoint
from folium import Map, PolyLine
from enum import Enum

class Tileset:
    def __init__(self, name: str, url: str, attr: str):
        self.name = name
        self.url = url
        self.attr = attr

class Tilesets(Enum):
    VOYAGER = Tileset(
        name='CartoDB Voyager (No Labels)',
        url='https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    )
    DARK_MATTER = Tileset(
        name='CartoDB Dark Matter (No Labels)',
        url='https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    )
    POSITRON = Tileset(
        name='CartoDB Positron (No Labels)',
        url='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    )

Point = Tuple[float, float]


def parse_gpx_data(gpx_str: str) -> GPX:
    return gpxpy.parse(gpx_str)

def get_center_point(gpx: GPX) -> Point:
    bounds = gpx.get_bounds()
    return (
        (bounds.max_latitude + bounds.min_latitude) / 2,
        (bounds.max_longitude + bounds.min_longitude) / 2,
    )


def gpx_pt_to_pt(track_pt: GPXTrackPoint) -> Point:
    return track_pt.latitude, track_pt.longitude


def generate_map(center_point: Point, route: List[Point], tileset: Tileset,) -> str:
    map_ = Map(
        tiles=tileset.url,
        attr=tileset.attr,
        location=center_point,
        zoom_start=14,
    )
    route = PolyLine(
        locations=route,
        color="red",
        weight=10,
        opacity=1,
    )
    map_.add_child(route)
    return map_

def map_to_png(map_: Map) -> str:
    return map_._to_png(2)

def write_png_bytes(png_bytes: bytes, filename: str) -> None:
    with open(filename, "wb") as f:
        f.write(png_bytes)

def get_output_file_name(filename: str = 'map', timestamp: datetime = datetime.utcnow()) -> str:
    return f"{filename}-{timestamp.strftime('%Y-%m-%d-%H-%M-%S')}.png"

def generate(raw_gpx_str: str, **config_kwargs) -> str:
    tileset_name = config_kwargs.get("tileset", "DARK_MATTER")
    filename = config_kwargs.get("filename")
    output_file_name = get_output_file_name(filename)
    tileset = Tilesets[tileset_name]

    gpx = parse_gpx_data(raw_gpx_str)
    center_point = get_center_point(gpx)
    route = [gpx_pt_to_pt(track_pt) for track_pt in gpx.tracks[0].segments[0].points]
    map_ = generate_map(
        center_point,
        route,
        tileset=tileset.value,
    )
    png = map_to_png(map_)
    write_png_bytes(png, output_file_name)
