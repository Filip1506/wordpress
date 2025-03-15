from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
from ftplib import FTP
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)

# MySQL-forbindelsesoplysninger
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

FTP_HOST = os.getenv("FTP_HOST")
FTP_USERNAME = os.getenv("FTP_USERNAME")
FTP_PASSWORD = os.getenv("FTP_PASSWORD")
FTP_UPLOAD_FOLDER = os.getenv("FTP_UPLOAD_FOLDER")
PDF_TEMPLATE_PATH = os.getenv("PDF_TEMPLATE_PATH")

def download_pdf_from_ftp():
    """Henter PDF-skabelonen fra Simply.com via FTP"""
    local_path = "POS8.pdf"  # Gem PDF'en lokalt

    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(PDF_TEMPLATE_PATH)  # Skift til den korrekte mappe

        with open(local_path, "wb") as file:
            ftp.retrbinary(f"RETR POS8.pdf", file.write)  # Hent filen

        ftp.quit()
        print(f"✔️ PDF-skabelon hentet fra FTP: {local_path}")
        return local_path

    except Exception as e:
        print(f"❌ Fejl ved hentning af PDF: {e}")
        return None

@app.route("/onboard", methods=["POST"])
def onboard():
    data = request.get_json()

    required_fields = ["business_name", "vat_number", "address", "postal_code_city", "contact_person", "phone_number", "email"]
    missing = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    customer_data = {field: data[field].strip() for field in required_fields}

    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        insert_query = """
        INSERT INTO customers (business_name, vat_number, address, postal_code_city, contact_person, phone_number, email)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, tuple(customer_data[field] for field in required_fields))
        db.commit()
        customer_id = cursor.lastrowid
        cursor.close()
        db.close()
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    # Hent PDF-skabelon
    template_path = download_pdf_from_ftp()
    if not template_path:
        return jsonify({"error": "Failed to retrieve PDF template"}), 500

    # Generer den udfyldte PDF
    try:
        output_pdf_path = f"customer_{customer_id}.pdf"
        doc = fitz.open(template_path)
        page = doc[0]

        pdf_fields = {
            "business_name": (65, 147),
            "vat_number": (420, 147),
            "address": (65, 166),
            "postal_code_city": (300, 166),
            "contact_person": (65, 186),
            "phone_number": (335, 186),
            "email": (420, 186)
        }

        for key, coord in pdf_fields.items():
            page.insert_text(coord, customer_data[key])

        doc.save(output_pdf_path)
        doc.close()
        print(f"✔️ PDF genereret: {output_pdf_path}")

        # Upload til FTP
        remote_pdf_path = upload_to_ftp(output_pdf_path, f"customer_{customer_id}.pdf")
        if not remote_pdf_path:
            return jsonify({"error": "Failed to upload PDF to Simply"}), 500

    except Exception as e:
        return jsonify({"error": f"PDF generation error: {str(e)}"}), 500

    return jsonify({
        "message": f"Customer {customer_data['business_name']} added successfully!",
        "pdf_path": remote_pdf_path
    }), 200

from flask import Flask, request, jsonify

@app.route("/questions", methods=["GET"])
def get_questions():
    try:
        questions_data = [
            {"key": "business_name", "text": "What is your business name?"},
            {"key": "vat_number", "text": "Enter your VAT number (V-tal)"},
            {"key": "address", "text": "Enter your business address"},
            {"key": "postal_code_city", "text": "Enter your postal code and city"},
            {"key": "contact_person", "text": "Who is the contact person?"},
            {"key": "phone_number", "text": "Enter phone number"},
            {"key": "email", "text": "Enter email address"}
        ]
        return jsonify(questions_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def upload_to_ftp(local_filepath, remote_filename):
    """Uploader PDF til Simply.com via FTP"""
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USERNAME, FTP_PASSWORD)
        ftp.cwd(FTP_UPLOAD_FOLDER)

        with open(local_filepath, "rb") as file:
            ftp.storbinary(f"STOR {remote_filename}", file)

        ftp.quit()
        print(f"✔️ PDF uploadet til: {FTP_UPLOAD_FOLDER}/{remote_filename}")
        return f"{FTP_UPLOAD_FOLDER}/{remote_filename}"

    except Exception as e:
        print(f"❌ Fejl ved FTP-upload: {e}")
        return None

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)