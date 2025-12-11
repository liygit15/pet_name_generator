from flask import Blueprint, request, abort, make_response
from ..db import db
from ..models.pet import Pet
from google import genai
from flask import jsonify

client = genai.Client()

bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def create_pet():
    request_body = request.get_json()
    pet_name = generate_name(request_body)
    request_body["name"] = pet_name

    pet = Pet(
        name=pet_name,
        animal_type=request_body["animal_type"],
        color=request_body["color"],
        personality=request_body["personality"]
    )

    db.session.add(pet)
    db.session.commit()

    return {"message": f"Pet name successfully added"}, 201

GENERATE_PROMPT = """
You are a creative pet name generator.

Generate ONE cute, simple pet name based on the following traits:
- Species: {species}
- Color: {color}
- Personality: {personality}

Rules:
- Only return the name.
- Do not include quotes.
- Do not include explanations.
- The name should be 1 to 2 words only.
- the only output should be string.
"""
def generate_name(request_body):
    input_message = GENERATE_PROMPT.format(
        species = request_body["animal_type"],
        color = request_body["color"],
        personality = request_body["personality"]
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=input_message
    )
    
    return response.text.strip()
    

@bp.get("")
def get_pets():
    pet_query = db.select(Pet)

    pets = db.session.scalars(pet_query)
    response = []

    for pet in pets:
        response.append(pet.to_dict())

    return response

@bp.get("/<pet_id>")
def get_single_pet(pet_id):
    pet = validate_model(Pet,pet_id)
    return pet.to_dict()

def validate_model(cls,id):
    try:
        id = int(id)
    except:
        response =  response = {"message": f"{cls.__name__} {id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)
    if model:
        return model

    response = {"message": f"{cls.__name__} {id} not found"}
    abort(make_response(response, 404))