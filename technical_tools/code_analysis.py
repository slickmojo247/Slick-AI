import ast
from typing import List, Dict

class CodeInspector:
    @staticmethod
    def get_code_structure(code: str) -> List[Dict]:
        """Parse code structure using AST"""
        try:
            tree = ast.parse(code)
            structures = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    structures.append({
                        "type": "function",
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "lineno": node.lineno
                    })
                elif isinstance(node, ast.ClassDef):
                    structures.append({
                        "type": "class",
                        "name": node.name,
                        "bases": [base.id for base in node.bases],
                        "lineno": node.lineno
                    })
                    
            return structures
        except SyntaxError:
            return [{"error": "Invalid syntax"}]

    @staticmethod
    def detect_language(code: str) -> str:
        """Detect programming language"""
        patterns = {
            "python": [r'def\s+\w+\(', r'class\s+\w+', r'import\s+\w+'],
            "javascript": [r'function\s+\w+\(', r'const\s+\w+', r'console\.log'],
            "bash": [r'^\s*#!\/bin\/bash', r'\$\w+', r'if\s*\[\s*']
        }
        
        for lang, regexes in patterns.items():
            if any(re.search(pattern, code) for pattern in regexes):
                return lang
        return "unknown"
