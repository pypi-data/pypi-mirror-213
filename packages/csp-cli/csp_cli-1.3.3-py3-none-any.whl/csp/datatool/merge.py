#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/11/3 15:43
# @Author  : xgy
# @Site    : 
# @File    : merge.py
# @Software: PyCharm
# @python version: 3.7.13
"""
import json
import os
import shutil
import xml.etree.ElementTree as ET
from csp.common.utils import check_jsonl


def text_entity(output, *datasets):
    id_all = []
    result = []
    for index, dataset in enumerate(datasets):
        if not os.path.isdir(dataset):
            raise IsADirectoryError("数据集必须为目录")
        data, _ = check_jsonl(dataset)
        for item in data:
            id = item["id"]
            if id in id_all:
                item["id"] = str(index) + "_" + str(id)
                result.append(item)
            else:
                result.append(item)
                id_all.append(id)

    os.makedirs(output, exist_ok=True)
    json_path = os.path.join(output, "ner.json")
    with open(json_path, "w", encoding="utf-8") as fw:
        for res in result:
            fw.write(json.dumps(res, ensure_ascii=False))
            fw.write("\n")


def det_voc(output, *datasets):

    os.makedirs(output, exist_ok=True)
    out_Annotations = os.path.join(output, "Annotations")
    out_ImageSets = os.path.join(output, "ImageSets", "Main")
    out_JPEGImages = os.path.join(output, "JPEGImages")
    out_labels = os.path.join(output, "labels.txt")
    out_txt = os.path.join(out_ImageSets, "train.txt")

    if os.path.exists(out_Annotations):
        shutil.rmtree(out_Annotations)
    if os.path.exists(out_ImageSets):
        shutil.rmtree(out_ImageSets)
    if os.path.exists(out_JPEGImages):
        shutil.rmtree(out_JPEGImages)

    os.makedirs(out_Annotations, exist_ok=True)
    os.makedirs(out_ImageSets, exist_ok=True)
    os.makedirs(out_JPEGImages, exist_ok=True)

    result = []
    labels_l = []
    file_name_l = []
    img_name_l = []

    for index, dataset in enumerate(datasets):
        item_Annotations = os.path.join(dataset, "Annotations")
        # item_ImageSets = os.path.join(dataset, "ImageSets", "Main")
        item_JPEGImages = os.path.join(dataset, "JPEGImages")
        # item_labels = os.path.join(dataset, "labels.txt")

        # Annotations 合并
        for root, _, files in os.walk(item_Annotations):
            for xml in files:
                xml_name_s = os.path.splitext(xml)[0]
                ori_path = os.path.join(root, xml)

                # 读取原来的xml文件
                tree = ET.parse(ori_path)
                xmlroot = tree.getroot()
                # 读取分类
                for obj in xmlroot.findall("object"):
                    label = obj.find("name").text
                    if label not in labels_l:
                        labels_l.append(label)

                if xml_name_s in file_name_l:
                    n_xml = str(index) + "_" + xml
                    det_path = os.path.join(out_Annotations, n_xml)
                    # 修改xml并保存
                    path = xmlroot.find("path")
                    path_text_old = path.text
                    text_old_l = path_text_old.split("\\")
                    path.text = "\\".join(text_old_l[:-1]) + "\\" + str(index) + "_" + text_old_l[-1]
                    filename = xmlroot.find("filename")
                    filename_text_old = filename.text
                    filename.text = str(index) + "_" + filename_text_old
                    tree.write(det_path)
                    result.append(str(index) + "_" + xml_name_s)
                else:
                    det_path = os.path.join(out_Annotations, xml)
                    shutil.copy(ori_path, det_path)
                    file_name_l.append(xml_name_s)
                    result.append(xml_name_s)

        # JPEGImages 合并
        for root, _, files in os.walk(item_JPEGImages):
            for img in files:
                img_name_s = os.path.splitext(img)[0]
                ori_path = os.path.join(root, img)
                # if img_name_s in file_name_l or img_name_s in img_name_l:
                if img_name_s in img_name_l:
                    n_img = str(index) + "_" + img
                    det_path = os.path.join(out_JPEGImages, n_img)
                    shutil.copy(ori_path, det_path)
                else:
                    det_path = os.path.join(out_JPEGImages, img)
                    shutil.copy(ori_path, det_path)
                    img_name_l.append(img_name_s)

    # ImageSets/Main/train.txt 生成
    if result:
        with open(out_txt, "w", encoding="utf-8") as fw1:
            for item in result:
                fw1.write(item)
                fw1.write("\n")
    # labels.txt 生成
    if labels_l:
        with open(out_labels, "w", encoding="utf-8") as fw2:
            for item in labels_l:
                fw2.write(item)
                fw2.write("\n")


def det_coco(output, *datasets):

    os.makedirs(output, exist_ok=True)
    out_Annotations = os.path.join(output, "annotations")
    out_JPEGImages = os.path.join(output, "train")
    out_json = os.path.join(out_Annotations, "train.json")

    if os.path.exists(out_Annotations):
        shutil.rmtree(out_Annotations)
    if os.path.exists(out_JPEGImages):
        shutil.rmtree(out_JPEGImages)

    os.makedirs(out_Annotations, exist_ok=True)
    os.makedirs(out_JPEGImages, exist_ok=True)

    i = 0 # ”annotations“ 中 id 重新标号
    file_name_l = []
    img_name_l = []
    category_l = []
    result = {"images": [],
              "type": "instances",
              "annotations": [],
              "categories": []}
    for index, dataset in enumerate(datasets):
        # annotations 合并
        item_annotations = os.path.join(dataset, "annotations")
        for item in os.listdir(item_annotations):
            if item.lower().endswith(".json"):
                json_path = os.path.join(item_annotations, item)
                with open(json_path, "r", encoding="utf-8") as fr:
                    data = json.load(fr)

                new_img_id = {}
                images = data["images"]
                for img in images:
                    file_name = img["file_name"]
                    id = img["id"]
                    new_id = len(result["images"])
                    new_img_id[str(id)] = str(new_id)
                    img["id"] = new_id
                    if file_name.lower() in file_name_l:
                        img["file_name"] = str(index) + "_" + file_name
                        result["images"].append(img)
                    else:
                        result["images"].append(img)
                        file_name_l.append(file_name)

                new_cate_id = {}
                categories = data["categories"]
                for cate in categories:
                    name = cate["name"]
                    old_id = cate["id"]
                    if name in category_l:
                        new_id = category_l.index(name)
                        new_cate_id[str(old_id)] = str(new_id)
                    else:
                        new_id = len(result["categories"])
                        new_cate_id[str(old_id)] = str(new_id)
                        cate["id"] = new_id
                        result["categories"].append(cate)
                        category_l.append(name)

                annotations = data["annotations"]
                for anno in annotations:
                    anno["id"] = i
                    anno["image_id"] = int(new_img_id[str(anno["image_id"])])
                    anno["category_id"] = int(new_cate_id[str(anno["category_id"])])
                    result["annotations"].append(anno)

        # 图片文件夹 合并
        for item in os.listdir(dataset):
            if item in ["trainval", "train", "val", "test", "eval", "eva"]:
                img_folder = os.path.join(dataset, item)
                for img in os.listdir(img_folder):
                    ori_path = os.path.join(img_folder, img)
                    if img.lower() in img_name_l:
                        new_img_name = str(index) + "_" + img
                        det_path = os.path.join(out_JPEGImages, new_img_name)
                        shutil.copy(ori_path, det_path)
                    else:
                        det_path = os.path.join(out_JPEGImages, img)
                        shutil.copy(ori_path, det_path)
                        img_name_l.append(img.lower())

    with open(out_json, "w", encoding="utf-8") as fw:
        json.dump(result, fw, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print("start")
