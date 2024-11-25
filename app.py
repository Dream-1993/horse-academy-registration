from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define folder for uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'pdf'}

# Configure the uploads set
photos = UploadSet('photos', IMAGES)
documents = UploadSet('documents', DOCUMENTS)
configure_uploads(app, (photos, documents))

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    if request.method == 'POST':
        # Personal details from the form
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        emergency_contact = request.form['emergency_contact']
        date = request.form['date']
        
        # Handle file uploads
        signature = request.files['signature']
        photo = request.files['photo']
        
        if signature and allowed_file(signature.filename):
            signature_filename = secure_filename(signature.filename)
            signature.save(os.path.join(app.config['UPLOAD_FOLDER'], signature_filename))
        else:
            return "Invalid signature file. Only PDF is allowed."
        
        if photo and allowed_file(photo.filename):
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        else:
            return "Invalid photo file. Only JPG, PNG, and PDF are allowed."
        
        # Here you can save the data to a database or send an email, etc.
        # For now, let's just print the data to console (this is just for demonstration).
        print(f"Registration submitted:\nName: {name}\nDOB: {dob}\nEmail: {email}\nPhone: {phone}")
        print(f"Address: {address}\nEmergency Contact: {emergency_contact}\nDate: {date}")
        print(f"Signature file: {signature_filename}\nPhoto file: {photo_filename}")
        
        # After successful submission, redirect or render a confirmation page
        return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return "Registration successful! We have received your details."

if __name__ == '__main__':
    app.run(debug=True)
