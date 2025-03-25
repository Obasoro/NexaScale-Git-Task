import os
import smtplib
import logging
import datetime
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from celery_config import celery  # Import from config, not celery_app

# Initialize Flask app
message_app = Flask(__name__)

# Configuration
message_app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='rpc://'
)

# Configure logging
logging.basicConfig(
    filename='/var/log/messaging_system.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Celery with app config
celery.conf.update(message_app.config)

# Routes
@message_app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        from tasks import send_email  # Import task when needed
        send_email.delay(sendmail)
        logging.info(f"Email task queued for {sendmail}")
        return jsonify({"message": "Email queued for sending"}), 200

    if talktome:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info(f"Talktome request received at {current_time}")
        return jsonify({"message": "Time logged successfully"}), 200

    return jsonify({"message": "No valid parameters provided"}), 400

@message_app.route('/logs')
def view_logs():
    try:
        with open('/var/log/messaging_system.log', 'r') as log_file:
            logs = log_file.read()
        return jsonify({"logs": logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    message_app.run(host='0.0.0.0', port=5000)