"""Utils."""

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cse_lk')


def parse_int(int_str, default=0):
    """Parse int."""
    try:
        return (int)(int_str)
    except ValueError:
        return default
