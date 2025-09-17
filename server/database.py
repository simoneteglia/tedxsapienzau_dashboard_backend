import pymongo
import os
from dotenv import load_dotenv
import csv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client["tedxsapienzau_gestione_personale"]


def loadVolunteers():
    print("Loading data into the MongoDB database...")

    volunteers_coll = db["volunteers"]

    with open("./volontarinew.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for index, volunteer in enumerate(csv_reader):
            new_volunteer = {
                "id": index + 1,
                "team": volunteer[0],  # Team di Appartenenza
                "status": volunteer[1],  # Status
                "subleader": volunteer[2],  # Subleader
                "cognome": volunteer[3],  # Cognome
                "nome": volunteer[4],  # Nome
                "genere": volunteer[5],  # Genere
                "ex_socio": volunteer[6],  # Ex Socio
                "data_dimissione": volunteer[7],  # Data Dimissione
                "note": volunteer[8],  # Note
                "telefono": volunteer[9],  # Telefono
                "email_personale": volunteer[10],  # Email personale
                "data_di_nascita": volunteer[11],  # Data di nascita
                "luogo_di_nascita": volunteer[12],  # Luogo di nascita
                "codice_fiscale": volunteer[13],  # Codice fiscale
                "luogo_di_residenza": volunteer[14],  # Luogo di residenza
                "indirizzo_di_domicilio": volunteer[15],  # Indirizzo di domicilio
                "iscritto_in_sapienza": volunteer[16],  # Sei iscritto in Sapienza?
                "matricola": volunteer[17],  # Matricola
                "email_istituzionale": volunteer[18],  # Email istituzionale
                "status_accademico": volunteer[19],  # Status accademico
                "facolta_di_appartenenza": volunteer[20],  # Facoltà di appartenenza
                "dipartimento": volunteer[21],  # Dipartimento
                "tipologia": volunteer[22],  # Tipologia
                "corso_di_laurea": volunteer[23],  # Corso
                "anno_di_iscrizione": volunteer[24],  # Anno di iscrizione
                "erasmus_o_estero": volunteer[25],  # Erasmus o periodo all'estero
                "associazione_esterna": volunteer[26],  # Associazione esterna
                "nome_associazione": volunteer[27],  # Nome associazione
                "data_ingresso_associazione": volunteer[
                    28
                ],  # Data di ingresso in Associazione
                "esigenze_alimentari": volunteer[29],  # Esigenze alimentari
                "taglia_tshirt": volunteer[30],  # Taglia T-Shirt
                "tshirt_presa": volunteer[31],  # T-Shirt Presa?
                "documenti_socio": volunteer[32],  # Documenti socio
                "tipo_di_documento": volunteer[33],  # Tipo di documento
                "numero_del_documento": volunteer[34],  # Numero del documento
                "scadenza_documento": volunteer[35],  # Scadenza documento
            }

            volunteers_coll.insert_one(new_volunteer)

    print("Collection 'volunteers' loaded successfully.")


loadVolunteers()
