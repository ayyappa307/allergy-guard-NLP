import json
import unittest
from fastapi.testclient import TestClient
from main import app

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_allergens(self):
        response = self.client.get("/api/allergens")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 25)
        self.assertEqual(data[0]["id"], "peanuts")

    def test_get_symptoms(self):
        response = self.client.get("/api/symptoms")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 35)

    def test_get_foods(self):
        response = self.client.get("/api/foods")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 30)

    def test_assess_known_allergies(self):
        # Assess known peanut allergy
        payload = {"allergens": ["peanuts"]}
        response = self.client.post("/api/assess/known", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check that we have unsafe foods containing peanuts
        # Thapala Chekkalu, Poornam Boorelu, Ariselu contain peanuts in our seed
        unsafe_names = [x["name"] for x in data["unsafe_foods"]]
        self.assertIn("Rice Crackers (Thapala Chekkalu)", unsafe_names)
        self.assertIn("Sweet Stuffed Dumplings (Poornam Boorelu)", unsafe_names)
        
        # Safe foods should not contain peanuts
        for food in data["safe_foods"]:
            self.assertNotIn("peanuts", food["allergens"])

    def test_assess_unknown_allergy_basic(self):
        # Post a simple unknown allergy form without photo
        response = self.client.post(
            "/api/assess/unknown",
            data={
                "food_id": "pesarattu",
                "symptoms": json.dumps(["tongue_swelling", "hives_urticaria"]),
                "food_text": "I ate moong dal dosa Pesarattu",
                "symptom_text": "I had a metallic taste and hives"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check top allergens
        self.assertTrue(len(data["top_allergens"]) > 0)
        # Should flag green gram or chili capsaicin
        top_allergen_ids = [x["id"] for x in data["top_allergens"]]
        self.assertTrue("green_gram" in top_allergen_ids or "chili_capsaicin" in top_allergen_ids)
        
        # Check doctor note details
        self.assertIn("disclaimer", data["doctor_note"])
        
        # Check severe symptom flag
        # hives, tongue swelling, metallic taste are Moderate symptoms, so severe should be False
        self.assertFalse(data["severe_symptom_detected"])
        self.assertFalse(data["emergency_alert"])

    def test_assess_unknown_allergy_severe(self):
        # Post severe symptoms
        response = self.client.post(
            "/api/assess/unknown",
            data={
                "symptoms": json.dumps(["diff_breathing", "low_bp"]),
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["severe_symptom_detected"])
        self.assertTrue(data["emergency_alert"])

if __name__ == "__main__":
    unittest.main()
