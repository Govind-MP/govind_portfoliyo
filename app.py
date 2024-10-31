from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

# Configure Flask-Mail for Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_ID')  # Your Gmail address
app.config['MAIL_PASSWORD'] = os.getenv('APP_PASS')   # Your app password (make sure there are no spaces)
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    if name and email and message:
        try:
            print("Attempting to send email...") 
            msg = Message(
                subject="New Message from Your Portfolio",
                sender=app.config['MAIL_USERNAME'],
                recipients=["govindmpatwork@gmail.com"]  # Email to receive messages
            )
            msg.body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            mail.send(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash("An error occurred while sending the message.", "error")
            print(f"Error: {e}")  # Log error details for troubleshooting
    else:
        flash("Please fill out all fields.", "error")

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.secret_key = '112233445566778899'  # Replace with a string for a secret key
    app.run(debug=True)
