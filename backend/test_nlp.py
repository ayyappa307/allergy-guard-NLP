import unittest
from nlp_engine import extract_entities

class TestNLPEngine(unittest.TestCase):
    
    def test_empty_input(self):
        result = extract_entities("")
        self.assertEqual(result, {"foods": [], "symptoms": []})
        
        result = extract_entities(None)
        self.assertEqual(result, {"foods": [], "symptoms": []})

    def test_food_extraction(self):
        text = "Today for breakfast I had Pesarattu and some Spiced Majjiga."
        result = extract_entities(text)
        self.assertIn("pesarattu", result["foods"])
        self.assertIn("spiced_majjiga", result["foods"])
        self.assertEqual(len(result["foods"]), 2)

    def test_symptom_extraction(self):
        text = "I have a skin rash and my lips are swelling. I feel dizzy too."
        result = extract_entities(text)
        self.assertIn("localized_rash", result["symptoms"])
        self.assertIn("mild_swelling", result["symptoms"])
        self.assertIn("dizziness", result["symptoms"])
        
    def test_combined_extraction(self):
        text = "I ate some Upma Pesarattu. Shortly after, I had difficulty breathing, my tongue started swelling, and I got hives."
        result = extract_entities(text)
        self.assertIn("upma_pesarattu", result["foods"])
        self.assertIn("diff_breathing", result["symptoms"])
        self.assertIn("tongue_swelling", result["symptoms"])
        self.assertIn("hives_urticaria", result["symptoms"])

    def test_synonyms_extraction(self):
        text = "After eating biryani, I felt lightheaded, nauseous, and started wheezing."
        result = extract_entities(text)
        self.assertIn("hyderabadi_biryani", result["foods"])
        self.assertIn("dizziness", result["symptoms"]) # lightheaded -> dizziness
        self.assertIn("nausea", result["symptoms"])    # nauseous -> nausea
        self.assertIn("wheezing", result["symptoms"])  # wheezing -> wheezing

if __name__ == "__main__":
    unittest.main()
