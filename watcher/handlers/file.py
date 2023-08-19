import os
import shutil


def create_tmp_dir(objPrefix: str) -> str:
    tmp_dir_root = "./tmp"
    tmp_dir = f"{tmp_dir_root}/{os.urandom(16).hex()}"
    tmp_dir_with_prefix = f"{tmp_dir}/{objPrefix}"

    if not os.path.exists(tmp_dir_with_prefix):
        os.makedirs(tmp_dir_with_prefix)

    return tmp_dir


def del_tmp_dir(tmp_dir: str):
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
