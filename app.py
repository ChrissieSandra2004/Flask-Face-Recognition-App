from flask import Flask, render_template, Response, request, redirect, url_for, session, flash, send_from_directory, jsonify
from flask_paginate import Pagination
from math import ceil
import cv2
import face_recognition
import numpy as np
from werkzeug.utils import secure_filename
import mysql.connector
import os
from datetime import date
import pandas as pd
from jinja2 import Environment
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity



app = Flask(__name__)
camera = cv2.VideoCapture(0)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/Images'
# app.secret_key = 'abcd@1234&xyz@123'

app.config['JWT_SECRET_KEY'] = 'abcd@1234&xyz@123'
jwt = JWTManager(app)

# Define a custom filter function for 'min'
def custom_min(a, b):
    return min(a, b)

# Add the custom filter to the Jinja2 environment
env = Environment()
env.filters['min'] = custom_min


# Connecting to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="flaskdb",
    auth_plugin='mysql_native_password'
)
cursor = db.cursor()

# Fetching image paths and names from the database
cursor.execute("SELECT empimg, fname FROM employees_data")
employee_data = cursor.fetchall()


# Loading known face encodings and names from the fetched data
known_face_encodings = []
known_face_names = []

for image_path, name in employee_data:
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

# Initializing some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

face_recognition_threshold = 0.6


def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []

            for face_encoding in face_encodings:
                # Compare face distances and use threshold for identification
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                name = known_face_names[best_match_index] if face_distances[best_match_index] < face_recognition_threshold else "Unknown"
                face_names.append(name)

            # Displaying the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                if name == "Unknown":
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                else:
                    cv2.rectangle(frame, (left, top), (right, bottom), (127, 189, 65), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (127, 189, 65), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



def check_admin_role(email):
    cursor.execute("SELECT roles FROM employees_data WHERE mail = %s", (email,))
    result = cursor.fetchone()
    
    if result and (result[0] == 'admin' or result[0] == 'global_admin'):
        return True
    else:
        return False

def authenticate_user(email, password):
    cursor.execute("SELECT mail, fname, lname, roles, empimg FROM employees_data WHERE mail = %s AND password = %s", (email, password))
    result = cursor.fetchone()
    return result


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['mail_id']
        password = request.form['password']

        user_info = authenticate_user(email, password)

        if user_info:
            session['user_email'] = user_info[0]
            session['user_fname'] = user_info[1]
            session['user_lname'] = user_info[2]

            # Fetch additional information from the employees_data table
            cursor.execute("SELECT roles, cmpcode FROM employees_data WHERE mail = %s", (email,))
            emp_data = cursor.fetchone()

            if emp_data:
                role = emp_data[0]
                cmpcode_emp = emp_data[1]

                if role == 'admin':
                    # Redirect to the 'admin' route and pass the 'cmpcode'
                    return redirect(url_for('admin', cmpcode=cmpcode_emp))
                elif role == 'global_admin':
                    return redirect(url_for('global_admin'))

            # If the role is null or there is no match, redirect to video_feed
            return redirect(url_for('videofeed'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the entire session
    session.clear()
    return redirect(url_for('index'))


@app.route('/set_entries_per_page', methods=['POST'])
def set_entries_per_page():
    if request.method == 'POST':
        per_page = request.form['per_page']
        if per_page == 'all':
            session.pop('per_page',None)
        else:
            per_page = int(per_page)
            session['per_page'] = per_page
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/')
def index():
    return render_template('index.html')
  
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/videofeed")
def videofeed():
    return render_template('webcam.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/global_admin')
def global_admin():
    per_page = int(request.args.get('per_page', 5))
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search_query', '')

    # Calculate the offset to determine which records to retrieve
    offset = (page - 1) * per_page

    # Query the database to retrieve the company data with search and pagination
    if per_page == 0:
        # Retrieve all records when per_page is 0
        cursor.execute("SELECT cmpname, cmpcode FROM 
                       companies_data WHERE cmpname LIKE %s", ('%' + search_query + '%',))
    else:
        cursor.execute("SELECT cmpname, cmpcode FROM companies_data WHERE cmpname LIKE %s LIMIT %s OFFSET %s", ('%' + search_query + '%', per_page, offset))
    companies_data = cursor.fetchall()

    # Calculate the total number of entries
    cursor.execute("SELECT COUNT(*) FROM companies_data WHERE cmpname LIKE %s", ('%' + search_query + '%',))
    total_entries = cursor.fetchone()[0]

    if per_page == 0:
        per_page = total_entries  # Display all entries if per_page is set to 0

    # Calculate pagination variables
    total_pages = int(ceil(total_entries / per_page))
    start = (page - 1) * per_page + 1
    end = min(page * per_page, total_entries)
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    pages_list = list(range(1, total_pages + 1))

    return render_template('global_admin.html', companies_data=companies_data, total_entries=total_entries, start=start, end=end,
                           prev_page=prev_page, next_page=next_page, pages_list=pages_list, per_page=per_page, search_query=search_query, page=page)


@app.route('/add_company', methods=['POST'])
def add_company():
    if request.method == 'POST':
        cmpname = request.form['cmpname']
        cmpcode = request.form['cmpcode']

        # Perform validation and insert the data into the database
        if not cmpname or not cmpcode:
            flash('Please fill in all the fields.', 'danger')
        else:
            cursor.execute("INSERT INTO companies_data (cmpname, cmpcode) VALUES (%s, %s)", (cmpname, cmpcode))
            db.commit()
            # flash('Company added successfully.', 'success')

    return redirect(url_for('global_admin'))

@app.route('/update_company', methods=['GET', 'POST'])
def update_company():
    if request.method == 'GET':
        # Retrieve the current company details
        cmpcode = request.args.get('cmpcode')
        cursor.execute("SELECT cmpname, cmpcode FROM companies_data WHERE cmpcode = %s", (cmpcode,))
        company_data = cursor.fetchone()
        if company_data:
            company_name, company_code = company_data
        else:
            flash('Company not found.', 'danger')
            return redirect(url_for('global_admin'))

        return render_template('update_company.html', company_name=company_name, company_code=company_code)

    if request.method == 'POST':
        # Update the company information
        cmpname = request.form['cmpname']
        cmpcode = request.form['cmpcode']

        if not cmpname or not cmpcode:
            flash('Please fill in all the fields.', 'danger')
        else:
            cursor.execute("UPDATE companies_data SET cmpname = %s where cmpcode = %s ", (cmpname, cmpcode))
            cursor.execute("UPDATE companies_data SET cmpcode = %s where cmpname = %s ", (cmpcode, cmpname))  

            # cursor.execute("UPDATE companies_data SET cmpcode = %s where cmpname = %s", (cmpcode, cmpname))
            db.commit()
            # flash('Company updated successfully.', 'success')
        return redirect(url_for('global_admin'))


@app.route('/delete_company', methods=['POST'])
def delete_company():
    if request.method == 'POST':
        cmpcode = request.form['cmpcode']
        
        # Get the list of employees associated with the company
        cursor.execute("SELECT empcode, empimg FROM employees_data WHERE cmpcode = %s", (cmpcode,))
        employees = cursor.fetchall()

        # Delete employees and their images
        for empcode, image_filename in employees:
            # Delete the employee's image file (assuming they are stored on the server)
            if image_filename:
                image_path = os.path.join('/static/images', image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)

            # Delete the employee from the database
            cursor.execute("DELETE FROM employees_data WHERE empcode = %s", (empcode,))

        # Delete the company from the database
        cursor.execute("DELETE FROM companies_data WHERE cmpcode = %s", (cmpcode,))
        
        db.commit()
        # flash('Company, associated employees, and their images deleted successfully.', 'success')
    
    return redirect(url_for('global_admin'))


@app.route('/admin', methods=['GET'])
def admin():
    cmpcode = request.args.get('cmpcode')
    page = request.args.get('page', default=1, type=int)
    search_query = request.args.get('search', default='', type=str)
    per_page = session.get('per_page', 5)

    records = get_records_by_cmpcode(cmpcode)

    if search_query:
        records = filter_records(records, search_query)

    total_entries = len(records)

    if per_page == 0:
        per_page = total_entries  # Display all entries if per_page is set to 0

    # Calculate pagination variables
    start, end, pagination, prev_page, next_page, pages_list = calculate_pagination(page, per_page, total_entries)

    # Slice the records for the current page
    entries = records[start:end]
    

    return render_template('admin.html', cmpcode=cmpcode, employees=entries, start=start, end=end,
                           pagination=pagination, prev_page=prev_page, next_page=next_page,
                           pages_list=pages_list, search_query=search_query, per_page=per_page)


def get_records_by_cmpcode(cmpcode):
    # Fetch records from employees_data where cmpcode matches
    cursor.execute("SELECT * FROM employees_data WHERE cmpcode = %s ORDER BY fname ASC", (cmpcode,))
    records = cursor.fetchall()
    return records

def filter_records(records, search_query):
    # Filter records based on the search query
    filtered_records = []
    for record in records:
        if search_query.lower() in record[1].lower():
            filtered_records.append(record)
    return filtered_records


def calculate_pagination(page, per_page, total_entries):
    start = (page - 1) * per_page
    end = min(start + per_page, total_entries)

    pagination = Pagination(page=page, per_page=per_page, total=total_entries)
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < pagination.total_pages else None
    pages_list = list(range(1, pagination.total_pages + 1))

    return  start, end, pagination, prev_page, next_page, pages_list

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['mail']
        password = request.form['password']
        file = request.files['empimg']
        dob = request.form['dob']
        empcode = request.form['empcode']
        status = request.form['status']
        cmpcode = request.form['cmpcode']


        # Check if the email already exists in the database
        cursor.execute("SELECT mail FROM employees_data WHERE mail = %s", (email,))
        existing_email = cursor.fetchone()

        if existing_email:
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('admin'))

        # Modify this part of your code in the 'insert' route:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Replace backslashes with forward slashes in img_path
            img_path = img_path.replace("\\", "/")
        else:
            flash('Invalid file format. Please upload an image with extensions jpg, jpeg, png, or gif.', 'danger')
            return redirect(url_for('admin'))

        cursor.execute("INSERT INTO employees_data (fname, lname, mail, password, empimg, dob, empcode, status, cmpcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fname, lname, email, password, img_path, dob, empcode, status, cmpcode))
        db.commit()
        
        # Load the updated employee data
        cursor.execute("SELECT empimg, fname FROM employees_data WHERE mail = %s", (email,))
        employee_data = cursor.fetchall()

        # Load and append the new employee's face encoding to the known_face_encodings list
        for image_path, name in employee_data:
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

        flash('Employee added successfully.', 'success')
        return redirect(url_for('admin', cmpcode=cmpcode))

# ---------------------------->

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        # id_data = request.form['id']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['mail']
        password = request.form['password']
        dob = request.form['dob']
        empimg_update = request.files['empimg_update']  # Updated image file
        # Get the current image path
        current_img_path = request.form['current_img_path']
        empcode = request.form['empcode']
        status = request.form['status']
        cmpcode = request.form['cmpcode']

        # Check if a new image is provided
        if empimg_update and allowed_file(empimg_update.filename):
            # Delete the old image from the folder
            if os.path.exists(current_img_path):
                os.remove(current_img_path)
            # Save the new image to the folder with a unique filename
            filename = secure_filename(empimg_update.filename)
            new_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            empimg_update.save(new_img_path)
            # Replace backslashes with forward slashes in img_path
            new_img_path = new_img_path.replace("\\", "/")
        else:
            # If no updated image is provided, use the current image path
            new_img_path = current_img_path

        # Update the employee's information and image path in the database
        cursor.execute("UPDATE employees_data SET fname=%s, lname=%s, mail=%s, dob=%s, password=%s, empimg=%s, empcode=%s, status=%s, cmpcode=%s WHERE mail=%s", (fname, lname, email, dob, password, new_img_path, empcode, status, cmpcode, email))
        db.commit()

        flash('Employee information updated successfully.', 'success')
        return redirect(url_for('admin', cmpcode=cmpcode))
       

@app.route('/delete/<string:email>', methods=['GET'])
def delete(email):
    # Remove the person's face encoding and name from the lists
    index_to_remove = None
    for i, known_email in enumerate(known_face_names):
        if known_email == email:
            index_to_remove = i
            break

    if index_to_remove is not None:
        known_face_encodings.pop(index_to_remove)
        known_face_names.pop(index_to_remove)

    # Get the path of the image associated with the email
    cursor.execute("SELECT empimg, cmpcode FROM employees_data WHERE mail=%s", (email,))
    result = cursor.fetchone()
    
    if result:
        image_path = result[0]
        cmpcode = result[1]
        # Check if the file exists and delete it
        if os.path.exists(image_path):
            os.remove(image_path)
            # flash(f"Image associated with '{email}' deleted successfully.", 'success')
        else:
            flash(f"Image associated with '{email}' does not exist.", 'warning')
    
    cursor.execute("DELETE FROM employees_data WHERE mail=%s", (email,))
    db.commit()

    flash('Employee deleted successfully.', 'success')
    
    # Reload the updated known_face_encodings and known_face_names
    cursor.execute("SELECT empimg, fname FROM employees_data")
    employee_data = cursor.fetchall()
    known_face_encodings.clear()
    known_face_names.clear()
    for image_path, name in employee_data:
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

    return redirect(url_for('admin', cmpcode=cmpcode))


@app.route('/check_email', methods=['POST'])
def check_email():
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT mail FROM employees_data WHERE mail = %s", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            return jsonify({'exists': True})
        else:
            return jsonify({'exists': False})

@app.route('/static/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/excel')
def download_excel():
    cursor.execute("SELECT mail, fname, lname, dob, password, empimg FROM employees_data")
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=['Email', 'First Name', 'Last Name', 'Date of Birth', 'Password', 'Image Path'])
    
    excel_writer = pd.ExcelWriter('employee_data.xlsx', engine='xlsxwriter')
    
    df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
    
    excel_writer.close()
    
    return send_from_directory('', 'employee_data.xlsx', as_attachment=True)



@app.route('/check_face_match', methods=['POST'])
def check_face_match():
    # Capture a frame from the camera
    success, frame = camera.read()
    if not success:
        return jsonify({"message": "Camera not available"})
 
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
     # Find faces in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    min_distance = float("inf")  # Initialize min_distance to positive infinity
    for face_encoding in face_encodings:
    # Compare the detected face with known face encodings
     face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
     match_index = np.argmin(face_distances)
     min_distance = face_distances[match_index]
     if min_distance <= face_recognition_threshold:
        matched_name = known_face_names[match_index]
         # Send a response to the frontend indicating a match
        response_data = {
            "message": "Matched",
            "name": matched_name,
            "attended": True,
        }
        return jsonify(response_data)
    else:
    # If no match is found after checking all face encodings, return a "Not Matched" response
        response_data = {
        "message": "Not Matched",
        "name": "Unknown",
        "attended": False,
       }
        return jsonify(response_data)


@app.route('/get_token', methods=['POST'])
def get_token():
    access_token = create_access_token(identity='anonymous_user')
    return jsonify(access_token=access_token), 200
    print(access_token)
# Access videofeed_jwt with token as a route parameter
@app.route('/videofeed_jwt', methods=['GET'])
@jwt_required()
def videofeed_jwt():
    # Access the token using the 'get_jwt_identity()' function
    current_user = get_jwt_identity()
    return render_template('webcam.html', current_user=current_user)    

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)

