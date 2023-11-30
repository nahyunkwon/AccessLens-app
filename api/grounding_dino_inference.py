import sys
sys.path.append('../../GroundingDINO')

from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import torch
import json
import os
from torchvision.ops import box_convert
import supervision as sv

from PIL import Image

basedir = os.path.abspath(os.path.dirname(__file__))
detected_object_folder = os.path.join(basedir, 'static', 'assets', 'images', 'object')

def crop_detected_objects(image_name, xyxy, phrases, common_classes):
      
    # Opens a image in RGB mode
    IMAGE_DIR = './static/assets/images/input/'
    im = Image.open(os.path.join(IMAGE_DIR, image_name))
    
    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    # width, height = im.size
    
    # Cropped image of above dimension
    # (It will not change original image)
    for i, phrase in enumerate(phrases):
        if phrase in common_classes:
            cropped = im.crop((xyxy[i][0], xyxy[i][1], xyxy[i][2], xyxy[i][3]))
            phrase = phrase.replace(" ", "_")
            cropped_image_name = phrase + ".png"
            cropped.save(os.path.join(detected_object_folder, image_name, cropped_image_name))
    

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


    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    cv2.imwrite(os.path.join('./inference_output', IMGNAME), annotated_frame)
    
    h, w, _ = image_source.shape
    boxes = boxes * torch.Tensor([w, h, w, h])
    xyxy = box_convert(boxes=boxes, in_fmt="cxcywh", out_fmt="xyxy").numpy()
    
    crop_detected_objects(image_name, xyxy, phrases, common_classes)
    
    keep_phrases = []
    
    for phrase in phrases:
        phrase = phrase.replace(" ", "_")
        if phrase in common_classes and phrase not in keep_phrases:
            keep_phrases.append(phrase)

    return keep_phrases
    

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
    