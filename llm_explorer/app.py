import os

import streamlit
import streamlit.web.bootstrap
from streamlit import config as _config

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "__init__.py")

_config.set_option("server.headless", True)
args = []

def main():
    streamlit.web.bootstrap.run(filename, "", args, flag_options={})