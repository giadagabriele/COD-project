from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)


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
        elif file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save("static/img/"+filename)
            return 'File uploaded!'+images()
            
        elif file and not allowed_file(file.filename):
            return 'File not accepted'+home()


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
        <body style="max-width: max-content; margin: auto; margin-top: 100px">
            <h1 style="color: red; font-family: Arial, Helvetica, sans-serif;">Upload your File</h1>
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <br><br>
                <input style="height:40px; width:250px;" type="submit" value="Upload">
                <br><br><br>
                <hr>
                <br><br>
                <a style="color: black;" href="http://127.0.0.1:5000/images"><button style="height:50px; width:250px;" type="button">List of images already uploaded</button></a>
            </form>
        </body>
    </html>
    """