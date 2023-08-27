from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main', methods=['GET'])
def main():
    # if request.method == 'POST':
    #     # do stuff when the form is submitted

    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('index'))

    # show the form, it wasn't submitted
    name = request.args['name']
    with open('/static/assets/data/3AD_dictionary_with_id.json', 'r') as f:
        dictionary = json.load(f)
        f.close()

    with open('/static/assets/data/3AD_design_info.json', 'r') as f:
        designs = json.load(f)
        f.close()
    
    objects = []

    print(designs["1852950"])

    if name == "bathroom_1.jpg":
        objects = ['handle__bar_small', 'switch__toggle_single', 'faucet__lever', 'bottle__pump', 'knob__rotate_round']
    

    return render_template('main.html', dictionary=dictionary, designs=designs, objects=objects)

@app.route('/demo')
def demo():
    # if request.method == 'POST':
    #     # do stuff when the form is submitted

    #     # redirect to end the POST handling
    #     # the redirect can be to the same route or somewhere else
    #     return redirect(url_for('index'))

    # show the form, it wasn't submitted
    return render_template('demo.html')

@app.route('/about')
def about():
    return 'About'