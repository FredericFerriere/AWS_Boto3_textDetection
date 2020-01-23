import boto3
import re
import base64
import io
from PIL import Image

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    ak = 'your Access Key'
    sak = 'your security access Key'
    stk = 'your security token'
    client = boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ak, aws_secret_access_key=sak, aws_session_token=stk)
    imgdata = request.get_data()
    imgstr = re.search(r'base64,(.*)', str(imgdata)).group(1)

    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(str(imgstr)))

    with open('output.png', 'rb') as image:
        res = client.detect_text(Image={'Bytes': image.read()})
        textDetected = res['TextDetections']
        respList = []
        for el in textDetected:
            if el['Type'] == 'WORD':
                respList.append(el['DetectedText'])
        response = jsonify(respList)

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response



if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000)