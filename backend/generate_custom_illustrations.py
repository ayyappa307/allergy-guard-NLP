import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

# Directories
ALLERGENS_DIR = os.path.join(IMAGES_DIR, "allergens")
FOODS_DIR = os.path.join(IMAGES_DIR, "foods")
PATTERNS_DIR = os.path.join(IMAGES_DIR, "patterns")
SYMPTOMS_DIR = os.path.join(IMAGES_DIR, "symptoms")
MEDICINES_DIR = os.path.join(IMAGES_DIR, "medicines")

for d in [ALLERGENS_DIR, FOODS_DIR, PATTERNS_DIR, SYMPTOMS_DIR, MEDICINES_DIR]:
    os.makedirs(d, exist_ok=True)

def create_gradient_bg(size, color1, color2):
    """Creates a beautiful vertical gradient image."""
    base = Image.new("RGB", size, color1)
    top = Image.new("RGB", size, color2)
    mask = Image.new("L", size)
    for y in range(size[1]):
        # Vertical gradient mask
        level = int((y / size[1]) * 255)
        for x in range(size[0]):
            mask.putpixel((x, y), level)
    base.paste(top, (0, 0), mask)
    return base

def draw_capsule(draw, center, length, radius, color):
    """Draws a medicine capsule shape."""
    cx, cy = center
    # Left half circle
    draw.pieslice([cx - length//2 - radius, cy - radius, cx - length//2 + radius, cy + radius], 90, 270, fill=color)
    # Right half circle
    draw.pieslice([cx + length//2 - radius, cy - radius, cx + length//2 + radius, cy + radius], 270, 90, fill=color)
    # Middle rectangle
    draw.rectangle([cx - length//2, cy - radius, cx + length//2, cy + radius], fill=color)

def generate_allergen_illustration(name, filename):
    filepath = os.path.join(ALLERGENS_DIR, filename)
    size = (300, 300)
    
    # Custom illustration styling based on allergen
    if name == "peanuts":
        img = create_gradient_bg(size, (254, 243, 199), (217, 119, 6)) # Amber
        draw = ImageDraw.Draw(img)
        # Draw peanut shell silhouettes
        draw.ellipse([80, 110, 160, 190], fill=(245, 158, 11), outline=(180, 83, 9), width=2)
        draw.ellipse([140, 110, 220, 190], fill=(245, 158, 11), outline=(180, 83, 9), width=2)
        draw.rectangle([120, 125, 180, 175], fill=(245, 158, 11))
    elif name == "dairy":
        img = create_gradient_bg(size, (224, 242, 254), (14, 165, 233)) # Blue
        draw = ImageDraw.Draw(img)
        # Milk bottle
        draw.rectangle([120, 100, 180, 220], fill=(255, 255, 255), outline=(2, 132, 199), width=3)
        draw.rectangle([130, 70, 170, 100], fill=(255, 255, 255), outline=(2, 132, 199), width=3)
    elif name == "eggs":
        img = create_gradient_bg(size, (241, 245, 249), (203, 213, 225)) # Slate
        draw = ImageDraw.Draw(img)
        # Egg yolk
        draw.ellipse([80, 80, 220, 220], fill=(255, 255, 255))
        draw.ellipse([120, 120, 180, 180], fill=(249, 115, 22))
    elif name == "chili_capsaicin":
        img = create_gradient_bg(size, (254, 226, 226), (239, 68, 68)) # Red
        draw = ImageDraw.Draw(img)
        # Chili curve
        draw.polygon([(100, 200), (140, 220), (190, 170), (220, 100), (200, 80), (150, 130)], fill=(220, 38, 38))
        draw.line([(210, 90), (230, 70)], fill=(22, 163, 74), width=6) # stem
    else:
        # Default elegant generic abstract allergen
        img = create_gradient_bg(size, (244, 252, 252), (204, 238, 238))
        draw = ImageDraw.Draw(img)
        draw.ellipse([100, 100, 200, 200], fill=(20, 184, 166), outline=(13, 148, 136), width=3)
        draw.line([120, 120, 180, 180], fill=(255, 255, 255), width=6)
        
    # Standard EHR Label
    draw.rectangle([0, 260, 300, 300], fill=(15, 118, 110))
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
    draw.text((15, 270), name.replace("_", " ").upper(), fill=(255, 255, 255), font=font)
    img.save(filepath)

def generate_food_illustration(name, filename):
    filepath = os.path.join(FOODS_DIR, filename)
    size = (400, 300)
    
    # Custom colored plates for authentic Andhra foods
    if " pesarattu" in name or "pesarattu" in name:
        img = create_gradient_bg(size, (236, 253, 245), (167, 243, 208)) # Moong Green theme
        draw = ImageDraw.Draw(img)
        # Crepe fold
        draw.ellipse([80, 50, 320, 250], fill=(16, 185, 129), outline=(4, 120, 87), width=3)
        draw.polygon([(100, 150), (300, 100), (280, 200)], fill=(110, 231, 183))
    elif "biryani" in name or "pulao" in name:
        img = create_gradient_bg(size, (255, 251, 235), (254, 243, 199)) # Saffron theme
        draw = ImageDraw.Draw(img)
        # Biryani plate
        draw.ellipse([60, 40, 340, 260], fill=(217, 119, 6), outline=(146, 64, 14), width=4)
        draw.ellipse([80, 60, 320, 240], fill=(252, 211, 77))
        # Spiced grains
        draw.ellipse([140, 120, 160, 140], fill=(239, 68, 68))
        draw.ellipse([220, 150, 235, 165], fill=(22, 163, 74))
    elif "mutton" in name or "kodi" in name or "pulusu" in name:
        img = create_gradient_bg(size, (254, 242, 242), (254, 226, 226)) # Curry red theme
        draw = ImageDraw.Draw(img)
        # Clay pot bowl
        draw.ellipse([80, 60, 320, 240], fill=(185, 28, 28), outline=(153, 27, 27), width=4)
        draw.ellipse([100, 80, 300, 220], fill=(127, 29, 29))
    elif "sweet" in name or "boorelu" in name or "pootharekulu" in name or "ariselu" in name:
        img = create_gradient_bg(size, (255, 247, 237), (253, 237, 217)) # Sweet Jaggery theme
        draw = ImageDraw.Draw(img)
        # Sweet balls/sheets
        draw.ellipse([100, 100, 180, 180], fill=(251, 146, 60), outline=(234, 88, 12), width=3)
        draw.ellipse([200, 120, 270, 190], fill=(251, 146, 60), outline=(234, 88, 12), width=3)
    else:
        # Default nice Southern Plate
        img = create_gradient_bg(size, (248, 250, 252), (226, 232, 240))
        draw = ImageDraw.Draw(img)
        # Plate rim
        draw.ellipse([80, 30, 320, 270], fill=(255, 255, 255), outline=(148, 163, 184), width=3)
        draw.ellipse([100, 50, 300, 250], fill=(241, 245, 249))
        
    # Standard Label
    draw.rectangle([0, 250, 400, 300], fill=(15, 118, 110))
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()
    draw.text((20, 265), name.replace("_", " ").upper(), fill=(255, 255, 255), font=font)
    img.save(filepath)

def generate_medicine_illustration(name, filename):
    filepath = os.path.join(MEDICINES_DIR, filename)
    size = (300, 300)
    
    if "antihistamines" in name:
        img = create_gradient_bg(size, (240, 249, 255), (186, 230, 253)) # Light blue theme
        draw = ImageDraw.Draw(img)
        # Draw two capsule capsules
        draw_capsule(draw, (110, 150), 60, 20, (14, 165, 233)) # Blue capsule
        draw_capsule(draw, (190, 150), 60, 20, (239, 68, 68)) # Red capsule
    elif "hydrocortisone" in name:
        img = create_gradient_bg(size, (244, 252, 252), (204, 238, 238)) # Teal theme
        draw = ImageDraw.Draw(img)
        # Draw cream squeeze tube
        draw.polygon([(110, 220), (190, 220), (170, 80), (130, 80)], fill=(255, 255, 255), outline=(13, 148, 136), width=3)
        draw.rectangle([130, 70, 170, 80], fill=(13, 148, 136)) # tube cap
    elif "saline" in name:
        img = create_gradient_bg(size, (240, 253, 244), (187, 247, 208)) # Green theme
        draw = ImageDraw.Draw(img)
        # Nasal spray bottle
        draw.rectangle([120, 140, 180, 230], fill=(255, 255, 255), outline=(22, 163, 74), width=3) # bottle
        draw.rectangle([140, 100, 160, 140], fill=(255, 255, 255), outline=(22, 163, 74), width=3) # nozzle
        draw.rectangle([130, 90, 170, 100], fill=(22, 163, 74)) # spray wings
    elif "epinephrine" in name:
        img = create_gradient_bg(size, (255, 251, 235), (254, 243, 199)) # Amber emergency pen theme
        draw = ImageDraw.Draw(img)
        # Injector pen
        draw.rectangle([90, 130, 210, 170], fill=(245, 158, 11), outline=(180, 83, 9), width=3) # Body
        draw.rectangle([210, 135, 230, 165], fill=(220, 38, 38)) # Red safety release cap
        draw.rectangle([70, 140, 90, 160], fill=(30, 41, 59)) # needle end
    else:
        # Generic medicine bottle
        img = create_gradient_bg(size, (248, 250, 252), (226, 232, 240))
        draw = ImageDraw.Draw(img)
        draw.rectangle([110, 120, 190, 220], fill=(255, 255, 255), outline=(71, 85, 105), width=3)
        draw.rectangle([130, 90, 170, 120], fill=(71, 85, 105))
        
    # Standard EHR Label
    draw.rectangle([0, 260, 300, 300], fill=(15, 118, 110))
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except IOError:
        font = ImageFont.load_default()
    draw.text((15, 270), name.replace("_", " ").upper(), fill=(255, 255, 255), font=font)
    img.save(filepath)

def generate_all_illustrations():
    print("Generating custom vector-style allergen illustrations...")
    allergens = ["peanuts", "tree_nuts", "dairy", "gluten", "shellfish", "eggs", "soy", "fish", "wheat", "corn", 
                 "sulfites", "food_dyes", "msg_sensitivity", "latex_fruit", "sesame_seeds_oil", "mustard_seeds_oil", 
                 "coconut", "curd_yogurt", "tamarind", "jaggery", "prawns_crustaceans", "black_gram", "green_gram", 
                 "chili_capsaicin", "celery"]
    for a in allergens:
        generate_allergen_illustration(a, f"{a}.jpg")
        
    print("\nGenerating custom vector-style food illustrations...")
    foods = ["pesarattu", "upma_pesarattu", "punugulu", "dibba_rottu", "garelu", "mirapakaya_bajji", "thapala_chekkalu", 
             "gunta_ponganalu", "hyderabadi_biryani", "kodi_pulao", "pulihora", "ragi_sangati", "mudda_pappu", "ulava_charu", 
             "pappu_charu", "pulagam", "majjiga_pulusu", "gutti_vankaya_kura", "panasa_puttu_koora", "pulasa_pulusu", 
             "natu_kodi_pulusu", "gongura_mutton", "avakaya_pachadi", "gongura_pachadi", "allam_pachadi", "kandi_podi", 
             "pootharekulu", "poornam_boorelu", "ariselu", "spiced_majjiga"]
    for f in foods:
        generate_food_illustration(f, f"{f}.jpg")

    print("\nGenerating custom vector-style medicine illustrations...")
    medicines = ["otc_antihistamines", "otc_hydrocortisone", "otc_saline_rinse", "rx_antihistamines", "rx_epinephrine", "rx_immunotherapy"]
    for m in medicines:
        generate_medicine_illustration(m, f"{m}.jpg")

if __name__ == "__main__":
    generate_all_illustrations()
    print("\nIllustration asset generation complete!")
