from ctypes.wintypes import HWND

from .adb import adb_screen, get_abi, get_sdk, get_vmsize
from .images import raw2opencv
from .minicap import minicap_available, minicap_install, minicap_screen
from .wincap import win_screen


class CaptureScreen():
    def __init__(self, device,method="minicap",quality=100) -> None:
        """
        __init__ 截图类

        Args:
            device (str|HWND): 设备id|窗口句柄
            method (str, optional): 截图方法. Defaults to "minicap"."adb","win32"
            quality (int, optional): 截图品质(1~100). Defaults to 100

        Raises:
            Exception: 使用minicap时如果minicap安装失败则抛出异常 "minicap isn't available"
        """
        if method == "win32":
            if not isinstance(device,HWND):
                raise ValueError("请输入窗口句柄!")
        elif method == "adb" or method == "minicap":
            if not isinstance(device,str):
                raise ValueError("请输入字符串")
        else:
            raise ValueError("请输入正确的方法")
        
        self.device = device
        
        if method == "minicap":
            self.quality = quality
            self.abi = get_abi(device)
            self.sdk = get_sdk(device)
            self.vmszie = get_vmsize(device)
            print(self.abi,self.sdk,self.vmszie,)
            if not minicap_available(device, self.vmszie):
                minicap_install(device, self.sdk, self.abi)
                if not minicap_available(device, self.vmszie):
                    raise Exception("minicap isn't available")


        
    def adb_screen(self):
        """
        adb_screen adb截图任意安卓版本

        Returns:
            mat: opencv格式图像
        """
        return raw2opencv(adb_screen(self.device))

    def minicap_screen(self):
        """
        minicap_screen 安卓5~12L专用截图

        Returns:
            mat: opencv格式图像
        """
        return raw2opencv(minicap_screen(self.device, self.sdk, self.vmszie,self.quality))

    def win32_screen(self):
        """
        win32_screen 可以遮挡，不能最小化

        Returns:
            mat: opencv格式图像
        """
        return raw2opencv(win_screen(self.device))





