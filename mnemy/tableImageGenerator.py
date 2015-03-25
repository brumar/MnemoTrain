import jinja2
TEMPLATE_FILE = "templateImages.html"

def createTemplate(table,sheetName="learn.html",path="./"): #table is a list of lists
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
                     "dicImages" : table,
                   }
    outputText = template.render( templateVars )
    return outputText

if __name__ == "__main__":
    dicImages=[]
    dicImages.append(["cartes/2C.bmp","cartes/2S.bmp","cartes/2H.bmp","cartes/2D.bmp"])
    dicImages.append(["cartes/3C.bmp","cartes/3S.bmp","cartes/3H.bmp","cartes/3D.bmp"])
    createTemplate(dicImages)
