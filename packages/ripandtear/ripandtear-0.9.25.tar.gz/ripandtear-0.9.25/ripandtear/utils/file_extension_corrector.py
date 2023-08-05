import magic
import logging

from pathlib import Path

log = logging.getLogger(__name__)


def check_extension(file_path):

    log.info("checking for correct file extension")

    file = Path(file_path)

    log.debug(f"filename extension: {file.suffix}")

    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)
    log.debug(mime_type)

    correct_file_extension = find_extension(mime_type)

    log.debug(f"correct file extension: {correct_file_extension}")

    if file.suffix == f".{correct_file_extension}":
        log.info("extensions match")
        return

    log.info("extensions dont match")
    file.rename(file.with_suffix(f".{correct_file_extension}"))
    log.info("extension changed")


def find_extension(extension: str) -> str:

    if extension in MIME_TYPES:
        return MIME_TYPES[extension]

    elif extension in MIME_TYPES.values():
        return extension

    else:
        return '???'


MIME_TYPES = {
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/x-bmp": "bmp",
    "image/x-ms-bmp": "bmp",
    "image/webp": "webp",
    "image/avif": "avif",
    "image/svg+xml": "svg",
    "image/ico": "ico",
    "image/icon": "ico",
    "image/x-icon": "ico",
    "image/vnd.microsoft.icon": "ico",
    "image/x-photoshop": "psd",
    "application/x-photoshop": "psd",
    "image/vnd.adobe.photoshop": "psd",

    "video/webm": "webm",
    "video/ogg": "ogg",
    "video/mp4": "mp4",
    "video/MP2T": "ts",
    "video/mp2t": "ts",
    "video/x-m4v": "mp4",
    "video/x-matroska": "mkv",
    "video/x-ms-asf": "wmv",
    "video/x-msvideo": "avi",
    "video/x-flv": "flv",
    "video/quicktime": "mov",
    "video/x-wav": "wav",

    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/mpeg": "mp3",
    "audio/x-m4a": "m4a",
    "audio/mpeg": "mp3",

    "application/zip": "zip",
    "application/x-zip": "zip",
    "application/x-zip-compressed": "zip",
    "application/rar": "rar",
    "application/x-rar": "rar",
    "application/x-rar-compressed": "rar",
    "application/x-7z-compressed": "7z",

    "application/pdf": "pdf",
    "application/x-pdf": "pdf",
    "application/x-shockwave-flash": "swf",

    "application/ogg": "ogg",
    # https://www.iana.org/assignments/media-types/model/obj
    "model/obj": "obj",
    "application/octet-stream": "bin",
    "text/html": "html",
    "text/plain": "txt"


}
