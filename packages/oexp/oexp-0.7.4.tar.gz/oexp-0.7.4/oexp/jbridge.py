import atexit
import socket
import subprocess
from typing import Optional

import oexp.access as access
from oexp.util import ops
from oexp.util import vals

import os

_jar_process: Optional[subprocess.Popen] = None
_java_sock: Optional[socket.socket] = None
_java_exit_sock: Optional[socket.socket] = None
_java_conn: Optional[socket.socket] = None
_java_exit_conn: Optional[socket.socket] = None


LOCAL_JAR = os.getenv("LOCAL_JAR")


# https://stackoverflow.com/questions/1395593/managing-resources-in-a-python-project
# https://docs.python.org/3/library/subprocess.html
# https://docs.python.org/3/library/importlib.resources.html#module-importlib.resources
def _init_java():
    global _java_sock, _jar_process, _java_exit_sock, _java_conn, _java_exit_conn
    if _java_sock is not None:
        return
    ops.download_jdk_if_needed()
    if (jar_path := LOCAL_JAR) is None:
        jar_path = ops.download_jar_if_needed()
    next_port_to_try = 50_000
    _java_sock, next_port_to_try = ops.server_socket(next_port_to_try)
    java = vals.java_executable()
    _jar_process = subprocess.Popen(
        [
            java,
            "-jar",
            jar_path,
            str(next_port_to_try)
        ],
    )
    _java_conn, addr = _java_sock.accept()
    next_port_to_try += 1
    _java_exit_sock, next_port_to_try = ops.server_socket(next_port_to_try)
    _java_conn.sendall(access.SET_EXIT_PORT)
    _java_conn.sendall(next_port_to_try.to_bytes(4, 'big'))
    _java_exit_conn, addr = _java_exit_sock.accept()
    # _java_exit_sock.connect(("localhost", int(access.PORT_EXIT)))
    atexit.register(kill_java)


def kill_java():
    _java_exit_conn.send(access.OexpExitSocketHeaders.EXIT.value)
    # https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
    # _java_sock.shutdown(socket.SHUT_RDWR)
    # https://stackoverflow.com/a/4084365/6596010
    _java_exit_conn.close()
    _java_conn.close()
    _java_exit_sock.close()
    _java_sock.close()
    _jar_process.kill()
