import os
import subprocess

from .config import ADB_PATH


def get_sdk(device:str):
    """获取设备sdk版本

    Args:
        device (str): 设备id

    Returns:
        int: 设备sdk版本号
    """
    return int(
         subprocess.run(
         [ADB_PATH,"-s",device, "shell",'getprop', 'ro.build.version.sdk'],
         stdout=subprocess.PIPE, text=True
         ).stdout.strip())

def get_vmsize(device:str):
    """获取设备分辨率

    Args:
        device (str): 设备id

    Returns:
        str: 设备分辨率格式为 "宽x高"
    """
    return subprocess.run(
         [ADB_PATH, "-s", device, "shell", "wm", "size"],
         stdout=subprocess.PIPE, text=True
         ).stdout.split(":")[-1].strip()

def get_abi(device:str):
    """获取设备abi版本

    Args:
        device (str): 设备id

    Returns:
        str: 设备abi版本号
    """
    return subprocess.run(
         [ADB_PATH,"-s",device, "shell",'getprop', 'ro.product.cpu.abi'],
         stdout=subprocess.PIPE, text=True).stdout.strip()

def adb_screen(device:str):
    """
    adb_screen adb截图

    Args:
        device (str): 设备id

    Returns:
        raw: 截图源数据
    """
    # 调用adb命令进行截图，并将输出传递给OpenCV进行处理
    process = subprocess.Popen([ADB_PATH,"-s",device, "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
    screenshot_data, _ = process.communicate()
    return screenshot_data

def adb_press(device:str,x:int,y:int,duration=150):
    """
    adb_press 按压

    Args:
        device (str): 设备id
        x (int): 横坐标
        y (int): 纵坐标
        duration (int, optional): 持续时间. Defaults to 150.
    """
    subprocess.run([ADB_PATH,"-s",device, "shell", "input","touchscreen", "swipe",str(x),str(y),str(x),str(y),str(duration)])

def adb_silde(device:str,pointArray:list,duration=250):
    """
    adb_silde 滑动

    Args:
        device (str): 设备id
        pointArray (list): [(x,y),(x,y),(x,y),(x,y)] 类似如此的坐标点列表
        duration (int, optional): 持续时间. Defaults to 250.
    """
    cmd = [ADB_PATH,"-s",device, "shell", "input","touchscreen", "swipe"]
    cmd.extend([str(coord) for point in pointArray for coord in point])
    cmd.append(str(duration))
    subprocess.run(cmd)

def get_devices():
    """
    get_devices 获取设备id列表

    Returns:
        list: 设备id列表
    """
    # 运行 adb devices 命令，并将输出分割成列表
    result = (
        subprocess.run([ADB_PATH, "devices"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .split("\n")
    )
    # 创建一个空列表，用于保存设备序号
    device_list = []
    # 遍历输出列表中的每一行，跳过表头和空行
    for line in result[1:]:
        if line.strip() != "":
            # 分割每一行，获取设备序号并添加到列表中
            device_list.append(line.split("\t")[0])
    if len(device_list) == 0:
        print("没有连接的设备")
        return []
    return device_list

def restart_adb():
    """
    restart_adb 重启adb
    """
    subprocess.run([ADB_PATH, "kill-server"])
    subprocess.run([ADB_PATH, "start-server"])

def clean_forward():
    """
    clean_forward 清理转发端口

    Returns:
        boolean: 有端口占用时返回true,反之返回false
    """
    result = (
        subprocess.run([ADB_PATH, "forward", "--list"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .split("\n")
    )
    forward_list = []
    for line in result:
        if line.strip() != "":
            # 分割每一行，获取设备序号并添加到列表中
            forward_list.append(line.split(" ")[1])
    if len(forward_list) == 0:
        return False
    for t in forward_list:
        print(t)
        subprocess.run([ADB_PATH, "forward", "--remove", t])
    return True

def open_app_setting(device:str, package_name:str):
    """
    open_app_details 打开应用的详情页(设置页)

    Args:
        device (str): 设备id
        package_name (str): 应用包名

    Returns:
        ean: 如果找不到该应用返回false; 否则返回true。
    """

    if package_name is not None:
        adb_command = '{} -s {} shell am start -n com.android.settings/.applications.InstalledAppDetails -d "package:{}"'.format(ADB_PATH,device,package_name)
        process = subprocess.Popen(adb_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        # 打印输出结果
        print(output.decode('utf-8'))
        return True
    else :
        return False
    
def uninstall_app(device:str, package_name:str):
    """
    通过包名卸载应用
    Args:
        device (str): 设备id
        package_name: 应用包名
    """
    adb_command = "{} -s {} uninstall {}".format(ADB_PATH,device,package_name) 
    subprocess.run(adb_command.split())
    
def set_resolution(device:str, width:int, height:int):
    """
    设置设备分辨率

    Args:
        device (str): 设备id
        width: 宽度
        height: 高度
    """
    adb_command = "{} -s {} shell wm size {}x{}".format(ADB_PATH,device,str(width),str(height)) 
    subprocess.run(adb_command.split())

def is_file(device:str,path:str):
    """
    isFile 返回路径path是否是文件。如果该路径指向一个文件,则命令返回true,否则返回false。

    Args:
        device (str): 设备id
        path (str): 路径
    """
    adb_command = "{} -s {} shell test -f {}".format(ADB_PATH,device,path) 
    process = subprocess.call(adb_command.split())
    if process == 0:
        return True
    elif process == 1:
        return False
    
def is_dir(device:str,path:str):
    """
    isFile 返回路径path是否是文件夹。如果该路径指向一个文件夹,则命令返回true,否则返回false。

    Args:
        device (str): 设备id
        path (str): 路径
    """
    adb_command = "{} -s {} shell test -d {}".format(ADB_PATH,device,path) 
    process = subprocess.call(adb_command.split())
    if process == 0:
        return True
    elif process == 1:
        return False    

def is_empty_dir(device:str,path:str):
    """
    isEmptyDir 返回文件夹path是否为空文件夹。如果该路径并非文件夹，则直接返回false。
    如果输入的不是文件夹路径则抛出异常
    Args:
        device (str): 设备id
        path (str): 路径
    """
    if is_dir(device,path):
        adb_command = "{} -s {} shell ls -a {}".format(ADB_PATH,device,path) 
        process = subprocess.run(adb_command.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL).stdout.decode('utf-8')
        if process == "":
            return True
        elif process != "":
            return False    
    else:
        raise Exception("这他妈不是文件夹路径")
    
def create_file(device:str,path:str):
    """
    create_file 创建一个文件

    Args:
        device (str): 设备id
        path (str): 路径
    """
    adb_command = "{} -s {} shell touch {}".format(ADB_PATH,device,path) 
    process = subprocess.call(adb_command.split(),stderr=subprocess.DEVNULL)
    if process == 0:
        return True
    elif process == 1:
        raise Exception("Not a directory")       

def exists(device:str,path:str):
    """
    exists 返回路径path是否存在。如果该路径存在,则命令返回true,否则返回false。

    Args:
        device (str): 设备id
        path (str): 路径
    """
    adb_command = "{} -s {} shell test -e {}".format(ADB_PATH,device,path) 
    process = subprocess.call(adb_command.split())
    if process == 0:
        return True
    elif process == 1:
        return False    

def read(device:str,path:str):
    """
    read 读取文本文件path的所有内容并返回。如果文件不存在,

    Args:
        device (str): 设备id
        path (str): 路径

    Raises:
        Exception: 读取失败
        Exception: 文件不存在

    """
    if exists(device,path):
        try:
            output = subprocess.check_output([ADB_PATH,'-s',device, 'shell', 'cat', path])
            content = output.decode('utf-8').rstrip('\n')
            return content
        except subprocess.CalledProcessError:
            print('Failed to read file.')
            raise Exception("读取失败")
    else:
        raise Exception("文件不存在")
    
def write(device:str,path:str, text:str):
    """
    write 把text写入到文件path中。如果文件存在则覆盖，不存在则创建。

    Args:
        device (str): 设备id
        path (str): 路径
        text (str): 文本内容

    Returns:
        boolean: 是否成功
    """
    process = subprocess.call([ADB_PATH,'-s',device,'shell','echo',text,'>',path])
    if process == 0:
        return True
    elif process == 1:
        raise Exception("写入失败")  

def append(device:str,path:str, text:str):
    """
    append 把text追加到文件path的末尾。如果文件不存在则创建。

    Args:
        device (str): 设备id
        path (str): 路径
        text (str): 文本内容

    Returns:
        boolean: _description_
    """
    if exists(device,path):
        process = subprocess.call([ADB_PATH,'-s',device,'shell','echo',text,'>>',path])
    else:
        process = subprocess.call([ADB_PATH,'-s',device,'shell','echo',text,'>',path])
    if process == 0:
        return True
    elif process == 1:
        raise Exception("写入失败")  

def copy(device:str,from_path:str, to_path:str):
    """
    copy 复制文件

    Args:
        device (str): 设备id
        from_path (str): 源文件路径
        to_path (str): 目标路径

    Raises:
        Exception: 文件不存在

    Returns:
        boolean: 是否成功
    """
    if exists(device,from_path):
        process = subprocess.call([ADB_PATH,'-s',device,'shell','cp',from_path,to_path])
        if process == 0:
            return True
        elif process == 1:
            return False  
    else:
        raise Exception("源文件不存在")

def move(device:str,from_path:str, to_path:str):
    """
    move 移动文件

    Args:
        device (str): 设备id
        from_path (str): 源文件路径
        to_path (str): 目标路径

    Raises:
        Exception: 文件不存在

    Returns:
        boolean: 是否成功
    """
    if exists(device,from_path):
        process = subprocess.call([ADB_PATH,'-s',device,'shell','mv',from_path,to_path])
        if process == 0:
            return True
        elif process == 1:
            return False  
    else:
        raise Exception("源文件不存在")  

def rename(device:str,from_path:str, to_name:str):
    """
    rename 重命名文件，并返回是否重命名成功

    Args:
        device (str): 设备id_
        from_path (str): 源文件路径
        to_name (str): 输入文件名/文件绝对路径都可以

    Raises:
        Exception: 文件不存在

    Returns:
        boolean: 是否成功
    """
    path,file_name = os.path.split(from_path)
    head,tail=os.path.split(to_name)

    if not tail:
        to_name = to_name
    else:
        to_name = tail

    if exists(device,from_path):
            process = subprocess.call([ADB_PATH,'-s',device,'shell','mv',from_path,f"{path}/{to_name}"])
            if process == 0:
                return True
            elif process == 1:
                return False  
    else:
        raise Exception("源文件不存在")
    
def remove(device:str,path:str):
    """
    remove 删除文件或空文件夹，返回是否删除成功。

    Args:
        device (str): 设备id
        path (str): 文件路径

    Returns:
        boolean: 是否成功
    """
    process = subprocess.call([ADB_PATH,'-s',device,'shell','rm',path])
    if process == 0:
        return True
    elif process == 1:
        return False  
   
def remove_dir(device:str,path:str):
    """
    remove_dir 删除文件夹，如果文件夹不为空，则删除该文件夹的所有内容再删除该文件夹，返回是否全部删除成功。

    Args:
        device (str): 设备id
        path (str): 文件路径

    Returns:
        boolean: 是否成功
    """
    process = subprocess.call([ADB_PATH,'-s',device,'shell','rm','-r',path])
    if process == 0:
        return True
    elif process == 1:
        return False   

def list_dir(device:str,path:str):
    """
    list_dir 列出文件夹path下的文件和文件夹的数组

    Args:
        device (str): 设备id
        path (str): 文件路径

    Raises:
        Exception: 文件不存在

    Returns:
        boolean: 是否成功
    """
    if is_dir(device,path):
        adb_command = "{} -s {} shell ls -a {}".format(ADB_PATH,device,path) 
        process = subprocess.run(adb_command.split(),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL).stdout.decode('utf-8')
        return process.split("\r\n")[:-1]
    else:
        raise Exception("这他妈不是文件夹路径啊")

    
if __name__=="__main__":
    print(list_dir("127.0.0.1:16384","/storage/emulated/0"))

