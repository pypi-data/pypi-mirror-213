#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/10 8:54
# @Author  : xgy
# @Site    : 
# @File    : transform.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import json
import os
import shutil
# import traceback
import xml.etree.ElementTree as ET

from loguru import logger

from csp.datatool.image_detection.utils import is_img_exists, read_txt, gen_voc_xml


class Voc2Coco:

    def __init__(self, data_dir, output_dir):
        self.data_dir = data_dir
        self.output_dir = output_dir

        self.voc_xml_dir = os.path.join(self.data_dir, 'Annotations')
        self.voc_img_dir = os.path.join(self.data_dir, 'JPEGImages')
        self.voc_txt_dir = os.path.join(self.data_dir, 'ImageSets', 'Main')
        self.voc_label_path = os.path.join(self.data_dir, 'labels.txt')

        self.coco_json_dir = os.path.join(self.output_dir, 'annotations')
        os.makedirs(self.coco_json_dir, exist_ok=True)

    def transform(self):
        """
        1. 'ImageSets/Main' 中 a.txt 文件对应转为coco中的 a.json，并生成 a 图片文件夹
        2. 无'ImageSets/Main'时，依据Annotations，自动生成'ImageSets/Main/trainval.txt', 并转为coco的trainval.json
        3. coco json 文件的 ["categories"]["id"]字段值，有labels.txt 时，为类别所在行数，无该文件时，按类别升序排列后次序确定
        1202
        数据集格式修改，无trainval，修改第二条
        2. 无'ImageSets/Main'时，依据Annotations，自动生成'ImageSets/Main/train.txt', 并转为coco的train.json
        """

        data_types = self.drop_imageset()

        categories = self.get_categories()

        self.check_xml(data_types)

        for t in data_types:
            coco_img_dir = os.path.join(self.output_dir, t)
            os.makedirs(coco_img_dir, exist_ok=True)
            xml_files = []
            txt_file = os.path.join(self.voc_txt_dir, t + '.txt')
            txt_list = read_txt(txt_file)
            for txt in txt_list:
                filename = txt.replace('\n', '')
                xml_file = os.path.join(self.voc_xml_dir, filename + ".xml")
                xml_files.append(xml_file)
                # 把原始图像复制到目标文件夹
                img_type = is_img_exists(self.voc_img_dir, filename)
                if img_type:
                    img_file = os.path.join(self.voc_img_dir, filename + img_type)
                    to_img_file = os.path.join(coco_img_dir, filename + img_type)
                    shutil.copy(img_file, to_img_file)

            # print("Number of xml files: {} in {}".format(len(xml_files), txt_file))
            # 不限制 txt 文件的名称 1207 修改为依 t 的取值而定
            out_json = os.path.join(self.coco_json_dir, t + '.json')
            self.convert(xml_files, out_json, categories)
            # print("Success: json file has been saved in {}".format(out_json))
            # print("Success: images have been saved in {}".format(coco_img_dir))

    def check_xml(self, data_types):
        xmls_in_anno = []
        for item in os.listdir(self.voc_xml_dir):
            if item.lower().endswith(".xml"):
                xmls_in_anno.append(item)

        img_in_folder = []
        for img in os.listdir(self.voc_img_dir):
            if img.lower().endswith(".jpg") or img.lower().endswith(".jpeg") or img.lower().endswith(".png"):
                img_name = os.path.splitext(img)[0]
                img_in_folder.append(img_name)

        num_trainval = 0
        num_test = 0
        for t in data_types:
            txt_file = os.path.join(self.voc_txt_dir, t + '.txt')
            txt_list = read_txt(txt_file)
            if t == "train":
                num_trainval = len(txt_list)
            if t == "val":
                num_test = len(txt_list)
            for txt in txt_list:
                filename = txt.replace('\n', '')
                xml_name = filename + ".xml"
                if xml_name in xmls_in_anno and filename in img_in_folder:
                    continue
                elif xml_name not in xmls_in_anno and filename in img_in_folder:
                    raise FileNotFoundError(
                        "{} 存在于 {}, 但 {} 中未找到".format(filename, txt_file, self.voc_xml_dir))
                elif xml_name in xmls_in_anno and filename not in img_in_folder:
                    raise FileNotFoundError(
                        "{} 存在于 {}, 但 {} 中未找到".format(filename, txt_file, self.voc_img_dir))
                elif xml_name not in xmls_in_anno and filename not in img_in_folder:
                    raise FileNotFoundError(
                        "{} 存在于 {}, 但 {} 或 {} 中未找到".format(filename, txt_file, self.voc_xml_dir, self.voc_img_dir))

        if os.path.exists(os.path.join(self.voc_txt_dir, "train" + '.txt')):
            if num_trainval != len(xmls_in_anno):
                logger.warning("标注文件数量与train.txt中文件数量不等!")
            if num_trainval != len(img_in_folder):
                logger.warning("图片文件数量与train.txt中文件数量不等!")

        if os.path.exists(os.path.join(self.voc_txt_dir, "val" + '.txt')):
            if num_test != len(xmls_in_anno):
                logger.warning("标注文件数量与val.txt中文件数量不等!")
            if num_test != len(img_in_folder):
                logger.warning("图片文件数量与val.txt中文件数量不等!")

    def drop_imageset(self):
        """
        # 判断是否有 ImageSets/Main/ 文件夹
        # 平台导出数据集有，标准voc没有，需分别处理
        # 没有则需先创建该文件夹并生成trainval.txt
        # 1202没有则需先创建该文件夹并生成train.txt
        """
        data_types = []
        if not os.path.exists(self.voc_txt_dir):
            os.makedirs(self.voc_txt_dir, exist_ok=True)
            # trainval_path = os.path.join(self.voc_txt_dir, "trainval.txt")
            trainval_path = os.path.join(self.voc_txt_dir, "train.txt")

            for root, _, files in os.walk(self.voc_xml_dir):
                for xml_item in files:
                    if not xml_item.endswith(".xml"):
                        continue
                    xml_name = os.path.splitext(xml_item)[0]

                    with open(trainval_path, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")

        for root, _, files in os.walk(self.voc_txt_dir):
            # num_txt = len(files)
            for txt_item in files:
                txt_name = os.path.splitext(txt_item)[0]
                data_types.append(txt_name)
        return data_types

    def convert(self, xml_files, json_path, categories):

        json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}

        # categories = self.get_categories(xml_files)
        bnd_id = 0 # ["annotations"]["id"] 从0开始编号
        for i, xml_file in enumerate(xml_files):
            tree = ET.parse(xml_file)
            root = tree.getroot()

            filename = os.path.splitext(os.path.basename(xml_file))[0]
            img_type = is_img_exists(self.voc_img_dir, filename)
            filename = filename + img_type
            image_id = i
            width = int(root.find("size").find("width").text)
            height = int(root.find("size").find("height").text)
            image = {
                "file_name": filename,
                "height": height,
                "width": width,
                "id": image_id}
            json_dict["images"].append(image)

            for obj in root.findall("object"):
                # try:
                # 有问题，直接报错
                bndbox = obj.find("bndbox")
                xmin = int(bndbox.find("xmin").text) - 1 if int(bndbox.find("xmin").text) != 0 else 0
                ymin = int(bndbox.find("ymin").text) - 1 if int(bndbox.find("ymin").text) != 0 else 0
                xmax = int(bndbox.find("xmax").text)
                ymax = int(bndbox.find("ymax").text)
                category_name = obj.find("name").text

                erro_msg = "文件 {} 标注的 xmin, xmax, ymin, ymax 存在错误: {} {} {} {}".format(xml_file, xmin, xmax, ymin, ymax)
                assert xmax > xmin, erro_msg
                assert ymax > ymin, erro_msg
                o_width = abs(xmax - xmin)
                o_height = abs(ymax - ymin)
                ann = {
                    "area": o_width * o_height,
                    "iscrowd": 0,
                    "image_id": image_id,
                    "bbox": [xmin, ymin, o_width, o_height],
                    "category_id": categories[category_name],
                    "id": bnd_id,
                    "ignore": 0,
                    "segmentation": [],
                }
                json_dict["annotations"].append(ann)
                bnd_id = bnd_id + 1
                # except:
                # traceback.print_exc()
                # print(xml_file)
                # logger.error(
                #     "some errors hanppend in xmin, xmax, ymin, ymax: {} {} {} {}")

        for cate, cid in categories.items():
            cat = {"supercategory": "",
                   "id": cid,
                   "name": cate}
            json_dict["categories"].append(cat)

        with open(json_path, "w", encoding="utf-8") as fw:
            json.dump(json_dict, fw, ensure_ascii=False, indent=4)

    def get_categories(self):
        """
        Generate category name to id mapping from a list of xml files.

        Arguments:
            xml_files {list} -- A list of xml file paths.

        Returns:
            dict -- category name to id mapping.
        """

        classes_names = []
        if os.path.exists(self.voc_label_path):
            with open(self.voc_label_path, "r", encoding="utf-8") as fr:
                txt_list = fr.readlines()
                for index, item in enumerate(txt_list):
                    item_list = item.split(" ")
                    classes_names.append(item_list[0].replace("\n", ""))
                    # 应对labels.txt 只有一列的情况
                    # try:
                    #     classes_names.append(item_list[1].replace("\n", ""))
                    # except IndexError:
                    #     classes_names.append(item_list[0].replace("\n", ""))
        else:
            xml_l = []
            for root, _, xml_files in os.walk(self.voc_xml_dir):
                for xml_file in xml_files:
                    xml_file = os.path.join(root, xml_file)
                    xml_l.append(xml_file)


            for xml_file in xml_l:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for obj_item in root.findall("object"):
                    name = obj_item.find("name").text
                    if name not in classes_names:
                        classes_names.append(name)
            # 排序的目的在于使得 coco2voc 时类别名称与id能保持一致
            classes_names = sorted(classes_names)
        # logger.info("the category dict: {}".format({name: i for i, name in enumerate(classes_names)}))

        return {name: i for i, name in enumerate(classes_names)}


class Coco2Voc:

    def __init__(self, data_dir, output_dir):

        self.data_dir = data_dir
        self.output_dir = output_dir

        self.origin_anno_dir = os.path.join(self.data_dir, 'annotations')  # 原始的coco的标注存放位置

        self.dst_ImageSets_txt_dir = os.path.join(self.output_dir, 'ImageSets', 'Main')  # VOC ImageSets
        self.dst_Annotations_dir = os.path.join(self.output_dir, 'Annotations')  # VOC Annotations
        self.dst_JPEGImages_dir = os.path.join(self.output_dir, 'JPEGImages')  # VOC JPEGImages
        self.dst_labes_path = os.path.join(self.output_dir, 'labels.txt')  # VOC labels.txt

        self.category = None

        os.makedirs(self.dst_ImageSets_txt_dir, exist_ok=True)
        os.makedirs(self.dst_Annotations_dir, exist_ok=True)
        os.makedirs(self.dst_JPEGImages_dir, exist_ok=True)

    def transform(self):
        self.check_file_consistency()

        data_types = ['train', "test", "val", "trainval"]
        for dataType in data_types:
            origin_Images_dir = os.path.join(self.data_dir, dataType)
            if os.path.exists(origin_Images_dir):
                # 加载 coco 标注数据 train.json
                annFile = '{}.json'.format(dataType)
                annpath = os.path.join(self.origin_anno_dir, annFile)
                with open(annpath, "r", encoding="utf-8") as fr:
                    json_data = json.load(fr)
                if not self.category:
                    self.category = json_data["categories"]

                # 生成 voc dataType.txt
                dst_ImageSets_txt_path = os.path.join(self.dst_ImageSets_txt_dir, dataType + '.txt')
                img_filenames = []
                images = json_data["images"]
                for image in images:
                    filename = image["file_name"]
                    img_filenames.append(filename)
                with open(dst_ImageSets_txt_path, 'w', encoding='utf-8') as output:
                    for item in img_filenames:
                        item_short = os.path.splitext(item)[0]
                        output.write(item_short)
                        output.write('\n')
                # print("生成 voc {}.txt 成功".format(dataType))

                # 复制 coco 图片到 voc 图片文件夹
                for ori_img_root, _, ori_files in os.walk(origin_Images_dir):
                    for ori_file in ori_files:
                        ori_path = os.path.join(ori_img_root, ori_file)
                        dst_path = os.path.join(self.dst_JPEGImages_dir, ori_file)
                        shutil.copy(ori_path, dst_path)
                # print("复制 coco 图片到 voc 图片文件夹 成功")

                # json 转xml
                self.json2xml(json_data)
                # print("json 转xml 成功")

        # 生成 labels.txt
        self.gen_labels()

    def check_file_consistency(self):
        data_types = ['train', "test", "val", "trainval"]
        for dataType in data_types:
            origin_Images_dir = os.path.join(self.data_dir, dataType)
            if os.path.exists(origin_Images_dir):
                img_names_in_folder = []
                for img in os.listdir(origin_Images_dir):
                    if img.lower().endswith(".jpg") or img.lower().endswith(".jpeg") or img.lower().endswith(".png"):
                        img_names_in_folder.append(img)

                # 加载 coco 标注数据 train.json
                # img_names_in_json = []
                annFile = '{}.json'.format(dataType)
                annpath = os.path.join(self.origin_anno_dir, annFile)
                with open(annpath, "r", encoding="utf-8") as fr:
                    json_data = json.load(fr)
                num_img_in_json = len(json_data["images"])

                for item in json_data["images"]:
                    item_name = item["file_name"]
                    if item_name in img_names_in_folder:
                        continue
                    else:
                        raise FileNotFoundError("{} 存在于 {}, 但 {} 中无法找到".format(item, annpath, origin_Images_dir))
                if len(img_names_in_folder) != num_img_in_json:
                    logger.warning("{} 中的图片数量与 {} 中图片数量不等!".format(annpath, origin_Images_dir))

    def gen_labels(self):
        category_l = []
        num_category = len(self.category)
        for num in range(num_category):
            # 生成labels.txt，确保按"id"大小依次写入 labels.txt
            for item in self.category:
                if item["id"] == num:
                    category_l.append(item["name"])
        with open(self.dst_labes_path, "w", encoding="utf-8") as fw:
            for index, cate in enumerate(category_l):
                if index == num_category - 1:
                    fw.write(cate)
                else:
                    fw.write(cate + "\n")

    def json2xml(self, data):
        images = data["images"]
        annotations = data["annotations"]
        categories = data["categories"]

        category_dict = {}
        for category in categories:
            category_dict[category["id"]] = category["name"]

        for img in images:
            file_name = img["file_name"]
            img_id = img["id"]
            height = img["height"]
            width = img["width"]

            xml_name = os.path.splitext(file_name)[0] + ".xml"
            xml_path = os.path.join(self.dst_Annotations_dir, xml_name)
            jpg_path = os.path.join(self.dst_JPEGImages_dir, file_name)

            # xml 配置
            xml_boxes = []
            for annotation in annotations:
                image_id = annotation["image_id"]
                if image_id == img_id:
                    bbox = annotation["bbox"]
                    box = {"xmin": bbox[0] + 1,
                           "ymin": bbox[1] + 1,
                           "xmax": bbox[0] + bbox[2],
                           "ymax": bbox[1] + bbox[3],
                           "category": category_dict[annotation["category_id"]]}
                    xml_boxes.append(box)
            gen_voc_xml(xml_boxes, jpg_path, width, height, xml_path)


def det_transform(folder, form, output, drop=True):
    if form.upper() == "VOC":
        data_transform = Voc2Coco(data_dir=folder, output_dir=output)
    elif form.upper() == "COCO":
        data_transform = Coco2Voc(data_dir=folder, output_dir=output)
    else:
        raise KeyError("form 参数值必须为 VOC 或 COCO")
    try:
        data_transform.transform()
    except Exception as ae:
        print(str(ae))
        if drop:
            shutil.rmtree(output)
        raise Exception("转换过程内部错误")


if __name__ == '__main__':
    print("start")
