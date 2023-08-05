import xml.etree.ElementTree as ET
import os

def indent(elem, level=0):  # 자료 출처 https://goo.gl/J8VoDK
    i = "\n" + level * " " * 4
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + " " * 4
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def read_xml(annotation_file_path):
    xml_info = []
    is_ok = False
    if not os.path.exists(annotation_file_path):
        return is_ok, xml_info

    tree = ET.parse(annotation_file_path)
    root = tree.getroot()
    for member in root.findall('object'):
        class_item = member.find('name')
        if class_item is None:
            print(f'Xml item not found: name : {annotation_file_path}')
            return is_ok, xml_info
        class_name = class_item.text
        item = []
        item.append(class_name) # 0

        bndbox = member.find('bndbox')
        item.append(root.find('size').find('height').text) # 1
        item.append(root.find('size').find('width').text) # 2
        item.append(root.find('size').find('depth').text)  # 3
        item.append(bndbox.find('xmin').text) # 4
        item.append(bndbox.find('ymin').text) # 5
        item.append(bndbox.find('xmax').text) # 6
        item.append(bndbox.find('ymax').text) # 7
        xml_info.append(item)

    is_ok = True
    # xml_info (class_name, width, height, xmin, ymin, xmax, ymax)
    return is_ok, xml_info

def make_xml(class_data, image_filename):
    is_ok = False

    if len(class_data) == 0 or image_filename is None:
        print('invalid parameters')
        return is_ok, None

    already_root_created = False

    for cls in class_data:
        if already_root_created == False:
            data = ET.Element('annotation')
            element1 = ET.SubElement(data, 'folder')
            element1.text = ' '
            element1 = ET.SubElement(data, 'filename')
            element1.text = image_filename
            element1 = ET.SubElement(data, 'path')
            element1.text = image_filename
            element1 = ET.SubElement(data, 'source')
            element1_1 = ET.SubElement(element1, 'database')
            element1_1.text = 'hyl'
            element1 = ET.SubElement(data, 'size')
            element1_1 = ET.SubElement(element1, 'width')
            element1_1.text = cls[2]
            element1_1 = ET.SubElement(element1, 'height')
            element1_1.text = cls[1]
            element1_1 = ET.SubElement(element1, 'depth')
            element1_1.text = cls[3]
            element1 = ET.SubElement(data, 'segmented')
            element1.text = '0'
            already_root_created = True

        element1 = ET.SubElement(data, 'object')
        element1_1 = ET.SubElement(element1, 'name')
        element1_1.text = cls[0]
        element1_1 = ET.SubElement(element1, 'pose')
        element1_1.text = 'Unspecified'
        element1_1 = ET.SubElement(element1, 'truncated')
        element1_1.text = '0'
        element1_1 = ET.SubElement(element1, 'difficult')
        element1_1.text = '0'
        element1_1 = ET.SubElement(element1, 'bndbox')
        element1_2 = ET.SubElement(element1_1, 'xmin')
        element1_2.text = cls[4]
        element1_2 = ET.SubElement(element1_1, 'xmax')
        element1_2.text = cls[6]
        element1_2 = ET.SubElement(element1_1, 'ymin')
        element1_2.text = cls[5]
        element1_2 = ET.SubElement(element1_1, 'ymax')
        element1_2.text = cls[7]

    is_ok = True

    return is_ok, data