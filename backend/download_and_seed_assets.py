import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Define directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
ALLERGENS_DIR = os.path.join(IMAGES_DIR, "allergens")
FOODS_DIR = os.path.join(IMAGES_DIR, "foods")
PATTERNS_DIR = os.path.join(IMAGES_DIR, "patterns")
SYMPTOMS_DIR = os.path.join(IMAGES_DIR, "symptoms")

# Create directories
for d in [STATIC_DIR, IMAGES_DIR, ALLERGENS_DIR, FOODS_DIR, PATTERNS_DIR, SYMPTOMS_DIR]:
    os.makedirs(d, exist_ok=True)

# User agent to prevent Wikimedia blocks
HEADERS = {'User-Agent': 'AllergyGuardAcademicProject/1.0 (academic; ayyap@example.com)'}

def download_image(url, target_path):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(target_path, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded: {os.path.basename(target_path)}")
        return True
    except Exception as e:
        print(f"Failed to download {url} -> {e}")
        return False

def generate_placeholder(name, target_path, size=(400, 300), bg_color=(230, 242, 242), text_color=(20, 80, 80)):
    # Create image with clean clinical calm background
    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Draw simple elegant border
    draw.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline=text_color, width=2)
    
    # Write text in the center
    # Fallback to default font
    try:
        # Try loading a common Windows font
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
        
    # Get text bounding box for centering
    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = draw.textsize(name, font=font) if hasattr(draw, "textsize") else (100, 20)
        
    # If font size is default, it might wrap poorly, let's keep it simple
    x = (size[0] - w) / 2
    y = (size[1] - h) / 2
    
    draw.text((x, y), name, fill=text_color, font=font)
    
    # Add a subtitle
    sub_text = "Academic Reference"
    try:
        sub_font = ImageFont.truetype("arial.ttf", 10)
    except IOError:
        sub_font = ImageFont.load_default()
        
    try:
        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        sw, sh = sub_bbox[2] - sub_bbox[0], sub_bbox[3] - sub_bbox[1]
    except AttributeError:
        sw, sh = draw.textsize(sub_text, font=sub_font) if hasattr(draw, "textsize") else (80, 10)
        
    sx = (size[0] - sw) / 2
    sy = y + h + 15
    draw.text((sx, sy), sub_text, fill=(120, 160, 160), font=sub_font)
    
    image.save(target_path)
    print(f"Generated placeholder for: {name}")

# Lists of image configurations
ALLERGENS = {
    "peanuts": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Peanut-whole-shelled.jpg",
    "tree_nuts": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Mixed_nuts.jpg",
    "dairy": "https://upload.wikimedia.org/wikipedia/commons/0/0e/Milk_glass.jpg",
    "gluten": "https://upload.wikimedia.org/wikipedia/commons/4/4b/Wheat_flour_close-up.jpg",
    "shellfish": "https://upload.wikimedia.org/wikipedia/commons/b/ba/Schalentiere.jpg",
    "eggs": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Egg_up_close.jpg",
    "soy": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Soybeans-02.jpg",
    "fish": "https://upload.wikimedia.org/wikipedia/commons/5/54/Fish_at_a_market.jpg",
    "wheat": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Wheat_close-up.jpg",
    "corn": "https://upload.wikimedia.org/wikipedia/commons/0/08/Corn_on_the_cob.jpg",
    "sulfites": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Sulfur-sample.jpg",
    "food_dyes": "https://upload.wikimedia.org/wikipedia/commons/8/82/Food_coloring_red_yellow_blue_green.jpg",
    "msg_sensitivity": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Monosodium_glutamate_crystals.jpg",
    "latex_fruit": "https://upload.wikimedia.org/wikipedia/commons/a/af/Avocado_with_stone.jpg",
    "sesame_seeds_oil": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Sesame_seeds.jpg",
    "mustard_seeds_oil": "https://upload.wikimedia.org/wikipedia/commons/8/87/Mustard_seeds.jpg",
    "coconut": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Coconut_whole_and_partially_sliced.jpg",
    "curd_yogurt": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Curds_in_bowl.jpg",
    "tamarind": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Tamarind_fruit.jpg",
    "jaggery": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Jaggery-powder.jpg",
    "prawns_crustaceans": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Cooked_shrimp_on_ice.jpg",
    "black_gram": "https://upload.wikimedia.org/wikipedia/commons/3/30/Urad_dal_white.jpg",
    "green_gram": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Mung_bean_seeds.jpg",
    "chili_capsaicin": "https://upload.wikimedia.org/wikipedia/commons/6/62/Red_chilis.jpg",
    "celery": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Celery_stalks.jpg"
}

PATTERNS = {
    "localized_urticaria": "https://upload.wikimedia.org/wikipedia/commons/e/eb/Urticaria_due_to_cold.jpg",
    "diffuse_redness": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Erythema_multiforme.jpg",
    "swelling": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Angioedema2010.jpg",
    "inconclusive": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Normal_skin_micrograph.jpg"
}

FOODS = {
    "pesarattu": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Pesarattu.jpg",
    "upma_pesarattu": "https://upload.wikimedia.org/wikipedia/commons/8/8e/Pesarattu_Upma_1.jpg",
    "punugulu": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Punugulu_with_chutney.jpg",
    "dibba_rottu": "", 
    "garelu": "https://upload.wikimedia.org/wikipedia/commons/6/61/Garelu%2C_a_south_indian_snack.jpg",
    "mirapakaya_bajji": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Mirchi_Bajji.jpg",
    "thapala_chekkalu": "",
    "gunta_ponganalu": "https://upload.wikimedia.org/wikipedia/commons/b/bd/Paddu.JPG",
    "hyderabadi_biryani": "https://upload.wikimedia.org/wikipedia/commons/c/cf/Hyderabadi_Chicken_Biryani.jpg",
    "kodi_pulao": "",
    "pulihora": "https://upload.wikimedia.org/wikipedia/commons/6/69/Pulihora_served_in_a_leaf.jpg",
    "ragi_sangati": "https://upload.wikimedia.org/wikipedia/commons/6/62/Ragi_Sangati%2C_popular_ragi_ball.jpg",
    "mudda_pappu": "",
    "ulava_charu": "",
    "pappu_charu": "",
    "pulagam": "",
    "majjiga_pulusu": "",
    "gutti_vankaya_kura": "https://upload.wikimedia.org/wikipedia/commons/7/77/Gutti_Vankaya_Koora.jpg",
    "panasa_puttu_koora": "",
    "pulasa_pulusu": "",
    "natu_kodi_pulusu": "",
    "gongura_mutton": "",
    "avakaya_pachadi": "https://upload.wikimedia.org/wikipedia/commons/1/11/Avakaya_pickle.jpg",
    "gongura_pachadi": "",
    "allam_pachadi": "",
    "kandi_podi": "",
    "pootharekulu": "https://upload.wikimedia.org/wikipedia/commons/0/05/Pootharekulu.JPG",
    "poornam_boorelu": "https://upload.wikimedia.org/wikipedia/commons/7/70/Poornalu.JPG",
    "ariselu": "https://upload.wikimedia.org/wikipedia/commons/4/45/Ariselu_Sweet.jpg",
    "spiced_majjiga": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Buttermilk_glass.jpg"
}

SYMPTOMS = {
    # Moderate
    "hives_urticaria": "Hives",
    "localized_rash": "Rash",
    "itchy_skin": "Itchy Skin",
    "mild_swelling": "Mild Swelling",
    "sneezing": "Sneezing",
    "runny_nose": "Runny Nose",
    "itchy_eyes": "Itchy Eyes",
    "stomach_cramps": "Stomach Cramps",
    "nausea": "Nausea",
    "diarrhea": "Diarrhea",
    "tongue_swelling": "Tongue Swelling",
    "metallic_taste": "Metallic Taste",
    "excessive_salivation": "Salivation",
    "tingling_mouth": "Tingling Mouth",
    "cough": "Cough",
    "heartburn": "Heartburn",
    # Severe
    "diff_breathing": "Dyspnea",
    "wheezing": "Wheezing",
    "throat_tightness": "Throat Tight",
    "diff_swallowing": "Dysphagia",
    "skin_pallor": "Skin Pallor",
    "confusion": "Confusion",
    "dizziness": "Dizziness",
    "fainting": "Fainting",
    "weak_pulse": "Weak Pulse",
    "low_bp": "Low BP",
    "severe_pain": "Severe Pain",
    "persistent_vomiting": "Vomiting",
    "severe_diarrhea": "Severe Diarrhea",
    "blue_lips": "Cyanosis",
    "chest_tightness": "Chest Tight",
    "hoarseness": "Hoarseness",
    "widespread_hives": "Body Hives",
    "impending_doom": "Impending Doom",
    "slurred_speech": "Slurred Speech"
}

def setup_assets():
    print("Setting up allergens...")
    for name, url in ALLERGENS.items():
        filename = f"{name}.jpg"
        filepath = os.path.join(ALLERGENS_DIR, filename)
        success = False
        if url:
            success = download_image(url, filepath)
        if not success:
            generate_placeholder(name.replace("_", " ").title(), filepath, size=(200, 200))
            
    print("\nSetting up patterns...")
    for name, url in PATTERNS.items():
        filename = f"{name}.jpg"
        filepath = os.path.join(PATTERNS_DIR, filename)
        success = False
        if url:
            success = download_image(url, filepath)
        if not success:
            generate_placeholder(name.replace("_", " ").title(), filepath, size=(400, 300), bg_color=(255, 235, 235), text_color=(120, 20, 20))

    print("\nSetting up foods...")
    for name, url in FOODS.items():
        filename = f"{name}.jpg"
        filepath = os.path.join(FOODS_DIR, filename)
        success = False
        if url:
            success = download_image(url, filepath)
        if not success:
            generate_placeholder(name.replace("_", " ").title(), filepath, size=(400, 300))

    print("\nSetting up symptoms...")
    for name, label in SYMPTOMS.items():
        filename = f"{name}.jpg"
        filepath = os.path.join(SYMPTOMS_DIR, filename)
        # For symptoms, we always generate custom distinct placeholders with appropriate warning colors
        # Moderate symptoms are light blue, severe are light red
        is_severe = name in [
            "diff_breathing", "wheezing", "throat_tightness", "diff_swallowing", "skin_pallor",
            "confusion", "dizziness", "fainting", "weak_pulse", "low_bp", "severe_pain",
            "persistent_vomiting", "severe_diarrhea", "blue_lips", "chest_tightness", "hoarseness",
            "widespread_hives", "impending_doom", "slurred_speech"
        ]
        bg = (255, 241, 242) if is_severe else (240, 249, 255)
        fg = (159, 18, 57) if is_severe else (3, 105, 161)
        generate_placeholder(label, filepath, size=(150, 150), bg_color=bg, text_color=fg)

if __name__ == "__main__":
    setup_assets()
    print("\nAsset setup complete!")
