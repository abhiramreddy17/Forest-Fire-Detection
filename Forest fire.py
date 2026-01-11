import cv2
import numpy as np
import smtplib
from email.message import EmailMessage
import time

# ---------------- EMAIL FUNCTION ----------------
def send_email_alert():
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@gmail.com"
    password = "your_app_password"

    msg = EmailMessage()
    msg.set_content("🔥 ALERT! Forest Fire Detected by Camera.")
    msg["Subject"] = "Forest Fire Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("📧 Email Alert Sent!")
    except Exception as e:
        print("Email Error:", e)

# ---------------- CAMERA START ----------------
cap = cv2.VideoCapture(0)

email_sent = False
last_email_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Fire color range (HSV)
    lower_fire = np.array([18, 50, 50])
    upper_fire = np.array([35, 255, 255])

    mask = cv2.inRange(hsv, lower_fire, upper_fire)
    fire_pixels = cv2.countNonZero(mask)

    # Threshold (adjustable)
    if fire_pixels > 3000:
        cv2.putText(frame, "🔥 FIRE DETECTED", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Send email only once every 60 seconds
        if not email_sent or time.time() - last_email_time > 60:
            send_email_alert()
            email_sent = True
            last_email_time = time.time()
    else:
        email_sent = False

    cv2.imshow("Forest Fire Detection", frame)
    cv2.imshow("Fire Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
