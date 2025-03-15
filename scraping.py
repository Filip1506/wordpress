import os
import re
import requests
from bs4 import BeautifulSoup

def hent_tekningarutskrift(v_tal):
    """
    1) Send GET-forespørgsel til /fo/feloeg/leita-i-skrasetingum med ?name=v_tal
    2) Find i resultatet det 'onclick="skrPopup(...)"', der svarer til Tekningarútskrift
    3) Parse method, id, s
    4) Hent PDF via /api/Skraseting/FelagPdf (eller LysingPdf) og gem i 'Tekningarútskrift'-mappen
    """

    # Opret en session for at håndtere cookies m.m.
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    # 1) Byg søge-URL
    base_url = "https://www.skraseting.fo"
    search_url = f"{base_url}/fo/feloeg/leita-i-skrasetingum"

    # Send GET med parameter "name" = v_tal
    params = {"name": v_tal}
    response = session.get(search_url, params=params)
    response.raise_for_status()

    # 2) Parse HTML med BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find alle elementer, der har et onclick-attribut med skrPopup(...)
    onclick_elements = soup.select("[onclick*=skrPopup]")

    # 3) Uddrag (method, id, s) fra onclick-attributten
    pattern = re.compile(r"skrPopup\((\d+),\s*(\d+),\s*'([^']+)'\)")
    links_fundet = []

    for elem in onclick_elements:
        match = pattern.search(elem.get("onclick", ""))
        if match:
            method_str, pdf_id, s_token = match.groups()
            method_int = int(method_str)
            # Bestem om det er FelagPdf eller LysingPdf
            endpoint = "LysingPdf" if method_int == 0 else "FelagPdf"
            links_fundet.append((endpoint, pdf_id, s_token))

    if not links_fundet:
        print("Ingen skrPopup(...) fundet i HTML'en. Tjek om du har de rigtige parametre.")
        return

    # Vælg den første i stedet for den sidste
    endpoint, pdf_id, s_token = links_fundet[0]
    print(f"Bruger: endpoint={endpoint}, id={pdf_id}, s={s_token}")

    # 4) Hent selve PDF'en
    pdf_url = f"{base_url}/api/Skraseting/{endpoint}?id={pdf_id}&s={s_token}"
    pdf_response = session.get(pdf_url)
    pdf_response.raise_for_status()

    # Opret mappe "Tekningarútskrift" hvis den ikke findes
    folder_name = "Tekningarútskrift"
    os.makedirs(folder_name, exist_ok=True)

    # Vælg et filnavn – fx "{v_tal}_tekningar.pdf"
    pdf_path = os.path.join(folder_name, f"{v_tal}_tekningar.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_response.content)

    print(f"PDF gemt som: {pdf_path}")

if __name__ == "__main__":
    # Eksempel: 2315
    v_tal = input("Indtast v-tal (fx 2315): ")
    hent_tekningarutskrift(v_tal)