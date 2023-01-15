from flask import Flask, render_template, request, redirect, url_for
import os
import sys
import random
import csv
import pandas as pd

app = Flask(__name__)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files/'
FILE_PATH = ''
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
data = []
already_ans =[]

# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    global data
    global FILE_PATH
    global already_ans
    data = []
    already_ans = []
    # get the uploaded file
    uploaded_file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    FILE_PATH = file_path
    print(FILE_PATH)
    # set the file path
    uploaded_file.save(FILE_PATH)
    csv = parseCSV(FILE_PATH)
    for i in range(len(csv)):
        data.append(csv.loc[i,"Question"])
    return redirect(request.url)

@app.route("/generate",methods=['GET', 'POST'])
def generateQuestion():
    global data
    global already_ans
    q = checkAA(random.choice(data))
    return render_template('index.html',data=q,aa=already_ans)



def parseCSV(filePath):
    df = pd.DataFrame(pd.read_excel(filePath), columns=["Question"])
    return df

def checkAA(q):
    global already_ans
    global data
    if len(already_ans) == len(data):
        already_ans = []
    while q in already_ans:
        print("qui")
        q = random.choice(data)
    already_ans.append(q)
    return q



if (__name__ == "__main__"):
     app.run(port = 5000)