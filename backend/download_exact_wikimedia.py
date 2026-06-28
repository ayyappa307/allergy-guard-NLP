import os
import requests
import time
from urllib.parse import quote_plus
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

# Target folders
ALLERGENS_DIR = os.path.join(IMAGES_DIR, "allergens")
FOODS_DIR = os.path.join(IMAGES_DIR, "foods")
PATTERNS_DIR = os.path.join(IMAGES_DIR, "patterns")
SYMPTOMS_DIR = os.path.join(IMAGES_DIR, "symptoms")
MEDICINES_DIR = os.path.join(IMAGES_DIR, "medicines")

# Make sure directories exist
for d in [ALLERGENS_DIR, FOODS_DIR, PATTERNS_DIR, SYMPTOMS_DIR, MEDICINES_DIR]:
    os.makedirs(d, exist_ok=True)

HEADERS = {
    "User-Agent": "AllergyGuardAcademicAssistant/3.0 (academic; student@allergyguard.org)"
}

def generate_clinical_placeholder(name, target_path, category_name):
    """Generate a clean, beautiful clinical placeholder if no real image is found."""
    size = (400, 300)
    bg_color = (240, 248, 248) # Clean medical cyan tint
    text_color = (30, 80, 80)
    
    image = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Border
    draw.rectangle([(10, 10), (size[0]-10, size[1]-10)], outline=text_color, width=2)
    
    # Fonts
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        sub_font = ImageFont.truetype("arial.ttf", 12)
    except IOError:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        
    # Main text (name)
    try:
        bbox = draw.textbbox((0, 0), name, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        w, h = (200, 20)
        
    x = (size[0] - w) / 2
    y = (size[1] - h) / 2 - 10
    draw.text((x, y), name, fill=text_color, font=font)
    
    # Subtitle (category)
    sub_text = f"Clinical Reference: {category_name}"
    try:
        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        sw, sh = sub_bbox[2] - sub_bbox[0], sub_bbox[3] - sub_bbox[1]
    except AttributeError:
        sw, sh = (150, 10)
        
    sx = (size[0] - sw) / 2
    sy = y + h + 20
    draw.text((sx, sy), sub_text, fill=(100, 150, 150), font=sub_font)
    
    image.save(target_path)
    print(f"[Placeholder] Generated for: {name}", flush=True)

def search_wikimedia_file(keywords):
    """Search Wikimedia Commons for keywords and return the first matching File page title."""
    for kw in keywords:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={quote_plus(kw)}&srnamespace=6&format=json"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                data = r.json()
                results = data.get("query", {}).get("search", [])
                if results:
                    title = results[0]["title"]
                    lower_title = title.lower()
                    if any(lower_title.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
                        return title
            time.sleep(0.05)
        except Exception as e:
            print(f"Error searching for keyword '{kw}': {e}", flush=True)
    return None

def get_wikimedia_direct_url(file_title):
    """Get the direct upload URL for a Wikimedia File title."""
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={quote_plus(file_title)}&prop=imageinfo&iiprop=url&format=json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            data = r.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_info in pages.items():
                imageinfo = page_info.get("imageinfo", [])
                if imageinfo:
                    return imageinfo[0]["url"]
    except Exception as e:
        print(f"Error getting URL for '{file_title}': {e}", flush=True)
    return None

def download_image(url, target_path):
    """Download image to the target path."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            with open(target_path, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"Download exception for {url}: {e}", flush=True)
    return False

def process_single_item(item_id, search_terms, folder, category_label):
    """Workflow to download or generate placeholder for a single item."""
    target_path = os.path.join(folder, f"{item_id}.jpg")
    
    # 1. Search for file title
    file_title = search_wikimedia_file(search_terms)
    
    # 2. If found, get direct URL and download
    downloaded = False
    if file_title:
        direct_url = get_wikimedia_direct_url(file_title)
        if direct_url:
            downloaded = download_image(direct_url, target_path)
            if downloaded:
                print(f"[Success] Downloaded {item_id}.jpg from Wikimedia", flush=True)
                
    # 3. Fallback to placeholder if download failed or wasn't found
    if not downloaded:
        display_name = item_id.replace("_", " ").title()
        generate_clinical_placeholder(display_name, target_path, category_label)

# Definitions of search terms
ALLERGENS = {
    "peanuts": ["Peanut-whole-shelled.jpg", "peanuts", "arachis hypogaea"],
    "tree_nuts": ["Mixed nuts.jpg", "walnuts cashews almonds", "tree nuts"],
    "dairy": ["Milk glass.jpg", "dairy milk", "milk carton"],
    "gluten": ["Wheat flour close-up.jpg", "wheat flour", "gluten food"],
    "shellfish": ["Schalentiere.jpg", "raw shellfish", "crabs lobster clam"],
    "eggs": ["Egg up close.jpg", "chicken eggs", "boiled eggs"],
    "soy": ["Soybeans-02.jpg", "soybeans", "edamame"],
    "fish": ["Fish at a market.jpg", "raw fish", "fresh fish"],
    "wheat": ["Wheat close-up.jpg", "wheat ears", "wheat grains"],
    "corn": ["Corn on the cob.jpg", "sweetcorn", "maize cob"],
    "sulfites": ["Dried apricots.jpg", "dried fruit sulfites", "wine glass red"],
    "food_dyes": ["Food coloring red yellow blue green.jpg", "food coloring dye", "colored candies"],
    "msg_sensitivity": ["Monosodium glutamate crystals.jpg", "monosodium glutamate", "white seasoning crystals"],
    "latex_fruit": ["Avocado with stone.jpg", "avocado fruit", "latex fruit allergy"],
    "sesame_seeds_oil": ["Sesame seeds.jpg", "sesame seeds white", "sesame oil bottle"],
    "mustard_seeds_oil": ["Mustard seeds.jpg", "mustard seeds yellow", "mustard oil cooking"],
    "coconut": ["Coconut whole and partially sliced.jpg", "coconut fruit", "coconut fresh"],
    "curd_yogurt": ["Curds in bowl.jpg", "yogurt curd", "plain yogurt bowl"],
    "tamarind": ["Tamarind fruit.jpg", "tamarind pods", "tamarind sour"],
    "jaggery": ["Jaggery-powder.jpg", "jaggery blocks", "unrefined cane sugar"],
    "prawns_crustaceans": ["Cooked shrimp on ice.jpg", "shrimp prawns", "cooked prawns"],
    "black_gram": ["Urad dal white.jpg", "black gram split", "urad dal"],
    "green_gram": ["Mung bean seeds.jpg", "green gram moong", "mung beans"],
    "chili_capsaicin": ["Red chilis.jpg", "chili peppers red", "chilli capsicum"],
    "celery": ["Celery stalks.jpg", "celery root", "celery fresh"]
}

FOODS = {
    "pesarattu": ["Pesarattu.jpg", "pesarattu green gram crepe", "pesarattu dosa"],
    "upma_pesarattu": ["Pesarattu Upma 1.jpg", "pesarattu upma", "upma dosa"],
    "punugulu": ["Punugulu with chutney.jpg", "punugulu street food", "punugulu fritters"],
    "dibba_rottu": ["Minapa Rotti", "dibba rottu", "thick urad dal pancake"],
    "garelu": ["Garelu, a south indian snack.jpg", "medu vada", "garelu vada"],
    "mirapakaya_bajji": ["Mirchi Bajji.jpg", "mirchi bajji street food", "mirapakaya bajji"],
    "thapala_chekkalu": ["sarvapindi flatbread", "thapala chekkalu", "rice flour flatbread chekkalu"],
    "gunta_ponganalu": ["Paddu.JPG", "gunta ponganalu appe", "ponganalu south indian"],
    "hyderabadi_biryani": ["Hyderabadi Chicken Biryani.jpg", "hyderabadi biryani", "chicken biryani"],
    "kodi_pulao": ["chicken pulao indian style", "chicken biryani pulao", "kodi pulao"],
    "pulihora": ["Pulihora served in a leaf.jpg", "tamarind rice pulihora", "pulihora rice"],
    "ragi_sangati": ["Ragi Sangati, popular ragi ball.jpg", "ragi sangati mudde", "ragi ball"],
    "mudda_pappu": ["boiled yellow dal", "toor dal mudda pappu", "cooked lentils yellow"],
    "ulava_charu": ["horse gram soup", "ulava charu horse gram", "horsegram soup"],
    "pappu_charu": ["sambar lentil soup", "pappu charu rasam", "andhra pappu charu"],
    "pulagam": ["moong dal khichdi", "split green gram rice pulagam", "pongal khichdi"],
    "majjiga_pulusu": ["kadhi buttermilk curry", "majjiga pulusu charu", "buttermilk soup vegetables"],
    "gutti_vankaya_kura": ["Gutti Vankaya Koora.jpg", "stuffed brinjal curry gutti vankaya", "eggplant curry stuffed"],
    "panasa_puttu_koora": ["jackfruit curry raw", "kathal ki sabji raw jackfruit", "jackfruit grated koora"],
    "pulasa_pulusu": ["fish curry godavari style", "andhra pulasa fish curry", "hilsa fish curry tamarind"],
    "natu_kodi_pulusu": ["country chicken curry spicy", "spicy andhra chicken curry", "natu kodi curry"],
    "gongura_mutton": ["gongura mutton", "sorrel leaves mutton curry", "andhra lamb curry"],
    "avakaya_pachadi": ["Avakaya pickle.jpg", "avakaya mango pickle", "andhra mango pickle avakaya"],
    "gongura_pachadi": ["gongura pachadi pickle", "sorrel leaves chutney gongura", "gongura pickle"],
    "allam_pachadi": ["ginger pickle sweet sour", "allam pachadi ginger", "ginger chutney south indian"],
    "kandi_podi": ["roasted lentil powder", "kandi podi andhra", "gunpowder spice mix"],
    "pootharekulu": ["Pootharekulu.JPG", "atreyapuram pootharekulu", "paper sweet pootharekulu"],
    "poornam_boorelu": ["Poornalu.JPG", "poornam boorelu", "sweet boorelu dumplings"],
    "ariselu": ["Ariselu Sweet.jpg", "ariselu jaggery sweet", "adirasam sweet"],
    "spiced_majjiga": ["Buttermilk glass.jpg", "spiced buttermilk majjiga", "sambharam buttermilk"]
}

MEDICINES = {
    "otc_antihistamines": ["antihistamine pills box", "allergy tablets OTC", "cetirizine loratadine"],
    "otc_hydrocortisone": ["hydrocortisone cream tube", "topical steroid cream", "hydrocortisone ointment"],
    "otc_saline_rinse": ["saline nasal spray bottle", "nasal spray bottle", "saline nasal wash"],
    "rx_antihistamines": ["prescription allergy pills", "prescription medicine bottle", "fexofenadine prescription"],
    "rx_epinephrine": ["EpiPen.jpg", "epinephrine auto-injector", "epipen trainer auto-injector"],
    "rx_immunotherapy": ["allergy shots vials", "allergy immunotherapy drops", "sublingual immunotherapy"]
}

SYMPTOMS = {
    "hives_urticaria": ["Urticaria due to cold.jpg", "urticaria hives skin", "hives rash"],
    "localized_rash": ["Erythema multiforme.jpg", "skin rash localized", "eczema skin rash"],
    "itchy_skin": ["pruritus skin scratching", "itchy skin scratching", "dry itchy skin scratching"],
    "mild_swelling": ["Angioedema2010.jpg", "swollen lip angioedema", "facial swelling mild"],
    "sneezing": ["sneezing tissue allergy", "sneezing person", "sneeze allergy"],
    "runny_nose": ["blowing nose tissue", "runny nose cold", "allergic rhinitis nose"],
    "itchy_eyes": ["rubbing itchy eyes", "red watery eyes itchy", "allergic conjunctivitis eyes"],
    "stomach_cramps": ["stomach pain abdominal cramp", "stomach cramps holding stomach", "abdominal pain stomachache"],
    "nausea": ["feeling sick nausea", "nausea headache person", "sick stomach feeling"],
    "diarrhea": ["gastrointestinal sickness", "dehydration water cup", "stomach cramps pain"],
    "tongue_swelling": ["macroglossia swollen tongue", "swollen tongue", "allergic reaction tongue"],
    "metallic_taste": ["mouth tongue clinic", "tasting food close-up", "metallic taste tongue"],
    "excessive_salivation": ["drooling mouth saliva", "excessive salivation spit", "saliva mouth close-up"],
    "tingling_mouth": ["lips tingling itching", "tingling mouth burning", "lip burning sensation"],
    "cough": ["coughing person clinic", "coughing dry cough", "cough cold allergy"],
    "heartburn": ["heartburn chest pain indigestion", "acid reflux burning chest", "indigestion chest hold"],
    "diff_breathing": ["shortness of breath dyspnea", "difficulty breathing inhaler", "asthma difficulty breathing"],
    "wheezing": ["stethoscope chest lungs", "wheezing lung sound clinical", "asthma wheeze stethoscope"],
    "throat_tightness": ["throat pain sore throat holding neck", "throat swelling anaphylaxis", "choking sensation neck"],
    "diff_swallowing": ["dysphagia difficulty swallowing", "pain swallowing throat", "swallowing difficulty pain"],
    "skin_pallor": ["pale skin pale face", "skin pallor pale hands", "circulatory shock pale skin"],
    "confusion": ["confused senior disorientation", "confusion puzzled person", "brain fog confusion"],
    "dizziness": ["dizziness spinning head vertigo", "lightheadedness dizzy head", "unsteady dizzy holding head"],
    "fainting": ["fainting unconscious pass out", "syncope fainting person", "loss of consciousness floor"],
    "weak_pulse": ["checking pulse wrist", "weak thready pulse wrist", "pulse check clinical doctor"],
    "low_bp": ["blood pressure measurement monitor sphygmomanometer", "blood pressure check", "hypotension"],
    "severe_pain": ["severe pain screaming stomach", "debilitating pain stomach", "acute severe abdominal pain"],
    "persistent_vomiting": ["vomiting sick basin", "vomiting illness bathroom", "puke sick person"],
    "severe_diarrhea": ["intravenous fluid bag hospital", "iv drip hospital bag", "dehydration clinical therapy"],
    "blue_lips": ["cyanosis blue lips", "cyanosis skin lips blue", "lack of oxygen blue lips"],
    "chest_tightness": ["chest pain holding chest heart attack", "chest tightness pressure", "angina chest pain"],
    "hoarseness": ["throat sore holding neck hoarse", "laryngitis sore throat hoarse", "muffled voice throat pain"],
    "widespread_hives": ["widespread urticaria rash", "severe hives widespread body", "urticaria rash severe"],
    "impending_doom": ["panic attack breathing bag", "impending doom anxiety fear", "panic attack holding head"],
    "slurred_speech": ["stroke facial droop slurred speech", "slurred speech clinical check", "difficulty speaking neurological"]
}

PATTERNS = {
    "localized_urticaria": ["Urticaria due to cold.jpg", "urticaria hives skin", "hives localized"],
    "diffuse_redness": ["Erythema multiforme.jpg", "erythema rash redness", "diffuse redness skin"],
    "swelling": ["Angioedema2010.jpg", "angioedema lip swelling", "swelling face angioedema"],
    "inconclusive": ["Normal skin micrograph.jpg", "normal healthy skin", "healthy skin texture"]
}

if __name__ == "__main__":
    print("AllergyGuard Concurrently-Accelerated Wikimedia Asset Syncing Script starting...", flush=True)
    start_time = time.time()
    
    tasks = []
    
    # Queue up all processing tasks
    for item_id, search_terms in ALLERGENS.items():
        tasks.append((item_id, search_terms, ALLERGENS_DIR, "Allergens"))
        
    for item_id, search_terms in FOODS.items():
        tasks.append((item_id, search_terms, FOODS_DIR, "South Indian Dishes"))
        
    for item_id, search_terms in MEDICINES.items():
        tasks.append((item_id, search_terms, MEDICINES_DIR, "Medicines"))
        
    for item_id, search_terms in SYMPTOMS.items():
        tasks.append((item_id, search_terms, SYMPTOMS_DIR, "Symptoms"))
        
    for item_id, search_terms in PATTERNS.items():
        tasks.append((item_id, search_terms, PATTERNS_DIR, "Visual Patterns"))
        
    print(f"Total tasks scheduled: {len(tasks)}. Executing with ThreadPoolExecutor...", flush=True)
    
    # Run with 15 concurrent threads
    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {
            executor.submit(process_single_item, item_id, search_terms, folder, cat): (item_id, cat)
            for item_id, search_terms, folder, cat in tasks
        }
        
        for future in as_completed(futures):
            item_id, cat = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"[Error] Task failed for {item_id} in {cat}: {e}", flush=True)
                
    duration = time.time() - start_time
    print(f"\nAllergyGuard Concurrently-Accelerated Sync completed in {duration:.1f} seconds!", flush=True)
