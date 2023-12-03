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
        

def run_detectron_on_image(image_name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    # dictionary_file = os.path.join(basedir, 'static', 'assets', 'data', '3AD_dictionary.json')
    # design_file = os.path.join(basedir, 'static/assets/data/3AD_design_info.json')

    image_dir = os.path.join(basedir, 'static', 'assets', 'images', 'input')    
    # image_dir = os.path.join('./static/assets/images/input/'
    # image_dir = ""

    cfg = set_cfg()
    
    dataset_name = image_name.split(".")[0]
    
    if dataset_name in DatasetCatalog.list():
        DatasetCatalog.remove(dataset_name)
    
    try:
        register_coco_instances(dataset_name, {}, os.path.join("../detectron2", dataset_name+".json"), os.path.join(image_dir, image_name))
    except:
        DatasetCatalog.remove(dataset_name)
        register_coco_instances(dataset_name, {}, os.path.join("../detectron2", dataset_name+".json"), os.path.join(image_dir, image_name))
    
    cfg.MODEL.WEIGHTS = "../detectron2/model_0002799.pth"
    cfg.DATASETS.TEST = (dataset_name, )
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set the testing threshold for this model
    predictor = DefaultPredictor(cfg)
    # test_metadata = MetadataCatalog.get("my_dataset_test")
    
    with open(os.path.join('../detectron2', 'labels.txt'), 'r') as f:
        classes = f.readlines()
    
    metadata = {"thing_classes": []}
    for c in classes:
        metadata["thing_classes"].append(c.split(" ")[-1].strip())
    
    # images = os.listdir(os.path.join(image_dir, 'images'))

    # for imageName in images:
    im = cv2.imread(os.path.join(image_dir, image_name))
    outputs = predictor(im)
    # print(outputs)
    
    # print('output instances ---- ')
    
    instances = outputs['instances']
    # print(instances.pred_boxes[0].tensor.tolist()[0])
    
    pred_classes = instances.pred_classes.tolist()
    
    phrases = []
    
    for c in pred_classes:
        phrases.append(classes[c].split(" ")[-1].strip())
    
    boxes = instances.pred_boxes.tensor.cpu().numpy()
    logits = instances.scores.tolist()
    
    # print(boxes)
    # print(logits)
  
    # v = Visualizer(im[:, :, ::-1],
    #                 metadata=metadata, 
    #                 scale=0.8
    #                 )
    # out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    # print(out)
    
    # cv2.imwrite('./inference_output_dt/' + image_name, out.get_image()[:, :, ::-1])

    try:
        if dataset_name in DatasetCatalog.list():
            DatasetCatalog.remove(dataset_name)
    except:
        pass
    
    return boxes, torch.Tensor(logits), phrases
    

def main():
    run_detectron_on_image()
    

if __name__ == "__main__":
    main()