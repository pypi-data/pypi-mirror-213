# scui
Demo static svelte UI distributed as a python package.


## UI
Minimal svelte demo app from `npm create svelte@latest`.

- Uses [static adapter](https://kit.svelte.dev/docs/adapter-static#usage)
- Does not include the usual svelte demo sverdle game (which requires a server)


```sh
cd ui
npm install

# dev server - type 'o' to open browser on http://localhost:5173
npm run dev

# build into build directory
npm run build
```

## pip installable scui package
This package includes a static web server and a bundle with the svelte UI build.

```sh
pip install scui
scui
```

### To rebuild and publish the scui package
This assumes that access to pypi.org has been configured.  
First npm install and npm build the svelte UI (see above)

```sh
pip install build twine
python -m build
python -m twine upload dist/*
````