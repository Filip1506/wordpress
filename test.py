from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# MySQL-forbindelsesoplysninger – juster efter behov
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Lasteliste",  # Opdater med dit MySQL-password
    "database": "onboarding"
}

@app.route("/onboard", methods=["POST"])
def onboard():
    # Hent kundeoplysninger fra JSON-body
    data = request.get_json()
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

    customer_data = {field: data[field].strip() for field in required_fields}

    # Forbind til MySQL
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
    except Exception as e:
        return jsonify({"error": f"Database connection error: {str(e)}"}), 500

    # Indsæt data i tabellen "customers"
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

    # Luk databaseforbindelsen
    cursor.close()
    db.close()

    # Returner succesbesked (uden PDF-info)
    return jsonify({
        "message": f"Customer {customer_data['business_name']} added successfully (ID: {customer_id})!"
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)