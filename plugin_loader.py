import os
import importlib.util
import inspect
from plugin_interface import Plugin

PLUGIN_DIR = "plugins"

def load_plugins():
    plugins = []

    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)
        return plugins

    for file in os.listdir(PLUGIN_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            path = os.path.join(PLUGIN_DIR, file)
            module_name = file[:-3]
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find subclasses of Plugin
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) 
                            and issubclass(obj, Plugin) 
                            and obj is not Plugin):
                            try:
                                instance = obj()
                                plugins.append(instance)
                            except Exception as e:
                                print(f"Error instantiating plugin {name}: {e}")
            except Exception as e:
                print(f"Failed to load plugin {file}: {e}")

    return plugins

