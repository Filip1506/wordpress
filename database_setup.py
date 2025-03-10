import psycopg2

# Forbind til PostgreSQL (Opdater med dine egne database-oplysninger)
conn = psycopg2.connect(
    dbname="din_database",  
    user="din_bruger",
    password="dit_password",
    host="localhost"
)
cur = conn.cursor()

# SQL: Opret tabel
cur.execute("""
CREATE TABLE IF NOT EXISTS kunde_data (
    id SERIAL PRIMARY KEY,

    -- Kunde (Sektion 1)
    virksomhedsnavn VARCHAR(255),
    cvr_nr VARCHAR(50),
    postadresse VARCHAR(255),
    postnummer VARCHAR(20),
    kontaktperson VARCHAR(255),
    area_code VARCHAR(10),
    telefon VARCHAR(50),
    email VARCHAR(255),

    -- Salgssted (Sektion 2)
    juridisk_adresse_sammesom_salgssted BOOLEAN,
    salgssted_navn VARCHAR(255),
    salgssted_telefon VARCHAR(50),
    salgssted_adresse VARCHAR(255),
    salgssted_postnummer VARCHAR(20),
    salgssted_kontakt VARCHAR(255),
    salgssted_email VARCHAR(255),
    saesonbutik VARCHAR(50),
    kaede VARCHAR(50),

    -- Virksomhed/Branche (Sektion 3)
    beskrivelse_ydelse VARCHAR(255),
    forventet_omsætning INT,
    forventet_gennemsnitskøb INT,
    bestillingsvarer BOOLEAN,
    bestillingsvarer_andel INT,
    depositum BOOLEAN,
    depositum_andel INT,
    tid_restbetaling VARCHAR(50),
    hvordan_restbetaling VARCHAR(50),

    -- Fysiske Personer (Sektion 4)
    ejer1_navn VARCHAR(255),
    ejer1_cpr VARCHAR(50),
    ejer1_skattepligt VARCHAR(50),
    ejer1_nationalitet VARCHAR(50),
    ejer1_andele DECIMAL(5,2),
    ejer1_pep BOOLEAN,

    ejer2_navn VARCHAR(255),
    ejer2_cpr VARCHAR(50),
    ejer2_skattepligt VARCHAR(50),
    ejer2_nationalitet VARCHAR(50),
    ejer2_andele DECIMAL(5,2),
    ejer2_pep BOOLEAN,

    ejer3_navn VARCHAR(255),
    ejer3_cpr VARCHAR(50),
    ejer3_skattepligt VARCHAR(50),
    ejer3_nationalitet VARCHAR(50),
    ejer3_andele DECIMAL(5,2),
    ejer3_pep BOOLEAN,

    ejer4_navn VARCHAR(255),
    ejer4_cpr VARCHAR(50),
    ejer4_skattepligt VARCHAR(50),
    ejer4_nationalitet VARCHAR(50),
    ejer4_andele DECIMAL(5,2),
    ejer4_pep BOOLEAN,

    -- Pengeinstitut (Sektion 6)
    pengeinstitut VARCHAR(255),
    reg_nr VARCHAR(50),
    konto_nr VARCHAR(50)
);
""")

conn.commit()
cur.close()
conn.close()
print("✅ Database-tabellen 'kunde_data' er oprettet!")