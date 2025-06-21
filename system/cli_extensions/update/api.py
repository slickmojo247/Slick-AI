# knowledge/api.py
from fastapi import APIRouter
from .core import KnowledgeCore
from .input_corrector import InputCorrector
from .spell_checker import CodeAwareSpellChecker

router = APIRouter()
knowledge_core = KnowledgeCore()
input_corrector = InputCorrector()
spell_checker = CodeAwareSpellChecker()

@router.post("/correct-input")
def correct_input(text: str, context: str = None):
    # Step 1: Spell check
    spell_checked = spell_checker.spell_check(text)
    
    # Step 2: Correct common mistakes
    corrected = input_corrector.correct_input(spell_checked, context)
    
    return {
        "original": text,
        "corrected": corrected,
        "correction_applied": text != corrected
    }

@router.post("/learn-mistake")
def learn_mistake(original: str, corrected: str, context: str = None):
    input_corrector.learn_from_correction(original, corrected, context)
    return {"status": "learned", "original": original, "corrected": corrected}

@router.get("/encyclopedia/{query}")
def search_encyclopedia(query: str, max_results: int = 5):
    results = knowledge_core.search_encyclopedia(query, max_results)
    return [dict(row) for row in results]

@router.get("/coding-manual/{language}/{concept}")
def get_coding_manual(language: str, concept: str):
    result = knowledge_core.search_coding_manual(language, concept)
    return dict(result) if result else {"error": "Not found"}

@router.get("/common-mistakes")
def get_common_mistakes(context: str = None, limit: int = 10):
    results = knowledge_core.get_common_mistakes(context)[:limit]
    return [dict(row) for row in results]