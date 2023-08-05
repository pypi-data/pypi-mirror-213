#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/8/23 16:54
# @Author  : xgy
# @Site    :
# @File    : voc_eval.py
# @Software: PyCharm
# @python version: 3.7.11
"""

# --------------------------------------------------------
# Fast/er R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Bharath Hariharan
# --------------------------------------------------------

import json
import pickle as cPickle
import pandas as pd
import shutil

import numpy as np
import os
import xml.etree.ElementTree as ET
from csp.common.utils import format


def rec_labels(annopath, imagesetfile):
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]

    labels_rec = []
    for i, imagename in enumerate(imagenames):
        file_path = os.path.join(annopath, imagename + ".xml")
        tree = ET.parse(file_path)
        for obj in tree.findall('object'):
            name = obj.find('name').text
            if name not in labels_rec:
                labels_rec.append(name)

    return labels_rec


def parse_rec(filename):
    """
    # 读取标注的xml文件
    Parse a PASCAL VOC xml file
    """
    tree = ET.parse(filename)
    objects = []
    labels_rec = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        obj_struct['pose'] = obj.find('pose').text
        obj_struct['truncated'] = int(obj.find('truncated').text)
        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [int(bbox.find('xmin').text),
                              int(bbox.find('ymin').text),
                              int(bbox.find('xmax').text),
                              int(bbox.find('ymax').text)]
        objects.append(obj_struct)


    return objects


def voc_ap(rec, prec, use_07_metric=False):
    """ ap = voc_ap(rec, prec, [use_07_metric])
    Compute VOC AP given precision and recall.
    If use_07_metric is true, uses the
    VOC 07 11 point method (default:False).
    计算AP值，若use_07_metric=true,则用11个点采样的方法，将rec从0-1分成11个点，这些点prec值求平均近似表示AP
    若use_07_metric=false,则采用更为精确的逐点积分方法
    """
    if use_07_metric:
        # 11 point metric
        ap = 0.
        for t in np.arange(0., 1.1, 0.1):
            if np.sum(rec >= t) == 0:
                p = 0
            else:
                p = np.max(prec[rec >= t])
            ap = ap + p / 11.
    else:
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.], rec, [1.]))
        mpre = np.concatenate(([0.], prec, [0.]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
    return ap


def voc_eval(det_data, annopath, imagesetfile, classname, cachedir, ovthresh=0.5, use_07_metric=False):
    """
    主函数，计算当前类别的recall和precision
    rec, prec, ap = voc_eval(detpath,
                                annopath,
                                imagesetfile,
                                classname,
                                [ovthresh],
                                [use_07_metric])
    Top level function that does the PASCAL VOC evaluation.
    #detpath检测结果txt文件，路径VOCdevkit/results/VOC20xx/Main/<comp_id>_det_test_aeroplane.txt。
    该文件格式：imagename1 confidence xmin ymin xmax ymax  (图像1的第一个结果)
                   imagename1 confidence xmin ymin xmax ymax  (图像1的第二个结果)
                   imagename1 confidence xmin ymin xmax ymax  (图像2的第一个结果)
                   ......
        每个结果占一行，检测到多少个BBox就有多少行，这里假设有20000个检测结果
    # detpath: Path to detections
    #     detpath.format(classname) should produce the detection results file.
    det_data：预测结果（json），格式见api文档https://www.yuque.com/qiuzhiqiang-scrrm/bfxhrz/qh112f
    annopath: Path to annotations
        annopath.format(imagename) should be the xml annotations file. #xml 标注文件。
    imagesetfile: Text file containing the list of images, one image per line. #数据集划分txt文件，路径VOCdevkit/VOC20xx/ImageSets/Main/test.txt这里假设测试图像1000张，那么该txt文件1000行。
    classname: Category name (duh) #种类的名字，即类别，假设类别2（一类目标+背景）, str 一个类别名
    cachedir: Directory for caching the annotations #缓存标注的目录路径VOCdevkit/annotation_cache,图像数据只读文件，为了避免每次都要重新读数据集原始数据。
    [ovthresh]: Overlap threshold (default = 0.5) #重叠的多少大小。
    [use_07_metric]: Whether to use VOC07's 11 point AP computation
        (default False) #是否使用VOC07的AP计算方法，voc07是11个点采样。
    """
    # assumes detections are in detpath.format(classname)
    # assumes annotations are in annopath.format(imagename)
    # assumes imagesetfile is a text file with each line an image name
    # cachedir caches the annotations in a pickle file

    # first load gt 加载ground truth。

    if not os.path.isdir(cachedir):
        os.mkdir(cachedir)
    imageset = os.path.splitext(os.path.basename(imagesetfile))[0]
    cachefile = os.path.join(cachedir, imageset + '_annots.pkl')
    # read list of images
    with open(imagesetfile, 'r') as f:
        lines = f.readlines()
    imagenames = [x.strip() for x in lines]

    if not os.path.isfile(cachefile):  # 如果只读文件不存在，则只好从原始数据集中重新加载数据
        # load annots
        recs = {}
        for i, imagename in enumerate(imagenames):
            # recs[imagename] = parse_rec(annopath.format(imagename))
            recs[imagename] = parse_rec(os.path.join(annopath, imagename + ".xml"))
            if i % 100 == 0:
                print('Reading annotation for {:d}/{:d}'.format(i + 1, len(imagenames)))  # 进度条
        # save
        print('Saving cached annotations to {:s}'.format(cachefile))
        with open(cachefile, 'wb') as f:
            cPickle.dump(recs, f)  # recs字典c保存到只读文件。
    else:
        # load
        with open(cachefile, 'rb') as f:
            recs = cPickle.load(f)  # 如果已经有了只读文件，加载到recs。

    # 读取标注数据 gt
    # extract gt objects for this class #按类别获取标注文件，recall和precision都是针对不同类别而言的，AP也是对各个类别分别算的。
    class_recs = {}  # 当前类别的标注
    npos = 0  # npos标记的目标数量
    for imagename in imagenames:
        # 所有xml标注数据中的 classname 类
        R = [obj for obj in recs[imagename] if obj['name'] == classname]  # 过滤，只保留recs中指定类别的项，存为R。
        bbox = np.array([x['bbox'] for x in R])  # 抽取bbox
        difficult = np.array([x['difficult'] for x in R]).astype(np.bool)  # 如果数据集没有difficult,所有项都是0.

        det = [False] * len(R)  # len(R)就是当前类别的gt目标个数，det表示是否检测到，初始化为false。
        npos = npos + sum(~difficult)  # 自增，非difficult样本数量，如果数据集没有difficult，npos数量就是gt数量。
        # 一个文件，一个类别，所有gt框信息
        class_recs[imagename] = {'bbox': bbox,
                                 'difficult': difficult,
                                 'det': det}

    # read dets 读取检测结果
    # detfile = detpath.format(classname)
    # with open(detfile, 'r') as f:
    #     lines = f.readlines()
    lines = det_data.get(classname, None)
    # 预测结果中该类别为0
    if not lines:
        rec, prec, ap = 0, 0, 0
        return rec, prec, ap

    splitlines = [x.strip().split('\t') for x in lines]  # 假设检测结果有20000个，则splitlines长度20000
    image_ids = [x[0] for x in splitlines]  # 检测结果中的图像名，image_ids长度20000，但实际图像只有1000张，因为一张图像上可以有多个目标检测结果
    confidence = np.array([float(x[1]) for x in splitlines])  # 检测结果置信度
    BB = np.array([[float(z) for z in x[2:]] for x in splitlines])  # 变为浮点型的bbox。

    # sort by confidence 将20000各检测结果按置信度排序
    sorted_ind = np.argsort(-confidence)  # 对confidence的index根据值大小进行降序排列。
    # sorted_scores = np.sort(-confidence) #降序排列。
    BB = BB[sorted_ind, :]  # 重排bbox，由大概率到小概率。
    image_ids = [image_ids[x] for x in sorted_ind]  # 对image_ids相应地进行重排。

    # go down dets and mark TPs and FPs
    nd = len(image_ids)  # 注意这里是20000，不是1000
    tp = np.zeros(nd)  # true positive，长度20000
    fp = np.zeros(nd)  # false positive，长度20000
    for d in range(nd):  # 遍历所有检测结果，因为已经排序，所以这里是从置信度最高到最低遍历
        R = class_recs[image_ids[d]]  # 当前检测结果所在图像的所有同类别gt
        bb = BB[d, :].astype(float)  # 当前检测结果bbox坐标
        ovmax = -np.inf
        BBGT = R['bbox'].astype(float)  # 当前检测结果所在图像的所有同类别gt的bbox坐标

        if BBGT.size > 0:
            # compute overlaps 计算当前检测结果，与该检测结果所在图像的标注重合率，一对多用到python的broadcast机制
            # intersection
            ixmin = np.maximum(BBGT[:, 0], bb[0])
            iymin = np.maximum(BBGT[:, 1], bb[1])
            ixmax = np.minimum(BBGT[:, 2], bb[2])
            iymax = np.minimum(BBGT[:, 3], bb[3])
            iw = np.maximum(ixmax - ixmin + 1., 0.)
            ih = np.maximum(iymax - iymin + 1., 0.)
            inters = iw * ih

            # union
            uni = ((bb[2] - bb[0] + 1.) * (bb[3] - bb[1] + 1.) +
                   (BBGT[:, 2] - BBGT[:, 0] + 1.) *
                   (BBGT[:, 3] - BBGT[:, 1] + 1.) - inters)

            overlaps = inters / uni
            ovmax = np.max(overlaps)  # 最大重合率
            jmax = np.argmax(overlaps)  # 最大重合率对应的gt

        if ovmax > ovthresh:  # 如果当前检测结果与真实标注最大重合率满足阈值
            if not R['difficult'][jmax]:
                if not R['det'][jmax]:
                    tp[d] = 1.  # 正检数目+1
                    R['det'][jmax] = 1  # 该gt被置为已检测到，下一次若还有另一个检测结果与之重合率满足阈值，则不能认为多检测到一个目标
                else:  # 相反，认为检测到一个虚警
                    fp[d] = 1.
        else:  # 不满足阈值，肯定是虚警
            fp[d] = 1.

    # compute precision recall
    fp = np.cumsum(fp)  # 积分图，在当前节点前的虚警数量，fp长度
    tp = np.cumsum(tp)  # 积分图，在当前节点前的正检数量
    rec = tp / float(npos)  # 召回率，长度20000，从0到1
    # avoid divide by zero in case the first detection matches a difficult
    # ground truth 准确率，长度20000，长度20000，从1到0
    prec = tp / np.maximum(tp + fp, np.finfo(np.float64).eps)
    ap = voc_ap(rec, prec, use_07_metric)
    return rec, prec, ap


def parse_submit(submit_file):
    """
    预测结果json转换为分类txt，按类别
    """
    rs_l = read_json(submit_file)
    out_dict = {}
    for result in rs_l:
        # filename = result['filename'].split('.')[0]
        # category = result['category']
        # confidence = result['score']
        # xmax = result["bndbox"]['xmax']
        # ymax = result["bndbox"]['ymax']
        # ymin = result["bndbox"]['ymin']
        # xmin = result["bndbox"]['xmin']
        filename = os.path.splitext(result['file_name'])[0]
        category = result['category']
        confidence = result['score']
        xmax = int(result["bbox"][0]) + int(result["bbox"][2])
        ymax = int(result["bbox"][1]) + int(result["bbox"][3])
        ymin = result["bbox"][1]
        xmin = result["bbox"][0]

        if not out_dict.get(category, None):
            out_dict[category] = [filename + "\t" + str(confidence) + "\t" + str(xmin) + "\t" + str(ymin) + "\t" + str(xmax) + "\t" + str(ymax)]
        else:
            out_dict[category].append(filename + "\t" + str(confidence) + "\t" + str(xmin) + "\t" + str(ymin) + "\t" + str(xmax) + "\t" + str(ymax))

    return out_dict


def read_json(file_path):
    with open(file_path, mode='r', encoding='utf-8') as f:
        return json.load(f)


def get_labels(labels_path=None):
    labels = []
    with open(labels_path, "r", encoding="utf-8") as fr:
        txt_list = fr.readlines()
        for index, item in enumerate(txt_list):
            item_list = item.split(" ")
            labels.append(item_list[0].replace("\n", ""))
    return labels


def eva_voc(submit_file, ori_dir, output=None):
    """
    需注意 submit_file 的格式
    """

    submit_data = parse_submit(submit_file)

    # origin_image_dir = None
    labels_path = os.path.join(ori_dir, "labels.txt")
    ann_path = os.path.join(ori_dir, "Annotations")
    # test_txt_path = os.path.join(ori_dir, "ImageSets/Main/val.txt")
    test_txt_folder = os.path.join(ori_dir, "ImageSets/Main")

    # val.txt 不存在时，基于所有 xml 文件生成
    test_txt_path = get_val_txt(test_txt_folder, ann_path)

    cachedir = os.path.join(output, "cachedir") if output else "./cachedir"

    rec_m = 0
    prec_m = 0
    mAP_m = 0
    # label_l = get_labels(labels_path)
    label_l = rec_labels(ann_path, test_txt_path)

    res_list = []
    for label in label_l:
        rec, prec, ap = voc_eval(submit_data, ann_path, test_txt_path, label, cachedir, ovthresh=0.5, use_07_metric=False)
        # res_list.append([label, rec[-1], prec[-1], ap])
        if type(rec) == np.ndarray:
            rec = rec[-1]
        if type(prec) == np.ndarray:
            prec = prec[-1]
        # res_list.append([label, rec, prec, ap])
        res_list.append({"category": label, "recall": round(rec, 3), "precision": round(prec, 3), "ap": round(ap, 3)})
        # rec_m += rec[-1]
        # prec_m += prec[-1]
        rec_m += rec
        prec_m += prec
        mAP_m += ap

    mAP = round(float(mAP_m) / len(label_l), 3)
    mrec = round(float(rec_m) / len(label_l), 3)
    mprec = round(float(prec_m) / len(label_l), 3)

    # res_list.append(["mean", mrec, mprec, mAP])
    # df = pd.DataFrame(data=res_list,columns=['category', 'recall', 'precision', 'ap'])
    # print(df)
    df_result = pd.DataFrame(data=res_list)
    os.makedirs(output, exist_ok=True)
    output_path = os.path.join(output, "result.csv")
    df_result.to_csv(output_path, index=False, sep=",", encoding="utf-8")

    # 格式化输出
    res_list.append({"category": "total", "recall": mrec, "precision": mprec, "ap": mAP})
    title_dict = {"类别": "category", "召回率": "recall", "准确率": "precision", "ap": "ap"}
    result_dict = {"data": res_list}
    format(result_dict, title_dict)
    shutil.rmtree(cachedir)

    # badcase
    # voc先转为coco
    from loguru import logger
    logger.info("badcase analysis")
    # from csp.datatool.transform import voc_coco
    from csp.datatool.image_detection.transform import det_transform
    out_coco = os.path.join(output, "coco") if output else "./coco"
    # voc_coco(dataset=ori_dir, output=out_coco)
    det_transform(ori_dir, form="voc", output=out_coco, drop=False)

    from csp.datatool.image_detection.eva_badcase import DetEva
    # gold_file = os.path.join(out_coco, "annotations", "val.json")
    # origin_image_dir = os.path.join(out_coco, "val")
    gold_file, origin_image_dir = get_val_json(out_coco, show=False)
    json_eva = DetEva(submit_file, gold_file, origin_image_dir=origin_image_dir, output=output)
    json_eva.eva()
    shutil.rmtree(out_coco)


def eva_coco(submit_file, ori_dir, output=None):
    from csp.datatool.image_detection.eva_badcase import DetEva
    gold_file, origin_image_dir = get_val_json(ori_dir)
    json_eva = DetEva(submit_file, gold_file, origin_image_dir=origin_image_dir, output=output)
    json_eva.eva(show=True)


def get_val_json(ori_dir, show=True):
    # val.json 判断
    annotation_path = os.path.join(ori_dir, "annotations")
    json_l = []
    for item in os.listdir(annotation_path):
        if item.lower().endswith(".json"):
            json_l.append(item)
    num_json = len(json_l)
    if num_json == 1:
        if json_l[0].lower() != "val.json":
            if show:
                print(" {} 中不含val.json，但仅有一份json文件，将以该json文件 {} 为答案json文件".format(annotation_path, json_l[0]))
            gold_file = os.path.join(annotation_path, json_l[0])
            json_name = os.path.splitext(json_l[0])[0]
            origin_image_dir = os.path.join(ori_dir, json_name)
        else:
            if show:
                print("只含val.json，将以 val.json 为答案json文件")
            gold_file = os.path.join(ori_dir, "annotations", "val.json")
            origin_image_dir = os.path.join(ori_dir, "val")
    elif num_json == 0:
        raise FileNotFoundError("{} 中未找到任何json文件".format(annotation_path))
    else:
        if "val.json" in json_l or "val.JSON" in json_l:
            if show:
                print("含多份json文件且含val.json，将以 val.json 为答案json文件")
            gold_file = os.path.join(ori_dir, "annotations", "val.json")
            origin_image_dir = os.path.join(ori_dir, "val")
        else:
            raise FileNotFoundError("{} 中含多份json文件，但未找到val.json".format(annotation_path))
    return gold_file, origin_image_dir


def get_val_txt(test_txt_folder, ann_path):
    if not os.path.exists(test_txt_folder):
        os.makedirs(test_txt_folder)
        test_txt_path = os.path.join(test_txt_folder, "val.txt")
        print("未找到 {}，将基于所有xml文件生成 {}".format(test_txt_folder, test_txt_path))
        with open(test_txt_path, "w", encoding="utf-8") as fw:
            for item in os.listdir(ann_path):
                if item.lower().endswith(".xml"):
                    xml_name = os.path.splitext(item)[0]
                    fw.write(xml_name)
                    fw.write("\n")

    else:
        txt_l = []
        for item in os.listdir(test_txt_folder):
            if item.lower().endswith(".txt"):
                txt_l.append(item)
        num_txt = len(txt_l)
        if num_txt == 1:
            if txt_l[0].lower() != "val.txt":
                print(" {} 中不含val.txt，但仅有一份txt文件，将以该txt文件 {} 为答案txt文件".format(test_txt_folder, txt_l[0]))
                test_txt_path = os.path.join(test_txt_folder, txt_l[0])
            else:
                print("只含val.txt，将以 val.txt 为答案txt文件")
                test_txt_path = os.path.join(test_txt_folder, "val.txt")

        elif num_txt == 0:
            test_txt_path = os.path.join(test_txt_folder, "val.txt")
            print("存在 {} 但未找到任何txt文件，将基于所有xml文件生成 {}".format(test_txt_folder, test_txt_path))
            with open(test_txt_path, "w", encoding="utf-8") as fw:
                for item in os.listdir(ann_path):
                    if item.lower().endswith(".xml"):
                        xml_name = os.path.splitext(item)[0]
                        fw.write(xml_name)
                        fw.write("\n")
            # raise FileNotFoundError("{} 中未找到任何txt文件".format(test_txt_folder))
        else:
            if "val.txt" in txt_l or "val.TXT" in txt_l:
                print("含多份txt文件且含val.txt，将以 val.txt 为答案txt文件")
                test_txt_path = os.path.join(test_txt_folder, "val.txt")
            else:
                raise FileNotFoundError("{} 中含多份txt文件，但未找到val.txt".format(test_txt_folder))
    return test_txt_path


def det_eva(submit_file, ori_dir, form: str, output=None):
    if form.lower() == "voc":
        eva_voc(submit_file, ori_dir, output=output)
    if form.lower() == "coco":
        eva_coco(submit_file, ori_dir, output=output)


if __name__ == '__main__':
    print("start eval")
