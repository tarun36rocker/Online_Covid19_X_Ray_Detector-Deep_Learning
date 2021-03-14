from __future__ import division, print_function
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.models import Sequential

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer


model = pickle.load(open('model.pkl', 'rb'))   



UPLOAD_FOLDER = '/static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def model_predict(img_path, model):
    test_image = image.load_img(img_path, target_size=(64, 64))
    test_image=image.img_to_array(test_image) #converts it into 3d array
    test_image=np.expand_dims(test_image,axis=0)
    prediction = model.predict(test_image)
    return prediction

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/predict',methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', prediction_text='No file at all ! ! ')
        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', prediction_text='File Error ! ')

        if file and allowed_file(file.filename):
            file_path=os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            prediction = model_predict(file_path, model)
            #print(prediction)
            count=0
            for i in range(len(prediction[0])):
                if(prediction[0][i]==0):
                    count+=1
                elif(prediction[0][i]==1):
                    break
            if(count==0):
                output="COVID_19"
                pic='https://www.diagnosticcentres.in/uploads/product_image/1585835705123597-coronavirus-2.jpg'
            elif(count==1):
                output="Normal Patient"
                pic='https://oc-covid19.org/wp-content/uploads/2021/03/Short_long-term_future-500x300.jpg' 
            else:
                output="Pneumonia"  
                pic='https://www.globaltimes.cn/Portals/0/attachment/2020/2020-01-11/d2422e61-633c-4c56-bf49-2d11325fd38d.jpeg'
            

               
            #output=prediction
            return render_template('final.html', prediction_text='X-Ray Results: {}'.format(output),pic=pic)
            



if __name__ == '__main__':
    app.run(debug=True)
    
