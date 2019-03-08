#!/usr/bin/python3

import boto3, json, os
from flask import Flask, render_template

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

app.run(host='0.0.0.0', port=8888, debug=True)
