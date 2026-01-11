import platform
import shutil

def get_system_info():
    info = {}

    info["OS"] = platform.system()
    info["OS Version"] = platform.version()
    info["Processor"] = platform.processor()

    total, used, free = shutil.disk_usage("/")
    info["Disk Total (GB)"] = round(total / (1024 ** 3), 2)
    info["Disk Free (GB)"] = round(free / (1024 ** 3), 2)

    return info