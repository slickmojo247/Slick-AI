# knowledge/spell_checker.py
import re
from spellchecker import SpellChecker

class CodeAwareSpellChecker:
    def __init__(self):
        self.spell = SpellChecker()
        self.code_keywords = self.load_code_keywords()
        self.spell.word_frequency.load_words(self.code_keywords)
    
    def load_code_keywords(self):
        """Load programming keywords from various languages"""
        keywords = []
        # Python keywords
        keywords.extend(['False', 'None', 'True', 'and', 'as', 'assert', 'async', 
                        'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 
                        'else', 'except', 'finally', 'for', 'from', 'global', 'if', 
                        'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 
                        'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'])
        
        # JavaScript keywords
        keywords.extend(['abstract', 'arguments', 'await', 'boolean', 'break', 'byte', 
                        'case', 'catch', 'char', 'class', 'const', 'continue', 'debugger', 
                        'default', 'delete', 'do', 'double', 'else', 'enum', 'eval', 
                        'export', 'extends', 'false', 'final', 'finally', 'float', 'for', 
                        'function', 'goto', 'if', 'implements', 'import', 'in', 'instanceof', 
                        'int', 'interface', 'let', 'long', 'native', 'new', 'null', 'package', 
                        'private', 'protected', 'public', 'return', 'short', 'static', 'super', 
                        'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'true', 
                        'try', 'typeof', 'var', 'void', 'volatile', 'while', 'with', 'yield'])
        
        # SQL keywords
        keywords.extend(['SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'OUTER', 'LEFT', 'RIGHT', 
                        'FULL', 'ON', 'GROUP', 'BY', 'HAVING', 'ORDER', 'BY', 'ASC', 'DESC', 
                        'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 
                        'ALTER', 'DROP', 'INDEX', 'VIEW', 'AND', 'OR', 'NOT', 'NULL', 'LIKE', 'IN'])
        
        return list(set(keywords))
    
    def spell_check(self, text):
        """Perform spell checking while ignoring code elements"""
        # Split text into code and non-code segments
        segments = self.split_code_and_text(text)
        
        corrected_segments = []
        for segment, is_code in segments:
            if is_code:
                corrected_segments.append(segment)
            else:
                corrected_segments.append(self.correct_text_segment(segment))
        
        return ''.join(corrected_segments)
    
    def split_code_and_text(self, text):
        """Split text into code and non-code segments"""
        segments = []
        # Regular expression to detect code blocks (backticks) and code-like elements
        pattern = r'(`[^`]+`|\b\w+\(\)|\b[a-z_][a-z0-9_]*\s*=\s*|\b[A-Z_][A-Z0-9_]+\b)'
        last_index = 0
        
        for match in re.finditer(pattern, text):
            # Text before the code segment
            if match.start() > last_index:
                segments.append((text[last_index:match.start()], False))
            
            # The code segment itself
            segments.append((match.group(0), True))
            last_index = match.end()
        
        # Remaining text after last code segment
        if last_index < len(text):
            segments.append((text[last_index:], False))
        
        return segments
    
    def correct_text_segment(self, text):
        """Correct spelling in a text segment"""
        words = re.findall(r'\b\w+\b', text)
        misspelled = self.spell.unknown(words)
        
        corrected_text = text
        for word in misspelled:
            # Get the most likely correction
            correction = self.spell.correction(word)
            if correction:
                # Replace only whole words to avoid partial replacements
                corrected_text = re.sub(r'\b' + re.escape(word) + r'\b', correction, corrected_text)
        
        return corrected_text