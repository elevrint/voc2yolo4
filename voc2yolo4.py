import xml
import xml.etree.ElementTree as ET
import os, sys, glob

def get_label_map(label_map_path):

    label_map = {}
    with open(label_map_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        for i, line in enumerate(lines):
            a = line.splitlines()[0]
            label_map[a] = i
    return label_map


def parse_xml(img, file, label_map):
    tree = ET.parse(file)
    
    root = tree.getroot()
    obs = root.findall('object')

    annotation = list()

    for i, ob in enumerate(obs):

        cnt = int()

        bndbox = ob.find('bndbox')
        name = ob.find('name').text
        name_idx = label_map[name]
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text

        tmp = xmin + "," + ymin + "," + str((int(xmax) - int(xmin))) + "," + str((int(ymax) - int(ymin))) + "," + str(name_idx)
        
        annotation.append(tmp)
    
    anno = img + " " + " ".join(annotation)

    return anno

annot_path = "C:/Users/G/Desktop/S_work/annot/*.xml"
img_path = "C:/Users/G/Desktop/S_work/img/*.jpg"

label_map_path = "./labelmap.names"
files_path = sorted(glob.glob(annot_path, recursive=True), key=os.path.getctime)
imgs_path = sorted(glob.glob(img_path, recursive=True), key=os.path.getctime)

label_map = get_label_map(label_map_path)
with open("C:/Users/G/Desktop/S_work/annot.txt",'w') as f:
    for img, file in zip(imgs_path, files_path):
        result_parse = parse_xml(img, file, label_map)
        print(result_parse)
        f.write(result_parse + "\n")

