from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import pymysql
import time

# Required for MySQL connection with pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

# MySQL database configuration for Docker
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'mysql+pymysql://root:password@db:3306/mydb'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Entry {self.name}>'

# Function to initialize database with retries
def init_db():
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.create_all()
            print("Database tables created successfully!")
            return True
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Failed to connect to database after multiple attempts")
                return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        if name and address:
            try:
                new_entry = Entry(name=name, address=address)
                db.session.add(new_entry)
                db.session.commit()
            except Exception as e:
                print(f"Error adding entry: {e}")
        return redirect('/')
    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view():
    try:
        entries = Entry.query.order_by(Entry.id).all()
        return render_template('records.html', entries=entries)
    except Exception as e:
        print(f"Error retrieving entries: {e}")
        return render_template('records.html', entries=[])

@app.route('/health', methods=['GET'])
def health():
    try:
        # Simple database check
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}, 500

if __name__ == "__main__":
    # Initialize database when starting
    if init_db():
        app.run(host="0.0.0.0", port=5000, debug=True)
    else:
        print("Failed to initialize database. Exiting.")
