import subprocess
from .config import ADB_PATH,LINESEQ,MINICAP_PATH,MINICAPSO_PATH


def line_breaker(sdk):
    if sdk >= 24:
        line_breaker = LINESEQ
    else:
        line_breaker = '\r' + LINESEQ
    return line_breaker.encode("ascii")


def minicap_screen(device, sdk, vm_size):
    """minicap 0.15~0.25s
    """
    raw_data = subprocess.check_output([ADB_PATH, "-s", device, "shell",
                                        "LD_LIBRARY_PATH=/data/local/tmp",
                                        "/data/local/tmp/minicap", "-P", f"{vm_size}@{vm_size}/0", "-s"],
                                       stderr=subprocess.DEVNULL)
    jpg_data = raw_data.split(b"for JPG encoder\n"+line_breaker(sdk))[-1]
    jpg_data = jpg_data.replace(line_breaker(sdk), b"\n")
    return jpg_data


def minicap_install(device, sdk, abi):
    """minicap

    Args:
        device (_type_): _description_
    """
    #在x86_64上运行32位minicap可正常运行
    if sdk >= 31 and abi == "x86_64":
        abi = "x86"


    MNC_HOME = "/data/local/tmp/minicap"
    MNC_SO_HOME = "/data/local/tmp/minicap.so"

    subprocess.run([
        ADB_PATH, "-s", device, "push",
        f"{MINICAP_PATH}/{abi}/minicap",
        MNC_HOME],
        stdout=subprocess.DEVNULL)

    subprocess.run([
        ADB_PATH, "-s", device, "push",
        f"{MINICAPSO_PATH}/android-{sdk}/{abi}/minicap.so",
        MNC_SO_HOME],
        stdout=subprocess.DEVNULL)

    subprocess.run([ADB_PATH, "-s", device, "shell", "chmod", "777", MNC_HOME])


def minicap_available(device, vm_size):
    """check minicap is available

    Args:
        device (_type_): _description_
        vm_size (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        result = subprocess.check_output([ADB_PATH, "-s", device, "shell",
                                          "LD_LIBRARY_PATH=/data/local/tmp",
                                          "/data/local/tmp/minicap", "-P", f"{vm_size}@{vm_size}/0", "-t"], stderr=subprocess.DEVNULL)
        if "OK" in result.decode('utf-8'):
            return True
        return False
    except subprocess.CalledProcessError:
        return False


