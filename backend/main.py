import os
import json
import uuid
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import db
import nlp_engine
import classifier
import scoring

app = FastAPI(
    title="AllergyGuard API",
    description="Academic NLP + Computer-Vision Food Allergy Assistant Backend",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOADS_DIR = os.path.join(STATIC_DIR, "images", "uploads")

# On serverless environments (Vercel), static files are served by the edge CDN,
# and the filesystem is read-only. We only mount static files if the directory exists.
if os.path.exists(STATIC_DIR):
    try:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    except Exception as e:
        print(f"Skipping static directory setup: {e}")
else:
    print("Static directory not found or running on Vercel. Bypassing local mount.")

# Mock Auth Helper
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        # Return a default mock user for development
        return {"id": "mock-user-123", "email": "patient@allergyguard.org"}
    token = authorization.split(" ")[1]
    if token == "invalid-token":
        raise HTTPException(status_code=401, detail="Invalid session token")
    # Decode user from token or mock it
    email = token if "@" in token else "patient@allergyguard.org"
    user = db.get_user_by_email(email)
    if not user:
        # Create user on the fly to simplify local development setup
        user = db.create_user("Mock User", email, "mock_password_hash")
    return user

# Pydantic schemas
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class KnownAssessRequest(BaseModel):
    allergens: List[str]

# --- GENERAL DATA ENDPOINTS ---

@app.get("/api/allergens")
def get_all_allergens():
    return db.get_allergens()

@app.get("/api/symptoms")
def get_all_symptoms():
    return db.get_symptoms()

@app.get("/api/foods")
def get_all_foods():
    return db.get_foods()

# --- AUTH ENDPOINTS ---

@app.post("/api/auth/register")
def register(req: RegisterRequest):
    user = db.get_user_by_email(req.email)
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    # Simple hash representation
    password_hash = f"hashed_{req.password}"
    new_user = db.create_user(req.name, req.email, password_hash)
    if not new_user:
        raise HTTPException(status_code=500, detail="Registration failed")
    return {"token": new_user["email"], "email": new_user["email"], "id": new_user["id"], "name": new_user.get("name")}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    user = db.get_user_by_email(req.email)
    if not user or user["password_hash"] != f"hashed_{req.password}":
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {"token": user["email"], "email": user["email"], "id": user["id"], "name": user.get("name")}


@app.get("/api/auth/profile")
def get_profile(user = Depends(get_current_user)):
    return user

# --- HISTORIC LOGS ---

@app.get("/api/logs")
def get_user_logs(user = Depends(get_current_user)):
    return db.get_query_logs(user["id"])

# --- CORE FEATURES ---

# 1. Known Allergy Assessment Endpoint
@app.post("/api/assess/known")
def assess_known_allergies(req: KnownAssessRequest):
    selected_allergens = set(req.allergens)
    all_foods = db.get_foods()
    
    # Fetch allergen details
    all_allergens = db.get_allergens()
    selected_allergens_details = [
        a for a in all_allergens if a["id"] in selected_allergens
    ]
    
    safe_foods = []
    unsafe_foods = []
    safe_alternatives = []
    
    for food in all_foods:
        food_allergens = set(food["allergens"])
        intersect = food_allergens.intersection(selected_allergens)
        
        if intersect:
            ingredients_field = food.get("ingredients", [])
            if isinstance(ingredients_field, str):
                try:
                    ingredients = json.loads(ingredients_field)
                except Exception:
                    ingredients = []
            elif isinstance(ingredients_field, list):
                ingredients = ingredients_field
            else:
                ingredients = []

            unsafe_foods.append({
                "id": food["id"],
                "name": food["name"],
                "image_path": food["image_path"],
                "description": food["description"],
                "triggered_allergens": list(intersect),
                "alternatives": food["alternatives"],
                "ingredients": ingredients,
                "protein_grams": food.get("protein_grams", 0),
                "protein_pct": food.get("protein_pct", 0),
                "calories": food.get("calories", 0),
                "carbs_grams": food.get("carbs_grams", 0),
                "fats_grams": food.get("fats_grams", 0)
            })
        else:
            safe_foods.append(food)
            
    # Compile a unique list of alternatives for the unsafe items
    seen_alts = set()
    for item in unsafe_foods:
        for alt in item["alternatives"]:
            if alt not in seen_alts:
                seen_alts.add(alt)
                safe_alternatives.append({
                    "name": alt,
                    "for_food": item["name"]
                })
                
    # Compile medicine guidance for known allergens
    all_medicines = db.get_medicines()
    stage_a_meds = []
    stage_b_meds = []
    
    for med in all_medicines:
        matched = any(a_id in med["mapped_allergens"] for a_id in selected_allergens)
        if matched or not selected_allergens:
            med_entry = {
                "category": med["category"],
                "description": med["description"],
                "warning": med["warning"],
                "image_path": med.get("image_path")
            }
            if med["stage"] == "A":
                stage_a_meds.append(med_entry)
            else:
                stage_b_meds.append(med_entry)
                
    doctor_note = {
        "disclaimer": "Educational content for this academic project — not a substitute for an in-person medical evaluation.",
        "mechanism": "Allergic reactions are hypersensitivity responses triggered when the immune system mistakenly identifies harmless food proteins as threats. Specifically, IgE antibodies bind to the allergen, triggering mast cells to release inflammatory chemicals like histamine. This causes blood vessel dilation (redness, swelling), smooth muscle contraction (difficulty breathing), and skin nerve irritation (itching/hives).",
        "see_doctor_bullets": [
            "You experience respiratory distress, throat constriction, or dizziness (anaphylaxis indicators).",
            "Symptoms recur consistently after consuming specific foods or food families.",
            "You require clinical diagnostic testing to confirm exact IgE-mediated triggers."
        ],
        "allergist_evaluation": "An allergist visit typically involves: a clinical interview, a Skin Prick Test (SPT) where tiny drops of allergen extracts are introduced to the skin surface, an IgE Blood Test to quantify circulating antibodies, or an Oral Food Challenge (OFC) conducted under strict medical supervision."
    }

    return {
        "selected_allergens_details": selected_allergens_details,
        "safe_foods": safe_foods,
        "unsafe_foods": unsafe_foods,
        "safe_alternatives": safe_alternatives,
        "doctor_note": doctor_note,
        "medicine_guidance": {
            "disclaimer": "Confirm with a doctor before using any medication. Dosages and brands are omitted for clinical safety.",
            "stage_a": stage_a_meds,
            "stage_b": stage_b_meds
        }
    }


# 2. Unknown Allergy Assessment Form Endpoint
@app.post("/api/assess/unknown")
async def assess_unknown_allergy(
    food_id: Optional[str] = Form(None),
    food_text: Optional[str] = Form(None),
    symptoms: Optional[str] = Form("[]"), # JSON array of symptom IDs
    symptom_text: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    user = Depends(get_current_user)
):
    try:
        try:
            symptom_ids = json.loads(symptoms)
        except Exception:
            symptom_ids = []
            
        # Save uploaded file and run image classification if present
        photo_url = None
        photo_analysis = None
        if photo:
            file_ext = os.path.splitext(photo.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            
            # Check if local uploads dir exists and is writable
            uploads_dir_exists = os.path.exists(UPLOADS_DIR)
            
            if uploads_dir_exists and os.access(UPLOADS_DIR, os.W_OK):
                save_path = os.path.join(UPLOADS_DIR, unique_filename)
                photo_url = f"/static/images/uploads/{unique_filename}"
            else:
                # Fallback to AWS Lambda /tmp directory
                save_path = os.path.join("/tmp", unique_filename)
                photo_url = "/static/images/uploads/skin_rash.jpg" # Clean fallback image
                
            with open(save_path, "wb") as f:
                content = await photo.read()
                f.write(content)
                
            # Run visual analyzer
            photo_analysis = classifier.analyze_skin_reaction(save_path)
            
        # Run free-text NLP keyword extraction
        extracted_foods = []
        extracted_symptoms = []
        
        if food_text:
            entities = nlp_engine.extract_entities(food_text)
            extracted_foods.extend(entities["foods"])
            
        if symptom_text:
            entities = nlp_engine.extract_entities(symptom_text)
            extracted_symptoms.extend(entities["symptoms"])
            
        # Merge direct and extracted elements
        all_food_ids = list(set(([food_id] if food_id else []) + extracted_foods))
        all_symptom_ids = list(set(symptom_ids + extracted_symptoms))
        
        # Calculate Risk Assessment
        assessment = scoring.calculate_allergy_assessment(
            food_ids=all_food_ids,
            symptom_ids=all_symptom_ids,
            photo_analysis=photo_analysis
        )
        
        top_allergens = assessment["top_allergens"]
        severe_symptom_detected = assessment["severe_symptom_detected"]
        
        # Generate Guidance and Support Content
        
        # A. Doctor's Note Content
        doctor_note = {
            "disclaimer": "Educational content for this academic project — not a substitute for an in-person medical evaluation.",
            "mechanism": "Allergic reactions are hypersensitivity responses triggered when the immune system mistakenly identifies harmless food proteins as threats. Specifically, IgE antibodies bind to the allergen, triggering mast cells to release inflammatory chemicals like histamine. This causes blood vessel dilation (redness, swelling), smooth muscle contraction (difficulty breathing), and skin nerve irritation (itching/hives).",
            "see_doctor_bullets": [
                "You experience respiratory distress, throat constriction, or dizziness (anaphylaxis indicators).",
                "Symptoms recur consistently after consuming specific foods or food families.",
                "You require clinical diagnostic testing to confirm exact IgE-mediated triggers."
            ],
            "allergist_evaluation": "An allergist visit typically involves: a clinical interview, a Skin Prick Test (SPT) where tiny drops of allergen extracts are introduced to the skin surface, an IgE Blood Test to quantify circulating antibodies, or an Oral Food Challenge (OFC) conducted under strict medical supervision."
        }
        
        # B. Food Guidance (avoidances and alternatives)
        all_foods = db.get_foods()
        foods_to_avoid = []
        safe_alternatives_list = []
        
        top_allergen_ids = {a["id"] for a in top_allergens}
        for food in all_foods:
            # Ensure allergens list is correctly parsed from JSON/string format
            food_allergens_field = food["allergens"]
            if isinstance(food_allergens_field, str):
                try:
                    food_allergens = set(json.loads(food_allergens_field))
                except Exception:
                    food_allergens = set()
            elif isinstance(food_allergens_field, list):
                food_allergens = set(food_allergens_field)
            else:
                food_allergens = set()
                
            triggered = [a_id for a_id in food_allergens if a_id in top_allergen_ids]
            if triggered:
                # Ensure alternatives field is correctly parsed from JSON/string format
                alternatives_field = food["alternatives"]
                if isinstance(alternatives_field, str):
                    try:
                        alternatives = json.loads(alternatives_field)
                    except Exception:
                        alternatives = []
                elif isinstance(alternatives_field, list):
                    alternatives = alternatives_field
                else:
                    alternatives = []
                    
                ingredients_field = food.get("ingredients", [])
                if isinstance(ingredients_field, str):
                    try:
                        ingredients = json.loads(ingredients_field)
                    except Exception:
                        ingredients = []
                elif isinstance(ingredients_field, list):
                    ingredients = ingredients_field
                else:
                    ingredients = []

                foods_to_avoid.append({
                    "id": food["id"],
                    "name": food["name"],
                    "image_path": food["image_path"],
                    "description": food["description"],
                    "triggered_allergens": triggered,
                    "alternatives": alternatives,
                    "ingredients": ingredients,
                    "protein_grams": food.get("protein_grams", 0),
                    "protein_pct": food.get("protein_pct", 0),
                    "calories": food.get("calories", 0),
                    "carbs_grams": food.get("carbs_grams", 0),
                    "fats_grams": food.get("fats_grams", 0)
                })
                for alt in alternatives:
                    if alt not in [x["name"] for x in safe_alternatives_list]:
                        safe_alternatives_list.append({"name": alt, "for_food": food["name"]})
                        
        # C. Medicine Guidance
        all_medicines = db.get_medicines()
        stage_a_meds = []
        stage_b_meds = []
        
        for med in all_medicines:
            # Ensure mapped_allergens list is correctly parsed from JSON/string format
            mapped_allergens_field = med["mapped_allergens"] if "mapped_allergens" in med else med.get("allergens")
            if isinstance(mapped_allergens_field, str):
                try:
                    mapped_allergens = set(json.loads(mapped_allergens_field))
                except Exception:
                    mapped_allergens = set()
            elif isinstance(mapped_allergens_field, list):
                mapped_allergens = set(mapped_allergens_field)
            else:
                mapped_allergens = set()
                
            # Match medicines mapping to any of the identified top allergens
            matched = any(a_id in mapped_allergens for a_id in top_allergen_ids)
            if matched or not top_allergen_ids: # Fallback: if no allergens, show generic
                med_entry = {
                    "category": med["category"],
                    "description": med["description"],
                    "warning": med["warning"],
                    "image_path": med.get("image_path")
                }
                if med["stage"] == "A":
                    stage_a_meds.append(med_entry)
                else:
                    stage_b_meds.append(med_entry)
                    
        # Format Results Package
        results_package = {
            "top_allergens": top_allergens,
            "severe_symptom_detected": severe_symptom_detected,
            "emergency_alert": severe_symptom_detected,
            "extracted_foods": extracted_foods,
            "extracted_symptoms": extracted_symptoms,
            "photo_analysis": photo_analysis,
            "doctor_note": doctor_note,
            "food_guidance": {
                "avoid": foods_to_avoid,
                "alternatives": safe_alternatives_list
            },
            "medicine_guidance": {
                "disclaimer": "Confirm with a doctor before using any medication. Dosages and brands are omitted for clinical safety.",
                "stage_a": stage_a_meds,
                "stage_b": stage_b_meds
            }
        }
        
        # Save log entry
        db.save_query_log(
            user_id=user["id"],
            query_text=f"Food: {food_text or ''} | Symptoms: {symptom_text or ''}",
            selected_symptoms=all_symptom_ids,
            photo_url=photo_url,
            photo_analysis=photo_analysis,
            results=results_package
        )
        
        return results_package
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Runtime crash inside assess_unknown_allergy",
                "message": str(e),
                "traceback": tb.split("\n")
            }
        )

