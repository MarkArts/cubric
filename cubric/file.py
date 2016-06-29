import os
import shutil

from .cubric import Tool, NonZero


class File(Tool):
    DIR = 1
    FILE = 2
    LINK = 3

    def present(self, path, type=DIR, mode=None, user=None, group=None,
                target=None):
        if type == File.LINK:
            if target:
                self.env.command("ln", "-sfn", path, target)
            else:
                self.env.command("ln", "-sfn", path)
            return self
        if type == File.DIR:
            self.env.mkdir(path)
        elif type == File.FILE:
            try:
                self.env.command("test", "-e", path)
            except NonZero:
                self.env.command("touch", path)
        if mode:
            self.env.chmod(path, mode)
        if user or group:
            self.env.chown(path, user, group)
        return self

    def removed(self, path):
        if not os.path.exists(path):
            return self
        self.env.command("rm", "-rf", path)
        return self

    def create(self, file, content):
        """ create a file with content """
        self.env.shell("echo '{0}' > {1}".format(content, file))
