# database.py

import random
import smtplib
import time
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import credentials, db

# ---------------- FIREBASE ADMIN SETUP ----------------

cred = credentials.Certificate("secrets.json")  # Ensure your JSON is correctly named
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://reclaimit-3ca24-default-rtdb.firebaseio.com/'
})

OTP_EXPIRY_SECONDS = 300  # 5 minutes
SENDER_EMAIL = "programmingmaster45@gmail.com"
SENDER_PASSWORD = "wuyn kbmc mtej eobw"  # Use app password (not your Gmail password)


# ---------------- OTP UTILS ----------------

def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(recipient_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP for login is: {otp}")
    msg["Subject"] = "Your OTP for Campus App"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("❌ Email send failed:", e)
        return False


def store_otp_in_db(email, otp):
    timestamp = int(time.time())
    db.reference(f"email_otps/{email.replace('.', '_')}").set({
        "otp": otp,
        "timestamp": timestamp
    })

def send_claim_verification_email(recipient_email, answer, email):
    try:
        sender_email = "programmingmaster45@gmail.com"          # Replace with your email
        sender_password = "wuyn kbmc mtej eobw"     # Use an App Password (for Gmail, etc.)

        subject = f"🔔 {email} Claimed the Item You Posted"
        body = f"""
Hello,

{email} is trying to claim the item you posted on the platform.
They responded to the verification question with the description:

------------------------
{answer}
------------------------

If you believe this person is the rightful owner, please contact them through their mail id.

Thank you,
ReclamIt by Aayushya Paswan
"""

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Verification email sent successfully to", recipient_email)
    except Exception as e:
        print("Failed to send email:", e)

def verify_otp(email, entered_otp):
    ref = db.reference(f"email_otps/{email.replace('.', '_')}").get()
    if not ref:
        return False, "No OTP found."

    saved_otp = ref.get("otp")
    saved_time = ref.get("timestamp")
    current_time = int(time.time())

    if current_time - saved_time > OTP_EXPIRY_SECONDS:
        return False, "OTP expired."

    if str(entered_otp) == str(saved_otp):
        return True, "OTP verified."
    else:
        return False, "Incorrect OTP."


# ---------------- USER MANAGEMENT ----------------

def register_user(email, username, password):
    try:
        uid = email.replace('.', '_')
        db.reference(f"users/{uid}").set({
            "email": email,
            "username": username,
            "password": password
        })
        return {"status": "success", "uid": uid}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def is_user_registered(email):
    uid = email.replace('.', '_')
    return db.reference(f"users/{uid}").get() is not None


def get_user_password(email):
    uid = email.replace('.', '_')
    user = db.reference(f"users/{uid}").get()
    if user:
        return user.get("password")
    return None


# ---------------- LOST ITEMS ----------------

def add_lost_item(image_url, description, email):
    item = {
        "image": image_url,
        "description": description,
        "status": "not returned",
        "posted_by": email
    }
    db.reference("items_lost").push(item)


def update_lost_item_status(item_id, new_status):
    db.reference(f"items_lost/{item_id}").update({"status": new_status})


# ---------------- FOUND ITEMS ----------------

def add_found_item(image_url, description, email):
    item = {
        "image": image_url,
        "description": description,
        "status": "found",
        "posted_by": email
    }
    db.reference("items_found").push(item)


def update_found_item_status(item_id, new_status):
    db.reference(f"items_found/{item_id}").update({"status": new_status})


# ---------------- ANONYMOUS ISSUES ----------------

def report_anonymous_issue(issue_text):
    db.reference("anonymous_issues").push({"issue": issue_text})


# ---------------- GETTERS ----------------

def get_all_lost_items():
    return db.reference("items_lost").get()


def get_all_found_items():
    return db.reference("items_found").get()


def get_all_anonymous_issues():
    return db.reference("anonymous_issues").get()

def get_email(username):
    user = db.reference("users").get()
    return user[username]['email']

user = db.reference("users").get()
print(user)
