from ctypes.wintypes import HWND
from .utils import raw2opencv
from .adb import get_sdk, get_vmsize, adb_screen, get_abi, adb_press, adb_silde
from .minicap import minicap_screen, minicap_available, minicap_install
from .minitouch import minitouch_install
from .win import win_screen
from pyminitouch import MNTDevice



class CaptureScreen():
    def __init__(self, device,method="minicap") -> None:
        """
        __init__ 截图类

        Args:
            device (str|HWND): 设备id|窗口句柄
            method (str, optional): 截图方法. Defaults to "minicap"."adb","win32"

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
            self.abi = get_abi(device)
            self.sdk = get_sdk(device)
            self.vmszie = get_vmsize(device)
            if not minicap_available(device, self.vmszie):
                minicap_install(device, self.sdk, self.abi)
                if minicap_available(device, self.vmszie):
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
        return raw2opencv(minicap_screen(self.device, self.sdk, self.vmszie))

    def win32_screen(self):
        """
        win32_screen 可以遮挡，不能最小化

        Returns:
            mat: opencv格式图像
        """
        return raw2opencv(win_screen(self.device))

class MiniDevice(MNTDevice, CaptureScreen):
    def __init__(self, device,method="minidevice"):
        """
        __init__ 初始化minidevice

        Args:
            device (str|hmwd): 安卓设备id|程序窗口句柄
            method (str, optional): 操作方法. Defaults to "minidevice"."adb","win32"
        """
        if method=="minidevice":
            try :
                CaptureScreen.__init__(self, device,method="minicap")
                self.captrueMethod = "minicap"
                minitouch_install(device, get_abi(device))
                MNTDevice.__init__(self, device)
                self.touchMethod = "minitouch"
            except AssertionError:
                print("please reboot your device!")
                exit()
        elif method=="adb":
            self.captrueMethod = method
            self.touchMethod = method
            CaptureScreen.__init__(self, device,method="adb")
        elif method =="win32":
            self.captrueMethod = method
            self.touchMethod = method
            CaptureScreen.__init__(self, device,method="win32")

        print("use {}".format(self.captrueMethod))
        print("use {}".format(self.touchMethod))
                

    def miniPress(self, x, y, duration=150, pressure=100):
        """
        miniPress 点击

        Args:
            x (int): 横坐标
            y (int): 纵坐标
            duration (int, optional): 持续时间. Defaults to 150.
            pressure (int, optional): 压力. Defaults to 100.
        """
        if self.touchMethod == "minitouch":
            self.tap([(x, y)],duration,pressure)

        elif self.touchMethod == "adb":
            adb_press(self.device, x, y, duration)

    def miniSwipe(self, pointArray, duration=500, pressure=100):
        """
        miniSwipe 滑动

        Args:
            pointArray (list): [(x,y),(x,y),(x,y)]坐标数组
            duration (int, optional): 持续时间. Defaults to 500.
            pressure (int, optional): 压力. Defaults to 100.
        """
        if self.touchMethod == "minitouch":
            self.swipe(pointArray, duration, pressure)

        elif self.touchMethod == "adb":
            adb_silde(self.device, pointArray, duration)

    def captureScreen(self):
        """
        captureScreen 截图

        Returns:
            mat: opencv图像
        """
        if self.captrueMethod == "minicap":
            return self.minicap_screen()

        elif self.captrueMethod == "adb":
            return self.adb_screen()
        elif self.captrueMethod == "win32":
            return self.win32_screen()


if __name__ == "__main__":
    import cv2
    g = MiniDevice("127.0.0.1:5555")
    cv2.imshow("", g.captureScreen())
    cv2.waitKey()
    g.stop()
