from typing import Optional
from pathlib import Path
from xml.etree import ElementTree as ET
from multiprocessing import Process
import pandas as pd
from copy import deepcopy
import cv2
from uuid import uuid4
import shutil


class VocStyle:
    def __init__(self, img_dir, data: Optional[pd.DataFrame]) -> None:
        self.img_dir = Path(img_dir)
        self.data = data
        self.data.columns = ["name", "cls", "x1", "y1", "x2", "y2"]
        self.names = list(set(self.data["name"].to_list()))
        self.cls_names = {}
    

    def write(self, names):
        for name in names:
            tree, root, filename, width, height, depth, obj = self.style()
            img = self.img_dir.joinpath(name + ".jpg")
            filename.text = img.name
            cv_img = cv2.imread(img.__str__())
            h, w, c = cv_img.shape
            width.text, height.text, depth.text = str(w), str(h), str(c)
            bboxes = self.data[self.data["name"]==name].to_numpy()
            for bbox in bboxes:
                obj_ = self.new_obj(obj, bbox)
                root.append(obj_)
            tree.write(self.img_dir.joinpath(name + ".xml"))
    
    def to_voc(self):
        n = len(self.names) // 5
        name_list = [self.names[i*n:(i+1)*n if i<4 else -1] for i in range(5)]
        for names in name_list:
            task = Process(target=self.write, args=(names, ))
            task.start()
                
    def style(self):
        tree0 = ET.parse("./xml/voc.xml")
        tree = deepcopy(tree0)
        root = tree.getroot()
        filename = root.find("filename")
        size = root.find("size")
        width = size.find("width")
        height = size.find("height")
        depth = size.find("depth")
        obj0 = root.find("object")
        obj = deepcopy(obj0)
        root.remove(obj0)
        return tree, root, filename, width, height, depth, obj

    def new_obj(self, obj, bbox):
        obj = deepcopy(obj)
        name = obj.find("name")
        bndbox = obj.find("bndbox")
        xmin = bndbox.find("xmin")
        ymin = bndbox.find("ymin")
        xmax = bndbox.find("xmax")
        ymax = bndbox.find("ymax")
        name.text, xmin.text, ymin.text, xmax.text, ymax.text = bbox[1:]
        return obj

    def voc_2_yolo(self):
        self.names = list(set(self.names) & set([i.stem for i in self.img_dir.glob("*.jpg") if \
            self.img_dir.joinpath(i.stem + ".xml").exists()]))
        assert len(self.names) > 0
        n = len(self.names) // 5
        name_list = [self.names[i*n:(i+1)*n if i<4 else -1] for i in range(5)]
        for names in name_list:
            task = Process(target=self.voc_2_yolo_, args=(names, ))
            task.start()

    def voc_2_yolo_(self, names):
        for name in names:
            bboxes = self.parse(name)
            with open(self.img_dir.joinpath(name + ".txt"), "w")as f:
                f.writelines(bboxes)

    def parse(self, name):
        anno = self.img_dir.joinpath(name + ".xml")
        tree = ET.parse(anno)
        root = tree.getroot()
        size = root.find("size")
        width = int(eval(size.find("width").text))
        height = int(eval(size.find("height").text))
        objs = root.findall("object")
        bboxes = []

        for obj in objs:
            cls = obj.find("name")
            if cls in self.cls_names:
                cls = self.cls_names[cls]
            else:
                self.cls_names[cls] = len(self.cls_names)
                self.cls = self.cls_names[cls]
            bndbox = obj.find("bndbox")
            x1 = int(eval(bndbox.find("xmin").text))
            y1 = int(eval(bndbox.find("ymin").text))
            x2 = int(eval(bndbox.find("xmax").text))
            y2 = int(eval(bndbox.find("ymax").text))
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            w = x2 - x1
            h = y2 - y1
            bbox = [cx / width, cy / height, w / width, h / height]
            bbox = f"{cls} " + " ".join(list(map(lambda x: str(x), bbox))) + "\n"
            bboxes.append(bbox)
        
        return bboxes


if __name__ == "__main__":
    
    names = list(range(1989))
    n = len(names) // 5
    name_list = [names[i*n:(i+1)*n if i<4 else -1] for i in range(5)]

    print([len(i) for i in name_list])
