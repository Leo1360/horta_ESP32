def loadPluginRegistry():
    import json
    with open("sd/plugins/registry.json","r") as f:
        return json.loads(f.read())
    pass

def savePluginRegistry(registry):
    import json
    with open("sd/plugins/registry.json","w") as f:
        f.write(json.dumps(registry))

def initializeActivePlugins():
    regitry = loadPluginRegistry()
    for plugin in regitry:
        if(plugin["isActive"]):
            initializePlugin(plugin["moduleName"])
    pass

def initializePlugin(moduleName):
    import gc
    mod = __import__("sd/plugins/" + moduleName)
    mod.init()
    del mod
    gc.collect()

def callHandler(eventName, data):
    import gc
    from loader import loadModule
    registry = loadPluginRegistry()
    for reg in registry:
        if(eventName in reg["handlers"] and reg["isActive"]):
            mod = loadModule(reg["moduleName"],"sd/plugins/")
            mod.handlers[eventName](data)
            del mod
            gc.collect()
    pass
