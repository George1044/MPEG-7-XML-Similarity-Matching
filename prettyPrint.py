
import lxml.etree as et

for i in range(1,1000):
    myFile = "XML/" + str(i) + ".xml"
    tree = et.parse(myFile)
    pretty = et.tostring(tree, encoding="unicode", pretty_print= True)
    file = open(myFile, 'w')
    file.write(pretty)
