import glob
import os
import xml.etree.cElementTree as ET

import cv2 as cv
import numpy as np

descriptors_ehd = np.empty(shape=[0, 80])
descriptors_clt = np.empty(shape=[0, 120])
descriptors_cst = np.empty(shape=[0, 64])
descriptors_htt = np.empty(shape=[0, 62])
os.chdir('./XMLSIMPLE')

###Processing ALL descriptors
all_files = glob.glob("*.xml")
for file in all_files:
    tree = ET.parse(file)
    root_xml = tree.getroot()
    edhs = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}EdgeHistogramType')
    for edh in edhs:
        line = edh.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        descriptors_ehd = np.concatenate((descriptors_ehd, np.array([numbers])))
    ColorLayoutTypes = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}ColorLayoutType')
    for clt in ColorLayoutTypes:
        line = clt.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        descriptors_clt = np.concatenate((descriptors_clt, np.array([numbers])))
    csts = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}ColorStructureType')
    for cst in csts:
        line = cst.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        descriptors_cst = np.concatenate((descriptors_cst, np.array([numbers])))
    htts = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}HomogeneousTextureType')
    for htt in htts:
        line = htt.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        descriptors_htt = np.concatenate((descriptors_htt, np.array([numbers])))

###Choosing one reference image
while True:
    number = input('Enter photo number: ')
    if(number == '0'):
        break
    file = str(number)+'.xml'
    file_visualize_reference = cv.imread('../imagesWang/' +file.replace('.xml', '') + '.jpg')
    cv.imshow('Reference', file_visualize_reference)
    tree = ET.parse(file)
    root_xml = tree.getroot()
    edhs = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}EdgeHistogramType')
    for edh in edhs:
        line = edh.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        chosenDescriptor_ehd = np.array(numbers)
    ColorLayoutTypes = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}ColorLayoutType')
    for clt in ColorLayoutTypes:
        line = clt.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        chosenDescriptor_clt = np.array(numbers)
    csts = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}ColorStructureType')
    for cst in csts:
        line = cst.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        chosenDescriptor_cst = np.array(numbers)
    htts = root_xml.findall('{urn:mpeg:mpeg7:schema:2004}HomogeneousTextureType')
    for htt in htts:
        line = htt.text
        number_strings = line.split()
        numbers = [float(n) for n in number_strings]
        chosenDescriptor_htt = np.array(numbers)




    ###Processing distance arrays
    distarr_ehd = []
    distarr_clt = []
    distarr_cst = []
    distarr_htt = []
    #Check closest index
    for descriptor in descriptors_ehd:
        sum = np.sum(np.abs(np.subtract(chosenDescriptor_ehd, descriptor)))
        distarr_ehd.append(sum)
    for descriptor in descriptors_clt:
        sum = np.sum(np.abs(np.subtract(chosenDescriptor_clt, descriptor)))
        distarr_clt.append(sum)
    for descriptor in descriptors_cst:
        sum = np.sum(np.abs(np.subtract(chosenDescriptor_cst, descriptor)))
        distarr_cst.append(sum)
    for descriptor in descriptors_htt:
        sum = np.sum(np.abs(np.subtract(chosenDescriptor_htt, descriptor)))
        distarr_htt.append(sum)

    k = 2
    print('original image: ',file)


    distarr = np.array(distarr_ehd)
    idx = np.argpartition(distarr, k)
    idx = idx[:k]
    print('Indices of the '+str(k-1)+' closest descriptors_ehd is: ')
    for i in idx[1:]:
        print(all_files[i])

    distarr = np.array(distarr_clt)
    idx = np.argpartition(distarr, k)
    idx = idx[:k]
    print('Indices of the '+str(k-1)+' closest descriptors_clt is: ')
    for i in idx[1:]:
        print(all_files[i])

    distarr = np.array(distarr_cst)
    idx = np.argpartition(distarr, k)
    idx = idx[:k]
    print('Indices of the '+str(k-1)+' closest descriptors_cst is: ')
    for i in idx[1:]:
        print(all_files[i])

    distarr = np.array(distarr_htt)
    idx = np.argpartition(distarr, k)
    idx = idx[:k]
    print('Indices of the '+str(k-1)+' closest descriptors_htt is: ')
    for i in idx[1:]:
        print(all_files[i])

    ###Normalizing
    distarr_ehd_n = distarr_ehd/np.max(distarr_ehd)
    distarr_clt_n = distarr_clt/np.max(distarr_clt)
    distarr_cst_n = distarr_cst/np.max(distarr_cst)
    distarr_htt_n = distarr_htt/np.max(distarr_htt)


    distarr_all = []

    for i in range(len(distarr_clt_n)):
        distarr_all.append( distarr_ehd_n[i]+distarr_cst_n[i]+distarr_htt_n[i])


    distarr = np.array(distarr_all)
    idx = np.argpartition(distarr, k)
    idx = idx[:k]
    print('Indices of the '+str(k-1)+' closest all descriptors is: ')



    for j in idx[1:]:
        print(all_files[j])
        file_visualize = cv.imread('../imagesWang/' + all_files[j].replace('.xml', '') + '.jpg')
        cv.imshow('test', file_visualize)


    cv.waitKey()