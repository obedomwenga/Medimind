# test_query.py
from metta import MeTTaEngine

engine = MeTTaEngine()
print("\n--- Testing getCauses ChestPain ---")
result = engine.query("getCauses ChestPain")
print("Result:", result)