import os
from PIL import Image

def analyze_skin_reaction(image_path: str) -> dict:
    """
    Lightweight image analysis using Pillow to assess visual patterns in skin reaction photos.
    This is an academic classifier, not a medical diagnosis.
    
    Returns:
        dict: {
            "label": "localized urticaria" | "diffuse redness" | "swelling" | "inconclusive",
            "confidence": float (0.0 to 1.0),
            "disclaimer": str,
            "metrics": dict
        }
    """
    DISCLAIMER = "Academic project reference pattern match only. This is not a clinical diagnosis or medical device."
    
    if not os.path.exists(image_path):
        return {
            "label": "inconclusive",
            "confidence": 0.5,
            "disclaimer": DISCLAIMER,
            "metrics": {"error": "Image file not found"}
        }
        
    try:
        with Image.open(image_path) as img:
            # Convert to RGB and resize for speed
            img = img.convert("RGB")
            img = img.resize((100, 100))
            
            # Extract pixels
            pixels = list(img.getdata())
            total_pixels = len(pixels)
            
            # Analyze redness: R > 1.2 * G and R > 1.2 * B
            red_pixels = 0
            high_red_pixels = 0
            sum_r, sum_g, sum_b = 0, 0, 0
            
            # We also track coordinates to check for localization (clustering)
            red_coords = []
            
            for idx, (r, g, b) in enumerate(pixels):
                sum_r += r
                sum_g += g
                sum_b += b
                
                # Check for redness threshold
                if r > 100 and r > (g * 1.25) and r > (b * 1.25):
                    red_pixels += 1
                    y = idx // 100
                    x = idx % 100
                    red_coords.append((x, y))
                    if r > 160:
                        high_red_pixels += 1
                        
            # Ratios
            red_ratio = red_pixels / total_pixels
            high_red_ratio = high_red_pixels / total_pixels
            avg_r = sum_r / total_pixels
            avg_g = sum_g / total_pixels
            avg_b = sum_b / total_pixels
            
            # Compute standard deviation of coordinates to detect patchiness (localization)
            # If red pixels are concentrated in specific areas (patches) -> Localized Urticaria
            # If red pixels are spread uniformly across the image -> Diffuse Redness
            is_localized = False
            if len(red_coords) > 100:
                mean_x = sum(pt[0] for pt in red_coords) / len(red_coords)
                mean_y = sum(pt[1] for pt in red_coords) / len(red_coords)
                var_x = sum((pt[0] - mean_x) ** 2 for pt in red_coords) / len(red_coords)
                var_y = sum((pt[1] - mean_y) ** 2 for pt in red_coords) / len(red_coords)
                std_dev = (var_x + var_y) ** 0.5
                # High standard deviation relative to count means spread out, low means concentrated
                # But standard deviation of completely random coordinates on 100x100 is around 40
                if std_dev < 30:
                    is_localized = True
            
            # Classification Logic
            if red_ratio > 0.4:
                # High amount of red pixels
                if is_localized:
                    label = "localized urticaria"
                    confidence = min(0.65 + (red_ratio * 0.3), 0.95)
                else:
                    label = "diffuse redness"
                    confidence = min(0.60 + (red_ratio * 0.35), 0.92)
            elif red_ratio > 0.15:
                # Moderate redness, check if there's high intensity or swelling features
                # Swelling/Edema often has higher green/blue components (skin-tone pale swelling)
                # combined with lower contrast or specific brightness
                if avg_r > 180 and avg_g > 150 and avg_b > 140 and (avg_r - avg_g) < 40:
                    label = "swelling"
                    confidence = 0.72
                else:
                    label = "localized urticaria"
                    confidence = 0.65
            elif avg_r > 190 and avg_g > 165 and avg_b > 155:
                # Pale/swollen look with low redness
                label = "swelling"
                confidence = 0.68
            else:
                label = "inconclusive"
                confidence = 0.85
                
            return {
                "label": label,
                "confidence": round(confidence, 2),
                "disclaimer": DISCLAIMER,
                "metrics": {
                    "red_ratio": round(red_ratio, 3),
                    "high_red_ratio": round(high_red_ratio, 3),
                    "avg_rgb": [round(avg_r, 1), round(avg_g, 1), round(avg_b, 1)],
                    "is_localized": is_localized
                }
            }
            
    except Exception as e:
        return {
            "label": "inconclusive",
            "confidence": 0.5,
            "disclaimer": DISCLAIMER,
            "metrics": {"error": f"Failed to analyze image: {str(e)}"}
        }
