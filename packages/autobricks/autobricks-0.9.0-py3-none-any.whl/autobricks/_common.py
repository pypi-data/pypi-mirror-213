from enum import Enum
from io import TextIOWrapper
import os
from typing import Union, List
import yaml
import json


class MetadataFormat(Enum):
    yaml = "yaml"
    json = "json"


def get_metadata_format(filename: str):
    """
    filename:str name of the file with the extension

    determines the supported format of the metadata files.
    """
    _, ext = os.path.splitext(filename)
    try:
        ext = MetadataFormat(ext[1:])
        return ext
    except Exception:
        return None


def load_format(f: TextIOWrapper, format: MetadataFormat):
    """
    f: TextIOWrapper        file stream from an open command
    format: MetadataFormat  metadata format

    reads the filestream using the correct library to parse the file format type
    """
    if format == MetadataFormat.yaml:
        data = yaml.safe_load(f)
    elif format == MetadataFormat.json:
        data = json.load(f)
    return data


def tags_exist_in(tags: Union[str, List[str], None], in_tags: List[str]):
    """
    tags: Union[str, List[str], None]   Tags that want to check are in the superset list. If there are no tags returns true
    in_tags: List[str]                  The target superset of tags you want to check if the tags are in

    This is a utility function to check is a set of tags are in a superset of tags.
    If the tags are none then it assumes that no tag filtered is being applied and
    therefore returns true.
    """
    if isinstance(tags, str):
        return tags in in_tags
    elif isinstance(tags, list):
        return set(tags).issubset(set(in_tags))
    else:
        return True
