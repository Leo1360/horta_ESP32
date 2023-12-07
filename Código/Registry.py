
def load(path):
    from json import loads
    with open(path,"r") as f:
        temp = f.read()
        try:
            return loads(temp)
        except:
            return {}

def save(path,reg):
    from json import dumps
    with open(path,"w") as f:
        f.write(dumps(reg))
    pass

def getString(path):
    with open(path,"r") as f:
        return f.read()

def removeElement(path,key):
    reg = load(path)
    try:
        reg.pop(key)
        save(path,reg)
    except:
        pass

def addElement(path,key,element):
    reg = load(path)
    try:
        reg[key] = element
        save(path,reg)
    except:
        pass

def getElement(path,key):
    reg = load(path)
    try:
        return reg[key]
    except:
        return {}

