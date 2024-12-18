# This file contains examples of global helper or utility functions that can be reused across the project.
import json


def get_hashed_filename(filename):
    """
    Retrieves the hashed filename for a given static asset from the manifest file.

    This function looks up a given original filename in the 'manifest.json' file,
    which maps original filenames to their hashed versions (e.g., for cache busting).
    If the manifest file or the filename does not exist, it gracefully falls back
    to returning the original filename.
    """
    try:
        with open("app/static/dist/manifest.json") as f:
            manifest = json.load(f)
        return manifest.get(filename, filename)
    except FileNotFoundError:
        return filename
