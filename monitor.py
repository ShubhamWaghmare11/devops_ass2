import time
import smtplib
from email.message import EmailMessage
import os
# ---------------- CONFIGURATION ----------------
LOG_FILE = "predictions.log"         # File where FastAPI logs predictions/errors
ERROR_THRESHOLD = 1                  # Number of errors to trigger alert
CHECK_INTERVAL = 10                  # Seconds between log checks

EMAIL_FROM = "gamermask64@gmail.com"  # Sender email
EMAIL_TO = "gamermask64@gmail.com"    # Receiver email (self)
EMAIL_SUBJECT = "FastAPI Prediction Error Alert"
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Gmail App Password (required if 2FA enabled)
# ------------------------------------------------

def send_email_alert(error_lines):
    """Send an email alert with error details."""
    msg = EmailMessage()
    msg.set_content(f"Alert! Errors detected in FastAPI predictions:\n\n{error_lines}")
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_log():
    """Continuously monitor the log file for errors."""
    last_size = 0  # Keep track of last read line
    while True:
        try:
            with open(LOG_FILE, "r") as f:
                lines = f.readlines()
            new_lines = lines[last_size:]
            last_size = len(lines)

            # Check for errors
            error_lines = [line for line in new_lines if "ERROR" in line]
            if len(error_lines) >= ERROR_THRESHOLD:
                send_email_alert("\n".join(error_lines))

        except FileNotFoundError:
            print(f"{LOG_FILE} not found. Waiting for file to be created...")
        except Exception as e:
            print(f"Monitoring error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("Starting log monitoring...")
    monitor_log()
