
from flask import Flask, render_template,request,flash
from werkzeug.utils import secure_filename
import cv2
import os

# Opencv is imported as cv2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'the random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Below method checks whether the file extension is allowed or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename,option):
     print(f"Option: {option} and filename: {filename}")
     img=cv2.imread(f"uploads/{filename}")
     match option:
         case "cgray":
             imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             cv2.imwrite(f"static/{filename}",imgProcessed)
             return filename
     pass

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="POST": 
        option=request.form.get("option")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            processImage(filename,option)
            flash(f"Your image has been processed and is available at <a href='/static/{filename}' target='_blank'> here</a>")
            return render_template("index.html")
        else:
            flash('Invalid file format. Please upload a valid image file.')
            return "error invalid file format"
    

    return render_template("index.html")

# To start the server run the below statement

app.run(debug=True, port=5001)