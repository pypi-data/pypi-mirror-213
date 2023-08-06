import json
from subprocess import call

notarizationPath = ""
isToCache = 1

def init(_notarizationPath, _isToCache) :
    global notarizationPath, isToCache
    notarizationPath = _notarizationPath
    isToCache = int(_isToCache)

def scriptContext(_filename) :
    return _filename

def notarizationContextRawfile():
    return "../.." + notarizationPath + "/../rawFile.csv"

def notarizationContext(_filename) :
    return "../.." + notarizationPath + "/" + _filename

def dayContext(_m, _filename) :
    if (_m >= 0) : raise Exception("No history at J", str(_m))
    day = json.load(open("../.." + notarizationPath + "/.config.json"))["day"] + _m
    if (day < 0) : raise Exception("No history at J", str(day))
    lastNotarization = json.load(open("../.." + notarizationPath + "/../../Day" + str(day) + "/.dayConfig.json"))["lastNotarization"]
    return "../.." + notarizationPath + "/../../Day" + str(day) + "/Notarization" + str(lastNotarization) + "/" + _filename

def finish(*args) :
    call(["rm", "-r","../__cache__"])
    if isToCache == 1 :
        call(["mkdir","../__cache__"])
        for i in args :
            try :
                call(["mv",str(i),"../__cache__"])
            except :
                print("Warning : ", str(i), "not found")
        print("Final result at :", "../__cache__")

    else : 
        for i in args : 
            try : 
                call(["mv",str(i),"../.." + notarizationPath])
            except :
                print("Warning : ", str(i), "not found")
        print("Final result at :", "../.." + notarizationPath)