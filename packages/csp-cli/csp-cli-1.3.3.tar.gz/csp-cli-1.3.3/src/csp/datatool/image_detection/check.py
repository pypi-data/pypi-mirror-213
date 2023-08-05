#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/28 16:08
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import json
import os
import xml.etree.ElementTree as ET

from loguru import logger

from csp.datatool.image_detection.utils import CheckDataset


class CheckVoc(CheckDataset):

    def __init__(self, dataset_dir, form="VOC", output_dir=None):
        super().__init__(dataset_dir, form, output_dir)
        self.labels_path = os.path.join(self.dataset_dir, "labels.txt")
        self.labels = []

    def get_labels(self):
        labels = []
        with open(self.labels_path, "r", encoding="utf-8") as fr:
            txt_list = fr.readlines()
            for index, item in enumerate(txt_list):
                item_list = item.split(" ")
                labels.append(item_list[0].replace("\n", ""))
        self.labels = labels

    # 判断标注数据(.xml)是否存在错误
    def is_anno_break(self):
        """
        需保证数据集根目录下存在labels.txt，用于判断是否存在类别错误
        """
        super().clear_out()
        self.get_labels()

        error_list_all = []

        for xml in os.listdir(self.anno_dir):
            flag_base = True
            flag_size = True
            flag_cls = True
            flag_no_obj = True
            flag_box = True

            xml_name = os.path.splitext(xml)[0]
            xml_path = os.path.join(self.anno_dir, xml)
            tree = ET.parse(xml_path)
            annotation = tree.getroot()  # 获取根节点， Element类

            # 图片尺寸为 0 判断
            size = annotation.find("size")
            if not size:
                flag_size = False
                with open(self.size_error_txt, "a+", encoding="utf-8") as fw:
                    if size is None:
                        result = {"file_name": xml_name, "message": "没有 'size' 字段", "data": {}}
                        fw.write(json.dumps(result, ensure_ascii=False))
                        fw.write("\n")

            # 基础 字段判断
            for item in ["folder", "filename", "path", "size", "source", "segmented"]:
                len_item = len(list(annotation.iter(item)))
                if len_item > 1:
                    # 字段重复
                    flag_base = False
                    with open(self.base_info_error_txt, "a+", encoding="utf-8") as fw:
                        result = {"file_name": xml_name, "message": "'{}' 字段出现不止一次".format(item), "data": {}}
                        fw.write(json.dumps(result, ensure_ascii=False))
                        fw.write("\n")
                elif len_item == 0:
                    # 字段不存在
                    flag_base = False
                    with open(self.base_info_error_txt, "a+", encoding="utf-8") as fw:
                        result = {"file_name": xml_name, "message": "没有 '{}' 字段".format(item), "data": {}}
                        fw.write(json.dumps(result, ensure_ascii=False))
                        fw.write("\n")
                else:
                    res = annotation.find(item)
                    text = res.text
                    # 字段为空
                    if not text:
                        flag_base = False
                        with open(self.base_info_error_txt, "a+", encoding="utf-8") as fw:
                            result = {"file_name": xml_name, "message": "'{}' 为空".format(item), "data": {}}
                            fw.write(json.dumps(result, ensure_ascii=False))
                            fw.write("\n")
            try:
                width = size.find("width")
            except ValueError:
                width = None
            except AttributeError:
                width = None

            try:
                height = size.find("width")
            except ValueError:
                height = None
            except AttributeError:
                height = None

            try:
                width_text = width.text
            except AttributeError:
                width_text = None
            try:
                height_text = height.text
            except AttributeError:
                height_text = None

            if not width_text or not height_text or width_text == "0" or height_text == "0":
                with open(self.size_error_txt, "a+", encoding="utf-8") as fw:
                    result = {"file_name": xml_name, "message": "width/height 为空或不存在",
                              "data": {"width": width_text,
                                       "height": height_text}}
                    fw.write(json.dumps(result, ensure_ascii=False))
                    fw.write("\n")
                flag_size = False


            # 判断 object 节点相关字段
            # 判断有无 object 节点
            obj_flag = annotation.find("object")
            if obj_flag:
                for obj in annotation.iter('object'):
                    try:
                        cls = obj.find('name').text
                    except AttributeError:
                        with open(self.cls_error_txt, "a+", encoding="utf-8") as fw:
                            result = {"file_name": xml_name,
                                      "message": "没有 'name' 字段",
                                      "data": {}}
                            fw.write(json.dumps(result, ensure_ascii=False))
                            fw.write("\n")
                    else:
                        # 类别错误判断
                        if cls not in self.labels:
                            flag_cls = False
                            with open(self.cls_error_txt, "a+", encoding="utf-8") as fw:
                                result = {"file_name": xml_name,
                                          "message": "标签不再标签表中",
                                          "data": {"name": cls}}
                                fw.write(json.dumps(result, ensure_ascii=False))
                                fw.write("\n")

                    # box 坐标值错误判断
                    bndbox = obj.find('bndbox')
                    if not bndbox:
                        # 无 bndbox 节点
                        flag_box = False
                        with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                            result = {"file_name": xml_name,
                                      "message": "没有 'bndbox' 字段",
                                      "data": {}}
                            fw.write(json.dumps(result, ensure_ascii=False))
                            fw.write("\n")
                    else:
                        try:
                            xmin = int(bndbox.find('xmin').text)
                        except ValueError:
                            xmin = None
                        except AttributeError:
                            xmin = None
                        try:
                            ymin = int(bndbox.find('ymin').text)
                        except ValueError:
                            ymin = None
                        except AttributeError:
                            ymin = None
                        try:
                            xmax = int(bndbox.find('xmax').text)
                        except ValueError:
                            xmax = None
                        except AttributeError:
                            xmax = None
                        try:
                            ymax = int(bndbox.find('ymax').text)
                        except ValueError:
                            ymax = None
                        except AttributeError:
                            ymax = None

                        if not xmin or not ymin or not xmax or not ymax:
                            flag_box = False
                            with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                                result = {"file_name": xml_name,
                                          "message": "一些属性不存在或为0",
                                          "data": {"xmin": xmin,
                                                   "ymin": ymin,
                                                   "xmax": xmax,
                                                   "ymax": ymax}}
                                fw.write(json.dumps(result, ensure_ascii=False))
                                fw.write("\n")

                        try:
                            # 无 xmin 等节点
                            xmin = int(bndbox.find('xmin').text)
                            ymin = int(bndbox.find('ymin').text)
                            xmax = int(bndbox.find('xmax').text)
                            ymax = int(bndbox.find('ymax').text)
                        except ValueError:
                            flag_box = False
                        except AttributeError:
                            flag_box = False
                        else:
                            if width is None and height is None:
                                if any(item < 0 for item in [xmin, ymin, xmax, ymax]) or xmin >= xmax or ymin >= ymax:
                                    flag_box = False
                                    with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                                        result = {"file_name": xml_name,
                                                  "message": "一些属性为负数或超出边界",
                                                  "data": {"xmin": xmin,
                                                           "ymin": ymin,
                                                           "xmax": xmax,
                                                           "ymax": ymax}}
                                        fw.write(json.dumps(result, ensure_ascii=False))
                                        fw.write("\n")
                            # if width.text and height.text:
                            if width and height:
                                # 坐标值 错误
                                if xmin < 0 or xmax < 0 or ymin < 0 or ymax < 0 or xmin >= xmax or ymin >= ymax or xmax > int(width.text) or ymax > int(height.text):
                                    flag_box = False
                                    with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                                        result = {"file_name": xml_name,
                                                  "message": "一些属性为负数或超出边界",
                                                  "data": {"xmin": xmin,
                                                           "ymin": ymin,
                                                           "xmax": xmax,
                                                           "ymax": ymax}}
                                        fw.write(json.dumps(result, ensure_ascii=False))
                                        fw.write("\n")

            else:
                flag_no_obj = False
                with open(self.no_obj_txt, "a+", encoding="utf-8") as fw:
                    result = {"file_name": xml_name,
                              "message": "没有 'object' 字段",
                              "data": {}}
                    fw.write(json.dumps(result, ensure_ascii=False))
                    fw.write("\n")

            if not flag_size or not flag_cls or not flag_no_obj or not flag_box or not flag_base:
                if xml_name not in error_list_all:
                    with open(self.error_list_txt, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")
                    error_list_all.append(xml_name)
        if os.path.exists(self.error_list_txt):
            logger.info("标注错误的文件名已保存至 {}".format(self.error_list_txt))
        else:
            print("标注文件未发现错误")

    def is_num_break(self):
        """
        判断标注数据xml文件数量、train.txt内文件名数量、原始图片数量是否一致
        """
        num_xml = 0
        for item in os.listdir(self.anno_dir):
            if item.lower().endswith(".xml"):
                num_xml += 1

        num_img = 0
        img_folder = os.path.join(self.dataset_dir, self.img_folder_names[0])
        for item in os.listdir(img_folder):
            if str(item).lower().endswith(".jpg") or str(item).lower().endswith(".png") or str(item).lower().endswith(".jpeg"):
                num_img += 1

        logger.info("{} 份标注文件包含在 {} 中, {} 张图片包含在 {} 中".format(num_xml, self.anno_dir, num_img, img_folder))

        num_txt_all = 0
        txt_folder = os.path.join(self.dataset_dir, "ImageSets/Main")
        if os.path.exists(txt_folder):
            for item in ["train", "test", "trainval", "val"]:
                txt_path = os.path.join(txt_folder, item + ".txt")
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as fr:
                        num_txt = len(fr.readlines())
                        logger.info("there are {} files in {}".format(num_txt, txt_path))
                        num_txt_all = num_txt_all + num_txt
                # else:
                #     logger.info("文件不存在 {}".format(txt_path))
        else:
            logger.info("{} 不存在".format(txt_folder))

        if not num_txt_all:
            if num_xml != num_img:
                logger.warning("annotations 与 images 文件数量不相等")
            if num_xml > num_img:
                return False
        else:
            if num_xml != num_img:
                logger.warning("annotations 与 images 文件数量不相等")
            if num_xml != num_txt_all:
                logger.warning("annotations 文件数量 与 {} 文件总和不一致".format(txt_folder))
            return False

        return True


class CheckCoco(CheckDataset):

    def __init__(self, dataset_dir, form="COCO", output_dir=None):
        super().__init__(dataset_dir, form, output_dir)

    # 判断标注数据(.json)是否存在错误
    def is_anno_break(self):
        super().clear_out()

        for item in os.listdir(self.dataset_dir):
            if item in self.img_folder_names:
                json_path = os.path.join(self.anno_dir, item + ".json")
                with open(json_path, "r", encoding="utf-8") as fr:
                    json_data = json.load(fr)

                error_all_flag = []
                error_all_list = []
                size_error_list = []
                box_error_list = []
                cls_error_list = []

                # file_error_list = []
                # img_id: [file_name, w, h] 键值对
                # try:
                #     images = json_data["images"]
                # except AttributeError:
                #     logger.error("there is no 'images' in {}".format(json_path))
                #     result = {"file_name": json_path, "message": "no 'images'", "data": {}}
                #     file_error_list.append(result)
                # else:
                images = json_data["images"]
                img_dict = {}
                for img in images:
                    file_name_short = os.path.splitext(img["file_name"])[0]

                    height = img.get("height", None)
                    width = img.get("width", None)
                    img_dict[img["id"]] = [file_name_short, width, height]

                    # w, h 为 0 或 不存在
                    if not height or not width:
                        if file_name_short not in error_all_flag:
                            # size_error_list.append(file_name_short)
                            # error_item = [file_name_short, item]
                            error_item = {"json_name": json_path, "message": "图片尺寸错误", "data": img}
                            size_error_list.append(error_item)
                            error_all_flag.append(file_name_short)

                        if file_name_short not in error_all_flag:
                            # error_all_list.append(file_name_short)
                            error_item = {"error_file_name": file_name_short}
                            error_all_list.append(error_item)
                            error_all_flag.append(file_name_short)

                # 类别 id 列表
                categories = json_data["categories"]
                category_id_list = []
                for category in categories:
                    category_id = category["id"]
                    category_id_list.append(category_id)

                annotations = json_data["annotations"]
                for anno in annotations:
                    image_id = anno["image_id"]
                    img_name = img_dict[image_id][0]
                    img_w = img_dict[image_id][1]
                    img_h = img_dict[image_id][2]

                    category_id = anno["category_id"]
                    # 非法类别 id
                    if category_id not in category_id_list:
                        # if img_name not in cls_error_list:
                            # error_item = [img_name, item]
                        error_item = {"json_name": json_path, "message": "标签id错误", "data": {"category_id": category_id}}
                        cls_error_list.append(error_item)
                        if img_name not in error_all_flag:
                            # error_all_list.append(img_name)
                            error_item = {"error_file_name": img_name}
                            error_all_list.append(error_item)
                            error_all_flag.append(img_name)
                    try:
                        # 因采用 x1, y1, w, h 排列方式，标注框只可能存在负数、超过边界两种错误
                        bbox = anno["bbox"]
                        x1, y1, w, h = bbox
                        x2 = x1 + w
                        y2 = y1 + h
                    except Exception:
                        # bbox 字段缺失或不完整
                        # if img_name not in box_error_list:
                            # box_error_list.append(img_name)
                        error_item = {"json_name": json_path, "message": "bbox 字段缺失或不完整", "data": anno}
                        box_error_list.append(error_item)
                        if img_name not in error_all_flag:
                            # error_all_list.append(img_name)
                            # error_item = [img_name, item]
                            error_item = {"error_file_name": img_name}
                            error_all_list.append(error_item)
                            error_all_flag.append(img_name)
                    else:
                        # w, h 值正常
                        if img_w and img_h:
                            # 坐标值异常
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or x2 > img_w or y2 > img_h:
                                # if img_name not in box_error_list:
                                #     # box_error_list.append(img_name)
                                #     error_item = [img_name, item]
                                #     box_error_list.append(error_item)
                                error_item = {"json_name": json_path, "message": "w/h 值正常但 bbox 值错误", "data": anno}
                                box_error_list.append(error_item)
                                if img_name not in error_all_flag:
                                    # error_all_list.append(img_name)
                                    # error_item = [img_name, item]
                                    error_item = {"error_file_name": img_name}
                                    error_all_list.append(error_item)
                                    error_all_flag.append(img_name)
                        # w 值正常， h 异常
                        elif img_w and not img_h:
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or x2 > img_w:
                                # if img_name not in box_error_list:
                                #     # box_error_list.append(img_name)
                                #     error_item = [img_name, item]
                                #     box_error_list.append(error_item)
                                error_item = {"json_name": json_path, "message": "w值正常，h值异常，bbox值错误", "data": anno}
                                box_error_list.append(error_item)
                                if img_name not in error_all_flag:
                                    # error_all_list.append(img_name)
                                    # error_item = [img_name, item]
                                    error_item = {"error_file_name": img_name}
                                    error_all_list.append(error_item)
                                    error_all_flag.append(img_name)
                        # h 值正常， w 异常
                        elif img_h and not img_w:
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or y2 > img_h:
                                # if img_name not in box_error_list:
                                    # box_error_list.append(img_name)
                                    # error_item = [img_name, item]
                                    # box_error_list.append(error_item)
                                error_item = {"json_name": json_path, "message": "h值正常，w值异常，bbox值错误", "data": anno}
                                box_error_list.append(error_item)
                                if img_name not in error_all_flag:
                                    # error_all_list.append(img_name)
                                    # error_item = [img_name, item]
                                    error_item = {"error_file_name": img_name}
                                    error_all_list.append(error_item)
                                    error_all_flag.append(img_name)
                # 写入对应文件中（.txt）
                result_list = [error_all_list, size_error_list, box_error_list, cls_error_list]
                txt_path_list = [self.error_list_txt, self.size_error_txt, self.box_error_txt, self.cls_error_txt]

                for result, txt_path in zip(result_list, txt_path_list):
                    if result:
                        with open(txt_path, "a+",  encoding="utf-8") as fw:
                            for result_item in result:
                                # fw.write(result_item[0] + "," + result_item[1])
                                fw.write(json.dumps(result_item, ensure_ascii=False))
                                fw.write("\n")

        if os.path.exists(self.error_list_txt):
            logger.info("标注错误文件名已保存至 {}".format(self.error_list_txt))
        else:
            print("标注文件未发现错误")

    def is_num_break(self):
        """
        判断标注数据json内文件数量、train内图片数量是否一致
        """
        for item in self.img_folder_names:
            json_path = os.path.join(self.anno_dir, item + ".json")
            img_path = os.path.join(self.dataset_dir, item)

            if os.path.exists(json_path) and os.path.exists(img_path):
                num_anno = 0
                with open(json_path, encoding="utf-8") as fr:
                    data = json.load(fr)
                    num_anno = len(data["images"])

                num_img = 0
                for item in os.listdir(img_path):
                    if item.lower().endswith(".jpg") or item.lower().endswith(".png") or item.lower().endswith(".jpeg"):
                        num_img += 1

                logger.info("{} 份标注文件包含在 {} 中, {} 张图片包含在 {} 中".format(num_anno, json_path, num_img, img_path))

                if num_anno != num_img:
                    logger.warning("json文件内图片数量与图片文件夹内图片数量不一致")
                if num_anno > num_img:
                    return False


def det_check(folder, form, output):
    if form.upper() == "VOC":
        data_check = CheckVoc(dataset_dir=folder, form="VOC", output_dir=output)
    elif form.upper() == "COCO":
        data_check = CheckCoco(dataset_dir=folder, form="COCO", output_dir=output)
    else:
        raise KeyError("form 参数必须是VOC或COCO")
    data_check.is_num_break()
    data_check.is_anno_break()
    data_check.is_img_break()


if __name__ == '__main__':
    print("start")
