from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
dictionary_file = os.path.join(basedir, 'static', 'assets', 'data', '3AD_dictionary.json')
# design_file = os.path.join(basedir, 'static/assets/data/3AD_design_info.json')

upload_folder = os.path.join(basedir, 'static', 'assets', 'images', 'input')
app.config['UPLOAD'] = upload_folder

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if request.method == 'POST':
#         file = request.files['img']
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD'], filename))
#         name = os.path.join(app.config['UPLOAD'], filename)
#         print(name)

#         ## add inference

#         with open(dictionary_file, 'r') as f:
#             dictionary = json.load(f)
#             f.close()

#         # with open(design_file, 'r') as f:
#         #     designs = json.load(f)
#         #     f.close()
        
#         objects = []

#         # objects = os.listdir(os.path.join(basedir, 'static/assets/images/object/'+name+'/'))
#         # objects = [x.split(".")[0] for x in objec
#         # ts]
#         return redirect(url_for('main', image=filename))
        # return render_template('main.html', name=name, dictionary=dictionary, objects=objects)


@app.route('/main', methods=['GET', 'POST'])
def main():

    # if request.method == 'POST':
    #     # do stuff when the form is submitted

    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('index'))

    # show the form, it wasn't submitted

    # user uploaded the photo
    if request.method == 'POST': 
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        # name = os.path.join(app.config['UPLOAD'], filename)
        image = filename

        # add inference here
        objects = []

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

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/about')
def about():
    return 'About'