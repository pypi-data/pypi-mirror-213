import dataclasses
import os
import typing

from altcos import common


class Platform(common.StrEnum):
    QEMU = "qemu"
    METAL = "metal"


class Format(common.StrEnum):
    QCOW2 = "qcow2"
    ISO = "iso"
    RAW = "raw"


@dataclasses.dataclass
class Disk:
    location: str | os.PathLike
    signature: typing.Optional[str | os.PathLike]
    uncompressed: typing.Optional[str | os.PathLike]
    uncompressed_signature: typing.Optional[str | os.PathLike]


@dataclasses.dataclass
class Artifact:
    disk: typing.Optional[Disk]


ALLOWED_FORMATS = {
    Platform.QEMU: {
        Format.QCOW2,
    },
    Platform.METAL: {
        Format.ISO,
        Format.RAW,
    }
}
