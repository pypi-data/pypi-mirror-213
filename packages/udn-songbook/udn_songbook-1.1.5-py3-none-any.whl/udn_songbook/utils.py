# utility functions that aren't really class-specific
import logging
import os
import re
from string import punctuation
from typing import Union


def make_dir(destdir: str, logger: Union[logging.Logger, None]):
    """
    Attempt to create a directory if it doesn't already exist
    Raise an error if the creation fails
    """
    if os.path.exists(destdir):
        return True
    else:
        try:
            os.makedirs(destdir)
            return True
        except (IOError, OSError) as E:
            logger.exception(f"Unable to create output dir {E.filename} - {E.strerror}")
            raise


def safe_filename(filename: str) -> str:
    """
    Just simple string translation to remove UNIX-unfriendly characters from filenames
    removes the following characters from filenames:

    """
    tt = {ord(char): "_" for char in punctuation if char not in ["#", "-", "_", "."]}
    # this replaces '#' though, so escape that.
    tt.update({ord("#"): "_sharp_"})

    return re.sub(r"_+", r"_", filename.translate(tt))
