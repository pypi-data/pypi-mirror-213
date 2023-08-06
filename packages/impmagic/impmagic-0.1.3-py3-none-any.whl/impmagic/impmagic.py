import __main__
import inspect
import sys

if 'imp_cache' not in __main__.__dict__:
    __main__.__dict__['imp_cache'] = {}
CACHE = __main__.__dict__['imp_cache']


#Importation de module à partir d'un tuple ou d'une liste ou d'un str
def load(data, func=None, globals_val=None):
    #Pour supporter l'import des modules locaux
    if "path" not in globals():
        if not func:
            frame = inspect.currentframe()
            frame = frame.f_back # remonte d'un niveau dans la pile d'appels
            path = frame.f_globals["__file__"] # récupère le chemin du fichier appelant
            del frame
        else:
            path = inspect.getfile(func)

        globals()['path'] = getattr(__import__('os', fromlist=['object']), 'path').dirname(path)
        if globals()['path'] not in sys.path:
            sys.path.append(globals()['path'])

    if not func:
        if globals_val:
            func = globals_val
        else:
            current_frame = inspect.currentframe()
            calling_frame = current_frame.f_back
            calling_globals = calling_frame.f_globals
            func = calling_globals
    else:
        func = func.__globals__

    if isinstance(data, tuple) or isinstance(data, list):
        for mod in data:
            if isinstance(mod, dict):
                if 'submodule' in mod and mod['submodule']!=None:
                    for sub in mod['submodule']:
                        try:
                            if 'as' in mod:
                                name = mod['module']+"."+sub+mod['as']
                                if name in CACHE:
                                    func[mod['as']] = CACHE[name]
                                else:
                                    funct_in = getattr(__import__(mod['module'], fromlist=['object']), sub)
                                    CACHE[name] = funct_in
                                    func[mod['as']] = funct_in
                            else:
                                name = mod['module']+"."+sub
                                if name in CACHE:
                                    func[sub] = CACHE[name]
                                else:
                                    funct_in = getattr(__import__(mod['module'], fromlist=['object']), sub)
                                    CACHE[name] = funct_in
                                    func[sub] = funct_in
                        except:
                            if 'as' in mod:
                                name = mod['module']+"."+sub+mod['as']
                                if name in CACHE:
                                    func[mod['as']] = CACHE[name]
                                else:
                                    funct = __import__(mod['module']+"."+sub, fromlist=['object'])
                                    CACHE[name] = funct
                                    func[mod['as']] = funct
                            else:
                                name = mod['module']+"."+sub
                                if name in CACHE:
                                    func[sub] = CACHE[name]
                                else:
                                    funct = __import__(mod['module']+"."+sub, fromlist=['object'])
                                    CACHE[name] = funct
                                    func[sub] = funct
                else:
                    if 'as' in mod:
                        name = mod['module']+"."+mod['as']
                        if name in CACHE:
                            func[mod['as']] = CACHE[name]
                        else:
                            funct = __import__(mod['module'], fromlist=['object'])
                            CACHE[name] = funct
                            func[mod['as']] = funct
                    else:
                        name = mod['module']
                        if name in CACHE:
                            func[mod['module']] = CACHE[name]
                        else:
                            funct = __import__(mod['module'], fromlist=['object'])
                            CACHE[name] = funct
                            func[mod['module']] = funct
            else:
                funct = get(mod)
                if funct!=None:
                    CACHE[mod] = funct
                    func[mod] = funct
                
    elif isinstance(data, str):
        if data in CACHE:
            func[data] = CACHE[data]
        else:
            funct = get(data)
            if funct!=None:
                CACHE[data] = funct
                func[data] = funct

#Décharger un module
def unload(modulename, uncache=False):
    if uncache:
        if modulename in CACHE:
            del CACHE[modulename]

    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    calling_globals = calling_frame.f_globals
    if modulename in calling_globals:
        del calling_globals[modulename]
    del sys.modules[modulename]

#Rechargement d'un module
def reload(modulename):
    unload(modulename, uncache=True)
    current_frame = inspect.currentframe()
    calling_frame = current_frame.f_back
    load(modulename, globals = calling_frame.f_globals)

#Chargement d'un module sans l'importer dans le code
def get(modulename):
    if 'imp_cache' in __main__.__dict__:
        if modulename in CACHE:
            return CACHE[modulename]

    try:
        funct = __import__(modulename, fromlist=['object'])
        return funct
    except:
        try:
            if "." in modulename:
                modulename = modulename.split(".")
                funct = __import__(".".join(modulename[:-1]), fromlist=['object'])

                funct = getattr(funct, modulename[-1])
                return funct
        except:
            return None
    return None

#Décorateur pour l'importation de module
def loader(*data):
    def inner(func):
        def wrapper(*args, **kwargs):
            load(data, func)
            return func(*args, **kwargs)
        return wrapper
    return inner 
