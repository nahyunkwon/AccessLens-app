import sys
sys.path.append('../../GroundingDINO')

from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import torch
import json
import os
from torchvision.ops import box_convert
import supervision as sv


def run_grounding_dino(text_prompt, image_name='Olivia_2.png'):
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
    TEXT_PROMPT = text_prompt
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25

    image_source, image = load_image(os.path.join(IMAGE_DIR, IMGNAME))

    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    
    print(boxes)
    print(logits)
    print(phrases)
    
    h, w, _ = image_source.shape
    boxes = boxes * torch.Tensor([w, h, w, h])
    xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    detections = sv.Detections(xyxy=xyxy)
    
    for ins in xyxy:
        print(ins) # in xyxy format

    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    cv2.imwrite(IMGNAME, annotated_frame)
    

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
    run_grounding_dino(text_prompt="refrigerator. microwave. fork")
    # main()
    