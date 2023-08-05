"""Demo static svelte UI distributed as a python package."""

__version__ = '0.0.2'

import os
import webbrowser
from aiohttp import web

def scui():
    """
    Run the scui web server and serve the scui UI.
    """
    app = web.Application()
    app.router.add_get('/', lambda _: web.HTTPFound('/index.html'))
    app.router.add_static('/', os.path.dirname(__file__) + '/dist')
    print(f'Starting scui web server from {os.path.dirname(__file__)}/dist')
    webbrowser.open('http://localhost:8080')
    web.run_app(app)

def main():
    scui()

if __name__ == '__main__':
    main()
