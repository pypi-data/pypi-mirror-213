from glob import glob

def scan_files(glob_path: str, recursive: bool = False):
    return sorted(glob(glob_path, recursive=recursive))