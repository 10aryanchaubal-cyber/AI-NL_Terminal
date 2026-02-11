import platform

def get_os():
    os_name = platform.system()
    if os_name == "Linux":
        return "LINUX"
    elif os_name == "Windows":
        return "WINDOWS"
    else:
        return "UNSUPPORTED"
