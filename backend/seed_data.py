import os
import json
from db import DB_FILE, load_db, save_db

def seed():
    db = load_db()
    
    # 1. Seed Allergens (exactly 25)
    db["allergens"] = [
        {"id": "peanuts", "name": "Peanuts", "thumbnail_path": "/static/images/allergens/peanuts.jpg", 
         "description": "Legumes growing underground, distinct from tree nuts. Common trigger for severe anaphylaxis."},
        {"id": "tree_nuts", "name": "Tree Nuts", "thumbnail_path": "/static/images/allergens/tree_nuts.jpg", 
         "description": "Includes almonds, cashews, walnuts, pistachios. Often causes lifelong allergies."},
        {"id": "dairy", "name": "Dairy", "thumbnail_path": "/static/images/allergens/dairy.jpg", 
         "description": "Milk proteins (whey and casein). Common in children, can cause digestive and skin reactions."},
        {"id": "gluten", "name": "Gluten", "thumbnail_path": "/static/images/allergens/gluten.jpg", 
         "description": "Proteins found in wheat, barley, and rye. Trigger for celiac disease and wheat allergy."},
        {"id": "shellfish", "name": "Shellfish", "thumbnail_path": "/static/images/allergens/shellfish.jpg", 
         "description": "Includes crab, lobster, shrimp, clams, oysters. A common adult-onset allergy."},
        {"id": "eggs", "name": "Eggs", "thumbnail_path": "/static/images/allergens/eggs.jpg", 
         "description": "Ovalbumin and other egg white/yolk proteins. Widely used in baking and binding."},
        {"id": "soy", "name": "Soy", "thumbnail_path": "/static/images/allergens/soy.jpg", 
         "description": "Soybeans and derived products. Widely found in processed foods and sauces."},
        {"id": "fish", "name": "Fish", "thumbnail_path": "/static/images/allergens/fish.jpg", 
         "description": "Finned fish (e.g., salmon, tuna, cod). Often distinct from shellfish allergy."},
        {"id": "wheat", "name": "Wheat", "thumbnail_path": "/static/images/allergens/wheat.jpg", 
         "description": "A cereal grain containing gluten and other allergen proteins like amylase trypsin inhibitors."},
        {"id": "corn", "name": "Corn", "thumbnail_path": "/static/images/allergens/corn.jpg", 
         "description": "Maize and maize derivatives. Can cause reactions to corn starch, syrup, or oil."},
        {"id": "sulfites", "name": "Sulfites", "thumbnail_path": "/static/images/allergens/sulfites.jpg", 
         "description": "Preservatives used in dried fruits, wines, and processed foods. Can trigger asthma-like symptoms."},
        {"id": "food_dyes", "name": "Food Dyes", "thumbnail_path": "/static/images/allergens/food_dyes.jpg", 
         "description": "Artificial coloring agents (e.g., Tartrazine, Red 40). Associated with hives and asthma."},
        {"id": "msg_sensitivity", "name": "MSG Sensitivity", "thumbnail_path": "/static/images/allergens/msg_sensitivity.jpg", 
         "description": "Monosodium glutamate, a flavor enhancer. Can cause flushing, headaches, or sweating in sensitive individuals."},
        {"id": "latex_fruit", "name": "Latex-Fruit Cross-Reactivity", "thumbnail_path": "/static/images/allergens/latex_fruit.jpg", 
         "description": "Allergy to proteins in latex that cross-react with fruits like avocado, banana, kiwi, chestnut."},
        {"id": "sesame_seeds_oil", "name": "Sesame Seeds/Oil", "thumbnail_path": "/static/images/allergens/sesame_seeds_oil.jpg", 
         "description": "Common ingredient in tahini, breadings, and oils. Rising allergen globally."},
        {"id": "mustard_seeds_oil", "name": "Mustard Seeds/Oil", "thumbnail_path": "/static/images/allergens/mustard_seeds_oil.jpg", 
         "description": "Seeds and oils from the mustard plant. Frequently used in Indian pickles and cooking."},
        {"id": "coconut", "name": "Coconut", "thumbnail_path": "/static/images/allergens/coconut.jpg", 
         "description": "Fruit of the coconut palm. Classified as a tree nut by the US FDA, though botanically a drupe."},
        {"id": "curd_yogurt", "name": "Curd/Yogurt (Casein)", "thumbnail_path": "/static/images/allergens/curd_yogurt.jpg", 
         "description": "Fermented dairy rich in casein protein. Casein is heat-stable and survives fermentation."},
        {"id": "tamarind", "name": "Tamarind", "thumbnail_path": "/static/images/allergens/tamarind.jpg", 
         "description": "Sour pod fruit used for flavoring in South Asian cooking. Can cause rare systemic hypersensitivity."},
        {"id": "jaggery", "name": "Jaggery (Mold-related)", "thumbnail_path": "/static/images/allergens/jaggery.jpg", 
         "description": "Unrefined cane sugar. Can harbor mold spores during storage, causing reactions in mold-sensitive patients."},
        {"id": "prawns_crustaceans", "name": "Prawns/Crustaceans", "thumbnail_path": "/static/images/allergens/prawns_crustaceans.jpg", 
         "description": "Specific shrimp/prawn allergens (tropomyosin). Heavily featured in coastal Andhra cuisine."},
        {"id": "black_gram", "name": "Black Gram (Urad Dal)", "thumbnail_path": "/static/images/allergens/black_gram.jpg", 
         "description": "Legume widely used in South Indian batters (idli, dosa, vada). Can cause IgE-mediated reactions."},
        {"id": "green_gram", "name": "Green Gram (Moong/Pesara)", "thumbnail_path": "/static/images/allergens/green_gram.jpg", 
         "description": "Legume used to make Pesarattu. Cross-reactive with other legumes like peas and lentils."},
        {"id": "chili_capsaicin", "name": "Chili/Capsaicin (Irritant Flag)", "thumbnail_path": "/static/images/allergens/chili_capsaicin.jpg", 
         "description": "Capsaicin is a chemical irritant in hot peppers that triggers non-allergic oral burning, flushing, and digestive upset."},
        {"id": "celery", "name": "Celery", "thumbnail_path": "/static/images/allergens/celery.jpg", 
         "description": "Common root/stalk allergen in Europe, can cause severe reactions. Included for complete academic screening."}
    ]
    
    # 2. Seed Symptoms (exactly 35: 16 moderate, 19 severe-critical) with image paths
    db["symptoms"] = [
        # Moderate (16)
        {"id": "hives_urticaria", "name": "Hives / Urticaria", "severity": "Moderate", "image_path": "/static/images/symptoms/hives_urticaria.jpg", "description": "Raised, extremely itchy red bumps or welts on the skin."},
        {"id": "localized_rash", "name": "Localized Rash or Redness", "severity": "Moderate", "image_path": "/static/images/symptoms/localized_rash.jpg", "description": "Redness or minor rash localized to one area of the skin."},
        {"id": "itchy_skin", "name": "Itchy Skin (Pruritus)", "severity": "Moderate", "image_path": "/static/images/symptoms/itchy_skin.jpg", "description": "Generalized itching sensation without obvious rash or hives."},
        {"id": "mild_swelling", "name": "Mild Lip/Eyelid Swelling", "severity": "Moderate", "image_path": "/static/images/symptoms/mild_swelling.jpg", "description": "Subtle swelling of the lips, eyelids, or face (angioedema)."},
        {"id": "sneezing", "name": "Sneezing", "severity": "Moderate", "image_path": "/static/images/symptoms/sneezing.jpg", "description": "Repetitive, sudden sneezing fits shortly after exposure."},
        {"id": "runny_nose", "name": "Runny/Stuffy Nose (Rhinitis)", "severity": "Moderate", "image_path": "/static/images/symptoms/runny_nose.jpg", "description": "Nasal congestion or watery discharge from the nose."},
        {"id": "itchy_eyes", "name": "Itchy, Watery Eyes", "severity": "Moderate", "image_path": "/static/images/symptoms/itchy_eyes.jpg", "description": "Redness, itching, and excessive tearing of the eyes."},
        {"id": "stomach_cramps", "name": "Mild Abdominal Cramps", "severity": "Moderate", "image_path": "/static/images/symptoms/stomach_cramps.jpg", "description": "Minor stomach discomfort or cramping after eating."},
        {"id": "nausea", "name": "Nausea", "severity": "Moderate", "image_path": "/static/images/symptoms/nausea.jpg", "description": "Feeling sick to the stomach or inclined to vomit."},
        {"id": "diarrhea", "name": "Mild Diarrhea", "severity": "Moderate", "image_path": "/static/images/symptoms/diarrhea.jpg", "description": "Loose stools, occurring once or twice shortly after food consumption."},
        {"id": "tongue_swelling", "name": "Tongue Swelling (Mild/Localized)", "severity": "Moderate", "image_path": "/static/images/symptoms/tongue_swelling.jpg", "description": "Slight swelling or tingling of the tongue."},
        {"id": "metallic_taste", "name": "Metallic Taste in Mouth", "severity": "Moderate", "image_path": "/static/images/symptoms/metallic_taste.jpg", "description": "A distinct copper or metallic taste on the tongue, often an early sign."},
        {"id": "excessive_salivation", "name": "Excessive Salivation", "severity": "Moderate", "image_path": "/static/images/symptoms/excessive_salivation.jpg", "description": "Increased saliva production or drooling."},
        {"id": "tingling_mouth", "name": "Tingling or Itching in Mouth", "severity": "Moderate", "image_path": "/static/images/symptoms/tingling_mouth.jpg", "description": "Oral allergy syndrome (tingling of lips, palate, or throat)."},
        {"id": "cough", "name": "Cough (Dry/Occasional)", "severity": "Moderate", "image_path": "/static/images/symptoms/cough.jpg", "description": "A light, dry cough without wheezing or shortness of breath."},
        {"id": "heartburn", "name": "Heartburn / Acid Reflux", "severity": "Moderate", "image_path": "/static/images/symptoms/heartburn.jpg", "description": "Burning sensation in the chest or throat due to irritants/spices."},

        # Severe-Critical (19)
        {"id": "diff_breathing", "name": "Difficulty Breathing", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/diff_breathing.jpg", "description": "Shortness of breath, chest tightness, or gasping for air."},
        {"id": "wheezing", "name": "Wheezing / Stridor", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/wheezing.jpg", "description": "Whistling or high-pitched sound during breathing, indicating airway constriction."},
        {"id": "throat_tightness", "name": "Throat Swelling / Tightness", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/throat_tightness.jpg", "description": "Feeling like the throat is closing up, voice sounds muffled."},
        {"id": "diff_swallowing", "name": "Difficulty Swallowing", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/diff_swallowing.jpg", "description": "Inability or pain when attempting to swallow liquids or food."},
        {"id": "skin_pallor", "name": "Skin Pallor / Sudden Paleness", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/skin_pallor.jpg", "description": "Sudden loss of color in the face/body, indicating circulatory compromise."},
        {"id": "confusion", "name": "Confusion / Disorientation", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/confusion.jpg", "description": "Inability to think clearly, memory gaps, or confusion."},
        {"id": "dizziness", "name": "Dizziness / Lightheadedness", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/dizziness.jpg", "description": "Feeling unsteady, faint, or spinny, indicating low blood pressure."},
        {"id": "fainting", "name": "Loss of Consciousness / Fainting", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/fainting.jpg", "description": "Passing out or falling unconscious due to systemic shock (anaphylaxis)."},
        {"id": "weak_pulse", "name": "Weak or Rapid Pulse", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/weak_pulse.jpg", "description": "A thready, fast, or barely palpable heartbeat."},
        {"id": "low_bp", "name": "Drop in Blood Pressure", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/low_bp.jpg", "description": "Severe hypotension causing extreme weakness or syncope."},
        {"id": "severe_pain", "name": "Severe Abdominal Pain", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/severe_pain.jpg", "description": "Intense, debilitating abdominal cramps or sharp pains."},
        {"id": "persistent_vomiting", "name": "Persistent Vomiting", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/persistent_vomiting.jpg", "description": "Continuous, uncontrollable vomiting shortly after ingestion."},
        {"id": "severe_diarrhea", "name": "Severe Watery Diarrhea", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/severe_diarrhea.jpg", "description": "Frequent, heavy watery stools indicating systemic GI reaction."},
        {"id": "blue_lips", "name": "Blueness of Lips or Skin", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/blue_lips.jpg", "description": "Cyanosis, indicating severe lack of oxygen in the blood."},
        {"id": "chest_tightness", "name": "Chest Pain or Tightness", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/chest_tightness.jpg", "description": "Pressure, squeezing, or pain in the chest area."},
        {"id": "hoarseness", "name": "Hoarseness / Muffled Voice", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/hoarseness.jpg", "description": "Sudden voice change, indicating swelling around vocal cords."},
        {"id": "widespread_hives", "name": "Widespread Hives & Swelling", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/widespread_hives.jpg", "description": "Hives covering large areas of the body, accompanied by severe swelling."},
        {"id": "impending_doom", "name": "Feeling of Impending Doom", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/impending_doom.jpg", "description": "An intense sensation of anxiety, panic, or fear that something fatal is happening."},
        {"id": "slurred_speech", "name": "Slurred Speech", "severity": "Severe-Critical", "image_path": "/static/images/symptoms/slurred_speech.jpg", "description": "Difficulty speaking clearly or articulating words, indicating neurological impact."}
    ]
    
    # 3. Seed Foods (30 Andhra/Telangana dishes)
    db["foods"] = [
        {"id": "pesarattu", "name": "Green Gram Crepe (Pesarattu)", "image_path": "/static/images/foods/pesarattu.jpg", 
         "description": "Healthy crepe made of green gram (moong dal) batter, ginger, and green chilies.",
         "ingredients": ["green gram", "ginger", "green chili", "cumin", "rice flour", "refined oil"],
         "allergens": ["green_gram", "chili_capsaicin"], 
         "alternatives": ["Rice Crepe (Rava Dosa - wheat-free option)", "Millets Dosa"]},
         
        {"id": "upma_pesarattu", "name": "Semolina Green Gram Crepe (Upma Pesarattu)", "image_path": "/static/images/foods/upma_pesarattu.jpg", 
         "description": "Green gram crepe stuffed with semolina (upma), roasted cashews, and ghee.",
         "ingredients": ["green gram", "semolina (wheat)", "cashews", "ghee (milk fat)", "ginger", "green chili", "mustard seeds"],
         "allergens": ["green_gram", "gluten", "wheat", "tree_nuts", "dairy", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Plain Pesarattu (ghee-free/wheat-free)", "Quinoa Upma Crepe"]},
         
        {"id": "punugulu", "name": "Fried Rice-Lentil Dumplings (Punugulu)", "image_path": "/static/images/foods/punugulu.jpg", 
         "description": "Deep-fried snack bites made from fermented rice and urad dal batter.",
         "ingredients": ["rice", "black gram (urad dal)", "chili", "onion", "wheat flour (for binding)", "peanut oil for frying"],
         "allergens": ["black_gram", "chili_capsaicin", "gluten", "wheat", "peanuts"],
         "alternatives": ["Steamed Idli Bites", "Baked Rice Crackers"]},
         
        {"id": "dibba_rottu", "name": "Thick Lentil Pancake (Dibba Rottu / Minapa Rotti)", "image_path": "/static/images/foods/dibba_rottu.jpg", 
         "description": "Thick, crispy South Indian pancake made of urad dal and rice rava.",
         "ingredients": ["black gram (urad dal)", "rice rava", "cumin", "ginger", "oil"],
         "allergens": ["black_gram"],
         "alternatives": ["Brown Rice Dosa", "Sorgo/Jowar Rotti"]},
         
        {"id": "garelu", "name": "Fried Lentil Donuts (Garelu)", "image_path": "/static/images/foods/garelu.jpg", 
         "description": "Savory fried donuts made from black gram (urad dal) batter, pepper, and ginger.",
         "ingredients": ["black gram (urad dal)", "onion", "ginger", "green chili", "black pepper", "peanut oil"],
         "allergens": ["black_gram", "chili_capsaicin", "peanuts"],
         "alternatives": ["Baked Lentil Patties", "Steamed Kudumulu"]},
         
        {"id": "mirapakaya_bajji", "name": "Chili Fritters (Mirapakaya Bajji)", "image_path": "/static/images/foods/mirapakaya_bajji.jpg", 
         "description": "Spicy green chili fritters stuffed with tamarind pulp and carom seeds, fried in chickpea batter.",
         "ingredients": ["banana pepper (green chili)", "chickpea flour", "tamarind pulp", "carom seeds", "peanut oil"],
         "allergens": ["chili_capsaicin", "tamarind", "peanuts"],
         "alternatives": ["Aloo Bajji (potato-based, mild chili)", "Stuffed Baked Capsicum"]},
         
        {"id": "thapala_chekkalu", "name": "Rice Crackers (Thapala Chekkalu)", "image_path": "/static/images/foods/thapala_chekkalu.jpg", 
         "description": "Crispy flattened rice-flour crackers containing peanuts, chana dal, and spices.",
         "ingredients": ["rice flour", "peanuts", "chana dal", "onion", "green chilies", "sesame seeds", "ghee"],
         "allergens": ["peanuts", "sesame_seeds_oil", "dairy", "chili_capsaicin"],
         "alternatives": ["Plain Baked Rice Crackers", "Roasted Chana Patties"]},
         
        {"id": "gunta_ponganalu", "name": "Pan-fried Rice-Lentil Dumplings (Gunta Ponganalu)", "image_path": "/static/images/foods/gunta_ponganalu.jpg", 
         "description": "Dumplings cooked in a special pan with holes, made of fermented rice-urad batter.",
         "ingredients": ["rice", "black gram (urad dal)", "onion", "mustard seeds", "green chili", "curry leaves"],
         "allergens": ["black_gram", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Steamed Idli", "Vegetable Oats Ponganalu"]},
         
        {"id": "hyderabadi_biryani", "name": "Hyderabadi Biryani", "image_path": "/static/images/foods/hyderabadi_biryani.jpg", 
         "description": "World-famous royal dish of basmati rice, meat marinated in yogurt and spices, cooked on slow heat (dum).",
         "ingredients": ["basmati rice", "mutton or chicken", "yogurt (curd)", "ghee", "onions", "saffron", "cashew paste", "spices"],
         "allergens": ["curd_yogurt", "dairy", "tree_nuts"],
         "alternatives": ["Pulao (ghee-free/yogurt-free)", "Plain Saffron Basmati Rice"]},
         
        {"id": "kodi_pulao", "name": "Chicken Pulao (Kodi Pulao)", "image_path": "/static/images/foods/kodi_pulao.jpg", 
         "description": "Spicy chicken and rice dish cooked with coconut milk and rich spices.",
         "ingredients": ["basmati rice", "chicken", "coconut milk", "ghee", "green chilies", "poppy seeds", "spices"],
         "allergens": ["coconut", "dairy", "chili_capsaicin"],
         "alternatives": ["Steamed Rice with Mild Chicken Curry", "Vegetable Pulao (coconut-free)"]},
         
        {"id": "pulihora", "name": "Tamarind Rice (Pulihora)", "image_path": "/static/images/foods/pulihora.jpg", 
         "description": "Tangy tamarind rice seasoned with mustard seeds, curry leaves, and roasted peanuts.",
         "ingredients": ["rice", "tamarind pulp", "peanuts", "mustard seeds", "turmeric", "sesame oil", "green chilies"],
         "allergens": ["tamarind", "peanuts", "mustard_seeds_oil", "sesame_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Lemon Rice (peanut-free)", "Coconut Rice (tamarind/peanut-free)"]},
         
        {"id": "ragi_sangati", "name": "Finger Millet Balls (Ragi Sangati)", "image_path": "/static/images/foods/ragi_sangati.jpg", 
         "description": "Nutritious balls made of finger millet (ragi) flour and cooked rice, traditionally eaten with ghee.",
         "ingredients": ["finger millet (ragi)", "rice", "water", "ghee (for serving)"],
         "allergens": ["dairy"],
         "alternatives": ["Plain Steamed Rice", "Quinoa Mash"]},
         
        {"id": "mudda_pappu", "name": "Boiled Yellow Lentils (Mudda Pappu)", "image_path": "/static/images/foods/mudda_pappu.jpg", 
         "description": "Thick, creamy plain boiled yellow pigeon peas (toor dal) served with hot rice and ghee.",
         "ingredients": ["toor dal", "water", "turmeric", "salt", "ghee"],
         "allergens": ["dairy"],
         "alternatives": ["Moong Dal (ghee-free)", "Steamed lentils with olive oil"]},
         
        {"id": "ulava_charu", "name": "Horse Gram Soup (Ulava Charu)", "image_path": "/static/images/foods/ulava_charu.jpg", 
         "description": "Traditional thick horse gram soup, highly spiced, served with fresh cream.",
         "ingredients": ["horse gram", "tamarind", "cream (milk product)", "ghee", "mustard seeds", "green chilies"],
         "allergens": ["tamarind", "dairy", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Pappu Charu (cream-free)", "Tomato Rasam"]},
         
        {"id": "pappu_charu", "name": "Lentil Vegetable Soup (Pappu Charu)", "image_path": "/static/images/foods/pappu_charu.jpg", 
         "description": "Comforting lentil soup with mixed vegetables, tamarind, and tempering.",
         "ingredients": ["toor dal", "mixed vegetables", "tamarind pulp", "green chilies", "mustard seeds", "turmeric"],
         "allergens": ["tamarind", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Tomato Rasam (tamarind-free)", "Simple Moong Dal soup"]},
         
        {"id": "pulagam", "name": "Rice & Yellow Moong Dal Porridge (Pulagam)", "image_path": "/static/images/foods/pulagam.jpg", 
         "description": "One-pot dish made of rice and split yellow moong dal, offered as a temple prasadam.",
         "ingredients": ["rice", "split yellow moong dal", "black pepper", "cumin", "ghee"],
         "allergens": ["green_gram", "dairy"],
         "alternatives": ["Simple Boiled Rice", "Peppery Oats Khichdi (lentil-free)"]},
         
        {"id": "majjiga_pulusu", "name": "Tempered Buttermilk Stew (Majjiga Pulusu / Charu)", "image_path": "/static/images/foods/majjiga_pulusu.jpg", 
         "description": "Buttermilk-based soup containing vegetables, thickened with chickpea flour and tempered.",
         "ingredients": ["curd (yogurt)", "chickpea flour", "bottle gourd", "turmeric", "mustard seeds", "fenugreek", "ginger", "chilies"],
         "allergens": ["curd_yogurt", "dairy", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Vegetable Clear Soup", "Tomato Rasam"]},
         
        {"id": "gutti_vankaya_kura", "name": "Stuffed Eggplant Curry (Gutti Vankaya Kura)", "image_path": "/static/images/foods/gutti_vankaya_kura.jpg", 
         "description": "Stuffed eggplant curry with a rich paste of peanuts, sesame seeds, coconut, and tamarind.",
         "ingredients": ["eggplant", "peanuts", "sesame seeds", "grated coconut", "tamarind pulp", "coriander seeds", "mustard seeds", "peanut oil"],
         "allergens": ["peanuts", "sesame_seeds_oil", "coconut", "tamarind", "mustard_seeds_oil"],
         "alternatives": ["Aloo Gobi (potato-cauliflower)", "Plain Roasted Eggplant"]},
         
        {"id": "panasa_puttu_koora", "name": "Grated Jackfruit Curry (Panasa Puttu Koora)", "image_path": "/static/images/foods/panasa_puttu_koora.jpg", 
         "description": "Unique grated raw jackfruit curry cooked with a sharp mustard paste.",
         "ingredients": ["raw jackfruit", "mustard paste (mustard oil/seeds)", "chana dal", "urad dal", "green chilies", "coconut oil"],
         "allergens": ["mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Stir-fried Raw Banana", "Mushroom Curry"]},
         
        {"id": "pulasa_pulusu", "name": "River Hilsa Fish Curry (Pulasa Pulusu)", "image_path": "/static/images/foods/pulasa_pulusu.jpg", 
         "description": "Highly prized fish curry made with River Godavari Pulasa fish, okra, tamarind, and spicy chilies.",
         "ingredients": ["Pulasa fish", "tamarind pulp", "okra (bhendi)", "green chilies", "mustard oil", "turmeric", "chili powder"],
         "allergens": ["fish", "tamarind", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Okra Tamarind Curry (vegan/fish-free)", "Tomato Pepper Soup"]},
         
        {"id": "natu_kodi_pulusu", "name": "Country Chicken Curry (Natu Kodi Pulusu)", "image_path": "/static/images/foods/natu_kodi_pulusu.jpg", 
         "description": "Spicy, country-style chicken curry loaded with capsaicin and poppy/sesame seeds.",
         "ingredients": ["country chicken", "red chili powder", "sesame seeds", "ginger-garlic", "coriander seeds", "mustard oil"],
         "allergens": ["chili_capsaicin", "sesame_seeds_oil", "mustard_seeds_oil"],
         "alternatives": ["Mild Chicken Stew (broth-based)", "Grilled Chicken breast"]},
         
        {"id": "gongura_mutton", "name": "Sorrel Leaves Mutton Curry (Gongura Mutton)", "image_path": "/static/images/foods/gongura_mutton.jpg", 
         "description": "Mutton cooked with sour sorrel leaves (gongura), spices, and peanut oil.",
         "ingredients": ["mutton", "gongura leaves", "onions", "green chilies", "ginger-garlic", "peanut oil", "spices"],
         "allergens": ["peanuts", "chili_capsaicin"],
         "alternatives": ["Plain Mutton Curry (non-sour)", "Herb Roasted Lamb"]},
         
        {"id": "avakaya_pachadi", "name": "Spicy Mango Pickle (Avakaya Pachadi)", "image_path": "/static/images/foods/avakaya_pachadi.jpg", 
         "description": "Spicy Andhra mango pickle prepared with mustard powder and sesame oil.",
         "ingredients": ["raw mango", "mustard powder", "red chili powder", "sesame oil", "salt", "fenugreek seeds"],
         "allergens": ["mustard_seeds_oil", "sesame_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Sweet Mango Chutney (mustard-free)", "Lime Pickle (oil-free)"]},
         
        {"id": "gongura_pachadi", "name": "Sorrel Leaves Chutney (Gongura Pachadi)", "image_path": "/static/images/foods/gongura_pachadi.jpg", 
         "description": "Tangy pickle made from sorrel leaves, green chilies, and sesame oil.",
         "ingredients": ["gongura leaves", "green chilies", "sesame oil", "garlic", "cumin", "salt"],
         "allergens": ["sesame_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Mint Coriander Chutney", "Yogurt Raita"]},
         
        {"id": "allam_pachadi", "name": "Ginger Pickle (Allam Pachadi)", "image_path": "/static/images/foods/allam_pachadi.jpg", 
         "description": "Spicy and sweet ginger pickle prepared with tamarind and jaggery.",
         "ingredients": ["ginger", "tamarind pulp", "jaggery", "red chilies", "sesame oil", "mustard seeds"],
         "allergens": ["tamarind", "jaggery", "sesame_seeds_oil", "mustard_seeds_oil", "chili_capsaicin"],
         "alternatives": ["Coconut Ginger Chutney (sugar-based)", "Fresh Ginger Garlic relish"]},
         
        {"id": "kandi_podi", "name": "Roasted Lentil Powder (Kandi Podi)", "image_path": "/static/images/foods/kandi_podi.jpg", 
         "description": "Roasted lentil powder (toor dal, chana dal) mixed with cumin and dry chilies, eaten with ghee.",
         "ingredients": ["toor dal", "chana dal", "dry red chilies", "cumin", "salt", "ghee (for serving)"],
         "allergens": ["dairy", "chili_capsaicin"],
         "alternatives": ["Sesame Podi (ghee-free)", "Roasted Garlic powder"]},
         
        {"id": "pootharekulu", "name": "Paper Sweet (Pootharekulu)", "image_path": "/static/images/foods/pootharekulu.jpg", 
         "description": "Delectable wafer-like paper sweet from Atreyapuram, made of rice starch sheets, sugar/jaggery, ghee, and cashews.",
         "ingredients": ["rice starch", "jaggery", "sugar", "ghee", "cashews", "almonds"],
         "allergens": ["jaggery", "dairy", "tree_nuts"],
         "alternatives": ["Rice Flour Phirni (nut-free)", "Dry Fruit-free Laddu (made with sugar & oil)"]},
         
        {"id": "poornam_boorelu", "name": "Sweet Stuffed Dumplings (Poornam Boorelu)", "image_path": "/static/images/foods/poornam_boorelu.jpg", 
         "description": "Deep-fried sweet dumplings stuffed with sweet chana dal, jaggery, and coconut, coated in urad dal batter.",
         "ingredients": ["chana dal", "jaggery", "fresh coconut", "black gram (urad dal)", "rice flour", "cardamom", "peanut oil"],
         "allergens": ["jaggery", "coconut", "black_gram", "peanuts"],
         "alternatives": ["Steamed Poornam Kudumulu (oil-free)", "Rice Payasam (coconut-free)"]},
         
        {"id": "ariselu", "name": "Sweet Rice-Jaggery Cakes (Ariselu)", "image_path": "/static/images/foods/ariselu.jpg", 
         "description": "Traditional deep-fried sweet made from rice flour, melted jaggery, and sesame seeds.",
         "ingredients": ["rice flour", "jaggery", "sesame seeds", "ghee", "peanut oil"],
         "allergens": ["jaggery", "sesame_seeds_oil", "dairy", "peanuts"],
         "alternatives": ["Rava Kesari (semolina based, sesame-free)", "Rice Payasam"]},
         
        {"id": "spiced_majjiga", "name": "Spiced Buttermilk (Spiced Majjiga)", "image_path": "/static/images/foods/spiced_majjiga.jpg", 
         "description": "Refreshing buttermilk spiced with ginger, curry leaves, green chilies, and coriander.",
         "ingredients": ["curd (yogurt)", "water", "ginger", "green chili", "coriander leaves", "salt"],
         "allergens": ["curd_yogurt", "dairy", "chili_capsaicin"],
         "alternatives": ["Coconut Water", "Lemon Water with salt and ginger"]}
    ]
    
    db["medicines"] = [
        # Stage A: OTC Categories
        {"id": "otc_antihistamines", "stage": "A", "category": "Oral Antihistamines", 
         "image_path": "/static/images/medicines/otc_antihistamines.jpg",
         "description": "A class of over-the-counter medications that block histamine receptors. Typically used to relieve itching, hives, sneezing, and runny nose.",
         "warning": "Consult a healthcare provider before use. May cause drowsiness depending on the formulation.",
         "mapped_allergens": ["peanuts", "tree_nuts", "dairy", "gluten", "shellfish", "eggs", "soy", "fish", "wheat", "corn", "sesame_seeds_oil", "coconut", "curd_yogurt", "prawns_crustaceans", "black_gram", "green_gram", "celery"]},
         
        {"id": "otc_hydrocortisone", "stage": "A", "category": "Topical Hydrocortisone Cream", 
         "image_path": "/static/images/medicines/otc_hydrocortisone.jpg",
         "description": "A mild over-the-counter corticosteroid ointment applied directly to the skin. Used to reduce swelling, redness, and intense itching of localized contact rashes.",
         "warning": "For external skin use only. Do not apply to open wounds or near the eyes.",
         "mapped_allergens": ["mustard_seeds_oil", "latex_fruit", "chili_capsaicin", "food_dyes"]},
         
        {"id": "otc_saline_rinse", "stage": "A", "category": "Saline Nasal Rinse / Spray", 
         "image_path": "/static/images/medicines/otc_saline_rinse.jpg",
         "description": "A simple over-the-counter sterile salt water spray used to flush allergens, dust, and excess mucus out of the nasal passages. Relieves rhinitis symptoms.",
         "warning": "Use distilled or sterile water if mixing rinses manually. Follow bottle directions.",
         "mapped_allergens": ["sulfites", "celery", "msg_sensitivity"]},

        # Stage B: Post-Diagnosis Clinical Pathways (Educational Only)
        {"id": "rx_antihistamines", "stage": "B", "category": "Prescription-strength Antihistamines", 
         "image_path": "/static/images/medicines/rx_antihistamines.jpg",
         "description": "High-potency, non-sedating histamine blockers prescribed by a doctor for long-term daily management of chronic allergic symptoms.",
         "warning": "Available only by prescription. A doctor determines if this is suitable based on clinical testing.",
         "mapped_allergens": ["peanuts", "tree_nuts", "dairy", "gluten", "shellfish", "eggs", "soy", "fish", "wheat", "corn", "sesame_seeds_oil", "coconut", "curd_yogurt", "prawns_crustaceans", "black_gram", "green_gram", "celery"]},
         
        {"id": "rx_epinephrine", "stage": "B", "category": "Epinephrine Auto-injector", 
         "image_path": "/static/images/medicines/rx_epinephrine.jpg",
         "description": "A portable emergency injection device containing epinephrine (adrenaline). It rapidly reverses severe airway obstruction, throat swelling, and drop in blood pressure during anaphylaxis.",
         "warning": "Prescribed to individuals with confirmed severe allergies. Must be carried at all times and administered immediately during a severe reaction before calling emergency services.",
         "mapped_allergens": ["peanuts", "tree_nuts", "shellfish", "eggs", "fish", "prawns_crustaceans", "black_gram", "green_gram", "sesame_seeds_oil", "dairy", "latex_fruit"]},
         
        {"id": "rx_immunotherapy", "stage": "B", "category": "Allergen Immunotherapy (AIT)", 
         "image_path": "/static/images/medicines/rx_immunotherapy.jpg",
         "description": "A long-term treatment (allergy shots or sublingual drops/tablets) administered under medical supervision to desensitize the immune system to specific allergens.",
         "warning": "Requires formal allergy diagnosis (e.g. skin prick testing) and is conducted over 3-5 years under close clinical observation.",
         "mapped_allergens": ["peanuts", "tree_nuts", "eggs", "dairy", "wheat", "celery"]}
    ]
    
    # Save seed data to file
    save_db(db)
    print("Seed data successfully populated in local_db.json!")

if __name__ == "__main__":
    seed()
