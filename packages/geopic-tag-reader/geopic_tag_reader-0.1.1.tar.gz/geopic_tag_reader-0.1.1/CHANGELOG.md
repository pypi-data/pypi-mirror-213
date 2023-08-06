# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.1.1]

### Added
- Support of Mapillary tags stored in EXIF tag `ImageDescription`


## [0.1.0]

### Added
- If GPS Date or time can't be read, fallbacks to Original Date EXIF tag associated with a reader warning
- New EXIF tags are supported: `GPSDateTime`

### Changed
- `tag_reader:warning` property has been moved from EXIF, and is now available as a direct property named `tagreader_warnings` of `GeoPicTags` class
- Reader now supports `GPSLatitude` and `GPSLongitude` stored as decimal values instead of tuple
- Reader now supports reading `FocalLength` written in `NUMBER/NUMBER` format
- If EXIF tags for heading `PoseHeadingDegrees` and `GPSImgDirection` have contradicting values, we use by default `GPSImgDirection` value and issue a warning, instead of raising an error

### Fixed
- EXIF tag `SubsecTimeOriginal` was not correctly read due to a typo


## [0.0.2] - 2023-05-10

### Added
- EXIF tag `UserComment` is now read and available in raw `exif` tags
- If not set, `GPSLatitudeRef` defaults to North and `GPSLongitudeRef` defaults to East
- A new `tag_reader:warning` property lists non-blocking warnings raised while reading EXIF tags


## [0.0.1] - 2023-03-31

### Added
- EXIF tag reading methods extracted from [GeoVisio API](https://gitlab.com/geovisio/api)


[Unreleased]: https://gitlab.com/geovisio/geo-picture-tag-reader/-/compare/0.1.1...main
[0.1.1]: https://gitlab.com/geovisio/geo-picture-tag-reader/-/compare/0.1.0...0.1.1
[0.1.0]: https://gitlab.com/geovisio/geo-picture-tag-reader/-/compare/0.0.2...0.1.0
[0.0.2]: https://gitlab.com/geovisio/geo-picture-tag-reader/-/compare/0.0.1...0.0.2
[0.0.1]: https://gitlab.com/geovisio/geo-picture-tag-reader/-/commits/0.0.1
