# ![GeoVisio](https://gitlab.com/geovisio/api/-/raw/develop/images/logo_full.png)

__GeoVisio__ is a complete solution for storing and __serving your own 📍📷 geolocated pictures__ (like [StreetView](https://www.google.com/streetview/) / [Mapillary](https://mapillary.com/)).

➡️ __Give it a try__ at [panoramax.ign.fr](https://panoramax.ign.fr/) or [geovisio.fr](https://geovisio.fr/viewer) !

## 📦 Components

GeoVisio is __modular__ and made of several components, each of them standardized and ♻️ replaceable.

![GeoVisio architecture](https://gitlab.com/geovisio/api/-/raw/develop/images/big_picture.png)

All of them are 📖 __open-source__ and available online:

|                               🌐 Server                                 |                      💻 Client                       |
|:-----------------------------------------------------------------------:|:----------------------------------------------------:|
|                 [API](https://gitlab.com/geovisio/api)                  |    [Website](https://gitlab.com/geovisio/website)    |
|            [Blur API](https://gitlab.com/geovisio/blurring)             | [Web viewer](https://gitlab.com/geovisio/web-viewer) |
| [GeoPic Tag Reader](https://gitlab.com/geovisio/geo-picture-tag-reader) |   [Command line](https://gitlab.com/geovisio/cli)    |


# 📷 GeoPic Tag Reader

This repository only contains the Python library to __extract standardized metadata__ from geolocated pictures EXIF metadata.

## Features

This tool allows you to:

- Analyse various EXIF variables to extract standardized metadata for geolocated pictures applications


## Install

GeoPicTagReader can be installed using two methods:

- From [PyPI](https://pypi.org/project/geopic-tag-reader/), the Python central package repository
- Using this [Git repository](https://gitlab.com/geovisio/geo-picture-tag-reader)

### From PyPI

Just launch this command:

```bash
pip install geopic_tag_reader
```

After this you should be able to use the CLI tool with the name `geopic-tag-reader`:

```bash
geopic-tag-reader --help
```

Alternatively, you can use [pipx](https://github.com/pypa/pipx) if you want all the script dependencies to be in a custom virtual env.

You need to [install pipx](https://pypa.github.io/pipx/installation/), then:

```bash
pipx install geopic_tag_reader
```

### From Git repository

Download the repository:

```bash
git clone https://gitlab.com/geovisio/geo-picture-tag-reader.git geopic_tag_reader
cd geopic_tag_reader/
```

To avoid conflicts, it's considered a good practice to create a _[virtual environment](https://docs.python.org/3/library/venv.html)_ (or virtualenv). To do so, launch the following commands:

```bash
# Create the virtual environment in a folder named "env"
python3 -m venv env

# Launches utilities to make environment available in your Bash
source ./env/bin/activate
```

Then, install the dependencies using pip:

```bash
pip install -e .
```

You can also install the `dev` dependencies if necessary (to have lints, format, tests, ...):

```bash
pip install -e .[dev]
```

Then, you can use the `geopic-tag-reader` command:
```bash
geopic-tag-reader --help
```


## Usage

This library can be used both from command-line or as Python module.

### As command-line

To see all available commands:

```bash
geopic-tag-reader --help
```

[Full documentation is also available here](./docs/CLI_USAGE.md).

### As Python library

In your own script, you can use:

```python
from geopic_tag_reader import reader
from PIL import Image

# Open an image with Pillow
img = Image.open("my_picture.jpg")

# Read EXIF metadata
metadata = reader.readPictureMetadata(img)

# Print results
print(metadata)
```

[Full documentation is also available here](./docs/API_USAGE.md).


## Development

### Tests

Tests are run using PyTest. You can simply run this command to launch tests:

```bash
pytest
```

### Documentation

High-level documentation is handled by [Typer](https://typer.tiangolo.com/). You can update the generated `USAGE.md` file using this command:

```bash
make docs
```

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Note that before opening a pull requests, you may want to check formatting and tests of your changes:

```bash
make ci
```

### Make a release

```bash
git checkout main
git pull

make docs ci
vim CHANGELOG.md							# Edit version + links at bottom
vim geopic_tag_reader/__init__.py	# Edit version

git add *
git commit -m "Release x.x.x"
git tag -a x.x.x -m "Release x.x.x"
git push origin main --tags
```



## 🤗 Special thanks

![Sponsors](https://gitlab.com/geovisio/api/-/raw/develop/images/sponsors.png)

GeoVisio was made possible thanks to a group of ✨ __amazing__ people ✨ :

- __[GéoVélo](https://geovelo.fr/)__ team, for 💶 funding initial development and for 🔍 testing/improving software
- __[Carto Cité](https://cartocite.fr/)__ team (in particular Antoine Riche), for 💶 funding improvements on viewer (map browser, flat pictures support)
- __[La Fabrique des Géocommuns (IGN)](https://www.ign.fr/institut/la-fabrique-des-geocommuns-incubateur-de-communs-lign)__ for offering long-term support and funding the [Panoramax](https://panoramax.fr/) initiative and core team (Camille Salou, Mathilde Ferrey, Christian Quest, Antoine Desbordes, Jean Andreani, Adrien Pavie)
- Many _many_ __wonderful people__ who worked on various parts of GeoVisio or core dependencies we use : 🧙 Stéphane Péneau, 🎚 Albin Calais & Cyrille Giquello, 📷 [Damien Sorel](https://www.strangeplanet.fr/), Pascal Rhod, Nick Whitelegg...
- __[Adrien Pavie](https://pavie.info/)__, for ⚙️ initial development of GeoVisio
- And you all ✨ __GeoVisio users__ for making this project useful !


## ⚖️ License

Copyright (c) GeoVisio team 2022-2023, [released under MIT license](https://gitlab.com/geovisio/geo-picture-tag-reader/-/blob/main/LICENSE).
