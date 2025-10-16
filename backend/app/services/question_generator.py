from typing import List, Dict, Optional
import random
import re
from app.services.nlp_engine import NLPEngine
from app.models.question import QuestionType, DifficultyLevel


class QuestionGenerator:
    """Service for generating questions from extracted text."""
    
    def __init__(self):
        self.nlp_engine = NLPEngine()
        self.question_templates = self._load_templates()
    
    def generate_questions(
        self,
        text: str,
        num_questions: int = 10,
        question_types: Optional[List[QuestionType]] = None,
        difficulty_mix: Optional[Dict[DifficultyLevel, float]] = None
    ) -> List[Dict]:
        """Generate questions from text based on configuration - FAST & ACCURATE."""
        
        # Validate input
        if not text or len(text.strip()) < 100:
            raise ValueError("Text is too short to generate questions. Need at least 100 characters.")
        
        if question_types is None:
            question_types = [QuestionType.MCQ, QuestionType.SHORT_ANSWER, QuestionType.LONG_ANSWER]
        
        if difficulty_mix is None:
            difficulty_mix = {
                DifficultyLevel.EASY: 0.4,
                DifficultyLevel.MEDIUM: 0.4,
                DifficultyLevel.HARD: 0.2
            }
        
        try:
            # FAST: Extract content for question generation (optimized)
            definitions = self.nlp_engine.extract_definitions(text)[:num_questions * 2]
            facts = self.nlp_engine.extract_facts(text)[:num_questions * 2]
            key_sentences = self.nlp_engine.extract_key_sentences(text, top_n=min(20, num_questions * 2))
            entities = self.nlp_engine.extract_entities(text)[:num_questions * 2]
            relationships = self.nlp_engine.extract_relationships(text)[:num_questions]
        except Exception as e:
            raise ValueError(f"Failed to analyze text: {str(e)}")
        
        # Check if we have enough content
        if not definitions and not facts and not key_sentences:
            raise ValueError("Could not extract enough content from text. The document may be too short or not contain suitable content for questions.")
        
        questions = []
        
        # Calculate EXACT questions per type
        questions_per_type = num_questions // len(question_types)
        remainder = num_questions % len(question_types)
        
        for idx, q_type in enumerate(question_types):
            # Distribute remainder to first types
            count = questions_per_type + (1 if idx < remainder else 0)
            type_questions = []
            
            try:
                if q_type == QuestionType.MCQ:
                    type_questions = self._generate_mcq(definitions, facts, entities, count)
                elif q_type == QuestionType.TRUE_FALSE:
                    type_questions = self._generate_true_false(facts, key_sentences, count)
                elif q_type == QuestionType.SHORT_ANSWER:
                    type_questions = self._generate_short_answer(definitions, key_sentences, count)
                elif q_type == QuestionType.LONG_ANSWER:
                    type_questions = self._generate_long_answer(key_sentences, relationships, count)
                elif q_type == QuestionType.FILL_BLANK:
                    type_questions = self._generate_fill_blank(definitions, facts, count)
                elif q_type == QuestionType.PROGRAMMING:
                    type_questions = self._generate_programming(text, count)
            except Exception as e:
                print(f"Warning: Failed to generate {q_type} questions: {e}")
                # Continue with other types
                continue
            
            questions.extend(type_questions)
        
        # Assign difficulties based on mix
        questions = self._assign_difficulties(questions, difficulty_mix)
        
        # ENSURE EXACT COUNT - 30 bola to 30 hi milega!
        if len(questions) > num_questions:
            questions = questions[:num_questions]
        elif len(questions) < num_questions:
            # If less, generate more from first type
            needed = num_questions - len(questions)
            try:
                extra = self._generate_mcq(definitions, facts, entities, needed)
                questions.extend(extra[:needed])
            except Exception as e:
                print(f"Warning: Could not generate additional questions: {e}")
        
        # Final validation
        if len(questions) == 0:
            raise ValueError("Failed to generate any questions. Please check if the document has sufficient text content.")
        
        return questions
    
    def _generate_mcq(self, definitions: List[Dict], facts: List[str], 
                      entities: List[Dict], count: int) -> List[Dict]:
        """Generate multiple choice questions."""
        questions = []
        
        # From definitions
        for defn in definitions[:count]:
            question = {
                "question_text": f"What is {defn['term']}?",
                "question_type": QuestionType.MCQ,
                "correct_answer": defn['definition'],
                "explanation": f"Based on the definition: {defn['sentence']}",
                "suggested_marks": 1.0
            }
            
            # Generate distractors (wrong options)
            options = [defn['definition']]
            # Add plausible distractors (simplified - in production, use better methods)
            options.extend(self._generate_distractors(defn['definition'], 3))
            random.shuffle(options)
            
            question["option_a"] = options[0]
            question["option_b"] = options[1]
            question["option_c"] = options[2]
            question["option_d"] = options[3]
            
            questions.append(question)
            
            if len(questions) >= count:
                break
        
        # From facts with entities
        for fact in facts[:count - len(questions)]:
            doc = self.nlp_engine.nlp(fact)
            if doc.ents:
                entity = doc.ents[0]
                question_text = fact.replace(entity.text, "______")
                
                question = {
                    "question_text": f"Fill in the blank: {question_text}",
                    "question_type": QuestionType.MCQ,
                    "correct_answer": entity.text,
                    "explanation": f"From the text: {fact}",
                    "suggested_marks": 1.0
                }
                
                options = [entity.text]
                options.extend(self._generate_distractors(entity.text, 3))
                random.shuffle(options)
                
                question["option_a"] = options[0]
                question["option_b"] = options[1]
                question["option_c"] = options[2]
                question["option_d"] = options[3]
                
                questions.append(question)
        
        return questions
    
    def _generate_true_false(self, facts: List[str], sentences: List[str], count: int) -> List[Dict]:
        """Generate true/false questions."""
        questions = []
        
        for fact in facts[:count]:
            # True statement
            if random.random() > 0.5:
                question = {
                    "question_text": f"True or False: {fact}",
                    "question_type": QuestionType.TRUE_FALSE,
                    "option_a": "True",
                    "option_b": "False",
                    "correct_answer": "True",
                    "explanation": "This statement is directly from the source material.",
                    "suggested_marks": 0.5
                }
            else:
                # False statement (negate or modify)
                modified = self._create_false_statement(fact)
                question = {
                    "question_text": f"True or False: {modified}",
                    "question_type": QuestionType.TRUE_FALSE,
                    "option_a": "True",
                    "option_b": "False",
                    "correct_answer": "False",
                    "explanation": f"The correct statement is: {fact}",
                    "suggested_marks": 0.5
                }
            
            questions.append(question)
            
            if len(questions) >= count:
                break
        
        return questions
    
    def _generate_short_answer(self, definitions: List[Dict], sentences: List[str], count: int) -> List[Dict]:
        """Generate short answer questions."""
        questions = []
        
        # From definitions
        for defn in definitions[:count]:
            templates = [
                f"Define {defn['term']}.",
                f"What is meant by {defn['term']}?",
                f"Explain the term {defn['term']}.",
            ]
            
            question = {
                "question_text": random.choice(templates),
                "question_type": QuestionType.SHORT_ANSWER,
                "correct_answer": defn['definition'],
                "explanation": f"Expected answer: {defn['definition']}",
                "suggested_marks": 2.0
            }
            questions.append(question)
            
            if len(questions) >= count:
                break
        
        # From key sentences
        for sent in sentences[:count - len(questions)]:
            # Convert statement to question
            question_text = self._statement_to_question(sent)
            
            question = {
                "question_text": question_text,
                "question_type": QuestionType.SHORT_ANSWER,
                "correct_answer": sent,
                "explanation": f"Expected answer should cover: {sent}",
                "suggested_marks": 3.0
            }
            questions.append(question)
        
        return questions
    
    def _generate_long_answer(self, sentences: List[str], relationships: List[Dict], count: int) -> List[Dict]:
        """Generate long answer questions."""
        questions = []
        
        templates = [
            "Explain in detail",
            "Discuss",
            "Describe",
            "Analyze",
            "Compare and contrast",
            "Evaluate"
        ]
        
        # Extract topics from sentences
        topics = []
        for sent in sentences:
            doc = self.nlp_engine.nlp(sent)
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) >= 2:
                    topics.append(chunk.text)
        
        topics = list(set(topics))[:count]
        
        for topic in topics:
            template = random.choice(templates)
            
            question = {
                "question_text": f"{template} {topic}.",
                "question_type": QuestionType.LONG_ANSWER,
                "correct_answer": f"A comprehensive answer should cover the key aspects of {topic} as discussed in the material.",
                "explanation": "This is an open-ended question requiring detailed explanation.",
                "suggested_marks": 5.0
            }
            questions.append(question)
            
            if len(questions) >= count:
                break
        
        return questions
    
    def _generate_fill_blank(self, definitions: List[Dict], facts: List[str], count: int) -> List[Dict]:
        """Generate fill-in-the-blank questions."""
        questions = []
        
        for fact in facts[:count]:
            doc = self.nlp_engine.nlp(fact)
            
            # Find important words to blank out
            important_tokens = [token for token in doc if token.pos_ in ["NOUN", "PROPN", "NUM"] 
                              and not token.is_stop]
            
            if important_tokens:
                token_to_blank = random.choice(important_tokens)
                question_text = fact.replace(token_to_blank.text, "______")
                
                question = {
                    "question_text": f"Fill in the blank: {question_text}",
                    "question_type": QuestionType.FILL_BLANK,
                    "correct_answer": token_to_blank.text,
                    "explanation": f"Complete sentence: {fact}",
                    "suggested_marks": 1.0
                }
                questions.append(question)
            
            if len(questions) >= count:
                break
        
        return questions
    
    def _generate_programming(self, text: str, count: int) -> List[Dict]:
        """Generate programming questions (if applicable)."""
        questions = []
        
        # Look for code-related keywords
        code_keywords = ['algorithm', 'function', 'program', 'code', 'implement', 
                        'write', 'develop', 'class', 'method']
        
        sentences = text.split('.')
        code_sentences = [s for s in sentences if any(kw in s.lower() for kw in code_keywords)]
        
        for sent in code_sentences[:count]:
            question = {
                "question_text": f"Write a program to {sent.strip().lower()}",
                "question_type": QuestionType.PROGRAMMING,
                "correct_answer": "Implementation should follow standard programming practices.",
                "explanation": "Evaluate based on correctness, efficiency, and code quality.",
                "suggested_marks": 10.0
            }
            questions.append(question)
            
            if len(questions) >= count:
                break
        
        return questions
    
    def _assign_difficulties(self, questions: List[Dict], 
                           difficulty_mix: Dict[DifficultyLevel, float]) -> List[Dict]:
        """Assign difficulty levels to questions based on mix."""
        total = len(questions)
        
        easy_count = int(total * difficulty_mix.get(DifficultyLevel.EASY, 0.4))
        medium_count = int(total * difficulty_mix.get(DifficultyLevel.MEDIUM, 0.4))
        hard_count = total - easy_count - medium_count
        
        difficulties = (
            [DifficultyLevel.EASY] * easy_count +
            [DifficultyLevel.MEDIUM] * medium_count +
            [DifficultyLevel.HARD] * hard_count
        )
        
        random.shuffle(difficulties)
        
        for i, question in enumerate(questions):
            if i < len(difficulties):
                question["difficulty"] = difficulties[i]
            else:
                question["difficulty"] = DifficultyLevel.MEDIUM
        
        return questions
    
    def _generate_distractors(self, correct_answer: str, count: int) -> List[str]:
        """Generate plausible wrong answers (distractors) for MCQs."""
        # Simplified distractor generation
        # In production, use more sophisticated methods (word embeddings, etc.)
        distractors = []
        
        words = correct_answer.split()
        
        for i in range(count):
            if len(words) > 3:
                # Shuffle words
                shuffled = words.copy()
                random.shuffle(shuffled)
                distractors.append(' '.join(shuffled))
            else:
                # Add generic distractors
                distractors.append(f"Alternative definition {i+1}")
        
        return distractors
    
    def _create_false_statement(self, true_statement: str) -> str:
        """Create a false version of a true statement."""
        # Simple negation or modification
        if " is " in true_statement:
            return true_statement.replace(" is ", " is not ")
        elif " are " in true_statement:
            return true_statement.replace(" are ", " are not ")
        else:
            return f"It is incorrect that {true_statement.lower()}"
    
    def _statement_to_question(self, statement: str) -> str:
        """Convert a statement to a question."""
        statement = statement.strip()
        
        # Simple conversion patterns
        if statement.startswith("The "):
            return "What is " + statement[4:].rstrip('.') + "?"
        elif " is " in statement:
            parts = statement.split(" is ", 1)
            return f"What is {parts[0]}?"
        else:
            return f"Explain: {statement}"
    
    def _load_templates(self) -> Dict:
        """Load question templates."""
        return {
            "definition": [
                "Define {term}.",
                "What is {term}?",
                "Explain the concept of {term}.",
            ],
            "explanation": [
                "Explain {concept}.",
                "Describe {concept}.",
                "Discuss {concept}.",
            ],
            "comparison": [
                "Compare {concept1} and {concept2}.",
                "What are the differences between {concept1} and {concept2}?",
            ]
        }
