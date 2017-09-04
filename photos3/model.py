"""
photos3.model
=============
Contains code for database models
"""
import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import JSONAttribute


class ImageMetaData(Model):
    class Meta:
        table_name = os.environ.get('META_TABLE')

    checksum = UnicodeAttribute(hash_key=True)
    exif = JSONAttribute()
    info = JSONAttribute()
