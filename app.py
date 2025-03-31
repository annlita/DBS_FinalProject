from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config.from_object(config.Config)
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')  # Render the first page from index.html

# Manage Equipment - List all equipment with filters
@app.route('/manage_equipment', methods=['GET', 'POST'])
def manage_equipment():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get filter parameters from the URL
    name = request.args.get('name', '').strip()
    type = request.args.get('type', '').strip()
    location = request.args.get('location', '').strip()
    vid = request.args.get('vid', '').strip()
    status = request.args.get('status', '').strip()
    purchase_date = request.args.get('purchase_date', '').strip()
    warranty_end_date = request.args.get('warranty_end_date', '').strip()

    # Base query
    query = "SELECT * FROM Equipment WHERE 1=1"
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
        cursor.execute('DELETE FROM Equipment WHERE EID=%s', (eid,))
        mysql.connection.commit()
        return redirect(url_for('manage_equipment'))

    return render_template('manage_equipment.html', equipment=equipment_data,
                           name=name, type=type, location=location, vid=vid,
                           status=status, purchase_date=purchase_date, warranty_end_date=warranty_end_date)

# Add Equipment
@app.route('/add_equipment', methods=['GET', 'POST'])
def add_equipment():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        location = request.form['location']
        status = request.form['status']
        vid = request.form['vid']
        purchase_date = request.form['purchase_date']
        warranty_end_date = request.form['warranty_end_date']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            INSERT INTO Equipment (name, type, location, status, VID, purchase_date, warranty_end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (name, type, location, status, vid, purchase_date, warranty_end_date))
        mysql.connection.commit()
        return redirect(url_for('manage_equipment'))
    
    return render_template('add_equipment.html')

# Edit Equipment
@app.route('/edit_equipment/<int:eid>', methods=['GET', 'POST'])
def edit_equipment(eid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
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

    cursor.execute('SELECT * FROM Equipment WHERE EID=%s', (eid,))
    equipment = cursor.fetchone()
    return render_template('edit_equipment.html', equipment=equipment)

# View Equipment with Filters
@app.route('/view_equipment', methods=['GET'])
def view_equipment():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Get filter parameters from the URL
    name = request.args.get('name', '').strip()
    type = request.args.get('type', '').strip()
    location = request.args.get('location', '').strip()
    vid = request.args.get('vid', '').strip()
    status = request.args.get('status', '').strip()
    purchase_date = request.args.get('purchase_date', '').strip()
    warranty_end_date = request.args.get('warranty_end_date', '').strip()

    # Base query
    query = "SELECT * FROM Equipment WHERE 1=1"
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
def view_security_incidents():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Get filter parameters from the URL
    iid = request.args.get('iid', '').strip()
    eid = request.args.get('eid', '').strip()
    severity = request.args.get('severity', '').strip()
    reporter = request.args.get('reporter', '').strip()
    report_date = request.args.get('report_date', '').strip()
    description = request.args.get('description', '').strip()
    resolve_date = request.args.get('resolve_date', '').strip()

    # Base query
    query = "SELECT * FROM SecurityIncident WHERE 1=1"
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

if __name__ == "__main__":
    app.run(debug=True)
