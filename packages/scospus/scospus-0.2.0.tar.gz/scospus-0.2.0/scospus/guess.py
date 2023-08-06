"""Not a very smart module that tries to guess a file type to parse

Suppose you have a data file at hand and don't know whether it contains DDS or
PUS packets, you can run the ``guess_reader`` function to obtain the class that
can read the file (or at least the first packet of the file).
"""
from scospus.dds import DDSReader
from scospus.pus import PUSReader
from scospus.airbuscsv import AirbusCSVReader


def guess_reader(filepath):
    """Guess what reader to use with the given file

    filepath should be a path to the file containing the packets you want to
    parse.

    Returns the type of the reader to use or ``None`` if all readers failed.

    This function will just try the various reader and return the one that does
    not die while parsing the first packet of the file.
    """
    for readertype in [AirbusCSVReader, DDSReader, PUSReader]:
        reader = readertype(filepath)
        try:
            reader.open()
            reader.read_next()
        except (RuntimeError, UnicodeError):
            continue
        finally:
            reader.close()
        return readertype

    return None
