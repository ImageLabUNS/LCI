__version__ = "0.0.1"
__author__ = 'Laboratorio de ciencia de las imagenes - UNS'
__credits__ = 'UNS - CONICET'

# importen los paquetes necesarios para que las funciones funcionen

import LCI.pantos
import LCI.utils
import LCI.pfi


from glob import glob as gl # This list paths
try:
    import geopandas as gpd
except:
    LCI.utils.install_package(geopandas)
import pandas as pd
import plotly.graph_objects as go # https://plotly.com/python/
from PIL import Image
from glob import glob as gl

            