from plugin_loader import load_plugins

PLUGINS = load_plugins()

def map_command(intent, os_type, e):
    # 🔌 Plugin commands
    for plugin in PLUGINS:
        if intent in plugin.intents:
            return plugin.execute(intent, e, os_type)


    # Core commands
    if os_type == "WINDOWS":
        if intent == "LIST_FILES":
            return "dir"
        if intent == "CURRENT_DIR":
            return "cd"
        if intent == "GO_BACK":
            return "cd .."
        if intent == "GO_HOME":
            return "cd %USERPROFILE%"
        if intent == "SYSTEM_INFO":
            return "systeminfo"
        if intent == "WHOAMI":
            return "whoami"
        if intent == "GO_TO" and e["name"]:
            return f"cd {e['name']}"
        if intent == "CREATE_FOLDER" and e["name"]:
            return f"mkdir {e['name']}"
        if intent == "DELETE_FOLDER" and e["name"]:
            return f"rmdir /s /q {e['name']}"
        if intent == "CREATE_FILE" and e["name"]:
            return f"type nul > {e['name']}"
        if intent == "DELETE_FILE" and e["name"]:
            return f"del {e['name']}"
        if intent == "RENAME_FILE" and e["source"] and e["destination"]:
            return f"ren {e['source']} {e['destination']}"
        if intent == "MOVE_FILE" and e["source"] and e["destination"]:
            return f"move {e['source']} {e['destination']}"
        if intent == "COPY_FILE" and e["source"] and e["destination"]:
            return f"copy {e['source']} {e['destination']}"
        if intent == "CAT_FILE" and e["name"]:
            return f"type {e['name']}"
        if intent == "UPGRADE_PIP":
            return "python -m pip install --upgrade pip"
        if intent == "UPGRADE_PACKAGE" and e["name"]:
            return f"pip install --upgrade {e['name']}"

        # System & Network
        if intent == "CHECK_RAM":
            return "wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value"
        if intent == "CHECK_CPU":
            return "wmic cpu get loadpercentage"
        if intent == "CHECK_DISK":
            return "wmic logicaldisk get size,freespace,caption"
        if intent == "CHECK_IP":
            return "ipconfig"
        if intent == "CHECK_INTERNET":
            return "ping 8.8.8.8 -n 1"
        if intent == "LIST_PROCESSES":
            return "tasklist"
        if intent == "KILL_PROCESS" and e["name"]:
            return f"taskkill /IM {e['name']} /F"
        if intent == "CLEAR_SCREEN":
            return "cls"

    if os_type == "LINUX":
        if intent == "LIST_FILES":
            return "ls"
        if intent == "CURRENT_DIR":
            return "pwd"
        if intent == "GO_BACK":
            return "cd .."
        if intent == "GO_HOME":
            return "cd ~"
        if intent == "SYSTEM_INFO":
            return "uname -a"
        if intent == "WHOAMI":
            return "whoami"
        if intent == "GO_TO" and e["name"]:
            return f"cd {e['name']}"
        if intent == "CREATE_FOLDER" and e["name"]:
            return f"mkdir {e['name']}"
        if intent == "DELETE_FOLDER" and e["name"]:
            return f"rm -rf {e['name']}"
        if intent == "CREATE_FILE" and e["name"]:
            return f"touch {e['name']}"
        if intent == "DELETE_FILE" and e["name"]:
            return f"rm {e['name']}"
        if intent == "RENAME_FILE" and e["source"] and e["destination"]:
            return f"mv {e['source']} {e['destination']}"
        if intent == "MOVE_FILE" and e["source"] and e["destination"]:
            return f"mv {e['source']} {e['destination']}"
        if intent == "COPY_FILE" and e["source"] and e["destination"]:
            return f"cp {e['source']} {e['destination']}"
        if intent == "CAT_FILE" and e["name"]:
            return f"cat {e['name']}"
        if intent == "UPGRADE_PIP":
            return "python3 -m pip install --upgrade pip"
        if intent == "UPGRADE_PACKAGE" and e["name"]:
            return f"pip install --upgrade {e['name']}"

        # System & Network
        if intent == "CHECK_RAM":
            return "free -h"
        if intent == "CHECK_CPU":
            return "top -bn1 | grep 'Cpu(s)'"
        if intent == "CHECK_DISK":
            return "df -h"
        if intent == "CHECK_IP":
            return "hostname -I"
        if intent == "CHECK_INTERNET":
            return "ping -c 1 8.8.8.8"
        if intent == "LIST_PROCESSES":
            return "ps aux"
        if intent == "KILL_PROCESS" and e["name"]:
            return f"pkill -f {e['name']}"
        if intent == "CLEAR_SCREEN":
            return "clear"

    return None
