<!-- markdownlint-disable -->

# API Overview

## Modules

- [`reader`](./reader.md#module-reader)

## Classes

- [`reader.GeoPicTags`](./reader.md#class-geopictags): Tags associated to a geolocated picture
- [`reader.PartialExifException`](./reader.md#class-partialexifexception): Exception for partial / missing EXIF information from image

## Functions

- [`reader.decodeMakeModel`](./reader.md#function-decodemakemodel): Python 2/3 compatible decoding of make/model field.
- [`reader.isExifTagUsable`](./reader.md#function-isexiftagusable): Is a given EXIF tag usable (not null and not an empty string)
- [`reader.readPictureMetadata`](./reader.md#function-readpicturemetadata): Extracts metadata from picture file


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
