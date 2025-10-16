import spacy
from typing import List, Dict, Tuple
import re
from collections import Counter


class NLPEngine:
    """NLP service for text analysis and concept extraction."""
    
    def __init__(self, model_name: str = "en_core_web_sm"):
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            raise Exception(f"spaCy model '{model_name}' not found. Run: python -m spacy download {model_name}")
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities from text."""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """Extract noun phrases (potential concepts)."""
        doc = self.nlp(text)
        noun_phrases = []
        
        for chunk in doc.noun_chunks:
            # Filter out very short or common phrases
            if len(chunk.text.split()) >= 2 and len(chunk.text) > 5:
                noun_phrases.append(chunk.text.strip())
        
        return list(set(noun_phrases))
    
    def extract_key_sentences(self, text: str, top_n: int = 10) -> List[str]:
        """Extract key sentences that could be used for questions."""
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        # Score sentences based on:
        # 1. Length (not too short, not too long)
        # 2. Presence of important entities
        # 3. Presence of key verbs
        
        scored_sentences = []
        for sent in sentences:
            score = self._score_sentence(sent)
            if score > 0:
                scored_sentences.append((sent, score))
        
        # Sort by score and return top N
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [sent for sent, score in scored_sentences[:top_n]]
    
    def _score_sentence(self, sentence: str) -> float:
        """Score a sentence for its suitability as a question source."""
        doc = self.nlp(sentence)
        score = 0.0
        
        # Length score (prefer 10-30 words)
        word_count = len([token for token in doc if not token.is_punct])
        if 10 <= word_count <= 30:
            score += 2.0
        elif 5 <= word_count < 10 or 30 < word_count <= 50:
            score += 1.0
        else:
            return 0.0  # Too short or too long
        
        # Entity score
        if doc.ents:
            score += len(doc.ents) * 0.5
        
        # Important verbs
        important_verbs = {'is', 'are', 'was', 'were', 'define', 'explain', 'describe', 
                          'calculate', 'determine', 'show', 'prove', 'demonstrate'}
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_ in important_verbs:
                score += 1.0
        
        # Has numbers (good for factual questions)
        if any(token.like_num for token in doc):
            score += 0.5
        
        return score
    
    def extract_definitions(self, text: str) -> List[Dict[str, str]]:
        """Extract definition-like sentences."""
        doc = self.nlp(text)
        definitions = []
        
        # Patterns for definitions
        definition_patterns = [
            r'(.+?)\s+is\s+(?:a|an|the)\s+(.+?)[\.\,]',
            r'(.+?)\s+refers to\s+(.+?)[\.\,]',
            r'(.+?)\s+means\s+(.+?)[\.\,]',
            r'(.+?)\s+can be defined as\s+(.+?)[\.\,]',
        ]
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            for pattern in definition_patterns:
                match = re.search(pattern, sent_text, re.IGNORECASE)
                if match:
                    definitions.append({
                        "term": match.group(1).strip(),
                        "definition": match.group(2).strip(),
                        "sentence": sent_text
                    })
                    break
        
        return definitions
    
    def extract_facts(self, text: str) -> List[str]:
        """Extract factual statements."""
        doc = self.nlp(text)
        facts = []
        
        for sent in doc.sents:
            sent_text = sent.text.strip()
            
            # Look for sentences with numbers, dates, or strong factual indicators
            has_number = any(token.like_num for token in sent)
            has_date = any(ent.label_ == "DATE" for ent in sent.ents)
            has_quantity = any(ent.label_ in ["QUANTITY", "PERCENT", "MONEY"] for ent in sent.ents)
            
            if has_number or has_date or has_quantity:
                if 10 <= len(sent_text.split()) <= 40:
                    facts.append(sent_text)
        
        return facts
    
    def identify_topics(self, text: str, num_topics: int = 5) -> List[str]:
        """Identify main topics using noun phrase frequency."""
        noun_phrases = self.extract_noun_phrases(text)
        
        # Count frequencies
        phrase_counter = Counter(noun_phrases)
        
        # Get most common
        top_topics = [phrase for phrase, count in phrase_counter.most_common(num_topics)]
        
        return top_topics
    
    def extract_relationships(self, text: str) -> List[Dict[str, str]]:
        """Extract subject-verb-object relationships."""
        doc = self.nlp(text)
        relationships = []
        
        for sent in doc.sents:
            for token in sent:
                if token.dep_ == "ROOT" and token.pos_ == "VERB":
                    subject = None
                    obj = None
                    
                    for child in token.children:
                        if child.dep_ in ["nsubj", "nsubjpass"]:
                            subject = child.text
                        elif child.dep_ in ["dobj", "pobj"]:
                            obj = child.text
                    
                    if subject and obj:
                        relationships.append({
                            "subject": subject,
                            "verb": token.text,
                            "object": obj,
                            "sentence": sent.text.strip()
                        })
        
        return relationships
    
    def calculate_text_complexity(self, text: str) -> Dict[str, float]:
        """Calculate text complexity metrics."""
        doc = self.nlp(text)
        
        sentences = list(doc.sents)
        words = [token for token in doc if not token.is_punct and not token.is_space]
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(token.text) for token in words) / len(words) if words else 0
        
        # Count complex words (3+ syllables - approximation)
        complex_words = sum(1 for token in words if len(token.text) > 6)
        complex_word_ratio = complex_words / len(words) if words else 0
        
        return {
            "avg_sentence_length": avg_sentence_length,
            "avg_word_length": avg_word_length,
            "complex_word_ratio": complex_word_ratio,
            "total_sentences": len(sentences),
            "total_words": len(words)
        }
