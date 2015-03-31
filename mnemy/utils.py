import subprocess, os,sys

def openFileMultipleOs(filepath):
    filepathWindows=filepath.replace("/","\\\\")
    #script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    #abs_file_path = os.path.join(script_dir, filepath)
    print("we are trying to open %s for you, if nothing happen, open it manually"%filepath)
    try:
        if sys.platform.startswith('darwin'):#mac
            subprocess.call(('open', filepath))
        elif os.name == 'nt': #windows
            os.startfile(filepathWindows)
        elif os.name == 'posix':#linux
            subprocess.call(('xdg-open', filepath))
    except:
        pass

def smartRawInput(message,defaultValue,operation=lambda x: x):
    # RawInput with default value if nothing is given and apply operation to in the opposite case
    # by default operation is identity
    message+=" (default="+str(defaultValue)+") : "
    inp=raw_input(message)
    out=defaultValue
    if(inp!=""):
        out=operation(inp)
    return out
