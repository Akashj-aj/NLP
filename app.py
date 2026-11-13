import os
from flask import Flask, render_template, request, jsonify
from prediction import ComplaintPredictor
from evaluation import load_evaluation_results, get_comparison_table

app = Flask(__name__)
predictor = ComplaintPredictor()

@app.route('/')
def index():
    eval_data = load_evaluation_results()
    best_model = eval_data.get('best_model', 'logistic_regression') if eval_data else 'logistic_regression'
    categories = eval_data.get('categories', []) if eval_data else []
    return render_template('index.html', best_model=best_model, categories=categories)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(silent=True)
        if not data:
            data = request.form

        text = data.get('text', '')
        model_key = data.get('model', 'logistic_regression')

        result = predictor.predict(text, model_key)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'An unexpected error occurred during prediction: {str(e)}'
        }), 500

@app.route('/comparison')
def comparison():
    eval_data = load_evaluation_results()
    comparison_table = get_comparison_table()
    return render_template(
        'comparison.html',
        eval_data=eval_data,
        comparison_table=comparison_table
    )

@app.route('/api/evaluation')
def api_evaluation():
    eval_data = load_evaluation_results()
    if not eval_data:
        return jsonify({'error': 'Evaluation results not available yet. Please train models first.'}), 404
    return jsonify(eval_data)

@app.route('/about')
def about():
    eval_data = load_evaluation_results()
    stats = eval_data.get('dataset_stats', {}) if eval_data else {}
    return render_template('about.html', stats=stats)

if __name__ == '__main__':
    # Flask development server
    app.run(host='127.0.0.1', port=5000, debug=True)

