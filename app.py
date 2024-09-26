from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database URI (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model for submissions
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(100), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Route to serve the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def handle_submission():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a new Submission object
    new_submission = Submission(name=name, email=email, message=message, time=submission_time)
    
    # Add to the database and commit
    db.session.add(new_submission)
    db.session.commit()

    return render_template('submitted.html', submission=new_submission)

# Route to display stored submissions
@app.route('/submissions')
def display_submissions():
    # Query all submissions from the database
    submissions = Submission.query.all()
    return render_template('submissions.html', submissions=submissions)

# Dynamic content route
@app.route('/dynamic')
def dynamic_content():
    quotes = [
        "The best way to predict the future is to create it.",
        "Success is not the key to happiness. Happiness is the key to success.",
        "Do not watch the clock; do what it does. Keep going.",
        "The only limit to our realization of tomorrow is our doubts of today.",
        "In the middle of difficulty lies opportunity.",
        "What lies behind us and what lies before us are tiny matters compared to what lies within us.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "You miss 100% of the shots you don’t take.",
        "Life is what happens when you're busy making other plans.",
        "Success usually comes to those who are too busy to be looking for it."
    ]
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_quote = quotes[datetime.now().second % len(quotes)]
    return render_template('dynamic.html', time=current_time, quote=random_quote)

if __name__ == '__main__':
    app.run(debug=True)
