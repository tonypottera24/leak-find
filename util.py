def filename_add_suffix(path, suffix=None, ext=None):
    filename = f"{path.parent}/{path.stem}"
    if suffix:
        filename += f"_{suffix}"
    if ext:
        filename += f".{ext}"
    else:
        filename += path.suffix
    return filename
