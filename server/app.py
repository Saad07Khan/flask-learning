
# from flask import Flask, request, jsonify
# from flask_mysqldb import MySQL
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend-backend communication

# # MySQL configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Jeddah_2017'
# app.config['MYSQL_DB'] = 'kineton'

# mysql = MySQL(app)

# @app.route('/')
# def home():
#     return "Welcome to the Kineton API. Use the /submit-form endpoint to submit data."

# @app.route('/submit-form', methods=['POST'])
# def submit_form():
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     message = data.get('message')

#     cursor = mysql.connection.cursor()
#     cursor.execute("INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
#     mysql.connection.commit()
#     cursor.close()

#     return jsonify({'message': 'Form submitted successfully!'})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)  


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Jeddah_2017'
app.config['MYSQL_DB'] = 'kineton'

mysql = MySQL(app)


EMAIL_ADDRESS = 'saadmohammedhan7@gmail.com'  
EMAIL_PASSWORD = 'tfry xsed cpuz hzlu'   

@app.route('/')
def home():
    return "Welcome to the Kineton API. Use the /submit-form endpoint to submit data."

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    mysql.connection.commit()
    cursor.close()

    try:
        send_email(name, email)
    except Exception as e:
        return jsonify({'message': 'Form submitted, but failed to send email.', 'error': str(e)}), 500

    return jsonify({'message': 'Form submitted successfully, and email sent!'})

def send_email(name, user_email):
    subject = "Thank you for contacting Kineton"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0;">
        <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 8px; margin-top: 30px;">
            <tr>
                <td style="padding: 20px; text-align: center; font-size: 24px; font-weight: bold; color: #333333;">
                    Thank You for Contacting Kineton
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; text-align: center; font-size: 16px; color: #555555;">
                    Dear {name},<br><br>
                    Thank you for reaching out to us. We have received your message and will get back to you shortly.<br><br>
                </td>
            </tr>
            <tr>
                <td style="padding: 20px; text-align: center; font-size: 14px; color: #888888;">
                    Best regards,<br>
                    <strong>The Kineton Team</strong>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True)
