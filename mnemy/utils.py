
def smartRawInput(message,defaultValue,operation=lambda x: x):
    # RawInput with default value if nothing is given and apply operation to in the opposite case
    # by default operation is identity
    message+=" (default="+str(defaultValue)+") : "
    inp=raw_input(message)
    out=defaultValue
    if(inp!=""):
        out=operation(inp)
    return out
