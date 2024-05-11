#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""

from datetime import datetime
from fabric.api import env, put, run
import os

# Define servers
env.hosts = ['54.84.221.42', '35.153.33.53']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Uncompress the archive to /data/web_static/releases/
        filename = os.path.basename(archive_path)
        folder_name = "/data/web_static/releases/{}".format(
            filename.split('.')[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")

        return True
    except Exception as e:
        return False
