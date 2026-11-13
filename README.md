# Complaint AI

Complaint AI is a Flask web application that classifies customer support complaints into 11 categories using TF-IDF features and three scikit-learn models:

- Multinomial Naive Bayes
- Logistic Regression
- Linear Support Vector Machine

## Features

- Complaint classification through a browser interface
- Preprocessed token display
- Model comparison metrics and confusion matrices
- Sample complaints for all supported categories

## Supported categories

`ACCOUNT`, `CANCEL`, `CONTACT`, `DELIVERY`, `FEEDBACK`, `INVOICE`, `ORDER`, `PAYMENT`, `REFUND`, `SHIPPING`, and `SUBSCRIPTION`.

## Run locally

Use Python 3.10 or newer:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open http://127.0.0.1:5000 in a browser.

The trained model artifacts are included in `models/`, so the application can run without retraining.

## Deployment

This is a Python Flask application and is best deployed as a web service on Render, Railway, or PythonAnywhere. For Render, use:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

The `models/` directory must be included in the deployed project.

## Project structure

```text
app.py                 Flask routes and application entry point
prediction.py          Model loading and prediction logic
preprocessing.py       Text normalization and preprocessing
evaluation.py          Evaluation data helpers
train_models.py        Model training and evaluation script
models/                Saved vectorizer, models, and metrics
dataset/               Training and challenge data
templates/             Flask HTML templates
static/                CSS and JavaScript assets
```
