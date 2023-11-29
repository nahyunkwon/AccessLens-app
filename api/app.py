from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
import shutil

import grounding_dino_inference as gd

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
dictionary_file = os.path.join(basedir, 'static', 'assets', 'data', '3AD_dictionary.json')
# design_file = os.path.join(basedir, 'static/assets/data/3AD_design_info.json')

upload_folder = os.path.join(basedir, 'static', 'assets', 'images', 'input')
app.config['UPLOAD'] = upload_folder

detected_object_folder = os.path.join(basedir, 'static', 'assets', 'images', 'object')
app.config['DETECTED_OBJECT'] = detected_object_folder # image name

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/main', methods=['GET', 'POST'])
def main():

    # if request.method == 'POST':
    #     # do stuff when the form is submitted

    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('index'))

    # show the form, it wasn't submitted
    
    with open(dictionary_file, 'r') as f:
        dictionary = json.load(f)
        f.close()

    # user uploaded the photo
    if request.method == 'POST': 
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename)) # save into images/input
        
        # detected object cropped images will go to here
        detected_object_path = os.path.join(app.config['DETECTED_OBJECT'], filename)
        
        try:
            os.makedirs(detected_object_path)
        except:
            shutil.rmtree(detected_object_path)
            os.makedirs(detected_object_path)
            
        # 1. GroundingDINO for common classes
        classes = list(dictionary.keys())
        
        common_classes = []
        
        for c in classes:
            common_c = c.split("__")[0].strip()
            common_c = common_c.replace("_", " ")
            if common_c not in common_classes:
                common_classes.append(common_c)
        
        text_prompt = ". ".join(common_classes)
        
        print(text_prompt)
            
        objects = gd.run_grounding_dino(text_prompt=text_prompt, image_name=filename)
        
        image = filename

        # 2. Detectron2 for inaccessibility classes
        

    # pre-defined demo
    else:
        image = request.args['image']
        objects = []

        objects = os.listdir(os.path.join(basedir, 'static/assets/images/object/'+image+'/'))
        objects = [x.split(".")[0] for x in objects]

    with open(dictionary_file, 'r') as f:
        dictionary = json.load(f)
        f.close()

    return render_template('main.html', image=image, dictionary=dictionary, objects=objects)

@app.route('/demo')
def demo():
    # if request.method == 'POST':
    #     # do stuff when the form is submitted

    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('demo.html')

@app.route('/design')
def design():
    
    with open(dictionary_file, 'r') as f:
        dictionary = json.load(f)
        f.close()
    
    return render_template('design.html', dictionary=dictionary, objects=list(dictionary.keys()))

@app.route('/upload')
def upload():
    return render_template('upload.html')

# @app.route('/about')
# def about():
#     return 'About'