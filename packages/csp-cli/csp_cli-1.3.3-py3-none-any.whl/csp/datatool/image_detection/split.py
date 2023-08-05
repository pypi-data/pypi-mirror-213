#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/7 11:04
# @Author  : xgy
# @Site    : 
# @File    : split.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import shutil
import random
import json
import sys

from loguru import logger

from csp.datatool.image_detection.utils import load_json


class VocSplit:

    def __init__(self, data_dir, ratios=None, output=None):
        self.data_dir = data_dir
        self.ratios = ratios
        self.output = output

    def split(self, mode=None):
        """
        VOC 数据集切分，优先级：
        1. train.txt, val.txt 同时存在删除后才能切分
        2. trainval.txt, train.txt 同时存在需指定其一作为切分依据（mode）
        3. trainval.txt, train.txt 有且只有一个时，以存在的文件为切分依据
        4. 无 txt 文件时，以Annotations 文件夹中所有文件为切分依据
        5. 切分后数据为train.txt, val.txt, 即原 train.txt 会被覆盖，trainval.txt 会被保留
        1202
        修改了数据集标准格式，不再有trainval，则必须含有train(若没有则基于所有数据自动生成train.txt)，删除mode参数
        """

        if self.ratios is None:
            train_ratio = 0.9
        else:
            train_ratio = self.ratios

        xmlfilepath = os.path.join(self.data_dir, 'Annotations')
        txtsavepath = os.path.join(self.data_dir, 'ImageSets/Main')
        imgsavepath = os.path.join(self.data_dir, 'JPEGImages')
        train_path = os.path.join(txtsavepath, "train.txt")
        label_path = os.path.join(self.data_dir, "labels.txt")

        out_train = os.path.join(self.output, "train")
        out_train_annotations = os.path.join(out_train, "Annotations")
        out_train_txt = os.path.join(out_train, "ImageSets/Main")
        out_train_images = os.path.join(out_train, "JPEGImages")

        out_eval = os.path.join(self.output, "eval")
        out_eval_annotations = os.path.join(out_eval, "Annotations")
        out_eval_txt = os.path.join(out_eval, "ImageSets/Main")
        out_eval_images = os.path.join(out_eval, "JPEGImages")

        os.makedirs(out_train, exist_ok=True)
        os.makedirs(out_train_annotations, exist_ok=True)
        os.makedirs(out_train_txt, exist_ok=True)
        os.makedirs(out_train_images, exist_ok=True)
        os.makedirs(out_eval, exist_ok=True)
        os.makedirs(out_eval_annotations, exist_ok=True)
        os.makedirs(out_eval_txt, exist_ok=True)
        os.makedirs(out_eval_images, exist_ok=True)

        # 复制转移labels.txt
        if os.path.exists(label_path):
            shutil.copy(label_path, os.path.join(out_train, "labels.txt"))
            shutil.copy(label_path, os.path.join(out_eval, "labels.txt"))

        # trainval_path = os.path.join(txtsavepath, "trainval.txt")
        # train_path = os.path.join(txtsavepath, "train.txt")
        # val_path = os.path.join(txtsavepath, "val.txt")

        # if os.path.exists(train_path) and os.path.exists(val_path):
        #     logger.error("train.txt and val.txt already exists, and there is no need to split."
        #                 "If you want to re split, please delete them first")
        #     sys.exit("train.txt 和 val.txt已存在，不需要切分，若想重新切分，请先删除他们并重新执行切分命令")
        #     # return False

        # if not mode:
        #     if os.path.exists(trainval_path) and os.path.exists(train_path):
        #         logger.error("both train.txt and trainval.txt are exist, please specify one using the parameter 'mode'")
        #         sys.exit("同时存在train.txt 和 trainval.txt，请使用’mode‘参数指定以哪份文件为切分依据")
        #         # return False

        # total_xml = None
        # if not mode:
        #     if os.path.exists(trainval_path):
        #         split_path = trainval_path
        #     elif os.path.exists(train_path):
        #         split_path = train_path
        #     else:
        #         os.makedirs(txtsavepath, exist_ok=True)
        #         total_xml = os.listdir(xmlfilepath)
        #         split_path = None
        # else:
        #     os.makedirs(txtsavepath, exist_ok=True)
        #     split_name = mode + ".txt"
        #     split_path = os.path.join(txtsavepath, split_name)
        #
        # if not total_xml:
        #     with open(split_path, "r", encoding="utf-8") as fr:
        #         xml_l = fr.readlines()
        #     total_xml = []
        #     for item in xml_l:
        #         total_xml.append(item.replace("\n", "") + ".xml")

        if not os.path.exists(train_path):
            total_xml = []
            os.makedirs(txtsavepath, exist_ok=True)
            for xml in os.listdir(xmlfilepath):
                if xml.lower().endswith(".xml"):
                    total_xml.append(xml.replace("\n", ""))
        else:
            with open(train_path, "r", encoding="utf-8") as fr:
                xml_l = fr.readlines()
                total_xml = []
                for item in xml_l:
                    total_xml.append(item.replace("\n", "") + ".xml")

        num = len(total_xml)
        list_ids = range(num)

        len_train = int(num * train_ratio)
        train_l = random.sample(list_ids, len_train)

        out_train_xml_l = []
        out_eval_xml_l = []

        # 生成 train.txt、val.txt
        for i in list_ids:
            name = total_xml[i][:-4] + '\n'
            if i in train_l:
                out_train_xml_l.append(name)
            else:
                out_eval_xml_l.append(name)

        with open(os.path.join(out_train_txt, 'train.txt'), 'w', encoding='utf-8') as fw1:
            for item in out_train_xml_l:
                fw1.write(item)

        with open(os.path.join(out_eval_txt, 'val.txt'), 'w', encoding='utf-8') as fw1:
            for item in out_eval_xml_l:
                fw1.write(item)

        # 复制转移xml
        for item in os.listdir(xmlfilepath):
            if item.lower().endswith(".xml"):
                item_name = os.path.splitext(item)[0]
                ori_xml = os.path.join(xmlfilepath, item)
                if item_name + "\n" in out_train_xml_l:
                    det_xml = os.path.join(out_train_annotations, item)
                    shutil.copy(ori_xml, det_xml)
                if item_name + "\n" in out_eval_xml_l:
                    det_xml = os.path.join(out_eval_annotations, item)
                    shutil.copy(ori_xml, det_xml)

        # 复制转移图片
        for item in os.listdir(imgsavepath):
            abs_item = os.path.join(imgsavepath, item)
            if os.path.isfile(abs_item):
                item_name = os.path.splitext(item)[0]
                item_type = os.path.splitext(item)[1]
                ori_img = os.path.join(imgsavepath, item)
                if item_type.lower() in [".jpg", ".jpeg", ".webp", ".bmp", ".png", '.rgb', '.tif', '.tiff', '.gif']:
                    if item_name + "\n" in out_train_xml_l:
                        det_img = os.path.join(out_train_images, item)
                        shutil.copy(ori_img, det_img)
                    if item_name + "\n" in out_eval_xml_l:
                        det_img = os.path.join(out_eval_images, item)
                        shutil.copy(ori_img, det_img)

        logger.info("切分结果以保存至 {}".format(self.output))


class CocoSplit:

    def __init__(self, data_dir, ratios=None, output=None):
        self.data_dir = data_dir
        self.ratios = ratios
        self.output = output
        self.ori_Annotations_dir = os.path.join(self.data_dir, "annotations")
        # self.ori_Images_dir = os.path.join(self.data_dir, "train")

    def split(self, mode=None):
        """
        COCO 数据集切分，优先级：
        0. 应保证coco数据目录结构满足定义要求， 即图片文件夹与json文件一一对应，如train与train.json
        1. train, val 同时存在删除后才能切分
        2. trainval, train 同时存在需指定其一作为切分依据（mode）
        3. train, train 有且只有一个时，以存在的文件为切分依据
        4. 切分后数据为train, val, 即原 train 会被覆盖，trainval 会被保留
        5. 切分后 train.json, val.json 中  ["images"]["id"] 均从0开始编号
        1202
        修改了数据集标准格式，不再有trainval，则必须含有train，删除mode参数
        """
        if not self.ratios:
            train_percent = 0.9
        else:
            train_percent = self.ratios

        # trainval_path = os.path.join(self.data_dir, "trainval")
        # train_path = os.path.join(self.data_dir, "train")
        # val_path = os.path.join(self.data_dir, "val")

        # annotations_path = os.path.join(self.data_dir, "annotations")
        # val_path = os.path.join(self.data_dir, "val")


        out_train = os.path.join(self.output, "train")
        out_train_annotations = os.path.join(out_train, "annotations")
        out_train_images = os.path.join(out_train, "train")

        out_eval = os.path.join(self.output, "eval")
        out_eval_annotations = os.path.join(out_eval, "annotations")
        out_eval_images = os.path.join(out_eval, "val")

        os.makedirs(out_train, exist_ok=True)
        os.makedirs(out_train_annotations, exist_ok=True)
        os.makedirs(out_train_images, exist_ok=True)
        os.makedirs(out_eval, exist_ok=True)
        os.makedirs(out_eval_annotations, exist_ok=True)
        os.makedirs(out_eval_images, exist_ok=True)

        out_train_json = os.path.join(out_train_annotations, "train.json")
        out_eval_json = os.path.join(out_eval_annotations, "val.json")

        # if os.path.exists(train_path) and os.path.exists(val_path):
        #     logger.error("train and val already exists, and there is no need to split."
        #                 "If you want to re split, please delete them first")
        #     sys.exit("train 和 val文件夹已存在，不需要切分，若想重新切分，请先删除他们并重新执行切分命令")
        #     # return False

        # if not mode:
        #     if os.path.exists(trainval_path) and os.path.exists(train_path):
        #         logger.error("both train and trainval are exist, please specify one using the parameter 'mode'")
        #         sys.exit("同时存在train 和 trainval，请使用’mode‘参数指定以哪份文件为切分依据")
        #         # return False

        # if mode is None:
        #     if os.path.exists(trainval_path) and not os.path.exists(train_path):
        #         data_types = ["trainval"]
        #     elif not os.path.exists(trainval_path) and os.path.exists(train_path):
        #         data_types = ["train"]
        #     else:
        #         # raise KeyError("train and trainval must have one in {}".format(self.data_dir))
        #         sys.exit("数据集目录下train 和 trainval至少应存在一个")
        # else:
        #     data_types = [mode]

        # 遍历annotations目录，若只存在一个json文件，以其为切分依据；若有多个，判断是否有train.json，有则以train.json为依据，否则以报错
        len_annotations = len(os.listdir(self.ori_Annotations_dir))
        if len_annotations == 0:
            raise FileNotFoundError("{} 为空".format(self.ori_Annotations_dir))
        elif len_annotations == 1:
            data_types = []
            for item in os.listdir(self.ori_Annotations_dir):
                data_types.append(os.path.splitext(item)[0])
        else:
            if os.path.exists(os.path.join(self.ori_Annotations_dir, "train.json")):
                data_types = ["train"]
            else:
                raise FileNotFoundError("切分失败{} 含多个json文件，且不含train.json")

        for i, datatype in enumerate(data_types):
            annFile = '{}.json'.format(datatype)
            annpath = os.path.join(self.ori_Annotations_dir, annFile)
            data = load_json(annpath)

            images = data["images"]
            categories = data["categories"]
            annotations = data["annotations"]
            coco_type = data["type"]

            # 按序号索引划分比例
            num = len(images)
            list_ids = range(num)

            len_train = int(num * train_percent)
            train = random.sample(list_ids, len_train)

            # 划分 images
            images_class, imgids_class, filename_class = self.split_images(images, list_ids, train)

            # 划分 annotations
            annotations_class = self.split_annotations(annotations, imgids_class)

            # 从0开始重新编号
            images_class, annotations_class = self.drop_index(images_class, annotations_class)

            train_json = {"images": images_class[0],
                          "type": coco_type,
                          "annotations": annotations_class[0],
                          "categories": categories}
            val_json = {"images": images_class[1],
                        "type": coco_type,
                        "annotations": annotations_class[1],
                        "categories": categories}

            # class_json = ["train", "val"]
            # list_json = [train_json, val_json]
            # for json_name, json_item in zip(class_json, list_json):
            #     json_item_path = os.path.join(self.ori_Annotations_dir, json_name + ".json")
            #     with open(json_item_path, "w", encoding="utf-8") as fw:
            #         json.dump(json_item, fw, ensure_ascii=False, indent=4)
            # logger.info("the annotations has been splited in to ['train.json', 'val.json'] saving in {}".format(self.ori_Annotations_dir))
            #
            # # 划分图片文件夹
            # self.split_im(filename_class, datatype)
            # logger.info("the images has been splited in to ['train', 'val'] saving in {}".format(os.path.join(self.data_dir)))

            # 生成切分后json
            with open(out_train_json, "w", encoding="utf-8") as fw1:
                json.dump(train_json, fw1, ensure_ascii=False, indent=4)
            with open(out_eval_json, "w", encoding="utf-8") as fw2:
                json.dump(val_json, fw2, ensure_ascii=False, indent=4)

            # 复制转移图片
            ori_img_dir = os.path.join(self.data_dir, datatype)
            for item in os.listdir(ori_img_dir):
                ori_img = os.path.join(ori_img_dir, item)
                if os.path.isfile(ori_img):
                    item_name = os.path.splitext(item)[0]
                    item_type = os.path.splitext(item)[1]
                    ori_img = os.path.join(ori_img_dir, item)
                    if item_type.lower() in [".jpg", ".jpeg", ".webp", ".bmp", ".png", '.rgb', '.tif', '.tiff', '.gif']:
                        if item in filename_class[0]:
                            det_img = os.path.join(out_train_images, item)
                            shutil.copy(ori_img, det_img)
                        if item in filename_class[1]:
                            det_img = os.path.join(out_eval_images, item)
                            shutil.copy(ori_img, det_img)
        logger.info("切分结果以保存至 {}".format(self.output))

    @staticmethod
    def drop_index(data_images, data_anno):
        # 从0开始重新编号
        n_data_images = []
        n_data_anno = []

        for imags, annos in zip(data_images, data_anno):
            n_imags = []
            n_annos = []
            imag_id_dict = {}
            for index, imag in enumerate(imags):
                imag_id_dict[str(imag["id"])] = index
                imag["id"] = index
                n_imags.append(imag)
            for index, anno in enumerate(annos):
                anno["id"] = index
                anno["image_id"] = imag_id_dict[str(anno["image_id"])]
                n_annos.append(anno)
            n_data_images.append(n_imags)
            n_data_anno.append(n_annos)
        return n_data_images, n_data_anno


    # 划分 images 字段
    @staticmethod
    def split_images(images, list_ids, train):
        images_train = []
        images_val = []

        images_train_imgids = []
        images_val_imgids = []

        images_train_filename = []
        images_val_filename = []

        for item in list_ids:
            if item in train:
                images_train.append(images[item])
                images_train_imgids.append(images[item]["id"])
                images_train_filename.append(images[item]["file_name"])
            else:
                images_val.append(images[item])
                images_val_imgids.append(images[item]["id"])
                images_val_filename.append(images[item]["file_name"])

        images_class = [images_train, images_val]
        imgids_class = [images_train_imgids, images_val_imgids]
        filename_class = [images_train_filename, images_val_filename]

        return images_class, imgids_class, filename_class

    # 划分 annotations 字段
    @staticmethod
    def split_annotations(annotations, imgids_class):
        annotations_train = []
        annotations_val = []

        # 划分 annotations
        for annotation in annotations:
            annotation_img_id = annotation["image_id"]
            if annotation_img_id in imgids_class[0]:
                annotations_train.append(annotation)
            else:
                annotations_val.append(annotation)

        annotations_class = [annotations_train, annotations_val]

        return annotations_class

    # 划分图片
    def split_im(self, filename_class, datatype):
        # 划分图片文件夹
        trainval_img_dir = os.path.join(self.data_dir, "trainval")
        train_img_dir = os.path.join(self.data_dir, "train")
        val_img_dir = os.path.join(self.data_dir, "val")

        os.makedirs(val_img_dir, exist_ok=True)
        # os.makedirs(train_img_dir, exist_ok=True)

        if datatype == "trainval":
            ori_Images_dir = trainval_img_dir
            os.makedirs(train_img_dir, exist_ok=True)
        elif datatype == "train":
            ori_Images_dir = train_img_dir
        else:
            raise KeyError("train and trainval must have one in {}".format(self.data_dir))

        for ori_Images_root, _, ori_img_files in os.walk(ori_Images_dir):
            for ori_img_file in ori_img_files:
                ori_img_path = os.path.join(ori_Images_root, ori_img_file)
                if ori_img_file in filename_class[0]:
                    if datatype == "trainval":
                        dst_img_val_path = os.path.join(train_img_dir, ori_img_file)
                        shutil.copy(ori_img_path, dst_img_val_path)
                    if datatype == "train":
                        pass
                else:
                    if datatype == "trainval":
                        dst_img_val_path = os.path.join(val_img_dir, ori_img_file)
                        shutil.copy(ori_img_path, dst_img_val_path)
                    if datatype == "train":
                        dst_img_test_path = os.path.join(val_img_dir, ori_img_file)
                        shutil.move(ori_img_path, dst_img_test_path)


def det_split(folder, form, ratio, output):
    if form.upper() == "VOC":
        data_split = VocSplit(data_dir=folder, ratios=ratio, output=output)
    elif form.upper() == "COCO":
        data_split = CocoSplit(data_dir=folder, ratios=ratio, output=output)
    else:
        raise KeyError("form 参数值必须为 VOC 或 COCO")
    data_split.split()


if __name__ == '__main__':
    print("start")
