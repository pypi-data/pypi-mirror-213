import os


class UnixUser(object):
    def __init__(self):
        self._home = os.environ['HOME']
        self._username = os.environ['USER']
        self._uid = str(os.getuid())
        self._gid = str(os.getgid())

    @property
    def home(self):
        return self._home

    @property
    def username(self):
        return self._username

    @property
    def uid(self):
        return self._uid

    @property
    def gid(self):
        return self._gid

    def home_subdir(self, subdir: str) -> str:
        R"""
        Returns the path to a subdirectory under the user's home directory on the host system.
        :param subdir: Subdirectory (e.g. ".ssh")
        :return: Absolute path to home sub
        """
        return os.path.join(self._home, subdir)
