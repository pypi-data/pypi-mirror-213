"""Demo static svelte UI distributed as a python package."""

__version__ = '0.0.1'

from aiohttp import web
import webbrowser

def scui():
    """
    Run the scui web server and serve the scui UI.
    """
    app = web.Application()
    app.router.add_get('/', lambda _: web.HTTPFound('/index.html'))
    app.router.add_static('/', 'src/scui/dist')
    webbrowser.open('http://localhost:8080')
    web.run_app(app)

def main():
    scui()

if __name__ == '__main__':
    main()
