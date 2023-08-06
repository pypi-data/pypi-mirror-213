import subprocess
import os
import socket
import urllib.request as request
from distutils.util import strtobool

from oexp import gen, access
from oexp.util import vals


def strtobool_none_is_false(val):
    if val is None:
        return False
    else:
        return strtobool(val)


VERBOSE = strtobool_none_is_false(os.getenv('VERBOSE'))


def verbose(s):
    if VERBOSE:
        print(s)


def server_socket(next_port_to_try):
    # _java_sock.connect(("localhost", int(access.PORT)))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    did_bind = False
    while next_port_to_try <= vals._last_port_to_try:
        try:
            sock.bind((vals._HOST, next_port_to_try))
            did_bind = True
            break
        except socket.error:
            verbose(f"port {next_port_to_try} is being used, trying for port {next_port_to_try + 1} ")
            next_port_to_try += 1
    if not did_bind:
        raise Exception("could not bind socket")
    sock.listen()
    return sock, next_port_to_try


def download_jdk_if_needed():
    platform_label = vals.jdk_platform_label()
    data_dir = vals.user_data_dir()
    tar_gz_folder = os.path.join(data_dir, "jdk.tar.gz")
    if not os.path.exists(tar_gz_folder):
        print("downloading java...")
        os.makedirs(data_dir, exist_ok=True)
        if os.path.exists(tar_gz_folder):
            os.remove(tar_gz_folder)
        #     https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html
        request.urlretrieve(
            f"https://download.oracle.com/java/17/archive/jdk-{gen.JAVA_VERSION}_{platform_label}_bin.tar.gz",
            tar_gz_folder
        )
        subprocess.run(
            [
                "/usr/bin/tar", "-xf",
                tar_gz_folder
            ],
            cwd=data_dir
        )
        print("finished downloading java!")


def download_jar_if_needed():
    data_dir = vals.user_data_dir()
    last_downloaded_jar_path = os.path.join(data_dir, f"last_downloaded_jar.txt")
    jar_path = os.path.join(data_dir, f"oexp-front-0-all.jar")

    need_to_download = True
    if os.path.exists(last_downloaded_jar_path):
        with open(last_downloaded_jar_path, 'r') as f:
            need_to_download = f.read() != gen.JAR_VERSION
    if need_to_download:
        if os.path.exists(jar_path):
            os.remove(jar_path)
        print("downloading jar...")
        request.urlretrieve(
            access.JAR_URL,
            jar_path
        )
        with open(last_downloaded_jar_path, 'w') as f:
            f.write(gen.JAR_VERSION)
        print("finished downloading jar!")
    return jar_path
