import os
import unittest
from classifier import analyze_skin_reaction

class TestClassifier(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.patterns_dir = os.path.join(self.base_dir, "static", "images", "patterns")

    def test_nonexistent_image(self):
        result = analyze_skin_reaction("does_not_exist.jpg")
        self.assertEqual(result["label"], "inconclusive")
        self.assertEqual(result["confidence"], 0.5)
        self.assertIn("not found", result["metrics"]["error"])

    def test_localized_urticaria_image(self):
        img_path = os.path.join(self.patterns_dir, "localized_urticaria.jpg")
        if os.path.exists(img_path):
            result = analyze_skin_reaction(img_path)
            # The placeholder is red-tinted, so it should classify as red/swelling/localized
            self.assertIn(result["label"], ["localized urticaria", "diffuse redness", "swelling"])
            self.assertGreaterEqual(result["confidence"], 0.6)
            self.assertIn("Academic project reference", result["disclaimer"])

    def test_inconclusive_image(self):
        img_path = os.path.join(self.patterns_dir, "inconclusive.jpg")
        if os.path.exists(img_path):
            result = analyze_skin_reaction(img_path)
            self.assertIn(result["label"], ["inconclusive", "localized urticaria", "diffuse redness", "swelling"])
            self.assertGreaterEqual(result["confidence"], 0.5)

if __name__ == "__main__":
    unittest.main()
