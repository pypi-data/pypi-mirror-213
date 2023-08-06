import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
import json


class util(object):
    def __init__(self):
        self.var = None

    def gdf_crs(self, gdf):
        b = gdf.total_bounds
        x = (b[0] + b[2]) / 2
        y = (b[1] + b[3]) / 2
        crs = '+proj=ortho +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0 +a=6371000 +b=6371000 +units=m +no_defs'.format(
            lat=x, lon=y)
        return crs

    def r_content_pretty(self, r):
        return json.dumps(json.loads(r.content), indent=4)

    def visualize(self, gdf):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_title("WGS84 (lat/lon)")
        gdf.plot(ax=ax, color='white', edgecolor='black')
        plt.show()

    def map(self, gdf, value=None, categorical=False):
        import folium
        if value is None:
            tooltip = ['gid', 'res', 'quad']
            column = None
            scheme = None
            style = {'stroke': True, 'color': 'black', 'weight': 1, 'opacity': 1.0, 'fill': True, 'fillOpacity': 0.0}
            highlight = {'fillOpacity': 0.3, 'fillColor': 'yellow'}
        elif value in gdf:
            tooltip = ['gid', 'res', 'quad', value]
            column = value
            scheme = 'naturalbreaks'
            style = {'stroke': True, 'color': 'black', 'weight': 1, 'opacity': 1.0, 'fill': True, 'fillOpacity': 0.6}
            highlight = {'fillOpacity': 0.9}
        else:
            logging.error('Value {x} not present in gdf'.format(x=value))

        m = gdf.explore(
            scheme=scheme,  # use mapclassify's natural breaks scheme
            legend=True,  # show legend
            k=10,  # use 10 bins
            legend_kwds=dict(colorbar=True),  # do not use colorbar
            name="DGGS",  # name of the layer in the map
            tooltip=tooltip,
            popup=tooltip,
            categorical=categorical,
            column=column,
            map_kwds={"scrollWheelZoom": False, "dragging": True},
            style_kwds=style,
            highlight_kwds=highlight
        )

        folium.TileLayer('cartodbdark_matter', control=True).add_to(m)  # use folium to add alternative tiles
        folium.LayerControl().add_to(m)  # use folium to add layer control

        return m

    
    def map2(self, gdf,value=None,categorical=False):
        import folium
        if value is None:
            tooltip = ['gid', 'res', 'quad']
            column = None
            scheme = None
            style = {'stroke': True, 'color': 'black', 'weight': 1, 'opacity': 1.0, 'fill': True, 'fillOpacity': 0.0}
            highlight = {'fillOpacity': 0.3, 'fillColor': 'yellow'}
        elif value in gdf:
            tooltip = ['gid', 'res', 'quad', value]
            column = value
            scheme = 'naturalbreaks'
            style = {'stroke': True, 'color': 'black', 'weight': 1, 'opacity': 1.0, 'fill': True, 'fillOpacity': 0.6}
            highlight = {'fillOpacity': 0.9}
        else:
            logging.error('Value {x} not present in gdf'.format(x=value))
        
        bbox=gdf.dissolve().bounds
        buildings = ox.geometries.geometries_from_bbox(bbox['miny'][0], bbox['maxy'][0], bbox['minx'][0], bbox['maxx'][0],tags = {'building': True})
        
        m = gdf.explore(
            scheme=scheme,  # use mapclassify's natural breaks scheme
            legend=True,  # show legend
            k=10,  # use 10 bins
            legend_kwds=dict(colorbar=True),  # do not use colorbar
            name="DGGS",  # name of the layer in the map
            tooltip=tooltip,
            popup=tooltip,
            categorical=categorical,
            column=column,
            map_kwds={"scrollWheelZoom": False, "dragging": True},
            style_kwds=style,
            highlight_kwds=highlight
        )

        folium.buildings.add_to(m)
        folium.TileLayer('cartodbdark_matter', control=True).add_to(m)  # use folium to add alternative tiles
        folium.LayerControl().add_to(m)  # use folium to add layer control
        
        return m
    
    def r_to_gdf(self, r, g='region'):
        logging.debug('Creating GeoDataFrame')
        if r.content is None:
            logging.error('No content in response')
            raise SystemExit(0)

        if g not in ['region', 'center']:
            logging.error('Unknown geometry, choose region or center')
            raise SystemExit(0)

        logging.debug('Convert response to DataFrame')
        df = pd.DataFrame.from_dict(r.json())

        logging.debug('Set geometry')
        df['geometry'] = df[g].apply(lambda x: shape(x))

        if 'properties' in df:
            logging.debug('Properties found')
            properties = pd.json_normalize(df['properties'])
            df = pd.concat([df[['gid', 'quad', 'res', 'geometry']], properties], axis=1)

        gdf = gpd.GeoDataFrame(df, geometry='geometry', crs=4326)

        return gdf