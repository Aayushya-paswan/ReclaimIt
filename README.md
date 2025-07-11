# ReclaimIt 

**ReclaimIt** is a centralized mobile application built using **Kivy** (Python) designed for college campuses to streamline **Lost & Found** tracking and **Anonymous Issue Reporting**.



**APP demo Video** :- https://drive.google.com/file/d/1K-P7L0CS6Psnqysofm_9NG-bc4fBe6Go/view?usp=sharing
---

## 🧩 Features

-  **User Authentication**
  - Secure login & signup with Firebase backend
  - OTP-based verification for email

- **Lost & Found Tracker**
  - Post lost/found items with images
  - Browse lists with filtering by category or date
  - Image, description and status saved in firebase

- 🛠**Anonymous Issue Reporting**
  - Raise concerns (hostel, academic, campus facilities)
  - Admin view for tracking and resolving complaints

- **Media Uploads**
  - Upload pictures for better identification of objects which are being tracked
  - Firebase Storage integration to store users and data of lost/found items
  - 


- **Smart UI/UX**
  - Animated Kivy interface with card-style screens
  - Optimized for mobile screen sizes

---

🛠️ Tech Stack
Frontend: Kivy (Python)

Backend: Firebase (Authentication + Realtime DB + Storage)

Tools: Buildozer (APK packaging), Git, PyCharm


---

## Getting Started (Development)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aayushya-paswan/ReclaimIt.git
   cd ReclaimIt
2. python -m venv venv
venv\Scripts\activate  # Windows

3. pip install -r requirements.txt

5. Setup Firebase
->Place your firebase_config.json in the root directory.

->File should contain your Firebase project credentials.

---

📱 Building for Android
Make sure you have:

Ubuntu/Linux system (or WSL)

Buildozer and dependencies installed

Then run:

bash
Copy
Edit
buildozer init
buildozer -v android debug
---
🙌 Acknowledgments
Built for the IIITDM Hackathon 2025, focused on impactful campus-centric mobile solutions.

---
🧑‍💻 Author
Aayushya Paswan

