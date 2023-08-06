import os
WORK_DIR = os.path.dirname(__file__)
ADB_PATH = "{}/bin/adb.exe".format(WORK_DIR)
MINITOUCH_PATH = "{}/bin/minitouch/libs".format(WORK_DIR)
MINICAP_PATH = "{}/bin/minicap/libs".format(WORK_DIR)
MINICAPSO_PATH = "{}/bin/minicap/jni".format(WORK_DIR)
LINESEQ = os.linesep