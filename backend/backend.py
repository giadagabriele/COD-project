from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

IMG_FOLDER = os.path.join('static', 'img')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    print(filename.split('.')[1].lower())
    return '.' in filename and \
           filename.split('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("static/img/"+filename)
            return 'File uploaded!'
        else:
            return 'File not accepted'


@app.route('/images')
def images():
    path = 'static/img/'
    files = os.listdir(path)
    return render_template('folder_images.html', files=files)



@app.route('/', methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>File Upload</title>
        </head>
        <body>
            <h1>Upload your File</h1>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    """


# SOLUTION:

# The payload could be a malicious file with a filename that has an allowed extension, such as "file.png.exe", which would bypass the extension filter.