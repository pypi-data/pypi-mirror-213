#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/9 15:20
# @Author  : xgy
# @Site    : 
# @File    : aug.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from datetime import datetime
import os, threading, math, time, yaml
import shutil

# import cv2
import numpy as np
from PIL import Image
import xml.etree.ElementTree as ET
from tqdm import tqdm
from loguru import logger

from csp.datatool.image_detection.bg_changed import bg_treat
from csp.datatool.image_detection.utils import read_xml_annotation
from csp.common.utils import RunSys


class DetAug:
    """
    基于VOC数据集的目标检测任务训练数据增强
    数据集需先切分，后增强
    切分后，Main 文件中必含有 trainval.txt
    只对 trainval.txt 部分增强
    """

    def __init__(self, data_dir, aug_file):
        self.data_dir = data_dir
        self.aug_file = aug_file
        self.IMG_DIR = self.data_dir + os.sep + "JPEGImages"
        self.XML_DIR = self.data_dir + os.sep + "Annotations"
        self.voc_txt_dir = os.path.join(self.data_dir, "ImageSets", "Main")
        # self.reset_dir()

        self.imgfiles = []
        self.methods = []
        self.config_dict = {}
        self.check_env()

        self.get_methods_from_yml()

    def check_env(self):
        try:
            from imgaug import augmenters as iaa
            import imgaug as ia
        except ImportError:
            logger.warning("未检测到 imgaug 尝试安装, pip install imgaug")
            install_cmd = "pip install imgaug"
            install_cmd1 = "pip install imageio==2.19.1"
            RunSys(command=install_cmd).run_cli()
            RunSys(command=install_cmd1).run_cli()
        try:
            import cv2
        except ImportError:
            logger.warning("未检测到 opencv 尝试安装, pip install opencv-python")
            install_cmd = "pip install opencv-python"
            RunSys(command=install_cmd).run_cli()

    def reset_dir(self):
        for item in [self.IMG_DIR, self.XML_DIR]:
            for each_file in os.listdir(item):
                if each_file.startswith('imgaug_'):
                    os.remove(item + os.sep + each_file)

    def aug(self, mode=None):
        self.reset_dir()
        """
        1. 只适用于 VOC 数据集
        2. trainval.txt、trainval.txt 存在其一时，以存在者为增强依据
        3. trainval.txt、trainval.txt 都存在时需指定其中一个（mode参数指定）
        4. 重新执行增强操作会覆盖上次的操作
        1202 
        数据集格式变更，只含train.txt，不含trainval.txt，消去mode参数
        """
        t1 = time.time()
        if not os.path.exists(self.data_dir):
            raise FileNotFoundError('未能找到相应文件夹，请核查传入的路径')

        # trainval_txt_path = os.path.join(self.voc_txt_dir, "trainval.txt")
        train_txt_path = os.path.join(self.voc_txt_dir, "train.txt")

        # if not mode:
        #     if os.path.exists(trainval_txt_path) and os.path.exists(train_txt_path):
        #         logger.error("both train and trainval are exist, please specify one using the parameter 'mode'")
        #         return False
        #     elif os.path.exists(trainval_txt_path) and not os.path.exists(train_txt_path):
        #         trainval_txt_path = trainval_txt_path
        #     elif not os.path.exists(trainval_txt_path) and os.path.exists(train_txt_path):
        #         trainval_txt_path = train_txt_path
        #     else:
        #         raise FileNotFoundError("train.txt and trainval.txt should have at least one")
        # else:
        #     aug_name = mode + ".txt"
        #     trainval_txt_path = os.path.join(self.voc_txt_dir, aug_name)

        trainval_txt_path = train_txt_path

        # 若初始不含train_txt_path，则基于全部xml文件生成train_txt_path
        # if not os.path.exists(self.voc_txt_dir):
        if not os.path.exists(trainval_txt_path):
            os.makedirs(self.voc_txt_dir, exist_ok=True)
            xml_names = []
            for root, _, files in os.walk(self.XML_DIR):
                for xml_file in files:
                    xml_name = os.path.splitext(xml_file)[0]
                    xml_names.append(xml_name)
            with open(trainval_txt_path, "w", encoding="utf-8") as fw:
                for item in xml_names:
                    item = item.replace("\n", "").replace("\r\n", "")
                    fw.write(item)
                    fw.write("\n")

        # rest trainval_txt_path
        with open(trainval_txt_path, "r", encoding="utf-8") as fr:
            xml_trainval_reset = fr.readlines()
        with open(trainval_txt_path, "w", encoding="utf-8") as fw:
            for item in xml_trainval_reset:
                if not item.strip().startswith("imgaug_"):
                    item = item.replace("\n", "").replace("\r\n", "")
                    fw.write(item)
                    fw.write("\n")

        # 读取原始 trainval_txt_path
        with open(trainval_txt_path, "r", encoding="utf-8") as fr:
            xml_trainval_ori = fr.readlines()
            xml_trainval_ori = [item.strip() for item in xml_trainval_ori]

        # 只有 trainval_txt_path 中的图片参与增强
        imgfiles_all = os.listdir(self.IMG_DIR)
        imgfiles = []
        for item in imgfiles_all:
            if os.path.splitext(item)[0] in xml_trainval_ori:
                imgfiles.append(item)
        self.imgfiles = imgfiles

        if not self.config_dict["basic"]["thread_num"]:
            self.aug_act()  # 未采用多线程
        else:
            self.threading_treat()

        # 生成新的trainval_txt_path
        xml_names = []
        for root, _, files in os.walk(self.XML_DIR):
            for xml_file in files:
                xml_name = os.path.splitext(xml_file)[0]
                xml_names.append(xml_name)
        with open(trainval_txt_path, "a+", encoding="utf-8") as fw:
            for item in xml_names:
                if item.startswith("imgaug_"):
                    item = item.replace("\n", "").replace("\r\n", "")
                    fw.write(item)
                    fw.write("\n")

        print('消耗时间 : %sS' % round(time.time() - t1, 2))

    def get_methods_from_yml(self):

        from imgaug import augmenters as iaa

        f = open(self.aug_file, encoding='utf8')
        data_dict = yaml.load(f, Loader=yaml.Loader)
        methods = []

        if 'Sequential' in data_dict.keys():
            seq_methods = []
            for method, paras in data_dict['Sequential'].items():
                if method == 'bg_changed':
                    methods.append({method: paras})

                elif method == 'WithColorspace':
                    k = data_dict["Sequential"][method]
                    if 'children' in k.keys():
                        if type(k['children']) == dict:
                            tmp1 = k['children']
                            for tmp2_method, tmp2_value in tmp1.items():
                                if type(tmp1[tmp2_method]) == dict:
                                    if 'children' in tmp1[tmp2_method].keys():
                                        tmp3 = tmp1[tmp2_method]['children']
                                        for tmp3_method, tmp3_value in tmp3.items():
                                            tmp2_value = getattr(iaa, tmp3_method)(tmp3_value)
                                    tmp1[tmp2_method]['children'] = tmp2_value
                            k['children'] = getattr(iaa, tmp2_method)(**tmp1[tmp2_method])
                    seq_methods.append(getattr(iaa, 'WithColorspace')(**k))
                elif method == 'Resize':
                    seq_methods.append(getattr(iaa, method)(paras))
                else:
                    if paras == None:
                        seq_methods.append(getattr(iaa, method)())
                    elif type(paras) in [int, float, list]:
                        seq_methods.append(getattr(iaa, method)(paras))
                    elif type(paras) == dict:
                        paras = {key: eval(value) if type(value) == str else value for key, value in paras.items()}
                        seq_methods.append(getattr(iaa, method)(**paras))
            methods.append(iaa.Sequential(seq_methods))
        else:
            for method, paras in data_dict.items():
                if method == 'bg_changed':
                    methods.append({method: paras})
                elif method == 'WithColorspace':
                    k = data_dict[method]
                    if 'children' in k.keys():
                        if type(k['children']) == dict:
                            tmp1 = k['children']
                            for tmp2_method, tmp2_value in tmp1.items():
                                if type(tmp1[tmp2_method]) == dict:
                                    if 'children' in tmp1[tmp2_method].keys():
                                        tmp3 = tmp1[tmp2_method]['children']
                                        for tmp3_method, tmp3_value in tmp3.items():
                                            tmp2_value = getattr(iaa, tmp3_method)(tmp3_value)
                                    tmp1[tmp2_method]['children'] = tmp2_value
                            k['children'] = getattr(iaa, tmp2_method)(**tmp1[tmp2_method])
                    methods.append(getattr(iaa, 'WithColorspace')(**k))
                elif method == 'Resize':
                    methods.append(getattr(iaa, method)(paras))
                elif method == "basic":  # 基础配置非增强方法配置
                    continue
                else:
                    if paras == None:
                        methods.append(getattr(iaa, method)())
                    elif type(paras) in [int, float, list]:
                        methods.append(getattr(iaa, method)(paras))
                    elif type(paras) == dict:
                        paras = {key: eval(value) if type(value) == str else value for key, value in paras.items()}
                        methods.append(getattr(iaa, method)(**paras))
        self.methods = methods
        self.config_dict = data_dict
        # return data_dict, methods

    def aug_act(self):
        import cv2
        import imgaug as ia
        # from PIL import Image

        if self.config_dict["basic"]["random"]:
            print('进入随机增强模式')
            aug_methods = [np.random.choice(self.methods)]  # 每个xml文件随机选择一种的增强方法
        else:
            print('进入常规增强模式')
            aug_methods = self.methods  # 每种所列方法，均进行一次增强操作
        flag_Sequential_bg_changed = False
        for method_num, aug_method in enumerate(aug_methods):
            for epoch in range(1, self.config_dict["basic"]["aug_times"] + 1):
                logger.info(" {} 增强方法第 {} 轮".format(method_num + 1, epoch))

                # bg_changed 方法特殊处理，imgaug 不包括该方法，因此需单独处理
                # 增强方法分别处理并分别生成新图片时，该方法先执行
                if type(aug_method) == dict and aug_method.get("bg_changed", None) and not self.config_dict.get("Sequential", None):
                    bg_treat(self.imgfiles, aug_method["bg_changed"]["bg_path"], method_num, epoch, self.IMG_DIR, self.XML_DIR)
                elif type(aug_method) == dict and aug_method.get("bg_changed", None) and self.config_dict.get("Sequential", None):
                    flag_Sequential_bg_changed = True
                    continue
                else:
                    for imgfile in tqdm(self.imgfiles):
                        image_id = os.path.splitext(imgfile)[0]
                        bndbox = read_xml_annotation(self.XML_DIR, image_id + '.xml')
                        if bndbox:
                            new_bndbox_list = []
                            seq_det = aug_method.to_deterministic()  # 保持坐标和图像同步改变，而不是随机
                            # img = Image.open(os.path.join(self.IMG_DIR, imgfile))  # 读取图片
                            # img = img.convert('RGB')
                            # img = np.array(img)
                            # 读取图片
                            img = cv2.imdecode(np.fromfile(os.path.join(self.IMG_DIR, imgfile), dtype=np.uint8), 1)
                            for i in range(len(bndbox)):  # bndbox坐标增强，依次处理所有的bbox
                                bbs = ia.BoundingBoxesOnImage(
                                    [ia.BoundingBox(x1=bndbox[i][0], y1=bndbox[i][1], x2=bndbox[i][2],
                                                    y2=bndbox[i][3])],
                                    shape=img.shape)
                                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                                new_bndbox_list.append([int(bbs_aug.bounding_boxes[0].x1),
                                                        int(bbs_aug.bounding_boxes[0].y1),
                                                        int(bbs_aug.bounding_boxes[0].x2),
                                                        int(bbs_aug.bounding_boxes[0].y2)])
                            image_aug = seq_det.augment_images([img])[0]
                            new_img_name = 'imgaug_%s_%s_' % (method_num + 1, epoch) + imgfile
                            path = os.path.join(self.IMG_DIR, new_img_name)  # 存储变化后的图片
                            # Image.fromarray(image_aug).save(path)
                            # 保存图片
                            cv2.imencode(os.path.splitext(imgfile)[-1], image_aug)[1].tofile(path)
                            self.change_xml_list_annotation(image_id, new_bndbox_list, method_num, epoch)  # 存储变化后的XML

                            # 增强方法先后处理并生成新图片时，该方法最后执行
                            if flag_Sequential_bg_changed:
                                imgfiles_Sequential = [new_img_name]
                                for epoch in range(1, self.config_dict["basic"]["aug_times"] + 1):
                                    bg_treat(imgfiles_Sequential,
                                             self.config_dict["Sequential"]["bg_changed"]["bg_path"], method_num, epoch,
                                             self.IMG_DIR, self.XML_DIR)

    def threading_treat(self):  # 使用多线程处理，以提升速度
        threads = self.config_dict["basic"]["thread_num"]
        if type(threads) == bool:
            threads = os.cpu_count()
        elif type(threads) == int and threads > 0:
            threads = threads
        else:
            raise TypeError("thread_num 必须为布尔值或正整数 {}".format(self.config_dict["basic"]["thread_num"]))

        print('%s 个线程正在执行...' % threads)
        NUMS = len(self.imgfiles)
        num_part = math.ceil(NUMS / threads)  # 计算每个线程要处理的最大数据量
        temp_t = []
        for thread_num in range(threads):
            son_imgfiles = self.imgfiles[num_part * thread_num: num_part * (thread_num + 1)]
            t = threading.Thread(target=self.aug_act, args=())
            temp_t.append(t)
            t.start()
        for t in temp_t:
            t.join()

    def change_xml_list_annotation(self, image_id, new_target, method_num, epoch):
        """
        增强图片的.xml文件
        :param image_id:
        :param new_target:
        :param method_num:
        :param epoch:
        :return:
        """
        tree = ET.parse(os.path.join(self.XML_DIR, image_id + '.xml'))  # 读取xml文件
        xmlroot = tree.getroot()
        size = xmlroot.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        index = 0
        # 将bbox中原来的坐标值换成新生成的坐标值
        for object in xmlroot.findall('object'):  # 找到root节点下的所有country节点
            bndbox = object.find('bndbox')  # 子节点下节点rank的值
            new_xmin = new_target[index][0]
            new_ymin = new_target[index][1]
            new_xmax = new_target[index][2]
            new_ymax = new_target[index][3]

            xmin = bndbox.find('xmin')
            xmin.text = str(max(new_xmin, 0))
            ymin = bndbox.find('ymin')
            ymin.text = str(max(new_ymin, 0))
            xmax = bndbox.find('xmax')
            xmax.text = str(min(new_xmax, width))
            ymax = bndbox.find('ymax')
            ymax.text = str(min(new_ymax, height))
            index = index + 1
        tree.write(os.path.join(self.XML_DIR, "imgaug_%s_%s_" % (method_num + 1, epoch) + str(image_id) + '.xml'))


def det_aug(data_dir, aug_config, form: str, mode=None):
    if form.lower() == "voc":
        data_aug = DetAug(data_dir=data_dir, aug_file=aug_config)
        data_aug.aug(mode)
    if form.lower() == "coco":
        # 方案一
        # 先转为voc格式-增强-转回coco
        from csp.datatool.image_detection.transform import det_transform
        from csp.common.utils import make_tmp
        tmp_dir, _ = make_tmp()
        create_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f")
        out_voc = os.path.join(tmp_dir, "vox_tmp_" + create_time)
        os.makedirs(out_voc, exist_ok=True)
        det_transform(data_dir, "coco", out_voc)
        try:
            data_aug = DetAug(data_dir=out_voc, aug_file=aug_config)
            data_aug.aug(mode)

            # 清理coco源数据集中的上一次增强遗留图像
            for item in os.listdir(data_dir):
                if item != "annotations" and os.path.isdir(os.path.join(data_dir, item)):
                    img_folder = os.path.join(data_dir, item)
                    for each_file in os.listdir(img_folder):
                        if each_file.startswith('imgaug_'):
                            os.remove(os.path.join(img_folder, each_file))

            det_transform(out_voc, "voc", data_dir, drop=False)
        except FileNotFoundError as fe:
            raise fe
            # print(str(fe))
            # if str(fe).endswith("trainval.txt'"):
            #     raise FileNotFoundError("trainval.json 不存在, 请使用-m 指定切分依据（trainval或train）， csp datatool aug det-coco -d 数据集 -c 增强文件 -m 增强依据")
            # if str(fe).endswith("train.txt'"):
            #     raise FileNotFoundError("train.json 不存在, 请使用-m 指定切分依据（trainval或train）， csp datatool aug det-coco -d 数据集 -c 增强文件 -m 增强依据")
            #     raise FileNotFoundError("train.json 不存在")
            # if str(fe).endswith("should have at least one"):
            #     raise FileNotFoundError("train.json, trainval.json均不存在，无法指定增强依据")
            # else:
            #     raise fe
        except Exception as ae:
            raise ae
        finally:
            shutil.rmtree(out_voc)


if __name__ == '__main__':
    print("start")
