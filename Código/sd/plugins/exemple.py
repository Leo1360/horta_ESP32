"""All plugins are lazy executed, and are only loaded when needed. Your code must not contain code out of functions"""
handlers = { # dict with the handlers pointing to it functions
    "befor_sensorReading":function,
    "after_sensorReading":function,
    "befor_readingSession":function,
    "after_readingSession":function,
    "on_sensorFailedReading":function,
    "on_pluginRequest":function
}

def init():
    print("iniciando...")

