#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo.
"""

from fabric import task
from datetime import datetime
import os


@task
def do_pack(c):
    """
    Compresses the content of web_static folder into a .tgz archive
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            os.makedirs("versions")
        file_path = "versions/web_static_{}.tgz".format(now)
        c.local("tar -cvzf {} web_static".format(file_path))
        print("web_static packed: {} -> {}Bytes".format(
            file_path, os.path.getsize(file_path)))
        return file_path
    except Exception as e:
        return None
