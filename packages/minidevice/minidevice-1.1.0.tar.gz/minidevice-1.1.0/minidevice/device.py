from pyminitouch import MNTDevice

from .adb import adb_press, adb_silde,get_devices
from .capture import CaptureScreen
from .minitouch import minitouch_install


class MiniDevice(MNTDevice, CaptureScreen):
    def __init__(self, device,method="minidevice",quality=100):
        """
        __init__ 初始化minidevice

        Args:
            device (str|hmwd): 安卓设备id|程序窗口句柄
            method (str, optional): 操作方法. Defaults to "minidevice"."adb","win32"
            quality (int, optional): 截图品质(1~100). Defaults to 100
        """
        if (method=="minidevice" or method=="adb") and (device in get_devices()):
            if method=="minidevice":
                try :
                    CaptureScreen.__init__(self, device,method="minicap",quality=quality)
                    self.captrueMethod = "minicap"
                    minitouch_install(device, self.abi)
                    MNTDevice.__init__(self, device)
                    self.touchMethod = "minitouch"
                except AssertionError:
                    print("please reboot your device!")
                    exit()
            elif method=="adb":
                self.captrueMethod = method
                self.touchMethod = method
                CaptureScreen.__init__(self, device,method="adb")
        else:
            raise ValueError("设备id不存在")
        
        if method =="win32":
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