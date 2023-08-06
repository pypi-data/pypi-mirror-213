import subprocess

from .config import ADB_PATH,MINITOUCH_PATH
from .adb import get_abi
def minitouch_install(device, abi=None):
    """安装minitouch

    Args:
        - device (str): 设备id
        - abi (str, optional): 设备架构,可以不填写,安装时自动获取. Defaults to None.
    """
    if abi is None:
        abi = get_abi(device)

    MNT_HOME = "/data/local/tmp/minitouch"

    subprocess.run([
        ADB_PATH, "-s", device, "push",
        F"{MINITOUCH_PATH}/{abi}/minitouch",
        MNT_HOME],
        stdout=subprocess.DEVNULL)

    subprocess.run([ADB_PATH, "-s", device, "shell", "chmod", "777", MNT_HOME])

