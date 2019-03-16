#!/usr/bin/python3

import boto3, json, os
from flask import Flask, render_template, send_from_directory
from flask import request

app = Flask(__name__)

## function to display hello world current time

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

## function to display login page

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/string')
def action():
    return render_template('string.html')

@app.route('/forgotpasswd')
def forgot():
    return render_template('forgotpasswd.html')

## function to display string in uppercase from lambda function

client = boto3.client('lambda', region_name='ap-south-1')

@app.route("/uc/<param>", methods=['GET'])
def helloworld(param):
    payload = '{"key":"%s"}' % (param)
    response = client.invoke(FunctionName='amit_lambda', Payload=payload)
    print(response)

    output= json.loads(response['Payload'].read().decode('utf-8'))
    result1 = {'input' :input ,'return_str':output}
    return render_template('ucase.html', result=result1)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

## Detect the images uploaded by user

@app.route('/image')
def index():
     return '''<form method=POST enctype=multipart/form-data action="upload">
     <p>WELCOME TO MY ZONE <br><br><br><br>
     <p>Select the file to Upload <br><br>
     <input type=file name=myfile> <br><br>
     <input type="submit" value="Upload File">
     </form><style>
body {
    -webkit-animation: colorchange 60s infinite;
    animation: colorchange 60s infinite;
}
@-webkit-keyframes colorchange {
     0%  {background: #33FFF3;}
    25%  {background: #78281F;}
    50%  {background: #117A65;}
    75%  {background: #DC7633;}
    100% {background: #9B59B6;}
}
@keyframes colorchange {
     0%  {background: #33FFF3;}
    25%  {background: #78281F;}
    50%  {background: #117A65;}
    75%  {background: #DC7633;}
    100% {background: #9B59B6;}
}
</style>
</body>'''

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['myfile']
    s3 = boto3.resource('s3')
    s3.Bucket('upload-amit').put_object(Key=file.filename, Body=request.files['myfile'])

    x = {
          'key1': 'upload-amit',
          'key2': file.filename
        }
    payload = json.dumps(x)

    response = client.invoke(FunctionName='uploadimagerekog',Payload=payload)
    output= json.loads(response['Payload'].read().decode('utf-8'))
    result = {'return_str':output}
    return render_template('uploadimage.html', result=result)

app.run(host='0.0.0.0', port=8888, debug=True)
