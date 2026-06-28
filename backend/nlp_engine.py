import os
import re

# Custom lightweight phrase/keyword NLP matcher to replace spaCy in production
# This keeps the serverless bundle size tiny and avoids AWS Lambda/Vercel package limits.

FOOD_PATTERNS = {
    "pesarattu": ["pesarattu", "moong dal dosa", "moong bean", "moong beans"],
    "upma_pesarattu": ["upma pesarattu"],
    "punugulu": ["punugulu", "punugulu batter"],
    "dibba_rottu": ["dibba rottu", "minapa rotti"],
    "garelu": ["garelu", "vada", "vadas"],
    "mirapakaya_bajji": ["mirapakaya bajji", "mirchi bajji", "chili bajji", "bajji"],
    "thapala_chekkalu": ["thapala chekkalu", "rice crackers"],
    "gunta_ponganalu": ["gunta ponganalu", "ponganalu"],
    "hyderabadi_biryani": ["hyderabadi biryani", "biryani"],
    "kodi_pulao": ["kodi pulao", "chicken pulao", "pulao"],
    "pulihora": ["pulihora", "tamarind rice"],
    "ragi_sangati": ["ragi sangati", "ragi ball", "ragi balls"],
    "mudda_pappu": ["mudda pappu", "yellow lentils", "toor dal"],
    "ulava_charu": ["ulava charu", "horse gram soup"],
    "pappu_charu": ["pappu charu", "lentil soup"],
    "pulagam": ["pulagam", "rice and split yellow mung"],
    "majjiga_pulusu": ["majjiga pulusu", "majjiga charu", "buttermilk stew"],
    "gutti_vankaya_kura": ["gutti vankaya kura", "gutti vankaya", "eggplant curry", "brinjal curry"],
    "panasa_puttu_koora": ["panasa puttu koora", "jackfruit curry", "raw jackfruit"],
    "pulasa_pulusu": ["pulasa pulusu", "fish curry", "hilsa fish"],
    "natu_kodi_pulusu": ["natu kodi pulusu", "country chicken curry", "chicken curry"],
    "gongura_mutton": ["gongura mutton", "mutton curry"],
    "avakaya_pachadi": ["avakaya pachadi", "mango pickle", "raw mango pickle"],
    "gongura_pachadi": ["gongura pachadi", "sorrel leaves pickle"],
    "allam_pachadi": ["allam pachadi", "ginger pickle"],
    "kandi_podi": ["kandi podi", "lentil powder"],
    "pootharekulu": ["pootharekulu", "paper sweet"],
    "poornam_boorelu": ["poornam boorelu", "poornalu", "sweet dumplings"],
    "ariselu": ["ariselu", "jaggery rice cake"],
    "spiced_majjiga": ["spiced majjiga", "buttermilk", "spiced buttermilk"]
}

SYMPTOM_PATTERNS = {
    # Moderate
    "hives_urticaria": ["hive", "hives", "urticaria", "welt", "welts", "itchy bumps", "red bumps"],
    "localized_rash": ["rash", "redness", "erythema", "skin rash", "localized rash", "contact rash"],
    "itchy_skin": ["itchy skin", "pruritus", "itching", "itchy"],
    "mild_swelling": ["lip swelling", "lips swelling", "eyelid swelling", "face swelling", "swollen lip", "swollen lips", "swollen eyes", "puffy face", "mild swelling", "swollen face"],
    "sneezing": ["sneezing", "sneeze", "sneezed"],
    "runny_nose": ["runny nose", "stuffy nose", "blocked nose", "nasal congestion", "rhinitis"],
    "itchy_eyes": ["itchy eyes", "watery eyes", "red eyes"],
    "stomach_cramps": ["stomach cramp", "stomach cramps", "abdominal cramps", "stomach pain", "stomach ache", "abdominal pain", "tummy ache"],
    "nausea": ["nausea", "nauseous", "feeling sick", "sick to stomach"],
    "diarrhea": ["diarrhea", "diarrhoea", "purging", "loose stools"],
    "tongue_swelling": ["tongue swelling", "swollen tongue", "tingling tongue", "itchy tongue"],
    "metallic_taste": ["metallic taste", "copper taste", "metal taste"],
    "excessive_salivation": ["excessive salivation", "extra saliva", "increased salivation", "drooling", "drool"],
    "tingling_mouth": ["tingling mouth", "tingling lips", "itchy mouth", "itchy lips", "burning mouth", "oral allergy"],
    "cough": ["cough", "coughing", "coughed", "dry cough"],
    "heartburn": ["heartburn", "acid reflux", "reflux"],
    
    # Severe-Critical
    "diff_breathing": ["difficulty breathing", "difficult breathing", "shortness of breath", "short of breath", "gasping for air", "dyspnea", "breathing difficulty"],
    "wheezing": ["wheezing", "wheeze", "wheezed", "stridor"],
    "throat_tightness": ["throat tightness", "throat closing", "throat constriction", "throat swelling", "swollen throat", "tight throat"],
    "diff_swallowing": ["difficulty swallowing", "difficult swallowing", "pain swallowing", "dysphagia", "swallowing difficulty"],
    "skin_pallor": ["pale skin", "pale face", "looking pale", "skin pallor", "paleness"],
    "confusion": ["confusion", "confused", "disorientation", "disoriented"],
    "dizziness": ["dizzy", "dizziness", "lightheaded", "lightheadedness", "giddy", "giddiness"],
    "fainting": ["faint", "fainted", "fainting", "syncope", "blackout", "unconscious", "collapse", "passed out", "passing out"],
    "weak_pulse": ["weak pulse", "rapid pulse", "fast heartbeat", "weak heartbeat", "thready pulse"],
    "low_bp": ["low bp", "drop in blood pressure", "low blood pressure", "hypotension"],
    "severe_pain": ["severe pain", "severe cramps", "intense pain", "debilitating cramps"],
    "persistent_vomiting": ["persistent vomiting", "continuous vomiting", "uncontrollable vomiting", "repeated vomiting", "vomited repeatedly", "cannot stop vomiting"],
    "severe_diarrhea": ["watery diarrhea", "severe diarrhea", "heavy diarrhea", "violent diarrhea"],
    "blue_lips": ["blue lips", "blueness of lips", "bluish lips", "cyanosis", "blue skin"],
    "chest_tightness": ["chest pain", "chest tightness", "chest pressure", "squeezing in chest"],
    "hoarseness": ["hoarse", "hoarseness", "muffled voice", "husky voice"],
    "widespread_hives": ["widespread hives", "generalized hives", "systemic hives", "widespread swelling", "hives all over"],
    "impending_doom": ["impending doom", "feeling of doom", "sense of doom", "fear of dying", "panic about dying"],
    "slurred_speech": ["slurred speech", "slurring words", "slurred words"]
}

def extract_entities(text: str) -> dict:
    if not text:
        return {"foods": [], "symptoms": []}
        
    normalized = text.lower().strip()
    
    foods = set()
    symptoms = set()
    
    # Run phrase matching for foods
    for food_id, phrases in FOOD_PATTERNS.items():
        for phrase in phrases:
            # Match boundary word boundaries to avoid false positives (e.g. matching "vada" in "lavadas")
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, normalized):
                foods.add(food_id)
                break  # Matched this food, skip remaining phrases for it
                
    # Run phrase matching for symptoms
    for symptom_id, phrases in SYMPTOM_PATTERNS.items():
        for phrase in phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, normalized):
                symptoms.add(symptom_id)
                break  # Matched this symptom, skip remaining phrases for it
                
    return {
        "foods": list(foods),
        "symptoms": list(symptoms)
    }
