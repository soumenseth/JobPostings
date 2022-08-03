import spacy
from spacy.matcher import PhraseMatcher
import pickle
import os
from Path import *


class DegreeExtractor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.phrase_matcher_model_file = os.path.join(MODELS_DIR, "degree_phrase_matcher.pickle")
        if os.path.exists(self.phrase_matcher_model_file):
            self.matcher = self.load_model()
        else:
            self.matcher = self.train_phrase_matcher()

    def train_phrase_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab)
        patterns = ["Bachelor's", "Bachelor’s Degree", "Bachelors", "Master's", "MS", "BS", "BTech", "phd", "Master’s Degree",
                    "Masters", "PhD"]
        for pattern in patterns:
            matcher.add('DEGREE', [self.nlp(pattern)])
        with open(self.phrase_matcher_model_file, 'wb') as fh:
            pickle.dump(matcher, fh)
        return matcher

    def load_model(self):
        with open(self.phrase_matcher_model_file, "rb") as fh:
            matcher = pickle.load(fh)
        return matcher

    def extract_degree(self, text):
        doc = self.nlp(text)
        matches = self.matcher(doc)
        degrees = []

        for match_id, start, end in matches:
            # string_id = self.nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            degrees.append({
                'match_id': match_id,
                # 'string_id': string_id,
                'start': start,
                'end': end,
                'text': span.text
            })
        return degrees
