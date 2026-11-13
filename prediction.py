import os
import re
import joblib
import numpy as np
from preprocessing import preprocess_text

class ComplaintPredictor:
    """
    Handles model loading and complaint classification.
    """
    def __init__(self, models_dir=None):
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.models_dir = models_dir
        self.vectorizer = None
        self.models = {}
        self.model_names = {
            'naive_bayes': 'Multinomial Naive Bayes',
            'logistic_regression': 'Logistic Regression',
            'linear_svm': 'Linear Support Vector Machine'
        }
        self.load_artifacts()

    def load_artifacts(self):
        vec_path = os.path.join(self.models_dir, 'tfidf_vectorizer.pkl')
        if os.path.exists(vec_path):
            self.vectorizer = joblib.load(vec_path)

        for key in ['naive_bayes', 'logistic_regression', 'linear_svm']:
            model_path = os.path.join(self.models_dir, f"{key}.pkl")
            if os.path.exists(model_path):
                self.models[key] = joblib.load(model_path)

    def is_ready(self):
        return self.vectorizer is not None and len(self.models) > 0

    def predict(self, text: str, model_key: str = 'logistic_regression'):
        """
        Predict category for the given complaint/query text using the chosen model.
        Returns:
            dict containing:
            - success: bool
            - category: str
            - model_name: str
            - model_key: str
            - cleaned_text: str
            - original_text: str
            - error: str (if any)
        """
        if not text or not text.strip():
            return {
                'success': False,
                'error': 'Please enter a complaint text to classify.'
            }

        if not self.is_ready():
            self.load_artifacts()
            if not self.is_ready():
                return {
                    'success': False,
                    'error': 'Model files not found. Please train the models before making predictions.'
                }

        if model_key not in self.models:
            return {
                'success': False,
                'error': f"Selected model '{model_key}' is not available."
            }

        cleaned = preprocess_text(text)
        if not cleaned.strip():
            return {
                'success': False,
                'error': 'Complaint text contains only stopwords or symbols. Please provide more descriptive text.'
            }

        # Keep inference compatible with artifacts trained before normalized
        # tags preserved underscores in their displayed form.
        model_text = cleaned
        for tag in re.findall(r'<[a-z]+_[a-z]+>', cleaned):
            if tag[1:-1] not in self.vectorizer.vocabulary_:
                model_text = model_text.replace(tag, tag[1:-1].replace('_', ' '))

        # Vectorize using saved TF-IDF vectorizer
        X_vec = self.vectorizer.transform([model_text])
        model = self.models[model_key]

        predicted_category = model.predict(X_vec)[0]

        display_text = re.sub(r'<[^>]+>', ' ', cleaned)
        display_text = ' '.join(display_text.split())

        return {
            'success': True,
            'category': predicted_category,
            'model_name': self.model_names.get(model_key, model_key),
            'model_key': model_key,
            'cleaned_text': display_text,
            'original_text': text
        }

