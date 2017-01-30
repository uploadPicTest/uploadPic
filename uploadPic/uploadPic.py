

import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


allowed_extensions = ['jpg', 'gif', 'png', 'jpeg']

def valid_extension(filename):
    ext = filename.split('.')[-1]
    return ext in allowed_extensions

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "temp/"
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route('/')
def main_page():
    return '''
    <!doctype html>
    <title>Display a photo</title>
    <p>Submit a file to display, max size 5 MB:</p>
    <p>I was pushed automatically to heroku from Drone!</p>
    <form method=POST enctype=multipart/form-data action="upload">
    <input type=file name=photo>
    <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        #First, make sure the browser thinks a file was sent
        if 'photo' not in request.files:
            return 'No file part present, please try again'
        file = request.files['photo']
        #Now check if a file really is attached
        if file.filename == '':
            return 'No file selected, please try again'
        if valid_extension(file.filename):
            filename = secure_filename(file.filename)
            save_location = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(save_location, filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
        else:
            return 'Please upload a valid file, extensions allowed are jpg, gif, png, jpeg'
        return 'File upload failed, unclear reasons, please try again'
    else:
        return 'File upload failed, please try again'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    save_location = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(save_location, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
