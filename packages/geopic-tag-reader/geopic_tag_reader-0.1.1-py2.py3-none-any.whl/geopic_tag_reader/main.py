import typer
from pathlib import Path
from geopic_tag_reader import reader
from PIL import Image

app = typer.Typer(help="GeoPicTagReader")


@app.command()
def read(
    image: Path = typer.Option(..., help="Path to your JPEG image file"),
):
    """Reads EXIF metadata from a picture file, and prints results"""

    img = Image.open(image)
    metadata = reader.readPictureMetadata(img)

    print("Latitude:", metadata.lat)
    print("Longitude:", metadata.lon)
    print("Timestamp:", metadata.ts)
    print("Heading:", metadata.heading)
    print("Type:", metadata.type)
    print("Make:", metadata.make)
    print("Model:", metadata.model)
    print("Focal length:", metadata.focal_length)

    if len(metadata.tagreader_warnings) > 0:
        print("Warnings raised by reader:")
        for w in metadata.tagreader_warnings:
            print(" - " + w)


if __name__ == "__main__":
    app()
