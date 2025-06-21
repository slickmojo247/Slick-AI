import spacy
from typing import Dict, Any, List
import logging

class ContextBuilder:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        try:
            self.nlp = spacy.load("en_core_web_sm")
            self.log.info("Loaded NLP model for context building")
        except:
            self.nlp = None
            self.log.warning("SpaCy model not available, using simple mode")

    def build(self, query: str, memory, user_context: Dict) -> Dict[str, Any]:
        """Enhanced context building with NLP"""
        base = {
            "query": query,
            "user": user_context,
            "memory": self._get_memory_context(query, memory),
            "linguistic": self._analyze_text(query)
        }
        return self._add_derived_context(base)

    def _analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform NLP analysis if available"""
        if not self.nlp:
            return {"entities": [], "verbs": []}
        
        doc = self.nlp(text)
        return {
            "entities": [(ent.text, ent.label_) for ent in doc.ents],
            "verbs": [token.lemma_ for token in doc if token.pos_ == "VERB"],
            "sentiment": doc.sentiment
        }

    def _add_derived_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer higher-level context"""
        context["inferred"] = {
            "likely_intent": self._detect_intent(context["query"]),
            "knowledge_gaps": self._find_gaps(context)
        }
        return context

    def _detect_intent(self, query: str) -> str:
        """Improved intent detection"""
        query = query.lower()
        if any(q in query for q in ["how to", "tutorial"]):
            return "instruction"
        elif any(q in query for q in ["why", "cause of"]):
            return "explanation"
        elif any(q in query for q in ["compare", "vs"]):
            return "comparison"
        return "information"

    def _find_gaps(self, context: Dict[str, Any]) -> List[str]:
        """Identify missing context"""
        gaps = []
        if not context["memory"]["related_queries"]:
            gaps.append("no_similar_queries")
        if "user" not in context or not context["user"]:
            gaps.append("no_user_profile")
        return gaps
