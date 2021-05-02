import os, sys
import dash
import dash_bootstrap_components as dbc
from flask_caching import Cache

crntPath = os.path.dirname(__file__)
sys.path.insert(1, os.path.join(crntPath))

# Definition

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.MINTY],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.8, maximum-scale=1.3, minimum-scale=0.5,'}],

                )
server = app.server
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))

app.title = "Hawzen"
app.config.suppress_callback_exceptions = True


CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': os.path.join(crntPath, "data2", "cache")
}
server.config.from_mapping(CACHE_CONFIG)
cache = Cache(server)
