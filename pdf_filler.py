import fitz  # PyMuPDF

def add_text_to_pdf(input_pdf, output_pdf, pages):
    doc = fitz.open(input_pdf)

    # Definer tekstegenskaber
    text_color = (0, 0, 0)  # Sort
    font_size = 10

    # Loop gennem hver side
    for page_num, sections in pages.items():
        page = doc[page_num]  # Hent den korrekte side
        print(f"Adding data for page {page_num + 1}")

        for section_name, fields in sections.items():  # Loop gennem sektioner
            print(f" - Section: {section_name}")
            for text, (x, y) in fields.items():  # Loop gennem felter i en sektion
                page.insert_text((x, y), text, fontsize=font_size, color=text_color)

    # Gem opdateret PDF
    doc.save(output_pdf)
    doc.close()
    print(f"Text added and saved to {output_pdf}")

input_pdf = "Swedbank_template.pdf"
output_pdf = "Swedbank_filled.pdf"

# Organized sections with correct structure
pages = {
    0: { #Side 1
        "Kunde": { #Sektion 1
            "Itco":                     (65, 147),  # Virksomhedens juridiske navn
            "12345678":                 (420, 147), # CVRnr
            "Test Street 1":            (65, 166),  # Postadresse
            "9000 Aalborg":             (300, 166), # Postnummer og By
            "Kenneth Skoubo Bærendsen": (65, 186),  # Kontaktperson
            "":                         (310, 186), # Area code
            "12345678 ":                (335, 186), # TelefonMobil 45
            "ksb@hotmail.com":          (420, 186)  # Email 
        },
        "Salgssted": {  #Sektion 2
            "":                         (55, 231),  # Sæt kryds her hvis den juridiske adresse er den samme som salgsstedets
            "Store Name":               (65, 250),  # Salgsstedets navn
            "12345678":                 (300, 250), # Salgsstedets telefon
            "9000 Aalborg":             (300, 269), # Salgsstedets adresse
            "Store Address 1":          (65, 269),  # Postnummer og By_2
            "Store Contact Person":     (65, 288),  # Kontaktperson på salgsstedet
            "Email Contact Person":     (300, 288), # Email kontaktperson
            "Sæsonbutik":               (65, 308),  # Hvis sæsonbutik anfør periode måneder
            "Kæde":                     (300, 308)  # Hvis indgår i kæde angiv hvilken
        },
        "Virksomhed/Branche": {  #Sektion 3
            "Vare/service eller ydelse":(65, 365),  # Beskrivelse af vare eller service ydelse feks børnetøj
            "Kortomsætning":            (65, 385),  # Forventet omsætning VISAMC pr år 
            "1000000000":               (300, 385), # Forventet gennemsnitskøb
            "":                         (61, 406),  # Ja Bestillingsvarer
            "":                         (109, 406), # Nej Bestillingsvarer
            "Hvis ja":                  (154, 406), # Andel bestillingsvarer
            "":                         (61, 425),  # Ja Depositum
            "":                         (109, 425), # Nej Depositum
            "Hvis ja, hvor stor":       (215, 425), # Andel depositum
            "Hvornår finder ?":         (310, 425), # Tid for restbetaling
            "Hvordan":                  (420, 425)  # Hvordan betales rest?
        },
        "Fysiske Personer, som direkte eller indirekte ejer 25 procent eller mere": {  #Sektion 4
            "":                         (55, 500),  # Sæt kryds her hvis der ikke findes nogen fysisk person der direkte eller indirekte ejer eller kontrollerer mere end 25  af virksomheden 
            "Navn1":                    (65, 534),  # NavnRow1
            "CPR1":                     (200, 534), # CPR nrRow1
            "Skat1":                    (265, 534), # Skattepligtig i landRow1
            "Nat1":                     (348, 534), # Nationalitet 1
            "Andel1":                   (433, 534), # Ejerandel i Row1
            "":                         (493, 534), # Ja
            "":                         (514, 534), # Nej

            "Navn2":                    (65, 554),  # NavnRow2  
            "CPR2":                     (200, 554), # CPR nrRow2
            "Skat2":                    (265, 554), # Skattepligtig i landRow2
            "Nat2":                     (348, 554), # Nationalitet 2
            "Andel2":                   (433, 554), # Ejerandel i Row2
            "":                         (493, 554), # Ja_2
            "":                         (514, 554), # Nej_2

            "Navn3":                    (65, 574),  # NavnRow3
            "CPR3":                     (200, 574), # CPR nrRow3
            "Skat3":                    (265, 574), # Skattepligtig i landRow3
            "Nat3":                     (348, 574), # Nationalitet 3
            "Andel3":                   (433, 574), # Ejerandel i Row3
            "":                         (493, 574), # Ja_3
            "":                         (514, 574), # Nej_3

            "Navn4":                    (65, 594),  # NavnRow4
            "CPR4":                     (200, 594), # CPR nrRow4
            "Skat4":                    (265, 594), # Skattepligtig i landRow4
            "Nat4":                     (348, 594), # Nationalitet 4
            "Andel4":                   (433, 594), # Ejerandel i Row4
            "":                         (493, 594), # Ja_4
            "":                         (514, 594), # Nej_4
        },
        "Information om terminalløsning": {  #Sektion 5 
        },
        "Pengeinstitut til udbetaling": {  #Sektion 6
            "Institut":                 (65, 755),  # Pengeinstituttets navn
            "reg. nr.":                 (300, 755), # Reg nr
            "Kntnr.":                   (365, 755)  # Kontonummer
        },
    },
    1: { #Side 2
        "Merchant Portal": {  #Sektion 7
            "Merchant Portal":          (65, 141), #
            "Personnummer":             (305, 141), #
            "Emailadr":                 (65, 161) #
        },
        "Underskrifter": {  #Sektion 8
            "Dato":                     (79, 567), #

            "Navn1":                    (65, 633), #
            "CPR1":                     (65, 653), #
            "Skattepligtig1":           (65, 673), #

            "Navn2":                    (190, 633), #
            "CPR2":                     (190, 653), #
            "Skattepligtig2":           (190, 673), #

            "Navn3":                    (309, 633), #
            "CPR3":                     (309, 653), #
            "Skattepligtig3":           (309, 673), #
        },
    },
    2: { #Side 3
        "Virksomhedsoplysninger": {  #Sektion 9
            
           
        },
        "Ejere": {  #Sektion 10
            
        },
        "Knt til afregning af kortomsætning": {  #Sektion 10
            
        },
        "Underskrift": {  #Sektion 10
            
        },
    },
}

add_text_to_pdf(input_pdf, output_pdf, pages)