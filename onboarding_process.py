from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS
#import fitz  # PyMuPDF  (Kun hvis du vil generere PDF)
import os


app = Flask(__name__)
CORS(app)

# MySQL-forbindelsesoplysninger – juster efter behov
db_config = {
    "host": "mysql30.unoeuro.com",  # Opdater med din Simply MySQL host
    "user": "itco_dk",  # Dit MySQL-brugernavn fra Simply
    "password": "BbawpD64fGFcdAEgrzRt",  # Dit MySQL-password
    "database": "itco_dk_db_test"  # Navn på databasen i Simply
}

# ----------------------------------------------------
# 1) GET /questions – returnerer en liste af spørgsmål
# ----------------------------------------------------
@app.route("/questions", methods=["GET"])
def get_questions():
    # Du kan definere spørgsmålene direkte her ...
    questions_data = [
        {"key": "business_name", "text": "What is your business name?"},
        {"key": "vat_number", "text": "Enter your VAT number (V-tal)"},
        {"key": "address", "text": "Enter your business address"},
        {"key": "postal_code_city", "text": "Enter your postal code and city"},
        {"key": "contact_person", "text": "Who is the contact person?"},
        {"key": "phone_number", "text": "Enter phone number"},
        {"key": "email", "text": "Enter email address"}
    ]

    # ... eller hente dem fra en database, fil, etc.
    return jsonify(questions_data), 200


# ----------------------------------------------------
# 2) POST /onboard – modtager data og gemmer i MySQL
# ----------------------------------------------------
@app.route("/onboard", methods=["POST"])
def onboard():
    data = request.get_json()

    # Forventede felter
    required_fields = [
        "business_name", 
        "vat_number", 
        "address", 
        "postal_code_city", 
        "contact_person", 
        "phone_number", 
        "email"
    ]

    # Tjek for manglende felter
    missing = [field for field in required_fields if field not in data or not data[field].strip()]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Rens og gem data i et dict
    customer_data = {field: data[field].strip() for field in required_fields}

    # Forbind til MySQL
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
    except Exception as e:
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500

    # Indsæt data i "customers"-tabellen
    insert_query = """
    INSERT INTO customers (business_name, vat_number, address, postal_code_city, contact_person, phone_number, email)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(insert_query, tuple(customer_data[field] for field in required_fields))
        db.commit()
        customer_id = cursor.lastrowid  # Få det auto-genererede ID
    except Exception as e:
        db.rollback()
        cursor.close()
        db.close()
        return jsonify({"error": f"Database insertion error: {str(e)}"}), 500

    # ----------------------------------------------------
    # PDF-kode (valgfri): Generer PDF, hvis ønsket
    # ----------------------------------------------------
    """
    try:
        pdf_folder = "New Customers"
        if not os.path.exists(pdf_folder):
            os.makedirs(pdf_folder)

        pdf_template = "Swedbank_template.pdf"  # Sørg for, at filen findes
        output_pdf = os.path.join(pdf_folder, f"Customer_{customer_id}.pdf")

        doc = fitz.open(pdf_template)
        pdf_fields = {
            "Virksomhedsnavn": (65, 147),
            "CVRnr": (420, 147),
            "Postadresse": (65, 166),
            "Postnummer og By": (300, 166),
            "Kontaktperson": (65, 186),
            "TelefonMobil": (335, 186),
            "Email": (420, 186)
        }
        page = doc[0]

        page.insert_text(pdf_fields["Virksomhedsnavn"], customer_data["business_name"])
        page.insert_text(pdf_fields["CVRnr"], customer_data["vat_number"])
        page.insert_text(pdf_fields["Postadresse"], customer_data["address"])
        page.insert_text(pdf_fields["Postnummer og By"], customer_data["postal_code_city"])
        page.insert_text(pdf_fields["Kontaktperson"], customer_data["contact_person"])
        page.insert_text(pdf_fields["TelefonMobil"], customer_data["phone_number"])
        page.insert_text(pdf_fields["Email"], customer_data["email"])

        doc.save(output_pdf)
        doc.close()

    except Exception as e:
        cursor.close()
        db.close()
        return jsonify({"error": f"Error generating PDF: {str(e)}"}), 500
    """

    # Luk databaseforbindelsen
    cursor.close()
    db.close()

    # Returner succesbesked (her uden PDF-information)
    return jsonify({
        "message": f"Customer {customer_data['business_name']} added successfully (ID: {customer_id})!"
        # ,"pdf": output_pdf  # Hvis du vil returnere stien til PDF'en
    }), 200


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))  # Brug 5001 i stedet for 5000
    app.run(host="0.0.0.0", port=port)