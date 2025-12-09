from flask import Flask, render_template, request, redirect, session, flash, url_for
from db import create_app, mysql
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from flask import session, flash, get_flashed_messages
from datetime import datetime
import MySQLdb.cursors




app = create_app()
app.secret_key = 'ERP_Hospital'  # Set your secret key for sessions

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Hash the password before storing
        hashed_password = generate_password_hash(password)

        # Get doctor-specific fields if role is Doctor
        specialization = request.form.get('specialization', None)
        contact = request.form.get('contact', None)

        cursor = mysql.connection.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))

        # Insert into Users table (store hashed password)
        cursor.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", 
                       (name, email, hashed_password, role))
        mysql.connection.commit()

        # If Doctor, insert into doctors table
        if role == "Doctor":
            user_id = cursor.lastrowid  # Get last inserted user ID
            cursor.execute("INSERT INTO doctors (id, name, specialization, contact) VALUES (%s, %s, %s, %s)", 
                           (user_id, name, specialization, contact))
            mysql.connection.commit()

        cursor.close()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['role'] = user['role']
            flash('Login successful!', 'success')

           
            # Redirect Based on User Role
            if user['role'] == 'Patient':
                return redirect(url_for('patient_dashboard'))
            elif user['role'] == 'Doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user['role'] == 'Receptionist':
                return redirect(url_for('receptionist_dashboard'))
            elif user['role'] == 'Lab':
                return redirect(url_for('lab_dashboard'))
            elif user['role'] == 'Finance':
                return redirect(url_for('finance_dashboard'))
            elif user['role'] == 'Inventory':
                return redirect(url_for('inventory_dashboard'))
            else:
                flash('Invalid role detected!', 'error')
                return redirect(url_for('login'))

        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')




# Patient Dashboard
@app.route('/patient/dashboard')
def patient_dashboard():
    if 'user_id' not in session or session['role'] != 'Patient':
        flash('Please login first!', 'error')
        return redirect(url_for('login'))

    patient_id = session['user_id']
    cursor = mysql.connection.cursor()

    # Fetching patient details
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()

    # Fetching appointment details
    cursor.execute('SELECT a.*, d.name AS doctor_name FROM appointments a JOIN doctors d ON a.doctor_id = d.id WHERE a.patient_id = %s', (patient_id,))
    appointments = cursor.fetchall()

    # Fetching medical records
    cursor.execute('SELECT * FROM medical_records WHERE patient_id = %s', (patient_id,))
    medical_records = cursor.fetchall()

    # Fetching billing information
    cursor.execute('SELECT * FROM billing WHERE patient_id = %s', (patient_id,))
    bills = cursor.fetchall()

    # Fetching doctor list for appointment booking
    cursor.execute('SELECT id, name, specialization FROM doctors')

    doctors = cursor.fetchall()

    cursor.close()

    return render_template('patient_dashboard.html', patient=patient, appointments=appointments, medical_records=medical_records, bills=bills, doctors=doctors)


# Patient Booking Appointment
@app.route('/patient/book_appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session or session['role'] != 'Patient':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

# Clear any previous flash messages
    session.pop('_flashes', None)

    patient_id = session['user_id']
    doctor_id = request.form.get('doctor_id')
    date = request.form.get('date')
    time = request.form.get('time')

    if not doctor_id or not date or not time:
        flash('All fields are required!', 'error')
        return redirect(url_for('patient_dashboard'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_id, date, time, status)
            VALUES (%s, %s, %s, %s, 'Waiting')
        ''', (patient_id, doctor_id, date, time))
        mysql.connection.commit()
        cursor.close()

        flash('Appointment request submitted! Status: Waiting.', 'success')
    except Exception as e:
        print("Database Error:", str(e))
        flash('Error booking appointment!', 'error')

    return redirect(url_for('patient_dashboard'))



# Doctor Dashboard
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session['role'] != 'Doctor':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    doctor_id = session['user_id']
    cursor = mysql.connection.cursor()

    # Fetching doctor details
    cursor.execute('SELECT * FROM doctors WHERE id = %s', (doctor_id,))
    doctor = cursor.fetchone()

 # Fetch only Scheduled appointments
    cursor.execute('''
        SELECT a.id, a.date, a.time, p.name AS patient_name, a.status
        FROM appointments a 
        JOIN patients p ON a.patient_id = p.id 
        WHERE a.doctor_id = %s AND a.status = %s
    ''', (doctor_id, 'Scheduled'))
    appointments = cursor.fetchall()

        # Fetch Completed appointments
    cursor.execute('''
        SELECT a.id, a.date, a.time, p.name AS patient_name, a.status
        FROM appointments a 
        JOIN patients p ON a.patient_id = p.id 
        WHERE a.doctor_id = %s AND a.status = %s
    ''', (doctor_id, 'Completed'))
    completed_appointments = cursor.fetchall()

    # Fetching patient details for adding records
    cursor.execute('SELECT id, name FROM patients')
    patients = cursor.fetchall()

    # Fetching all medical records added by the doctor
    cursor.execute('''
       SELECT m.*, p.name AS patient_name 
        FROM medical_records m 
       JOIN patients p ON m.patient_id = p.id 
       WHERE m.doctor_id = %s
    ''', (doctor_id,))
    medical_records = cursor.fetchall()

    cursor.close()

    return render_template('doctor_dashboard.html', doctor=doctor, appointments=appointments, patients=patients, medical_records=medical_records, completed_appointments=completed_appointments,)


# Update Appointment Status (e.g., Completed, Cancelled)
@app.route('/doctor/update_appointment/<int:appointment_id>', methods=['POST'])
def update_appointment_status(appointment_id):
    if 'user_id' not in session or session['role'] != 'Doctor':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    status = request.form['status']

     # Allow only status change to "Completed"
    if status != 'Completed':
        flash('Invalid status update!', 'error')
        return redirect(url_for('doctor_dashboard'))
    
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE appointments SET status = %s WHERE id = %s', (status, appointment_id))
    mysql.connection.commit()
    cursor.close()

    flash('Appointment status updated!', 'success')
    return redirect(url_for('doctor_dashboard'))


@app.route('/doctor/add_record', methods=['POST'])
def add_medical_record():
    if 'user_id' not in session or session['role'] != 'Doctor':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    # Debugging: Print received form data
    print("Received Form Data:", request.form)

    patient_id = request.form.get('patient_id')
    diagnosis = request.form.get('diagnosis')
    prescription = request.form.get('prescription')
    doctor_id = session.get('user_id')  # Ensure doctor ID is retrieved

    # Check if values are missing
    if not patient_id or not diagnosis or not prescription:
        flash('All fields are required!', 'error')
        return redirect(url_for('doctor_dashboard'))

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription) 
            VALUES (%s, %s, %s, %s)
        ''', (patient_id, doctor_id, diagnosis, prescription))
        
        mysql.connection.commit()
        cursor.close()
        
        flash('Medical record added successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()  # Rollback to prevent partial insert
        print("Database Error:", str(e))  # Print exact error in console
        flash('Error adding medical record!', 'error')

    return redirect(url_for('doctor_dashboard'))

@app.route('/doctor/request_test', methods=['POST'])
def doctor_request_test():
    if 'user_id' not in session or session['role'] != 'Doctor':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    test_name = request.form['test_name']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO lab_tests (patient_id, test_name, status)
        VALUES (%s, %s, 'Pending')
    """, (patient_id, test_name))
    mysql.connection.commit()
    cursor.close()

    flash('Lab test requested successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))  # or wherever you want


# Receptionist Dashboard
@app.route('/receptionist/dashboard')
def receptionist_dashboard():
    if 'user_id' not in session or session['role'] != 'Receptionist':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

# Clear any previous flash messages
    session.pop('_flashes', None)
    
    cursor = mysql.connection.cursor()

    # Fetch Patients and Doctors for scheduling
    cursor.execute('SELECT id, name FROM patients')
    patients = cursor.fetchall()
    cursor.execute('SELECT id, name FROM doctors')
    doctors = cursor.fetchall()

 # Fetch appointments with 'Waiting' status
    cursor.execute('''
        SELECT a.id, a.date, a.time, d.name AS doctor_name, p.name AS patient_name
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN patients p ON a.patient_id = p.id
        WHERE a.status = %s
    ''', ('Waiting',))
    waiting_appointments = cursor.fetchall()

      # Fetch appointments with 'Scheduled' status
    cursor.execute('''
        SELECT a.id, a.date, a.time, d.name AS doctor_name, p.name AS patient_name
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN patients p ON a.patient_id = p.id
        WHERE a.status = %s
    ''', ('Scheduled',))
    scheduled_appointments = cursor.fetchall()

    cursor.close()

    return render_template('receptionist_dashboard.html', patients=patients, doctors=doctors, waiting_appointments=waiting_appointments, scheduled_appointments=scheduled_appointments)

# Add Patient
@app.route('/receptionist/add_patient', methods=['POST'])
def add_patient():
    if 'user_id' not in session or session['role'] != 'Receptionist':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    session.pop('_flashes', None)

    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    contact = request.form['contact']
    address = request.form['address']
    medical_history = request.form.get('medical_history', '')

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO patients (name, age, gender, contact, address, medical_history) VALUES (%s, %s, %s, %s, %s, %s)',
                   (name, age, gender, contact, address, medical_history))
    mysql.connection.commit()
    cursor.close()

    flash('Patient added successfully!', 'success')
    return redirect(url_for('receptionist_dashboard'))


# Schedule Appointment (Receptionist sets status to 'Scheduled')
@app.route('/receptionist/schedule_appointment', methods=['POST'])
def schedule_appointment():
    if 'user_id' not in session or session['role'] != 'Receptionist':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    appointment_id = request.form['appointment_id']

    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE appointments 
        SET status = %s 
        WHERE id = %s
    ''', ('Scheduled', appointment_id))
    mysql.connection.commit()
    cursor.close()

    flash('Appointment scheduled successfully!', 'success')
    return redirect(url_for('receptionist_dashboard'))


# Cancel Appointment (Receptionist sets status to 'Cancelled')
@app.route('/receptionist/cancel_appointment', methods=['POST'])
def cancel_appointment():
    if 'user_id' not in session or session['role'] != 'Receptionist':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    appointment_id = request.form['appointment_id']

    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE appointments 
        SET status = %s 
        WHERE id = %s
    ''', ('Cancelled', appointment_id))
    mysql.connection.commit()
    cursor.close()

    flash('Appointment canceled successfully!', 'success')
    return redirect(url_for('receptionist_dashboard'))

@app.route('/lab/dashboard')
def lab_dashboard():
    if 'user_id' not in session or session['role'] != 'Lab':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT t.test_id, t.test_name, t.status
        FROM lab_tests t
        JOIN patients p ON t.patient_id = p.id
        WHERE t.status = 'Pending'
    """)
    test_requests = cursor.fetchall()

    cursor.execute("""
        SELECT t.test_id, p.name AS patient_name, t.test_name, t.report_url
        FROM lab_tests t
        JOIN patients p ON t.patient_id = p.id
        WHERE t.status = 'Completed'
    """)
    completed_reports = cursor.fetchall()

    cursor.close()

    return render_template('lab_dashboard.html', test_requests=test_requests, completed_reports=completed_reports)


@app.route('/lab/upload_report', methods=['POST'])
def upload_report():
    if 'user_id' not in session or session['role'] != 'Lab':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    test_id = request.form['test_id']
    report_file = request.files['report_file']

    if report_file and allowed_file(report_file.filename):
        filename = secure_filename(report_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        report_file.save(file_path)

        db_path = os.path.join('static/uploads', filename)

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE lab_tests SET status = 'Completed', report_url = %s WHERE test_id = %s", (db_path, test_id))
        mysql.connection.commit()
        cursor.close()

        flash('Report uploaded successfully!', 'success')
    else:
        flash('Invalid file type or no file selected.', 'error')

    return redirect(url_for('lab_dashboard'))


"""
# Finance Dashboard
@app.route('/finance/dashboard')
def finance_dashboard():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT b.id, p.name AS patient_name, b.amount, b.payment_status, b.payment_date FROM billing b JOIN patients p ON b.patient_id = p.id")
    bills = cursor.fetchall()

    cursor.execute("SELECT i.id, p.name AS patient_name, i.provider, i.policy_number FROM insurance i JOIN patients p ON i.patient_id = p.id")
    insurance_claims = cursor.fetchall()
    
    cursor.close()
    return render_template('finance_dashboard.html', bills=bills, insurance_claims=insurance_claims)


# Generate Bill
@app.route('/finance/generate_bill', methods=['POST'])
def generate_bill():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    amount = request.form['amount']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO billing (patient_id, amount, payment_status) VALUES (%s, %s, %s)",
                   (patient_id, amount, 'Pending'))
    mysql.connection.commit()
    cursor.close()

    flash('Bill generated successfully!', 'success')
    return redirect(url_for('finance_dashboard'))

# Verify Payment
@app.route('/finance/verify_payment', methods=['POST'])
def verify_payment():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    bill_id = request.form['bill_id']

    cursor = mysql.connection.cursor()

    # Verify if bill exists and is in 'Pending' state
    cursor.execute("SELECT payment_status FROM billing WHERE id = %s", (bill_id,))
    bill = cursor.fetchone()

    if not bill:
        flash('Bill not found!', 'error')
    elif bill['payment_status'] == 'Paid':
        flash('Payment already verified.', 'info')
    else:
        # Update to Paid and set the payment date to current time
        cursor.execute("UPDATE billing SET payment_status = 'Paid', payment_date = NOW() WHERE id = %s", (bill_id,))
        mysql.connection.commit()
        flash('Payment verified successfully!', 'success')

    cursor.close()
    return redirect(url_for('finance_dashboard'))

# Add Insurance Route
@app.route('/finance/add_insurance', methods=['POST'])
def add_insurance():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    provider = request.form['provider']
    policy_number = request.form['policy_number']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO insurance (patient_id, provider, policy_number) VALUES (%s, %s, %s)",
                   (patient_id, provider, policy_number))
    mysql.connection.commit()
    cursor.close()

    flash('Insurance added successfully!', 'success')
    return redirect(url_for('finance_dashboard'))


# Manage Insurance Claims (Submit Claims)
@app.route('/finance/manage_insurance', methods=['POST'])
def manage_insurance():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    provider = request.form['provider']
    policy_number = request.form['policy_number']

    # Ensure insurance exists before submitting a claim
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM insurance WHERE patient_id = %s AND provider = %s AND policy_number = %s",
                   (patient_id, provider, policy_number))
    insurance = cursor.fetchone()

    if not insurance:
        flash('No matching insurance found. Please add insurance first.', 'error')
    else:
        cursor.execute("INSERT INTO insurance_claims (patient_id, provider, policy_number, status) VALUES (%s, %s, %s, 'Pending')",
                       (patient_id, provider, policy_number))
        mysql.connection.commit()
        flash('Insurance claim submitted successfully!', 'success')

    cursor.close()
    return redirect(url_for('finance_dashboard'))
"""

@app.route('/finance/dashboard')
def finance_dashboard():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT b.id, p.name AS patient_name, b.amount, b.final_amount, b.payment_status, b.payment_date
        FROM billing b
        JOIN patients p ON b.patient_id = p.id
    """)
    bills = cursor.fetchall()

    cursor.execute("""
        SELECT i.id, p.name AS patient_name, i.provider, i.policy_number, i.coverage_percent
        FROM insurance i
        JOIN patients p ON i.patient_id = p.id
    """)
    insurances = cursor.fetchall()

    cursor.close()
    return render_template('finance_dashboard.html', bills=bills,insurances=insurances)

@app.route('/finance/add_insurance', methods=['POST'])
def add_insurance():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    provider = request.form['provider']
    policy_number = request.form['policy_number']
    coverage_percent = request.form['coverage_percent']

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO insurance (patient_id, provider, policy_number, coverage_percent)
        VALUES (%s, %s, %s, %s)
    """, (patient_id, provider, policy_number, coverage_percent))
    mysql.connection.commit()
    cursor.close()

    flash('Insurance added successfully!', 'success')
    return redirect(url_for('finance_dashboard'))

@app.route('/finance/generate_bill', methods=['POST'])
def generate_bill():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    patient_id = request.form['patient_id']
    amount = float(request.form['amount'])
    claim_insurance = request.form.get('claim_insurance') == 'on'
    final_amount = amount

    cursor = mysql.connection.cursor()

    if claim_insurance:
        provider = request.form['provider']
        policy_number = request.form['policy_number']

        # Check insurance
        cursor.execute("""
            SELECT coverage_percent FROM insurance
            WHERE patient_id = %s AND provider = %s AND policy_number = %s
        """, (patient_id, provider, policy_number))
        insurance = cursor.fetchone()

        if insurance:
            coverage = insurance['coverage_percent'] or 0
            discount = amount * (coverage / 100)
            final_amount = round(amount - discount, 2)

            # Add claim
            cursor.execute("""
                INSERT INTO insurance_claims (patient_id, provider, policy_number, status)
                VALUES (%s, %s, %s, 'Pending')
            """, (patient_id, provider, policy_number))

            flash(f"Insurance claimed with {coverage}% coverage. Final amount: ${final_amount}", 'info')
        else:
            flash("Insurance not found. Proceeding without claim.", 'warning')

    # Insert bill
    cursor.execute("""
        INSERT INTO billing (patient_id, amount, final_amount, payment_status)
        VALUES (%s, %s, %s, 'Pending')
    """, (patient_id, amount, final_amount))

    mysql.connection.commit()
    cursor.close()

    flash('Bill generated successfully!', 'success')
    return redirect(url_for('finance_dashboard'))


@app.route('/finance/verify_payment', methods=['POST'])
def verify_payment():
    if 'user_id' not in session or session['role'] != 'Finance':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    bill_id = request.form['bill_id']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT payment_status FROM billing WHERE id = %s", (bill_id,))
    bill = cursor.fetchone()

    if not bill:
        flash('Bill not found!', 'error')
    elif bill['payment_status'] == 'Paid':
        flash('Already verified.', 'info')
    else:
        cursor.execute("UPDATE billing SET payment_status = 'Paid', payment_date = NOW() WHERE id = %s", (bill_id,))
        mysql.connection.commit()
        flash('Payment verified successfully!', 'success')

    cursor.close()
    return redirect(url_for('finance_dashboard'))

# Inventory Dashboard
@app.route('/inventory/dashboard')
def inventory_dashboard():
    if 'user_id' not in session or session['role'] != 'Inventory':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT p.id, p.medicine_name, p.stock, p.expiry_date, COALESCE(s.name, 'Unknown') AS supplier_name
        FROM pharmacy p
        LEFT JOIN suppliers s ON p.supplier_id = s.id
    """)
    medicines = cursor.fetchall()

    cursor.execute("SELECT medicine_name, stock FROM pharmacy WHERE stock < 10")
    low_stock_alerts = cursor.fetchall()

    cursor.close()
    return render_template('inventory_dashboard.html', medicines=medicines, low_stock_alerts=low_stock_alerts)
@app.route('/inventory/manage_medicine', methods=['POST'])
def manage_medicine():
    if 'user_id' not in session or session['role'] != 'Inventory':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    try:
        medicine_name = request.form['medicine_name']
        stock = int(request.form['stock'])
        expiry_date = request.form['expiry_date']
        supplier_name = request.form['supplier_name']
        supplier_contact = request.form['supplier_contact']

        cursor = mysql.connection.cursor()

        # Check or insert supplier
        cursor.execute("SELECT id FROM suppliers WHERE name = %s", (supplier_name,))
        supplier = cursor.fetchone()

        if not supplier:
            cursor.execute("INSERT INTO suppliers (name, contact) VALUES (%s, %s)", (supplier_name, supplier_contact))
            mysql.connection.commit()
            supplier_id = cursor.lastrowid
        else:
            supplier_id = supplier['id']

        # Check for existing medicine
        cursor.execute("SELECT id FROM pharmacy WHERE medicine_name = %s AND supplier_id = %s", (medicine_name, supplier_id))
        med = cursor.fetchone()

        if med:
            cursor.execute("""
                UPDATE pharmacy SET stock = stock + %s, expiry_date = %s
                WHERE id = %s
            """, (stock, expiry_date, med['id']))
            flash('Stock updated successfully!', 'success')
        else:
            cursor.execute("""
                INSERT INTO pharmacy (medicine_name, stock, expiry_date, supplier_id)
                VALUES (%s, %s, %s, %s)
            """, (medicine_name, stock, expiry_date, supplier_id))
            flash('Medicine added successfully!', 'success')

        mysql.connection.commit()

    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error: {str(e)}', 'error')

    finally:
        cursor.close()

    return redirect(url_for('inventory_dashboard'))
@app.route('/inventory/adjust_stock', methods=['POST'])
def adjust_stock():
    if 'user_id' not in session or session['role'] != 'Inventory':
        flash('Unauthorized access!', 'error')
        return redirect(url_for('login'))

    medicine_id = request.form['medicine_id']
    action = request.form['action']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT stock FROM pharmacy WHERE id = %s", (medicine_id,))
    medicine = cursor.fetchone()

    if not medicine:
        flash('Medicine not found.', 'error')
    else:
        new_stock = medicine['stock'] + 1 if action == 'increase' else medicine['stock'] - 1
        if new_stock < 0:
            flash('Stock cannot be negative.', 'error')
        else:
            cursor.execute("UPDATE pharmacy SET stock = %s WHERE id = %s", (new_stock, medicine_id))
            mysql.connection.commit()
            flash(f'Stock {"increased" if action == "increase" else "decreased"} successfully.', 'success')

    cursor.close()
    return redirect(url_for('inventory_dashboard'))



# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
