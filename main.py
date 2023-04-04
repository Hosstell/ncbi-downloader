import requests
import xml.etree.ElementTree as ET

TERM = "potato virus Y"

PATH = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "nucleotide",
    "term": TERM,
    "RetMax": 1000,
    "RetStart": 0
}

all_ids = []

while True:
    response = requests.get(PATH, params=params)
    data = ET.fromstring(response.text)
    ids = [id_.text for id_ in data[3]]
    if len(ids) == 0:
        break

    all_ids.extend(ids)
    params["RetStart"] += params["RetMax"]


def download_fasta(id_):
    path = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nucleotide",
        "id": id_,
        "rettype": "fasta",
        "retmode": "text"
    }
    response = requests.get(path, params=params)
    return response.text


count = 0
all_fasta = ""
for id_ in all_ids:
    count += 1

    try:
        fasta = download_fasta(id_)
    except:
        print(f"Произошла ошибка при скачивание fasta (id={id_})")
        continue

    if len(fasta) < 7880:
        print(count, len(ids), "-")
        continue

    print(count, len(all_ids))
    all_fasta += fasta


file = open(f"output/{TERM}.fasta", "w")
file.write(all_fasta)
file.close()
