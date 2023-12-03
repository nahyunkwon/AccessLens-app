import sys
sys.path.append('../../GroundingDINO')

from typing import Tuple, List

from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import torch
import json
import os
from torchvision.ops import box_convert
import supervision as sv

from PIL import Image

import detectron_inference as dt
import app

basedir = os.path.abspath(os.path.dirname(__file__))
detected_object_folder = os.path.join(basedir, 'static', 'assets', 'images', 'object')

import numpy as np

def custom_annotate(image_source, phrases, logits, xyxy) -> np.ndarray:
    # h, w, _ = image_source.shape
    # boxes = boxes * torch.Tensor([w, h, w, h])
    # xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    detections = sv.Detections(xyxy=xyxy)

    labels = [
        f"{phrase} {logit:.2f}"
        for phrase, logit
        in zip(phrases, logits)
    ]

    box_annotator = sv.BoxAnnotator()
    annotated_frame = cv2.cvtColor(image_source, cv2.COLOR_RGB2BGR)
    annotated_frame = box_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
    return annotated_frame

def crop_detected_objects(image_name, xyxy, phrases, common_classes):
      
    # Opens a image in RGB mode
    IMAGE_DIR = './static/assets/images/input/'
    im = Image.open(os.path.join(IMAGE_DIR, image_name))
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    # width, height = im.size
    
    # Cropped image of above dimension
    # (It will not change original image)
    
    with open(os.path.join('../detectron2', 'labels.txt'), 'r') as f:
        labels = f.readlines()
    
    inacc_classes = []
    
    for c in labels:
        inacc_classes.append(c.split(" ")[-1].strip())
    
    print('cropping', phrases)
    for i, phrase in enumerate(phrases):
        if phrase in common_classes or phrase in inacc_classes:
            print(phrase, xyxy[i])
            cropped = im.crop((xyxy[i][0], xyxy[i][1], xyxy[i][2], xyxy[i][3]))
            phrase = phrase.replace(" ", "_")
            cropped_image_name = phrase + ".png"
            cropped.save(os.path.join(detected_object_folder, image_name, cropped_image_name))
    
    """
    GroundingDINO inference
    """
def run_grounding_dino(common_classes, image_name='Olivia_2.png'):
    """ Run grounding dino

    Args:
        text_prompt (_type_): _description_
        image_name (str, optional): _description_. Defaults to 'Olivia_2.png'.
    """
    model = load_model("../groundingdino/GroundingDINO_SwinT_OGC.py", "../groundingdino/groundingdino_swint_ogc.pth")
    # IMAGE_PATH = "/media/nahyun/HDD/3dpfix-gt/train/separation/"
    # IMGNAME = "542_o5m0sn.jpg"

    
    IMAGE_DIR = './static/assets/images/input/'
    IMGNAME = image_name
    TEXT_PROMPT = ". ".join(common_classes)
    BOX_TRESHOLD = 0.45
    TEXT_TRESHOLD = 0.45

    image_source, image = load_image(os.path.join(IMAGE_DIR, IMGNAME))

    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    
    # print(boxes)
    # print(logits)
    # print(phrases)

    h, w, _ = image_source.shape
    boxes = boxes * torch.Tensor([w, h, w, h])
    xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    
    # print('xyxy', xyxy)
    # print('xyxy type', type(xyxy))
    # print('xyxy[0] type', type(xyxy[0]))
    # print('xyxy shape', xyxy.shape)
    
    keep_phrases = []
    keep_xyxy = []
    keep_logits = []
    
    for i, phrase in enumerate(phrases):
        phrase = phrase.replace(" ", "_")
        if phrase in common_classes and phrase not in keep_phrases:
            keep_phrases.append(phrase)
            keep_xyxy.append(xyxy[i].tolist())
            keep_logits.append(logits[i])
            
    # print("keep_xyxy", keep_xyxy)
            
    keep_logits = torch.Tensor(keep_logits)
    
    ## add detectron2 inference   
    dt_boxes, dt_logits, dt_phrases = dt.run_detectron_on_image(image_name)
    
    
    # print("final-----gd--")
    # print(keep_xyxy)
    # print(keep_logits)
    # print(keep_phrases)

    
    # print("final-----dt--")
    # print(dt_boxes)
    # print(dt_logits)
    # print(dt_phrases)
    
    # print(np.array(dt_boxes))
    
    # dt_ndarray = []
    # for dt_box in dt_boxes:
    #     # keep_xyxy.append(np.array(dt_box, dtype=np.float32))
    #     # keep_xyxy.append(dt_box)
    #     dt_ndarray.append(np.array(dt_box, dtype=np.float32))
    # dt_ndarray = np.array(dt_ndarray)
    # print('dt boxes', dt_boxes, type(dt_boxes), type(dt_boxes[0]), dt_boxes.shape)
    if len(keep_phrases) != 0:
        keep_xyxy = np.append(keep_xyxy, dt_boxes, axis=0)
        # keep_xyxy += dt_boxes
        final_logits = torch.cat((keep_logits, dt_logits))
        keep_phrases += dt_phrases
    else:
        keep_xyxy = dt_boxes
        final_logits = dt_logits
        keep_phrases = dt_phrases
    
    # print('keep_xyxy', keep_xyxy)
    
    annotated_frame = custom_annotate(image_source, keep_phrases, final_logits, keep_xyxy)
    cv2.imwrite(os.path.join('./static/assets/images/inference_output', IMGNAME), annotated_frame)
    
    crop_detected_objects(image_name, keep_xyxy, keep_phrases, common_classes)

    return list(set(keep_phrases))
    

def main():
    dictionary = "./static/assets/data/3AD_dictionary.json"
    
    with open(dictionary, 'r') as f:
        data = json.load(f)
    
    objects = list(data.keys())
    
    root_objects = []
    
    for o in objects:
        root_objects.append(o.split("__")[0])
        
    print(root_objects)

if __name__ == "__main__":
    run_grounding_dino(common_classes=app.get_common_classes())
    # main()
    