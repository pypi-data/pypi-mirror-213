import sys


def is_linux() -> bool:
    """
    Check current platform is Linux
    :return: True on Linux
    """
    return sys.platform in ('linux',)
