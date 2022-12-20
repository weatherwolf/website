import os

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
from main import RunFile

app = Flask(__name__)
filename = 'none'

@app.route('/', methods=['GET', 'POST'])
def home():
    global filename
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('input', filename))
            
            # RunFile(filename)
        return redirect(url_for('loading'))
    return render_template('home.html')


@app.route('/loading')
def loading():
    print(filename)
    render_template('loading.html')
    if filename != 'none':
        RunFile(filename)
    return redirect(url_for('download'))

@app.route('/download', methods=['GET', 'POST'])
def download():
    return render_template('download.html', files=os.listdir('output'))
    # return "Success"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(debug=True)