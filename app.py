from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
import smtplib
from email.message import EmailMessage
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'rajesh-portfolio-secret-key')

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
TO_EMAIL = os.getenv('TO_EMAIL', EMAIL_ADDRESS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:subpath>')
def catch_all(subpath):
    return redirect(url_for('index'))

@app.route('/send-message', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not all([name, email, message]):
        return jsonify({'success': False, 'message': 'Please fill in all required fields'}), 400

    try:
        msg = EmailMessage()
        msg['Subject'] = f"Portfolio Contact: {subject}" if subject else "New Contact from Portfolio"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = TO_EMAIL
        msg.set_content(
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Subject: {subject}\n\n"
            f"Message:\n{message}"
        )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'success': True, 'message': 'Your message has been sent successfully!'})
    except Exception as e:
        app.logger.error(f"Error sending email: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to send message. Please try again later.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
