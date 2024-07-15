# It is hard to find a library to unpack *with permission*
# and securely

from pathlib import Path
from zipfile import ZipFile
import tarfile
from stat import S_IXUSR
import gzip, bz2
import io
from typing import AnyStr, cast, IO, TextIO, BinaryIO
from subprocess import check_output, STDOUT
import os

ZIP_UNIX_SYSTEM = 3


def is_zip(file: Path) -> bool:
    try:
        with ZipFile(file, "r") as zf:
            return zf.testzip() is None
    except Exception as ex:
        return False


def zip_extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    # extract by calling `unzip`, because ZipFile does not handle symlinks
    # https://stackoverflow.com/questions/19737570/how-do-i-preserve-symlinks-when-unzipping-an-archive-using-python
    check_output(["unzip", "-q", str(file), "-d", str(target_dir)], stderr=STDOUT)

    with ZipFile(file, "r") as zf:
        for info in zf.infolist():
            extracted_path = target_dir / Path(info.filename)

            if info.create_system == ZIP_UNIX_SYSTEM and extracted_path.is_file():
                unix_attributes = info.external_attr >> 16
                if unix_attributes & S_IXUSR:
                    extracted_path.chmod(extracted_path.stat().st_mode | S_IXUSR)


def tar_extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    with tarfile.open(file, "r") as tf:
        tf.extractall(path=target_dir, filter="data")


def extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    if is_zip(file):
        zip_extract_all_with_executable_permission(file, target_dir)
    else:
        tar_extract_all_with_executable_permission(file, target_dir)


def write_cin(file: Path, content: str) -> None:
    if file.name.endswith(".gz"):
        with gzip.GzipFile(file, "w", compresslevel=9, mtime=0.0) as binary_file:
            with io.TextIOWrapper(cast(IO[bytes], binary_file)) as f:
                f.write(content)
    else:
        file.write_text(content)


def read_cin(file: Path) -> str:
    with read_cin_file_object(file) as f:
        return f.read()


def read_cin_file_object(file: Path) -> TextIO:
    if file.name.endswith(".gz"):
        return gzip.open(file, "rt")
    elif file.name.endswith(".bz2"):
        return bz2.open(file, "rt")
    else:
        return file.open(mode="r")


def byte_read_cin_file_object(file: Path) -> BinaryIO:
    if file.name.endswith(".gz"):
        return cast(BinaryIO, gzip.open(file, "rb"))  # truncate missing
    elif file.name.endswith(".bz2"):
        return cast(BinaryIO, bz2.open(file, "rb"))  # truncate missing
    else:
        return file.open("rb")
