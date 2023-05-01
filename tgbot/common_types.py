from strenum import StrEnum
from typing import TypedDict, Optional, Dict, Any


class FileTypes(StrEnum):
    Photo = "photo"
    Video = "video"
    Document = "document"


class File(TypedDict):
    file_id: str
    file: FileTypes


def convert_file_to_dict(file: File) -> Dict[str, str]:
    return {
        "file_id": file['file_id'],
        "file": file['file'].value
    }


def convert_dict_to_file(d: Dict[str, str]) -> File:
    return File(
        file_id=d['file_id'],
        file=FileTypes(d['file'])
    )