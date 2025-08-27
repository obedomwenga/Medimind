# metta.py
from hyperon import MeTTa, Atom
import os
import re

class MeTTaEngine:
    def __init__(self, metta_file="metta_kb/medical.metta"):
        self.metta = MeTTa()
        self.load_file(metta_file)
    
    def load_file(self, filepath):
        """Load a .metta file, handling multi-line expressions correctly"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"MeTTa file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove comments
        lines = [line.split(';')[0].strip() for line in content.splitlines()]
        text = ' '.join(lines)  # Flatten to one string for easier parsing

        i = 0
        parsed_expressions = []

        while i < len(text):
            if text[i].isspace():
                i += 1
                continue
            if text[i] == '(':
                # Parse balanced parentheses
                start = i
                depth = 0
                for j in range(i, len(text)):
                    if text[j] == '(': depth += 1
                    elif text[j] == ')': depth -= 1
                    if depth == 0:
                        expr = text[start:j+1]
                        try:
                            atom = self.metta.parse_single(expr)
                            self.metta.space().add_atom(atom)
                            parsed_expressions.append(expr)
                            print(f"Loaded: {expr[:60]}{'...' if len(expr) > 60 else ''}")
                        except Exception as e:
                            print(f"Error parsing: {expr[:60]}...")
                            print(f"Error: {e}")
                        i = j + 1
                        break
                else:
                    print("Unbalanced parentheses in expression starting at:", text[i:i+50])
                    break
            else:
                # Skip non-parenthesized tokens (shouldn't happen in MeTTa)
                i += 1

        print(f"\n✅ Loaded {len(parsed_expressions)} expressions.\n")

    def query(self, expression):
        try:
            result = self.metta.run(f"!({expression})")
            strings = []
            for atom in result:
                s = str(atom)
                # If it looks like a list: "[A, B, C]", extract items
                if s.startswith('[') and ',' in s:
                    # Extract atoms inside brackets
                    items = re.findall(r'\w+', s)
                    strings.extend(items)
                elif s != expression and not s.startswith('('):
                    strings.append(s.strip())
            return strings if strings else [f"No result for {expression}"]
        except Exception as e:
            print(f"Query error: {e}")
            return [f"Error: {e}"]

    def add_knowledge(self, fact):
        try:
            atom = self.metta.parse_single(fact)
            self.metta.space().add_atom(atom)
            return f"Learned: {fact}"
        except Exception as e:
            return f"Failed to learn: {e}"