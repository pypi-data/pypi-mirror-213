import os
import pytest
from PIL import Image
from geopic_tag_reader import reader

FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fixtures")


def assertGeoPicTagsEquals(gpt, expectedDict):
    assert gpt.lat == expectedDict.get("lat")
    assert gpt.lon == expectedDict.get("lon")
    assert gpt.ts == expectedDict.get("ts")
    assert gpt.heading == expectedDict.get("heading")
    assert gpt.type == expectedDict.get("type")
    assert gpt.make == expectedDict.get("make")
    assert gpt.model == expectedDict.get("model")
    assert gpt.focal_length == expectedDict.get("focal_length")
    assert gpt.tagreader_warnings == expectedDict.get("tagreader_warnings", [])
    assert len(gpt.exif) > 0


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "1.jpg"))
def test_readPictureMetadata(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 49.00688961988304,
            "lon": 1.9191854417991367,
            "ts": 1627550214.0,
            "heading": 349,
            "type": "equirectangular",
            "make": "GoPro",
            "model": "Max",
            "focal_length": 3,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "a1.jpg"))
def test_readPictureMetadata_negCoords(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/a1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 48.33756428166505,
            "lon": -1.9331088333333333,
            "ts": 1652453580.0,
            "heading": 32,
            "type": "equirectangular",
            "make": "GoPro",
            "model": "Max",
            "focal_length": 3,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "b1.jpg"))
def test_readPictureMetadata_flat(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/b1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 48.139852239480945,
            "lon": -1.9499731060073981,
            "ts": 1429976268.0,
            "heading": 155,
            "type": "flat",
            "make": "OLYMPUS IMAGING CORP.",
            "model": "SP-720UZ",
            "focal_length": 4.66,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "c1.jpg"))
def test_readPictureMetadata_flat2(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/c1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 48.85779642035038,
            "lon": 2.3392783047650747,
            "ts": 1430744932.0,
            "heading": 302,
            "type": "flat",
            "make": "Canon",
            "model": "EOS 6D0",
            "focal_length": 35.0,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "d1.jpg"))
def test_readPictureMetadata_xmpHeading(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/d1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 50.87070833333333,
            "lon": -1.5260916666666666,
            "ts": 1600008019.767,
            "heading": 67,
            "type": "equirectangular",
            "make": "Google",
            "model": "Pixel 3",
            "focal_length": None,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "e1.jpg"))
def test_readPictureMetadata_noHeading(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/e1.jpg"))
    assertGeoPicTagsEquals(
        result,
        {
            "lat": 48.15506638888889,
            "lon": -1.6844680555555556,
            "ts": 1666166194.0,
            "heading": None,
            "type": "flat",
            "make": "SONY",
            "model": "FDR-X1000V",
            "focal_length": 2.8,
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_Ricoh_Theta.jpg"))
def test_readPictureMetadata_ricoh_theta(datafiles):
    for f in datafiles.listdir():
        result = reader.readPictureMetadata(Image.open(str(f)))
        assertGeoPicTagsEquals(
            result,
            {
                "focal_length": 0.75,
                "heading": 270,
                "lat": 48.83930905577957,
                "lon": 2.3205357914890987,
                "make": "RICOH",
                "model": "THETA m15",
                "ts": 1458911533.0,
                "type": "equirectangular",
            },
        )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_V4MPack.jpg"))
def test_readPictureMetadata_v4mpack(datafiles):
    for f in datafiles.listdir():
        result = reader.readPictureMetadata(Image.open(str(f)))
        assertGeoPicTagsEquals(
            result,
            {
                "focal_length": None,
                "heading": 64,
                "lat": 47.08506017299737,
                "lon": -1.2761512389983616,
                "make": "STFMANI",
                "model": "V4MPOD 1",
                "ts": 1555417213.0,
                "type": "equirectangular",
            },
        )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "IMG_20210720_161352.jpg"))
def test_readPictureMetadata_a5000(datafiles):
    result = reader.readPictureMetadata(
        Image.open(str(datafiles) + "/IMG_20210720_161352.jpg")
    )
    assertGeoPicTagsEquals(
        result,
        {
            "focal_length": 4.103,
            "heading": 355,
            "lat": 48.96280504578332,
            "lon": 2.51197323068765,
            "make": "OnePlus",
            "model": "ONEPLUS A5000",
            "ts": 1626797632.199995,
            "type": "flat",
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "IMG_20210720_144918.jpg"))
def test_readPictureMetadata_a5000_2(datafiles):
    with pytest.raises(reader.PartialExifException) as e_info:
        result = reader.readPictureMetadata(
            Image.open(str(datafiles) + "/IMG_20210720_144918.jpg")
        )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_V4MPack.jpg"))
def test_readPictureMetadata_comment(datafiles):
    result = reader.readPictureMetadata(Image.open(str(datafiles) + "/img_V4MPack.jpg"))
    assert result.exif["UserComment"] == b"DCIM\\627MEDIA"


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "int_long_tag.jpg"))
def test_readPictureMetadata_int_long_tag(datafiles):
    """
    int_long_tag.jpg has an invalid longituderef tag, it's '52227'
    But since the  longitude ref is optional (and default to E based on https://www.exiftool.org/geotag.html) we get a valid position
    """
    r = reader.readPictureMetadata(Image.open(str(datafiles) + "/int_long_tag.jpg"))
    assertGeoPicTagsEquals(
        r,
        {
            "focal_length": None,
            "heading": 255,
            "lat": 44.09732280555556,
            "lon": 4.700622,
            "make": None,
            "model": None,
            "ts": 1673515020.0,
            "type": "flat",
            "tagreader_warnings": [
                "GPSLongitudeRef not found, assuming GPSLongitudeRef is East"
            ],
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_invalid_gps_date.jpg"))
def test_readPictureMetadata_invalidGpsDate(datafiles):
    """
    Handles fallback to OriginalDate EXIF tag if GPS time is invalid
    """
    r = reader.readPictureMetadata(
        Image.open(str(datafiles) + "/img_invalid_gps_date.jpg")
    )
    assertGeoPicTagsEquals(
        r,
        {
            "focal_length": 4.2,
            "heading": 202,
            "lat": 48.88026828330809,
            "lon": 2.358506155368721,
            "make": "samsung",
            "model": "M-G930F",
            "ts": 1631101437.0754,
            "type": "flat",
            "tagreader_warnings": [
                "Skipping GPS date/time as it was not recognized:\n\tGPSTimeStamp and GPSDateTime don't contain supported time format"
            ],
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_gps_datestamp.jpg"))
def test_readPictureMetadata_gpsDateStamp(datafiles):
    result = reader.readPictureMetadata(
        Image.open(str(datafiles) + "/img_gps_datestamp.jpg")
    )
    assertGeoPicTagsEquals(
        result,
        {
            "focal_length": 4.2,
            "heading": 139,
            "lat": 48.803342005175907,
            "lon": 2.4833190643002672,
            "make": "Apple",
            "model": "iPhone 12 Pro",
            "ts": 1682785851.565,
            "type": "flat",
            "tagreader_warnings": [
                "Skipping GPS date/time as it was not recognized:\n\tGPSTimeStamp and GPSDateTime don't contain supported time format"
            ],
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_gps_date_string.jpg"))
def test_readPictureMetadata_gpsDateString(datafiles):
    result = reader.readPictureMetadata(
        Image.open(str(datafiles) + "/img_gps_date_string.jpg")
    )
    assertGeoPicTagsEquals(
        result,
        {
            "focal_length": 3.99,
            "heading": 182,
            "lat": 45.624742577465156,
            "lon": -1.001555796557295,
            "make": "Apple",
            "model": "iPhone 8 Plus",
            "ts": 1564313142.529,
            "type": "flat",
            "tagreader_warnings": [
                "Skipping GPS date/time as it was not recognized:\n\tGPSTimeStamp and GPSDateTime don't contain supported time format"
            ],
        },
    )


@pytest.mark.datafiles(os.path.join(FIXTURE_DIR, "img_categorisee.jpg"))
def test_readPictureMetadata_categories(datafiles):
    result = reader.readPictureMetadata(
        Image.open(str(datafiles) + "/img_categorisee.jpg")
    )
    assert "mediapro:CatalogSets" in result.exif
    assert "MicrosoftPhoto:LastKeywordXMP" in result.exif
    assert "acdsee:categories" in result.exif
