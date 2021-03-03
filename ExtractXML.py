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
    Mpeg7.set("xmlns:mpeg7", "urn:mpeg:mpeg7:schema:2004")
    MediaLocator = ET.SubElement(Mpeg7, 'MediaLocator')
    MediaURI = ET.SubElement(MediaLocator, 'MediaURI')
    MediaURI.text = mediaURI
    valueCSD = csd[csd.find(" "):]
    valueSCD = scd[scd.find(" "):]
    valueCLD = cld[cld.find(" "):]
    valueDCD = dcd[dcd.find(" "):]
    valueHTD = htd[htd.find(" "):]
    valueEHD = ehd[ehd.find(" "):]

    # Color Structure Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:ColorStructureType')
    Descriptor = ET.SubElement(ComplexType, 'Values')
    Descriptor.text = valueCSD

    # Scalable Color Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:ScalableColorType')
    ComplexType.set('numOfCoeff', '128')
    ComplexType.set('numOfBitPlanesDiscarded', '0')
    Descriptor = ET.SubElement(ComplexType, 'Coeff')
    Descriptor.text = valueSCD

    # Color Layout Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:ColorLayoutType')
    tokens = valueCLD.split()
    YDCCoeff = str(tokens[0])
    YACCoeff63 = " ".join(tokens[1:64])
    CbDCCoeff = str(tokens[64])
    CbACCoeff27 = " ".join(tokens[65:92])
    CrDCCoeff = str(tokens[92])
    CrACCoeff27 = " ".join(tokens[93:120])
    Descriptor = ET.SubElement(ComplexType, 'YDCCoeff')
    Descriptor.text = YDCCoeff
    Descriptor = ET.SubElement(ComplexType, 'CbDCCoeff')
    Descriptor.text = CbDCCoeff
    Descriptor = ET.SubElement(ComplexType, 'CrDCCoeff')
    Descriptor.text = CrDCCoeff
    Descriptor = ET.SubElement(ComplexType, 'YACCoeff63')
    Descriptor.text = YACCoeff63
    Descriptor = ET.SubElement(ComplexType, 'CbACCoeff27')
    Descriptor.text = CbACCoeff27
    Descriptor = ET.SubElement(ComplexType, 'CrACCoeff27')
    Descriptor.text = CrACCoeff27

    # Dominant Color Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:DominantColorType')
    tokens = valueDCD.split()
    dominantColors = int(tokens[0])
    spatialCoherency = tokens[1]
    Descriptor = ET.SubElement(ComplexType, 'SpatialCoherency')
    Descriptor.text = str(spatialCoherency)
    for i in range(0, dominantColors):
        Value = ET.SubElement(ComplexType, 'Value')
        percentage = tokens[2 + i*7]
        Descriptor = ET.SubElement(Value, 'Percentage')
        Descriptor.text = str(percentage)
        indices = " ".join(tokens[(3 + 7*i):(6 + 7*i)])
        Descriptor = ET.SubElement(Value, "Index")
        Descriptor.text = indices
        variances = " ".join(tokens[(6 + 7*i):(9 + 7*i)])
        Descriptor = ET.SubElement(Value, "ColorVariance")
        Descriptor.text = variances

    # Homogeneous Texture Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:HomogeneousTextureType')
    tokens = valueHTD.split()
    average = str(tokens[0])
    standardDeviation = str(tokens[1])
    energy = " ".join(tokens[2:32])
    energyDeviation = " ".join(tokens[32:62])
    Descriptor = ET.SubElement(ComplexType, 'Average')
    Descriptor.text = average
    Descriptor = ET.SubElement(ComplexType, 'StandardDeviation')
    Descriptor.text = standardDeviation
    Descriptor = ET.SubElement(ComplexType, 'Energy')
    Descriptor.text = energy
    Descriptor = ET.SubElement(ComplexType, 'EnergyDeviation')
    Descriptor.text = energyDeviation

    # Edge Histogram Descriptor
    ComplexType = ET.SubElement(Mpeg7, 'mpeg7:EdgeHistogramType')
    Descriptor = ET.SubElement(Mpeg7, 'BinCounts')
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
