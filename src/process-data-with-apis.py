from flask import Flask, request, jsonify
import pandas as pd
from PIL import Image
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import base64
from flask_cors import CORS

from matplotlib import pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

from pathlib import Path

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return "hello world!"

@app.route('/api/process-csv', methods=['POST'])
def process_csv():
    print('process_csv')
    file = request.files['file']
    print(str(file.filename))
    df = pd.read_csv(file)
    # process the CSV data and generate an image
    image = fetch_chart(df,file)
    # return the processed image as JSON
    response_data = {'imageUrl': "data:image/jpeg;base64,"+image_to_base64(image)}
    return jsonify(response_data)

def fetch_chart(df,file):
    file_name=str(file.filename)
    img_name=file_name.split('.')[0]+'.png'
    print('img_name',img_name)
    plt.scatter(df['x'],df['y'],color='blue')

    img_path=Path(img_name)
    plt.savefig(img_path)
    img=Image.open(img_path)
    return img


@app.route('/api/fit_model',methods=['POST'])
def fit_model():
    print('fit model')
    file = request.files['file']
    file_name=str(file.filename)
    print(str(file.filename))
    # print(os.path.exists(file))
    df = pd.read_csv(file)   
    image,modelCoef,coefDeter=fetch_linear_reg_plot(df,file_name)
    response_data = {'imageUrl': "data:image/jpeg;base64,"+image_to_base64(image),'modelCoef':modelCoef,'coefDeter':coefDeter}
    return jsonify(response_data)


def fetch_linear_reg_plot(df,file_name):

    fit_img_name=file_name.split('.')[0]+'_fit.png'
    print('img_name',fit_img_name)
    img_path=Path(fit_img_name)
    print('fit linear model ')

    model=LinearRegression()
    # x=np.array(df['x'])
    y=np.array(df['y'])
    x=np.array([[x] for x in df['x']])

    x_train=x[:-10]
    y_train=y[:-10]

    x_test=x[-10:]
    y_test=y[-10:]

    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)

    y_pred_train=model.predict(x_train)
    # The coefficients
    coef=round(model.coef_[0],3)
    print("Coefficients: \n", coef)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    coef_deter=r2_score(y_test, y_pred)
    print("Coefficient of determination: %.2f" % coef_deter)


    # Plot outputs
    plt.scatter(x_train, y_train, color="blue")
    plt.plot(x_test, y_pred, color="yellow", linewidth=3)
    plt.plot(x_train, y_pred_train, color="green", linewidth=4)

    plt.xticks(())
    plt.yticks(())
    fit_img_path=Path(fit_img_name)
    plt.savefig(fit_img_path)
    img=Image.open(fit_img_path)
    return img,coef,coef_deter

def image_to_base64(image):
    with io.BytesIO() as buffer:
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)
