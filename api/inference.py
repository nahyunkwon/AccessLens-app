# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
import torch
from detectron2.utils.visualizer import ColorMode
import glob, pathlib

from PIL import Image

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.engine import DefaultTrainer

from detectron2.data.datasets import register_coco_instances
import os
from detectron2.engine import DefaultTrainer
from detectron2.evaluation import COCOEvaluator, DatasetEvaluators

def set_cfg():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("../configs/COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml"))
    cfg.DATASETS.TRAIN = ("access_train",)
    cfg.DATASETS.TEST = ("access_val", "access_test", )

    NUM_EPOCH = 200
    TOTAL_NUM_IMAGES = 2000
    ITERS_IN_ONE_EPOCH = int(TOTAL_NUM_IMAGES / cfg.SOLVER.IMS_PER_BATCH)

    cfg.DATALOADER.NUM_WORKERS = 1
    cfg.MODEL.WEIGHTS = "../configs/pretrained/model_final_b275ba.pkl"  # Let training initialize from model zoo
    cfg.SOLVER.IMS_PER_BATCH = 16  # This is the real "batch size" commonly known to deep learning people
    cfg.SOLVER.BASE_LR = 0.001  # pick a good LR
    cfg.SOLVER.MAX_ITER = NUM_EPOCH * ITERS_IN_ONE_EPOCH   # 300 iterations seems good enough for this toy dataset; you will need to train longer for a practical dataset
    cfg.SOLVER.STEPS = []        # do not decay learning rate
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 256   # The "RoIHead batch size". 128 is faster, and good enough for this toy dataset (default: 512)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 21  # only has one class (ballon). (see https://detectron2.readthedocs.io/tutorials/datasets.html#update-the-config-for-new-datasets)
    cfg.SOLVER.CHECKPOINT_PERIOD = 200
    cfg.TEST.EVAL_PERIOD = 200
    
    return cfg


def add_images_to_coco(image_dir, coco_filename):
    image_filenames = os.listdir(os.path.join(image_dir, 'images'))
    images = []
    
    print(image_filenames)
    
    for i, image_filename in enumerate(image_filenames):
        image_path = os.path.join(image_dir, 'images', image_filename)
        im = Image.open(image_path)
        width, height = im.size
        image_details = {
            "id": i + 1,
            "height": height,
            "width": width,
            "file_name": str(image_path),
        }
        images.append(image_details)
    
    data = {}
    # This will overwrite the image tags in the COCO JSON file
    try:
        with open(coco_filename) as f:
            data = json.load(f)
    except:
        pass
    
    data['images'] = images

    with open(coco_filename, 'w') as coco_file:
        json.dump(data, coco_file, indent = 4)
        

def test_image(image_dir):

    cfg = set_cfg()
    
    register_coco_instances("my_dataset_test", {}, os.path.join(image_dir, "my_dataset_test.json"), os.path.join(image_dir, 'images'))
    
    cfg.MODEL.WEIGHTS = "../detectron2/model_0002799.pth"
    cfg.DATASETS.TEST = ("my_dataset_test", )
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
    predictor = DefaultPredictor(cfg)
    # test_metadata = MetadataCatalog.get("my_dataset_test")
    
    with open(os.path.join(image_dir, 'labels.txt'), 'r') as f:
        classes = f.readlines()
    
    metadata = {"thing_classes": []}
    for c in classes:
        metadata["thing_classes"].append(c.split(" ")[-1].strip())
    
    images = os.listdir(os.path.join(image_dir, 'images'))

    for imageName in images:
        im = cv2.imread(os.path.join(image_dir, 'images', imageName))
        outputs = predictor(im)
        print(outputs)
        v = Visualizer(im[:, :, ::-1],
                        metadata=metadata, 
                        scale=0.8
                        )
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        # print(out)
        cv2.imwrite('./inference_output/' + imageName, out.get_image()[:, :, ::-1])
        

def main():
    image_dir = './case_study'
    # add_images_to_coco('./case_study', 'my_dataset_test.json')
    test_image(image_dir)
    
    

if __name__ == "__main__":
    main()