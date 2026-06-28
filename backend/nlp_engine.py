import os
import spacy
from spacy.pipeline import EntityRuler

nlp = None

def init_nlp():
    global nlp
    if nlp is not None:
        return
        
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = spacy.blank("en")
        
    ruler = nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
    
    patterns = []
    
    # 1. FOOD PATTERNS
    food_patterns = {
        "pesarattu": [[{"LOWER": "pesarattu"}], [{"LOWER": "moong"}, {"LOWER": "dal"}, {"LOWER": "dosa"}]],
        "upma_pesarattu": [[{"LOWER": "upma"}, {"LOWER": "pesarattu"}]],
        "punugulu": [[{"LOWER": "punugulu"}]],
        "dibba_rottu": [[{"LOWER": "dibba"}, {"LOWER": "rottu"}], [{"LOWER": "minapa"}, {"LOWER": "rotti"}]],
        "garelu": [[{"LOWER": "garelu"}], [{"LOWER": "vada"}]],
        "mirapakaya_bajji": [[{"LOWER": "mirapakaya"}, {"LOWER": "bajji"}], [{"LOWER": "mirchi"}, {"LOWER": "bajji"}]],
        "thapala_chekkalu": [[{"LOWER": "thapala"}, {"LOWER": "chekkalu"}]],
        "gunta_ponganalu": [[{"LOWER": "gunta"}, {"LOWER": "ponganalu"}], [{"LOWER": "ponganalu"}]],
        "hyderabadi_biryani": [[{"LOWER": "hyderabadi"}, {"LOWER": "biryani"}], [{"LOWER": "biryani"}]],
        "kodi_pulao": [[{"LOWER": "kodi"}, {"LOWER": "pulao"}], [{"LOWER": "pulao"}]],
        "pulihora": [[{"LOWER": "pulihora"}], [{"LOWER": "tamarind"}, {"LOWER": "rice"}]],
        "ragi_sangati": [[{"LOWER": "ragi"}, {"LOWER": "sangati"}], [{"LOWER": "ragi"}, {"LOWER": "ball"}]],
        "mudda_pappu": [[{"LOWER": "mudda"}, {"LOWER": "pappu"}], [{"LOWER": "pappu"}]],
        "ulava_charu": [[{"LOWER": "ulava"}, {"LOWER": "charu"}]],
        "pappu_charu": [[{"LOWER": "pappu"}, {"LOWER": "charu"}]],
        "pulagam": [[{"LOWER": "pulagam"}]],
        "majjiga_pulusu": [[{"LOWER": "majjiga"}, {"LOWER": "pulusu"}], [{"LOWER": "majjiga"}, {"LOWER": "charu"}]],
        "gutti_vankaya_kura": [[{"LOWER": "gutti"}, {"LOWER": "vankaya"}, {"LOWER": "kura"}], [{"LOWER": "gutti"}, {"LOWER": "vankaya"}], [{"LOWER": "eggplant"}, {"LOWER": "curry"}]],
        "panasa_puttu_koora": [[{"LOWER": "panasa"}, {"LOWER": "puttu"}, {"LOWER": "koora"}], [{"LOWER": "jackfruit"}, {"LOWER": "curry"}]],
        "pulasa_pulusu": [[{"LOWER": "pulasa"}, {"LOWER": "pulusu"}], [{"LOWER": "fish"}, {"LOWER": "curry"}]],
        "natu_kodi_pulusu": [[{"LOWER": "natu"}, {"LOWER": "kodi"}, {"LOWER": "pulusu"}], [{"LOWER": "chicken"}, {"LOWER": "curry"}]],
        "gongura_mutton": [[{"LOWER": "gongura"}, {"LOWER": "mutton"}], [{"LOWER": "mutton"}, {"LOWER": "curry"}]],
        "avakaya_pachadi": [[{"LOWER": "avakaya"}, {"LOWER": "pachadi"}], [{"LOWER": "mango"}, {"LOWER": "pickle"}]],
        "gongura_pachadi": [[{"LOWER": "gongura"}, {"LOWER": "pachadi"}]],
        "allam_pachadi": [[{"LOWER": "allam"}, {"LOWER": "pachadi"}], [{"LOWER": "ginger"}, {"LOWER": "pickle"}]],
        "kandi_podi": [[{"LOWER": "kandi"}, {"LOWER": "podi"}], [{"LOWER": "lentil"}, {"LOWER": "powder"}]],
        "pootharekulu": [[{"LOWER": "pootharekulu"}]],
        "poornam_boorelu": [[{"LOWER": "poornam"}, {"LOWER": "boorelu"}], [{"LOWER": "poornalu"}]],
        "ariselu": [[{"LOWER": "ariselu"}]],
        "spiced_majjiga": [[{"LOWER": "spiced"}, {"LOWER": "majjiga"}], [{"LOWER": "buttermilk"}]]
    }
    
    for food_id, pattern_lists in food_patterns.items():
        for pat in pattern_lists:
            patterns.append({"label": "FOOD", "pattern": pat, "id": food_id})
            
    # 2. SYMPTOM PATTERNS
    symptom_patterns = {
        # Moderate
        "hives_urticaria": [
            [{"LOWER": {"IN": ["hive", "hives", "urticaria", "welt", "welts"]}}],
            [{"LOWER": "itchy"}, {"LOWER": "bumps"}],
            [{"LOWER": "red"}, {"LOWER": "bumps"}]
        ],
        "localized_rash": [
            [{"LOWER": {"IN": ["skin", "localized", "contact"]}}, {"OP": "*"}, {"LOWER": {"IN": ["rash", "redness", "erythema"]}}],
            [{"LOWER": "rash"}],
            [{"LOWER": "redness"}]
        ],
        "itchy_skin": [
            [{"LOWER": {"IN": ["itchy", "itching"]}}, {"LOWER": "skin"}],
            [{"LOWER": "pruritus"}],
            [{"LOWER": "itching"}]
        ],
        "mild_swelling": [
            [{"LOWER": {"IN": ["lip", "lips", "eyelid", "eyelids", "face", "eye", "eyes", "cheek", "cheeks"]}}, {"OP": "*"}, {"LOWER": {"IN": ["swelling", "swell", "swollen", "puffiness", "puffy"]}}],
            [{"LOWER": "mild"}, {"LOWER": "swelling"}]
        ],
        "sneezing": [
            [{"LOWER": {"IN": ["sneezing", "sneeze", "sneezed"]}}]
        ],
        "runny_nose": [
            [{"LOWER": {"IN": ["runny", "stuffy", "blocked"]}}, {"LOWER": "nose"}],
            [{"LOWER": "nasal"}, {"LOWER": "congestion"}],
            [{"LOWER": "rhinitis"}]
        ],
        "itchy_eyes": [
            [{"LOWER": "itchy"}, {"LOWER": "eyes"}],
            [{"LOWER": "watery"}, {"LOWER": "eyes"}],
            [{"LOWER": "red"}, {"LOWER": "eyes"}]
        ],
        "stomach_cramps": [
            [{"LOWER": {"IN": ["stomach", "abdominal", "belly"]}}, {"OP": "*"}, {"LOWER": {"IN": ["cramp", "cramps", "pain", "ache"]}}],
            [{"LOWER": "stomach"}, {"LOWER": "discomfort"}]
        ],
        "nausea": [
            [{"LOWER": {"IN": ["nausea", "nauseous", "nauseating"]}}],
            [{"LOWER": "sick"}, {"LOWER": "to"}, {"LOWER": "stomach"}]
        ],
        "diarrhea": [
            [{"LOWER": {"IN": ["diarrhea", "diarrhoea", "purging"]}}]
        ],
        "tongue_swelling": [
            [{"LOWER": "tongue"}, {"OP": "*"}, {"LOWER": {"IN": ["swelling", "swell", "swollen", "tingling", "tingle", "itch", "itching"]}}]
        ],
        "metallic_taste": [
            [{"LOWER": {"IN": ["metallic", "copper", "metal"]}}, {"LOWER": "taste"}]
        ],
        "excessive_salivation": [
            [{"LOWER": {"IN": ["excessive", "extra", "increased", "more"]}}, {"OP": "*"}, {"LOWER": {"IN": ["saliva", "salivation", "drool", "drooling"]}}]
        ],
        "tingling_mouth": [
            [{"LOWER": {"IN": ["tingle", "tingling", "itch", "itching", "burn", "burning"]}}, {"LOWER": {"IN": ["mouth", "lips", "palate", "throat", "oral"]}}],
            [{"LOWER": "oral"}, {"LOWER": "allergy"}]
        ],
        "cough": [
            [{"LOWER": {"IN": ["cough", "coughing", "coughed"]}}],
            [{"LOWER": "dry"}, {"LOWER": "cough"}]
        ],
        "heartburn": [
            [{"LOWER": {"IN": ["heartburn", "reflux"]}}],
            [{"LOWER": "acid"}, {"LOWER": "reflux"}]
        ],
        
        # Severe-Critical
        "diff_breathing": [
            [{"LOWER": {"IN": ["difficulty", "difficult", "trouble", "struggle", "struggling", "shortness", "short"]}}, {"OP": "*"}, {"LOWER": {"IN": ["breathing", "breathe", "breath"]}}],
            [{"LOWER": "gasping"}, {"LOWER": "for"}, {"LOWER": "air"}],
            [{"LOWER": "dyspnea"}]
        ],
        "wheezing": [
            [{"LOWER": {"IN": ["wheezing", "wheeze", "wheezed", "stridor"]}}]
        ],
        "throat_tightness": [
            [{"LOWER": "throat"}, {"OP": "*"}, {"LOWER": {"IN": ["tightness", "tight", "closing", "constriction", "swelling", "swell", "swollen"]}}]
        ],
        "diff_swallowing": [
            [{"LOWER": {"IN": ["difficulty", "difficult", "hard", "pain", "trouble"]}}, {"OP": "*"}, {"LOWER": {"IN": ["swallowing", "swallow"]}}],
            [{"LOWER": "dysphagia"}]
        ],
        "skin_pallor": [
            [{"LOWER": {"IN": ["pale", "paleness", "pallor"]}}, {"OP": "*"}, {"LOWER": {"IN": ["skin", "face", "look", "looking"]}}]
        ],
        "confusion": [
            [{"LOWER": {"IN": ["confusion", "confused", "disorientation", "disoriented"]}}]
        ],
        "dizziness": [
            [{"LOWER": {"IN": ["dizzy", "dizziness", "lightheaded", "lightheadedness", "giddy", "giddiness"]}}]
        ],
        "fainting": [
            [{"LOWER": {"IN": ["faint", "fainted", "fainting", "syncope", "blackout", "unconscious", "collapse", "collapsed"]}}],
            [{"LOWER": "passed"}, {"LOWER": "out"}],
            [{"LOWER": "passing"}, {"LOWER": "out"}]
        ],
        "weak_pulse": [
            [{"LOWER": {"IN": ["weak", "rapid", "fast", "racing", "thready"]}}, {"OP": "*"}, {"LOWER": {"IN": ["pulse", "heartbeat", "heartrate", "heart"]}}]
        ],
        "low_bp": [
            [{"LOWER": {"IN": ["drop", "low", "fall"]}}, {"OP": "*"}, {"LOWER": {"IN": ["pressure", "bp", "hypotension"]}}]
        ],
        "severe_pain": [
            [{"LOWER": {"IN": ["severe", "intense", "extreme", "bad"]}}, {"OP": "*"}, {"LOWER": {"IN": ["pain", "cramps", "cramping"]}}]
        ],
        "persistent_vomiting": [
            [{"LOWER": {"IN": ["persistent", "continuous", "uncontrollable", "repeated", "frequent", "constant"]}}, {"OP": "*"}, {"LOWER": {"IN": ["vomiting", "vomit", "throwing", "throw"]}}],
            [{"LOWER": "vomited"}, {"LOWER": "repeatedly"}],
            [{"LOWER": "cannot"}, {"LOWER": "stop"}, {"LOWER": "vomiting"}]
        ],
        "severe_diarrhea": [
            [{"LOWER": {"IN": ["watery", "severe", "heavy", "violent"]}}, {"OP": "*"}, {"LOWER": {"IN": ["diarrhea", "diarrhoea"]}}]
        ],
        "blue_lips": [
            [{"LOWER": {"IN": ["blue", "blueness", "bluish", "gray", "grey"]}}, {"OP": "*"}, {"LOWER": {"IN": ["lips", "lip", "face", "skin", "cyanosis"]}}]
        ],
        "chest_tightness": [
            [{"LOWER": "chest"}, {"OP": "*"}, {"LOWER": {"IN": ["pain", "tightness", "pressure", "squeezing", "heaviness"]}}]
        ],
        "hoarseness": [
            [{"LOWER": {"IN": ["hoarse", "hoarseness", "muffled", "husky"]}}, {"OP": "*"}, {"LOWER": {"IN": ["voice", "vocal", "speech"]}}]
        ],
        "widespread_hives": [
            [{"LOWER": {"IN": ["widespread", "generalized", "systemic", "full", "whole"]}}, {"OP": "*"}, {"LOWER": {"IN": ["hives", "rash", "swelling"]}}]
        ],
        "impending_doom": [
            [{"LOWER": {"IN": ["impending", "sense"]}}, {"OP": "*"}, {"LOWER": "doom"}],
            [{"LOWER": "panic"}, {"LOWER": "about"}, {"LOWER": "dying"}]
        ],
        "slurred_speech": [
            [{"LOWER": {"IN": ["slurred", "slurring"]}}, {"OP": "*"}, {"LOWER": {"IN": ["speech", "words", "talking"]}}]
        ]
    }
    
    for symptom_id, pattern_lists in symptom_patterns.items():
        for pat in pattern_lists:
            patterns.append({"label": "SYMPTOM", "pattern": pat, "id": symptom_id})

    ruler.add_patterns(patterns)

def extract_entities(text: str) -> dict:
    if not text:
        return {"foods": [], "symptoms": []}
        
    init_nlp()
    doc = nlp(text)
    
    foods = set()
    symptoms = set()
    
    for ent in doc.ents:
        if ent.ent_id_:
            if ent.label_ == "FOOD":
                foods.add(ent.ent_id_)
            elif ent.label_ == "SYMPTOM":
                symptoms.add(ent.ent_id_)
                
    return {
        "foods": list(foods),
        "symptoms": list(symptoms)
    }
