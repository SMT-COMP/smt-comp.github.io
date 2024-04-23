# It is hard to find a library to unpack *with permission*
# and securely

from pathlib import Path
from zipfile import ZipFile
import tarfile
from stat import S_IXUSR

ZIP_UNIX_SYSTEM = 3


def zip_extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    with ZipFile(file, "r") as zf:
        for info in zf.infolist():
            extracted_path = Path(zf.extract(info, target_dir))

            if info.create_system == ZIP_UNIX_SYSTEM and extracted_path.is_file():
                unix_attributes = info.external_attr >> 16
                if unix_attributes & S_IXUSR:
                    extracted_path.chmod(extracted_path.stat().st_mode | S_IXUSR)


def tar_extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    with tarfile.open(file, "r") as tf:
        tf.extractall(path=target_dir, filter="data")


def extract_all_with_executable_permission(file: Path, target_dir: Path) -> None:
    if str(file).endswith(".zip"):
        zip_extract_all_with_executable_permission(file, target_dir)
    else:
        tar_extract_all_with_executable_permission(file, target_dir)
