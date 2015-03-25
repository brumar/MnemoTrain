import jinja2
TEMPLATE_FILE = "templateFaces.html"

def createTemplate(table,sheetName="learnFaces.html",path="./"): #table is a list of lists
    string=generateTemplate(table,path)
    with open(sheetName, "wb") as f:
        f.write(string)

def generateTemplate(table,path):
    templateLoader = jinja2.FileSystemLoader( searchpath="./" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template( TEMPLATE_FILE )


    templateVars = {
                     "description" : "A simple inquiry of function.",
                     "path":path,
                     "dicImages" : table
                   }
    outputText = template.render( templateVars )
    return outputText
