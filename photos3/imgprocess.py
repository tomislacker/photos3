"""
photos3.imgprocess
==================
Contains code for processing images
"""
import os
import tempfile

from PIL import Image
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

from photos3.model import ImageMetaData


def get_image_data(img):
    """
    Returns basic information and exif data

    :param img: PIL image
    :returns: Tuple of basic info and exif info
    :rtype: tuple
    """
    basicdata = {
        k: v
        for k, v in img.info.items()
        if k != 'exif'
    }

    exifdata = {}
    try:
        # Read exif data from image, if available
        raw_exif = img._getexif()

        # Convert tag codes into named values
        exifdata = {
            TAGS.get(tag, tag): str(val).strip()
            for tag, val in raw_exif.items()
        }

    except AttributeError:
        print("WARNING: File ({t}) '{f}' does not have EXIF data".format(
            t=img.__class__.__name__,
            f=file_path))

    return basicdata, exifdata


def _get_image_from_s3(s3_object):
    """
    Downloads & returns a temporary file and PIL image

    :param s3_object: New photo in S3
    :type s3_object: boto3.resources.factory.s3.Object
    :returns: Tuple of tmp_filename and PIL Image
    """
    # Download S3 object to temporary file
    _, file_extension = os.path.splitext(s3_object.key)
    tmp_file, tmp_filename = tempfile.mkstemp(suffix=file_extension)
    s3_object.download_file(tmp_filename)

    # Open the image
    img = Image.open(tmp_filename)

    return tmp_filename, img


def ingest_image(s3_object):
    """
    Handles new image ingestion

    :param s3_object: New photo in S3
    :type s3_object: boto3.resources.factory.s3.Object
    :returns: DynamoDB entry for new metadata
    :rtype: photos3.model.ImageMetaData
    """
    tmp_filename, img = _get_image_from_s3(s3_object)

    # Read all metadata from the file
    basicdata, exifdata = get_image_data(img)

    # Remove the image
    try:
        os.remove(tmp_filename)
    except Exception:
        # Ignore the inability to remove the file
        pass

    # Save entry to the database
    image_entry = ImageMetaData(s3_object.key)
    image_entry.info = basicdata
    image_entry.exif = exifdata
    image_entry.save()

    return image_entry


def create_thumbnail(s3_object, width, height):
    """
    Creates a thumbnail image

    :param s3_object: New photo in S3
    :type s3_object: boto3.resources.factory.s3.Object
    :param width: Maximum width
    :type width: int
    :param height: Maximum height
    :type height: int
    """
    tmp_filename, img = _get_image_from_s3(s3_object)

    try:
        os.remove(tmp_filename)
    except Exception:
        # Ignore the inability to remove the file
        pass

    # Perform thumbnail creation and re-save file
    img.thumbnail([width, height], Image.ANTIALIAS)
    img.save(tmp_filename)

    # Push the thumbnail into S3
    s3_thumbnail = s3_object.Bucket().Object("thumbnail/{x}x{y}/{f}".format(
        x=width,
        y=height,
        f=os.path.basename(s3_object.key)))

    s3_thumbnail.upload_file(tmp_filename)
