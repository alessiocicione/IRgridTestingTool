import xml.etree.ElementTree as et
import lxml.etree as etree
import os


def write(data, destination, tag = ""):
    root = et.Element("root")
    doc = et.SubElement(root, f"data_{tag}")

    for element in data:
        et.SubElement(doc, "gridstate", tag = tag).text = element
    tree = et.ElementTree(root)
    tree.write("files/output.xml") #raw xml
    x = etree.parse("files/output.xml")

    filename = f"data_{tag}"
    path = destination + '/' + filename + '.xml'
    print("aggpath:")
    print(path)
    uniq = 1
    try:
        while os.path.exists(path):
            path = destination + '/' + filename + '_' + str(uniq) + '.xml'
            uniq += 1
            print("aggpathV2:")
            print(path)

        with open(path, "wb") as f:
            f.write(etree.tostring(x, pretty_print=True))
            f.close()
    except Exception as ex:
        print(ex)