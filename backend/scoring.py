import json
from db import get_allergens, get_foods, get_symptoms

# Mappings of specific non-standard allergens to their relevant symptoms
# standard IgE allergens (peanuts, tree nuts, etc.) map to all standard symptoms by default
SPECIAL_ALLERGEN_SYMPTOMS = {
    "chili_capsaicin": {
        "positive": ["heartburn", "tingling_mouth", "excessive_salivation", "localized_rash", "nausea", "runny_nose"],
        "negative": ["diff_breathing", "wheezing", "throat_tightness", "diff_swallowing", "skin_pallor", "confusion", "dizziness", "fainting", "weak_pulse", "low_bp", "blue_lips", "chest_tightness", "widespread_hives", "impending_doom", "slurred_speech"]
    },
    "msg_sensitivity": {
        "positive": ["metallic_taste", "excessive_salivation", "nausea", "localized_rash", "heartburn", "dizziness", "cough"],
        "negative": ["diff_breathing", "wheezing", "throat_tightness", "diff_swallowing", "skin_pallor", "fainting", "weak_pulse", "low_bp", "blue_lips", "widespread_hives", "impending_doom", "slurred_speech"]
    },
    "sulfites": {
        "positive": ["sneezing", "runny_nose", "cough", "diff_breathing", "wheezing", "itchy_eyes", "localized_rash", "stomach_cramps"],
        "negative": ["metallic_taste", "excessive_salivation", "tingling_mouth"]
    },
    "latex_fruit": {
        "positive": ["tingling_mouth", "mild_swelling", "hives_urticaria", "itchy_skin", "localized_rash", "stomach_cramps", "nausea"],
        "negative": []
    },
    "jaggery": {
        "positive": ["sneezing", "runny_nose", "cough", "hives_urticaria", "itchy_skin", "itchy_eyes", "stomach_cramps"],
        "negative": []
    }
}

def calculate_allergy_assessment(food_ids, symptom_ids, photo_analysis=None):
    """
    Evaluates symptoms, foods, and photo analysis to determine likely allergens.
    
    Args:
        food_ids (list): IDs of foods eaten
        symptom_ids (list): IDs of symptoms present
        photo_analysis (dict, optional): Result of skin pattern image classifier
        
    Returns:
        dict: {
            "top_allergens": [{"id": str, "name": str, "score": float, "description": str}],
            "severe_symptom_detected": bool,
            "emergency_alert": bool
        }
    """
    allergens = get_allergens()
    foods = get_foods()
    symptoms = get_symptoms()
    
    # 1. Map photo analysis to symptoms
    resolved_symptom_ids = set(symptom_ids)
    photo_symptom_weight = 1.0
    
    if photo_analysis and photo_analysis.get("label") != "inconclusive":
        label = photo_analysis["label"]
        conf = photo_analysis["confidence"]
        photo_symptom_weight = conf
        
        if label == "localized urticaria":
            resolved_symptom_ids.add("hives_urticaria")
        elif label == "diffuse redness":
            resolved_symptom_ids.add("localized_rash")
        elif label == "swelling":
            resolved_symptom_ids.add("mild_swelling")
            
    # 2. Check for severe symptoms
    severe_symptom_detected = False
    symptom_dict = {s["id"]: s for s in symptoms}
    
    for s_id in resolved_symptom_ids:
        if s_id in symptom_dict and symptom_dict[s_id]["severity"] == "Severe-Critical":
            severe_symptom_detected = True
            break
            
    # 3. Determine candidate allergens from foods eaten
    food_dict = {f["id"]: f for f in foods}
    eaten_allergens = set()
    for f_id in food_ids:
        if f_id in food_dict:
            eaten_allergens.update(food_dict[f_id]["allergens"])
            
    # 4. Score each allergen
    scores = {}
    
    for allergen in allergens:
        a_id = allergen["id"]
        score = 0.0
        
        # Factor A: Food Matching (Baseline 50.0 points if matched)
        # If food was specified, the allergen MUST be in the food to be high likelihood.
        if food_ids:
            if a_id in eaten_allergens:
                score += 50.0
            else:
                # If foods were identified and this allergen is NOT in them, penalize heavily.
                score -= 100.0
        else:
            # If no food was specified at all, we give a default food baseline so symptom matching works
            score += 15.0
            
        # Factor B: Symptom Matching
        # Check if the allergen is standard IgE or a special allergen
        if a_id in SPECIAL_ALLERGEN_SYMPTOMS:
            positives = SPECIAL_ALLERGEN_SYMPTOMS[a_id]["positive"]
            negatives = SPECIAL_ALLERGEN_SYMPTOMS[a_id]["negative"]
            
            for s_id in resolved_symptom_ids:
                # Apply weight if it's the photo-mapped symptom
                weight = photo_symptom_weight if s_id not in symptom_ids else 1.0
                
                if s_id in positives:
                    # Give points for matching symptoms
                    is_severe = s_id in symptom_dict and symptom_dict[s_id]["severity"] == "Severe-Critical"
                    score += (20.0 if is_severe else 15.0) * weight
                elif s_id in negatives:
                    # Penalize for symptoms that do NOT match this non-IgE irritant/sensitivity
                    score -= 30.0 * weight
        else:
            # Standard IgE Allergen
            # Standard IgE allergens map to almost all systemic symptoms
            for s_id in resolved_symptom_ids:
                weight = photo_symptom_weight if s_id not in symptom_ids else 1.0
                
                # Exclude symptoms specific only to chili/msg if they don't apply,
                # but standard IgE allergens trigger hives, breathing, swelling, cramps, etc.
                is_severe = s_id in symptom_dict and symptom_dict[s_id]["severity"] == "Severe-Critical"
                
                if s_id in ["heartburn", "excessive_salivation", "metallic_taste"]:
                    # Less typical for standard IgE, but possible
                    score += 5.0 * weight
                else:
                    # Hives, swelling, diarrhea, breathing issues are typical
                    score += (25.0 if is_severe else 15.0) * weight
                    
        # Caps and floors
        scores[a_id] = max(0.0, score)
        
    # 5. Format results
    top_allergens = []
    for allergen in allergens:
        a_id = allergen["id"]
        final_score = scores[a_id]
        if final_score > 0.0:
            # Map score to percentage (max 98.0% for educational sanity)
            percentage = min(98.0, round(final_score, 1))
            top_allergens.append({
                "id": a_id,
                "name": allergen["name"],
                "score": percentage,
                "description": allergen["description"]
            })
            
    # Sort by score descending
    top_allergens.sort(key=lambda x: x["score"], reverse=True)
    
    # Keep top 1-3
    top_allergens = top_allergens[:3]
    
    # If no allergens matched (e.g. all penalized), return empty list or fallback
    return {
        "top_allergens": top_allergens,
        "severe_symptom_detected": severe_symptom_detected,
        "emergency_alert": severe_symptom_detected
    }
