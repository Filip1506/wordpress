import mysql.connector
import fitz  # PyMuPDF

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lasteliste",  # Your MySQL password
    database="onboarding"
)

cursor = db.cursor(dictionary=True)

# Fetch the latest customer
cursor.execute("SELECT * FROM customers ORDER BY customer_id DESC LIMIT 1")
customer = cursor.fetchone()

# Check if data is available
if not customer:
    print("No customer data found.")
    exit()

# Load the PDF template
pdf_template = "Swedbank_template.pdf"  # Update with the correct filename
output_pdf = "Filled_Swedbank.pdf"

doc = fitz.open(pdf_template)

# Define PDF field positions (update with actual coordinates)
fields = {
    "Virksomhedsnavn": (65, 147),
    "CVRnr": (420, 147),
    "Postadresse": (65, 166),
    "Postnummer og By": (300, 166),
    "Kontaktperson": (65, 186),
    "TelefonMobil": (335, 186),
    "Email": (420, 186)
}

# Get first page
page = doc[0]

# Insert data at specified coordinates
page.insert_text(fields["Virksomhedsnavn"], customer["business_name"])
page.insert_text(fields["CVRnr"], customer["vat_number"])
page.insert_text(fields["Postadresse"], customer["address"])
page.insert_text(fields["Postnummer og By"], customer["postal_code_city"])
page.insert_text(fields["Kontaktperson"], customer["contact_person"])
page.insert_text(fields["TelefonMobil"], customer["phone_number"])
page.insert_text(fields["Email"], customer["email"])

# Save the new PDF
doc.save(output_pdf)
doc.close()

print(f"✅ PDF '{output_pdf}' successfully created with customer data!")