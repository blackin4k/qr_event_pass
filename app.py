from flask import Flask, render_template, request, redirect, url_for, jsonify
import qrcode
import os
import uuid
from datetime import datetime

app = Flask(__name__)

# Ensure QR code storage folder exists
QR_FOLDER = 'static/qrcodes'
os.makedirs(QR_FOLDER, exist_ok=True)

# In-memory database (for simplicity)
qr_data = {}

# Home page - Generate QR code
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        unique_id = str(uuid.uuid4())
        qr_content = f"{unique_id}"

        qr_path = os.path.join(QR_FOLDER, f"{unique_id}.png")
        qr = qrcode.make(qr_content)
        qr.save(qr_path)

        # Store QR data
        qr_data[unique_id] = {
            'scan_count': 0,
            'created_at': datetime.now(),
        }

        return render_template('qr_generated.html', qr_path=qr_path, unique_id=unique_id)

    return render_template('index.html')

# QR Scan Page
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        qr_id = request.form.get('qr_id')

        if qr_id in qr_data:
            qr_data[qr_id]['scan_count'] += 1
            duplicate = qr_data[qr_id]['scan_count'] > 1

            return render_template('scan_result.html', qr_info=qr_data[qr_id], duplicate=duplicate, qr_id=qr_id)

        return "Invalid QR Code", 404

    return render_template('scan.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
