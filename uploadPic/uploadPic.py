
#Richard Ott
#2017/01/29
#Simple flask program to upload a picture and display it to the user
#This heavily follows the instructions at http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

#This could be made a lot better, of course.  The first improvement would
#be to give the uploaded pictures unique names, to avoid the possibility of
#collisions (which would be nearly inevitable in an actual production
#environment).  Another would be to make the error states more informative
#and have a link in them back to the primary page, or have them
#automatically redirect the user after a certain amount of time
#Also, this is *not* scalable to web scale as is, since it's using the
#built in flask server rather than gunicorn (to save development time).
#It should also perodically (or probably every time) delete these image files
#since they're being housed on local disk, it will eventually fill


import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

#Restrict to only image files
allowed_extensions = ['jpg', 'gif', 'png', 'jpeg']

def valid_extension(filename):
    ext = filename.split('.')[-1]
    return ext in allowed_extensions

#Setup a folder to store files, and a max size to allow of 5 MB
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

#Displays the local file back to the user
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    save_location = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(save_location, filename)

#This sets it up to be run with a simple "python uploadPic.py", but uses
#flask's built in server, which isn't great.  This is also very insecure
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
