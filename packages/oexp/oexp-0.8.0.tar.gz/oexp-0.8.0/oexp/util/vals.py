import platform
from functools import lru_cache
import subprocess
import os
from oexp import gen

system = platform.system()
_HOST = "127.0.0.1"
_last_port_to_try = 51_000


@lru_cache()
def cpu():
    if system == 'Linux':
        return subprocess.check_output(['uname', '-m']).decode().strip()
    else:
        return subprocess.check_output(['/usr/sbin/sysctl', 'machdep.cpu.brand_string']).decode().strip()


@lru_cache()
def user_data_dir():
    d = {
        'Darwin': lambda: os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'oexp'),
        'Linux': lambda: os.path.join(os.path.expanduser('~'), '.oexp')
    }
    if system not in d:
        raise Exception(f"TODO: implement user_data_dir for {system}")
    else:
        return d[system]()


@lru_cache()
def jdk_platform_label():
    my_cpu = cpu()
    if my_cpu == "machdep.cpu.brand_string: Apple M1 Max":
        platform_label = "macos-aarch64"
    elif my_cpu == "x86_64":
        platform_label = "linux-x64"
    else:
        raise Exception(f"need to figure out java for {my_cpu}")
    return platform_label


@lru_cache()
def jdk_folder():
    j_version = f"jdk-{gen.JAVA_VERSION}"
    data_dir = user_data_dir()
    if system == 'Linux':
        j_folder = os.path.join(data_dir, j_version)
    else:
        j_folder = os.path.join(data_dir, j_version + ".jdk")
    return j_folder



@lru_cache()
def java_executable():
    j_folder = jdk_folder()
    if system == 'Linux':
        java = os.path.join(j_folder, "bin/java")
    else:
        java = os.path.join(j_folder, "Contents/Home/bin/java")
    return java