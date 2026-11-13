import json
import os

def load_evaluation_results(results_path=None):
    """
    Load actual model evaluation metrics saved during training.
    """
    if results_path is None:
        results_path = os.path.join(os.path.dirname(__file__), 'models', 'evaluation_results.json')
    
    if not os.path.exists(results_path):
        return None
    
    with open(results_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_comparison_table():
    """
    Format evaluation results into a clean list of model summaries.
    """
    data = load_evaluation_results()
    if not data:
        return []
    
    models = []
    best_key = data.get('best_model')
    for key, info in data.get('models', {}).items():
        models.append({
            'key': key,
            'name': info.get('name'),
            'accuracy': info.get('accuracy'),
            'precision': info.get('precision'),
            'recall': info.get('recall'),
            'f1_score': info.get('f1_score'),
            'is_best': key == best_key
        })
    return models

