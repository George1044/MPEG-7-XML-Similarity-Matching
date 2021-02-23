import xml.etree.ElementTree as ET

count = 1
CSD = open("CSD.txt", "r")
SCD = open("SCD.txt", "r")
CLD = open("CLD.txt", "r")
DCD = open("DCD.txt", "r")
HTD = open("HTD.txt", "r")
EHD = open("EHD.txt", "r")
for csd, scd, cld, dcd, htd, ehd in zip(CSD, SCD, CLD, DCD, HTD, EHD):
    print(count)
    mediaURI = str(count) + ".jpg"
    Mpeg7 = ET.Element('Mpeg7')
    Mpeg7.set("xmlns:urn", "urn:mpeg:mpeg7:schema:2004")
    MediaLocator = ET.SubElement(Mpeg7, 'MediaLocator')
    MediaURI = ET.SubElement(MediaLocator, 'MediaURI')
    MediaURI.text = mediaURI
    valueCSD = csd[csd.find(" "):]
    valueSCD = scd[scd.find(" "):]
    valueCLD = cld[cld.find(" "):]
    valueDCD = dcd[dcd.find(" "):]
    valueHTD = htd[htd.find(" "):]
    valueEHD = ehd[ehd.find(" "):]
    Descriptor = ET.SubElement(Mpeg7, 'urn:ColorStructureType')
    Descriptor.text = valueCSD
    Descriptor = ET.SubElement(Mpeg7, 'urn:ScalableColorType')
    Descriptor.text = valueSCD
    Descriptor = ET.SubElement(Mpeg7, 'urn:ColorLayoutType')
    Descriptor.text = valueCLD
    Descriptor = ET.SubElement(Mpeg7, 'urn:DominantColorType')
    Descriptor.text = valueDCD
    Descriptor = ET.SubElement(Mpeg7, 'urn:HomogeneousTextureType')
    Descriptor.text = valueHTD
    Descriptor = ET.SubElement(Mpeg7, 'urn:EdgeHistogramType')
    Descriptor.text = valueEHD

    myData = ET.tostring(Mpeg7, encoding="unicode")
    myFile = open("XML/" + str(count) + ".xml", "w")
    myFile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + myData)
    myFile.close()
    count += 1

# imagesNames = ""
# for i in range(1, 1000):
#     imagesNames = imagesNames + "\nimagesWang/" + str(i) + ".jpg"
#
# myFile = open("images.txt", "w")
# myFile.write(imagesNames)