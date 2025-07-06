import random
import time
import smtplib
from email.message import EmailMessage
from firebase_admin import credentials, db

OTP_EXPIRY_SECONDS = 300  # 5 minutes
SENDER_EMAIL = "programmingmaster45@gmail.com"
SENDER_PASSWORD = "wuyn kbmc mtej eobw"

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(recipient_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your OTP for registration is: {otp}")
    msg["Subject"] = "Email Verification - Campus Utility App"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("Email send failed:", e)
        return False

def store_otp_in_db(email, otp):
    timestamp = int(time.time())
    db.reference(f"email_otps/{email.replace('.', '_')}").set({
        "otp": otp,
        "timestamp": timestamp
    })

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

def register_user(email, username, password):
    try:
        db.reference(f"users/{username}").set({
            "email": email,
            "username": username,
            "password": password
        })
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def is_user_registered(username):
    return db.reference(f"users/{username}").get() is not None

def get_user_password(username):
    ref = db.reference(f"users/{username}").get()
    if ref and "password" in ref:
        return ref["password"]
    return None

def is_email_registered(email):
    uid = email.replace('.', '_')
    user_ref = db.reference(f"users/{uid}").get()
    return user_ref is not None