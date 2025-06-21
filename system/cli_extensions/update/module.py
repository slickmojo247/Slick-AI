# learning/module.py
from typing import Dict, Optional
from dataclasses import dataclass
import re
from spellchecker import SpellChecker
from knowledge.base import KnowledgeBase

@dataclass
class ProcessedInput:
    raw_input: str
    corrected: str
    context: Dict
    enhanced: bool = False

class LearningModule:
    def __init__(self):
        self.spell_checker = CodeAwareSpellChecker()
        self.input_corrector = InputCorrector()
        self.knowledge_enhancer = KnowledgeEnhancer()
        self.knowledge_retention = KnowledgeRetention()
        
    async def process_input(self, user_input: str) -> ProcessedInput:
        """Full processing pipeline for user input"""
        # Step 1: Input correction
        corrected = self.input_corrector.correct(user_input)
        
        # Step 2: Spell checking
        spell_checked = self.spell_checker.check(corrected)
        
        # Step 3: Knowledge enhancement
        enhanced, context = await self.knowledge_enhancer.enhance(spell_checked)
        
        # Step 4: Display preparation
        display_result = self._prepare_display(enhanced, context)
        
        # Step 5: Learning feedback loop
        await self.knowledge_retention.log_interaction(
            original=user_input,
            processed=enhanced,
            context=context
        )
        
        return ProcessedInput(
            raw_input=user_input,
            corrected=enhanced,
            context=context,
            enhanced=enhanced != user_input
        )

    def _prepare_display(self, text: str, context: Dict) -> str:
        """Format results for display with context"""
        if not context:
            return text
            
        context_str = "\n".join(f"{k}: {v}" for k,v in context.items())
        return f"{text}\n\n[Context]\n{context_str}"

class CodeAwareSpellChecker(SpellChecker):
    def __init__(self):
        super().__init__()
        self._load_code_keywords()
        
    def _load_code_keywords(self):
        """Load programming terms from knowledge base"""
        from knowledge.base import CODING_KEYWORDS
        self.word_frequency.load_words(CODING_KEYWORDS)
        
    def check(self, text: str) -> str:
        """Enhanced spell checking that preserves code blocks"""
        # Skip code blocks between ```
        parts = re.split(r'(```.*?```)', text)
        for i, part in enumerate(parts):
            if not part.startswith('```'):
                parts[i] = super().correction(part)
        return ''.join(parts)

class InputCorrector:
    COMMON_PATTERNS = [
        (r',(\s*[\)\]\}])', r'\1'),  # Trailing commas
        (r'(\w)\s+(\()', r'\1\2'),    # Space before parenthesis
        # Add more patterns from your original corrector
    ]
    
    def __init__(self):
        from knowledge.base import CommonMistakesDB
        self.mistakes_db = CommonMistakesDB()
        
    def correct(self, text: str) -> str:
        """Multi-layer input correction"""
        # Apply common pattern fixes
        for pattern, replacement in self.COMMON_PATTERNS:
            text = re.sub(pattern, replacement, text)
            
        # Fix known common mistakes
        text = self._fix_known_mistakes(text)
        
        return text
        
    def _fix_known_mistakes(self, text: str) -> str:
        """Use common mistakes database"""
        words = text.split()
        corrected = []
        for word in words:
            correction = self.mistakes_db.get_correction(word)
            corrected.append(correction or word)
        return ' '.join(corrected)

class KnowledgeEnhancer:
    def __init__(self):
        from knowledge.base import Encyclopedia, CodingManuals
        self.encyclopedia = Encyclopedia()
        self.coding_manuals = CodingManuals()
        
    async def enhance(self, text: str) -> tuple[str, Dict]:
        """Enrich input with contextual knowledge"""
        context = {}
        
        # Get encyclopedia context
        en_context = await self.encyclopedia.get_context(text)
        if en_context:
            context.update(en_context)
            
        # Get coding context if relevant
        if self._is_code_related(text):
            code_context = await self.coding_manuals.get_examples(text)
            if code_context:
                context.update(code_context)
                
        # Enhance the text if we found relevant context
        enhanced_text = text
        if context:
            enhanced_text = f"{text} [context-enhanced]"
            
        return enhanced_text, context
        
    def _is_code_related(self, text: str) -> bool:
        """Check if input appears to be code-related"""
        code_keywords = {'function', 'loop', 'variable', 'def ', 'class '}
        return any(kw in text.lower() for kw in code_keywords)

class KnowledgeRetention:
    def __init__(self):
        from knowledge.base import KnowledgeBase
        self.knowledge_base = KnowledgeBase()
        
    async def log_interaction(self, original: str, processed: str, context: Dict):
        """Store learned information in knowledge bases"""
        # Store in encyclopedia if conceptual
        if context.get('encyclopedia'):
            await self.knowledge_base.encyclopedia.insert(
                concept=context['concept'],
                explanation=context['encyclopedia']
            )
            
        # Store in coding manuals if technical
        if context.get('code_example'):
            await self.knowledge_base.coding_manuals.insert(
                topic=context['topic'],
                example=context['code_example']
            )
            
        # Update common mistakes if correction was made
        if original != processed:
            await self.knowledge_base.common_mistakes.log_correction(
                mistake=original,
                correction=processed
            )