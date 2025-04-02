from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import MySQLdb.cursors


import pymysql


from config import Config  # Import config settings

app = Flask(__name__)
app.secret_key = 'NetGuard_SK'


# Load MySQL settings from config.py
app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB
app.config['MYSQL_PORT'] = 11810
app.config['MYSQL_CONNECT_TIMEOUT'] = 20


mysql = MySQL(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Flask-Mail setup (assuming you're using Flask-Mail for email sending)

# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, uid, email, role):
        self.id = uid
        self.email = email
        self.role = role

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("SELECT * FROM user WHERE UID = %s", (user_id,))
        user = cursor.fetchone()
        if user:
            return User(user["UID"], user["email"], user["role"])
    return None

# ---------------- AUTHENTICATION ROUTES ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and user['password'] == password:  # Check password without hash
                login_user(User(user['UID'], user['email'], user['role']))
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/')
@login_required
def index():
    return render_template('index.html')  # Render the first page from index.html

# Manage Equipment - List all equipment with filters
@app.route('/manage_equipment', methods=['GET', 'POST'])
@login_required
def manage_equipment():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:

    
        # Get filter parameters from the URL
        name = request.args.get('name', '').strip()
        type = request.args.get('type', '').strip()
        location = request.args.get('location', '').strip()
        vid = request.args.get('vid', '').strip()
        status = request.args.get('status', '').strip()
        purchase_date = request.args.get('purchase_date', '').strip()
        warranty_end_date = request.args.get('warranty_end_date', '').strip()

        # Base query
        query = "SELECT * FROM equipment WHERE 1=1"
        params = []

        # Add filters if provided
        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")
        if type:
            query += " AND type LIKE %s"
            params.append(f"%{type}%")
        if location:
            query += " AND location LIKE %s"
            params.append(f"%{location}%")
        if vid:
            query += " AND VID = %s"
            params.append(vid)
        if status:
            query += " AND status = %s"
            params.append(status)
        if purchase_date:
            query += " AND purchase_date = %s"
            params.append(purchase_date)
        if warranty_end_date:
            query += " AND warranty_end_date = %s"
            params.append(warranty_end_date)

        cursor.execute(query, tuple(params))
        equipment_data = cursor.fetchall()

        if request.method == 'POST' and 'delete' in request.form:
            # Handle equipment deletion
            eid = request.form['eid']
            cursor.execute('DELETE FROM equipment WHERE EID=%s', (eid,))
            mysql.connection.commit()
            return redirect(url_for('manage_equipment'))

    return render_template('manage_equipment.html', equipment=equipment_data,
                           name=name, type=type, location=location, vid=vid,
                           status=status, purchase_date=purchase_date, warranty_end_date=warranty_end_date)

# Add Equipment
@app.route('/add_equipment', methods=['GET', 'POST'])
@login_required
def add_equipment():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        if request.method == 'POST':
            name = request.form['name']
            type = request.form['type']
            location = request.form['location']
            status = request.form['status']
            vid = request.form['vid']
            purchase_date = request.form['purchase_date']
            warranty_end_date = request.form['warranty_end_date']
            
            
            cursor.execute('''
                INSERT INTO equipment (name, type, location, status, VID, purchase_date, warranty_end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (name, type, location, status, vid, purchase_date, warranty_end_date))
            mysql.connection.commit()
            return redirect(url_for('manage_equipment'))
    
    return render_template('add_equipment.html')

# Edit Equipment
@app.route('/edit_equipment/<int:eid>', methods=['GET', 'POST'])
@login_required
def edit_equipment(eid):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        
        
        if request.method == 'POST':
            name = request.form['name']
            type = request.form['type']
            location = request.form['location']
            status = request.form['status']
            vid = request.form['vid']
            purchase_date = request.form['purchase_date']
            warranty_end_date = request.form['warranty_end_date']
            
            cursor.execute('''
                UPDATE Equipment SET name=%s, type=%s, location=%s, status=%s, VID=%s, purchase_date=%s, warranty_end_date=%s
                WHERE EID=%s
            ''', (name, type, location, status, vid, purchase_date, warranty_end_date, eid))
            mysql.connection.commit()
            return redirect(url_for('manage_equipment'))

        cursor.execute('SELECT * FROM equipment WHERE EID=%s', (eid,))
        equipment = cursor.fetchone()
    return render_template('edit_equipment.html', equipment=equipment)

# View Equipment with Filters
@app.route('/view_equipment', methods=['GET'])
@login_required
def view_equipment():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        

        # Get filter parameters from the URL
        name = request.args.get('name', '').strip()
        type = request.args.get('type', '').strip()
        location = request.args.get('location', '').strip()
        vid = request.args.get('vid', '').strip()
        status = request.args.get('status', '').strip()
        purchase_date = request.args.get('purchase_date', '').strip()
        warranty_end_date = request.args.get('warranty_end_date', '').strip()

        # Base query
        query = "SELECT * FROM equipment WHERE 1=1"
        params = []

        # Add filters if provided
        if name:
            query += " AND name LIKE %s"
            params.append(f"%{name}%")
        if type:
            query += " AND type LIKE %s"
            params.append(f"%{type}%")
        if location:
            query += " AND location LIKE %s"
            params.append(f"%{location}%")
        if vid:
            query += " AND VID = %s"
            params.append(vid)
        if status:
            query += " AND status = %s"
            params.append(status)
        if purchase_date:
            query += " AND purchase_date = %s"
            params.append(purchase_date)
        if warranty_end_date:
            query += " AND warranty_end_date = %s"
            params.append(warranty_end_date)

        cursor.execute(query, tuple(params))
        equipments = cursor.fetchall()

    return render_template('view_equipment.html', equipments=equipments,
                           name=name, type=type, location=location, vid=vid,
                           status=status, purchase_date=purchase_date, warranty_end_date=warranty_end_date)

@app.route('/view_security_incidents', methods=['GET'])
@login_required
def view_security_incidents():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        
        
        # Get filter parameters from the URL
        iid = request.args.get('iid', '').strip()
        eid = request.args.get('eid', '').strip()
        severity = request.args.get('severity', '').strip()
        reporter = request.args.get('reporter', '').strip()
        report_date = request.args.get('report_date', '').strip()
        description = request.args.get('description', '').strip()
        resolve_date = request.args.get('resolve_date', '').strip()

        # Base query
        query = "SELECT * FROM securityincident WHERE 1=1"
        params = []

        # Add filters if provided
        if iid:
            query += " AND IID = %s"
            params.append(iid)
        if eid:
            query += " AND EID = %s"
            params.append(eid)
        if severity:
            query += " AND severity LIKE %s"
            params.append(f"%{severity}%")
        if reporter:
            query += " AND reporter LIKE %s"
            params.append(f"%{reporter}%")
        if report_date:
            query += " AND report_date = %s"
            params.append(report_date)
        if description:
            query += " AND description LIKE %s"
            params.append(f"%{description}%")
        if resolve_date == 'Pending':
            query += " AND resolve_date IS NULL"
        elif resolve_date:
            query += " AND resolve_date = %s"
            params.append(resolve_date)

        # Execute the query with parameters
        cursor.execute(query, tuple(params))
        incidents = cursor.fetchall()
    
    return render_template('view_security_incidents.html', incidents=incidents,
                           iid=iid, eid=eid, severity=severity, reporter=reporter,
                           report_date=report_date, description=description, resolve_date=resolve_date)

@app.route('/maintenance_contracts', methods=['GET', 'POST'])
@login_required
def maintenance_contracts():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        
        # Get filter parameters from request
        cid = request.args.get('cid', '').strip()
        vid = request.args.get('vid', '').strip()
        vendor_name = request.args.get('vendor_name', '').strip()
        eid = request.args.get('eid', '').strip()
        equipment_name = request.args.get('equipment_name', '').strip()
        service_level = request.args.get('service_level', '').strip()
        equipment_type = request.args.get('equipment_type', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()

        query = '''
            SELECT 
                maintenancecontract.CID, 
                maintenancecontract.start_date, 
                maintenancecontract.end_date, 
                maintenancecontract.service_level, 
                maintenancecontract.EID, 
                maintenancecontract.VID,
                equipment.name AS equipment_name, 
                equipment.type AS equipment_type, 
                vendor.name AS vendor_name, 
                vendor.contact_person AS vendor_contact
            FROM 
                maintenancecontract
            JOIN 
                equipment ON maintenancecontract.EID = equipment.EID
            JOIN 
                vendor ON maintenancecontract.VID = vendor.VID
            WHERE 1=1
        '''
        params = []

        # Apply filters if they exist
        if cid:
            query += " AND maintenancecontract.CID = %s"
            params.append(cid)
        if vid:
            query += " AND maintenancecontract.VID = %s"
            params.append(vid)
        if vendor_name:
            query += " AND maintenancecontract.vendor_name = %s"
            params.append(f"%{vendor_name}%")
        if eid:
            query += " AND maintenancecontract.EID = %s"
            params.append(eid)
        if equipment_name:
            query += " AND maintenancecontract.equipment_name = %s"
            params.append(f"%{equipment_name}%")
        if service_level:
            query += " AND maintenancecontract.service_level LIKE %s"
            params.append(f"%{service_level}%")
        if equipment_type:
            query += " AND equipment.type LIKE %s"
            params.append(f"%{equipment_type}%")
        if start_date:
            query += " AND maintenancecontract.start_date = %s"
            params.append(start_date)
        if end_date:
            query += " AND maintenancecontract.end_date = %s"
            params.append(end_date)

        cursor.execute(query, tuple(params))
        maintenance_contracts = cursor.fetchall()

    return render_template('maintenance_contracts.html', maintenance_contracts=maintenance_contracts)

# Add Maintenance Contract
@app.route('/add_maintenance_contract', methods=['GET', 'POST'])
@login_required
def add_maintenance_contract():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        if request.method == 'POST':
            eid = request.form['eid']
            vid = request.form['vid']
            service_level = request.form['service_level']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            
            cursor.execute('''
                INSERT INTO maintenancecontract (EID, VID, service_level, start_date, end_date)
                VALUES (%s, %s, %s, %s, %s)
            ''', (eid, vid, service_level, start_date, end_date))
            mysql.connection.commit()
            return redirect(url_for('maintenance_contracts'))
        
        # Fetch equipment and vendor data for dropdowns in the form
        cursor.execute("SELECT * FROM equipment")
        equipment = cursor.fetchall()

        cursor.execute("SELECT * FROM vendor")
        vendors = cursor.fetchall()

    return render_template('add_maintenance_contract.html')


# Edit Maintenance Contract
@app.route('/edit_maintenance_contract/<int:cid>', methods=['GET', 'POST'])
@login_required
def edit_maintenance_contract(cid):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
        
        
        if request.method == 'POST':
            eid = request.form['eid']
            vid = request.form['vid']
            service_level = request.form['service_level']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
            cursor.execute('''
                UPDATE maintenancecontract SET EID=%s, VID=%s, service_level=%s, start_date=%s, end_date=%s
                WHERE CID=%s
            ''', (eid, vid, service_level, start_date, end_date, cid))
            mysql.connection.commit()
            return redirect(url_for('maintenance_contracts'))

        cursor.execute('SELECT * FROM maintenancecontract WHERE CID=%s', (cid,))
        contract = cursor.fetchone()

        # Fetch equipment and vendor data for dropdowns in the form
        cursor.execute("SELECT * FROM equipment")
        equipment = cursor.fetchall()

        cursor.execute("SELECT * FROM vendor")
        vendors = cursor.fetchall()

    return render_template('edit_maintenance_contract.html', contract=contract, equipment=equipment, vendors=vendors)
@app.route('/delete_maintenance_contract/<int:cid>', methods=['POST'])
@login_required
def delete_maintenance_contract(cid):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
      
        cursor.execute('DELETE FROM maintenancecontract WHERE CID=%s', (cid,))
        mysql.connection.commit()
        return redirect(url_for('maintenance_contracts'))



if __name__ == "__main__":
    app.run(debug=True)