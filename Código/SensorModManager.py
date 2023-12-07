regPath = "sd/sensorModules/registry.json"

def moduleExists(modname):
    from Registry import getElement
    if(getElement(regPath,modname) == {}):
        return True
    else:
        return False

def listMods():
    from Registry import load
    return load(regPath)

def getJson():
    from Registry import getString
    return getString(regPath)