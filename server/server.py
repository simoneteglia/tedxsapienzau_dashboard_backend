import pymongo
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from bson import ObjectId
from json import loads as parse_json
from datetime import datetime

app = Flask(__name__, static_folder="../client/build", static_url_path="")
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def fetch():
    return jsonify({"message": "Server working", "status": 200})


@app.before_request
def before_request():
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
            "Access-Control-Allow-Credentials": "true",
        }
        return ("", 200, headers)


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["tedxsapienzau_gestione_personale"]


@app.route("/volunteers", methods=["GET"])
def get_volunteers():
    volunteers_coll = db["volunteers"]
    volunteers = volunteers_coll.find()
    volunteers_list = []
    for volunteer in volunteers:
        volunteer["_id"] = str(volunteer["_id"])
        volunteers_list.append(volunteer)
    return jsonify({"volunteers": volunteers_list, "status": 200})


def parse_json(data):
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, dict):
        return {key: parse_json(value) for key, value in data.items()}
    if isinstance(data, list):
        return [parse_json(item) for item in data]
    return data


@app.route("/volunteer", methods=["GET"])
def get_volunteer_details():
    id = request.args.get("id")

    print(f"Fetching volunteer with matricola: {id}")

    volunteers_coll = db["volunteers"]

    if not id:
        return jsonify({"message": "Missing id", "status": 400})

    try:
        query = {"matricola": int(id)}
    except ValueError:
        return jsonify(
            {"message": "Invalid student_id format. It should be an integer.", "status": 400}
        )

    volunteer = volunteers_coll.find_one(query)

    if not volunteer:
        return jsonify({"message": "Volunteer not found", "status": 404})

    return jsonify({"volunteer": parse_json(volunteer), "status": 200})


@app.route("/volunteer", methods=["POST"])
def add_volunteer():
    try:
        data = request.json

        print(data)

        if not data:
            return jsonify({"message": "No data provided", "status": 400})

        if "id" not in data or not isinstance(data["id"], int):
            return jsonify(
                {
                    "message": "Field 'id' is required and must be an integer",
                    "status": 400,
                }
            )

        volunteers_coll = db["volunteers"]

        if volunteers_coll.find_one({"id": data["id"]}):
            return jsonify(
                {"message": "Volunteer with this id already exists", "status": 400}
            )

        required_fields = [
            "id",
            "team",  # Team di Appartenenza
            "status",  # Status
            "subleader",  # Subleader
            "cognome",  # Cognome
            "nome",  # Nome
            "genere",  # Genere
            "ex_socio",  # Ex Socio
            "data_dimissione",  # Data Dimissione
            "note",  # Note
            "telefono",  # Telefono
            "email_personale",  # Email personale
            "data_di_nascita",  # Data di nascita
            "luogo_di_nascita",  # Luogo di nascita
            "codice_fiscale",  # Codice fiscale
            "luogo_di_residenza",  # Luogo di residenza
            "indirizzo_di_domicilio",  # Indirizzo di domicilio
            "iscritto_in_sapienza",  # Sei iscritto in Sapienza?
            "matricola",  # Matricola
            "email_istituzionale",  # Email istituzionale
            "status_accademico",  # Status accademico
            "facolta_di_appartenenza",  # Facoltà di appartenenza
            "dipartimento",  # Dipartimento
            "tipologia",  # Tipologia
            "corso_di_laurea",  # Corso
            "anno_di_iscrizione",  # Anno di iscrizione
            "erasmus_o_estero",  # Erasmus o periodo all'estero
            "associazione_esterna",  # Associazione esterna
            "nome_associazione",  # Nome associazione
            "data_ingresso_associazione",  # Data di ingresso in Associazione
            "esigenze_alimentari",  # Esigenze alimentari
            "taglia_tshirt",  # Taglia T-Shirt
            "tshirt_presa",  # T-Shirt Presa?
            "documenti_socio",  # Documenti socio
            "tipo_di_documento",  # Tipo di documento
            "numero_del_documento",  # Numero del documento
            "scadenza_documento",  # Scadenza documento
        ]

        volunteer_data = {field: data.get(field, "") for field in required_fields}

        volunteers_coll.insert_one(volunteer_data)

        return jsonify(
            {
                "message": "Volunteer added successfully",
                "volunteer": volunteer_data,
                "status": 201,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e), "status": 500})


@app.route("/volunteer", methods=["PUT"])
def update_volunteer():
    matricola = request.args.get("id")
    volunteers_coll = db["volunteers"]

    try:
        if not matricola:
            return jsonify({"error": "Missing matricola"}), 400

        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        query = {"matricola": int(matricola)}

        volunteer = volunteers_coll.find_one(query)
        if not volunteer:
            return jsonify({"error": "Volunteer not found"}), 404

        updated_data = {k: v for k, v in data.items() if v is not None}
        volunteers_coll.update_one(query, {"$set": updated_data})

        updated_volunteer = volunteers_coll.find_one(query)
        updated_volunteer["_id"] = str(updated_volunteer["_id"])

        return jsonify({
            "message": "Volunteer updated successfully",
            "volunteer": updated_volunteer,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/disable_volunteer", methods=["PUT"])
def disable_volunteer():
    id_param = request.args.get("id")
    matricola_param = request.args.get("matricola")
    volunteers_coll = db["volunteers"]

    if not id_param and not matricola_param:
        return jsonify({"error": "Missing id or matricola"}), 400

    try:
        if id_param:
            query = {"id": int(id_param)}
        else:
            query = {"matricola": int(matricola_param)}

        volunteer = volunteers_coll.find_one(query)
        if not volunteer:
            return jsonify({"error": "Volunteer not found"}), 404

        update_fields = {
            "ex_socio": True,
            "data_dimissione": datetime.utcnow().strftime("%d-%m-%Y"),
        }

        volunteers_coll.update_one(query, {"$set": update_fields})

        updated_volunteer = volunteers_coll.find_one(query)
        updated_volunteer["_id"] = str(updated_volunteer["_id"])

        return jsonify({
            "message": "Volontario eliminato",
            "volunteer": updated_volunteer,
            "status": 200,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/volunteers/by_city", methods=["GET"])
def volunteers_by_city():
    volunteers_coll = db["volunteers"]

    pipeline = [
        {"$group": {"_id": "$luogo_di_nascita", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]

    result = list(volunteers_coll.aggregate(pipeline))

    return jsonify({
        "data": [{"city": r["_id"], "count": r["count"]} for r in result if r["_id"]]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5500))
    app.run(host="0.0.0.0", port=port, debug=True)
