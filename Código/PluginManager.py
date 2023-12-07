regPath = "sd/plugins/registry.json"

def initializeActivePlugins():
    from Registry import load
    registry = load(regPath)
    for plugin in registry.keys():
        if(registry[plugin]["isActive"]):
            initializePlugin(plugin)
    pass

def initializePlugin(moduleName):
    import gc
    from loader import loadModule
    mod = __import__("sd/plugins/" + moduleName)
    mod.init()
    del mod
    gc.collect()

def callHandler(eventName, data):
    import gc
    from Registry import load
    registry = load(regPath)
    for modname in registry.keys():
        if(eventName in registry[modname]["handlers"] and registry[modname]["isActive"]):
            mod = __import__("sd/plugins/"+modname["moduleName"])
            mod.handlers[eventName](data)
            del mod
            gc.collect()
    pass

def getJson():
    from Registry import getString
    return getString(regPath)

def activatePlugin(pluginName):
    import Registry
    reg = Registry.load(regPath)
    try:
        reg[pluginName]["isActive"] = True
        Registry.save(regPath,reg)
        return True
    except:
        return False

def deactivatePlugin(pluginName):
    import Registry
    reg = Registry.load(regPath)
    try:
        reg[pluginName]["isActive"] = False
        Registry.save(regPath,reg)
        return True
    except:
        return False

