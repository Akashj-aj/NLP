import os
import sys
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)

from preprocessing import preprocess_text

# ---------------------------------------------------------------------------
# Import multi-topic training data (110 realistic multi-topic examples,
# 10 per category across all 11 categories)
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dataset'))
from multi_topic_data import MULTI_TOPIC_TRAINING_DATA


def build_challenge_set():
    """Load the 33-sample OOD challenge set from dataset/challenge_dataset.py."""
    from challenge_dataset import CHALLENGE_DATASET
    return CHALLENGE_DATASET


def train_and_evaluate():
    orig_path    = os.path.join('dataset', 'customer_support_original_backup.csv')
    combined_path = os.path.join('dataset', 'customer_support.csv')

    if not os.path.exists(orig_path):
        raise FileNotFoundError(f"Original backup dataset not found at {orig_path}.")
    if not os.path.exists(combined_path):
        raise FileNotFoundError(f"Combined dataset not found at {combined_path}.")

    # ------------------------------------------------------------------
    # 1. Load & clean the original backup (26,872 raw rows → ~24,635 after dedup)
    # ------------------------------------------------------------------
    print(f"Loading original dataset from {orig_path}...")
    df_orig = pd.read_csv(orig_path)
    df_orig = df_orig[['instruction', 'category']].copy()
    df_orig.dropna(subset=['instruction', 'category'], inplace=True)
    df_orig = df_orig[df_orig['instruction'].astype(str).str.strip() != '']
    df_orig = df_orig[df_orig['category'].astype(str).str.strip() != '']
    df_orig.drop_duplicates(subset=['instruction'], inplace=True)
    df_orig['cleaned_text'] = df_orig['instruction'].apply(preprocess_text)
    df_orig = df_orig[df_orig['cleaned_text'].str.strip() != '']
    print(f"Original clean records: {len(df_orig)}")

    # ------------------------------------------------------------------
    # 2. Reproduce the exact original 80:20 stratified split (random_state=42)
    #    — locks the 4,927 holdout test samples permanently
    # ------------------------------------------------------------------
    X_orig   = df_orig['cleaned_text'].values
    y_orig   = df_orig['category'].values
    instr_orig = df_orig['instruction'].values

    X_train_orig, X_test, y_train_orig, y_test, instr_train_orig, instr_test = train_test_split(
        X_orig, y_orig, instr_orig,
        test_size=0.20, random_state=42, stratify=y_orig
    )

    print(f"Original 80:20 partition → Train: {len(X_train_orig)}, Test: {len(X_test)}")
    assert len(X_test)        == 4927,  f"Expected 4,927 test samples, found {len(X_test)}"
    assert len(X_train_orig)  == 19708, f"Expected 19,708 train samples, found {len(X_train_orig)}"

    # ------------------------------------------------------------------
    # 3. Extract the 60 hand-written augmented examples from customer_support.csv
    #    (rows present in combined but NOT in original backup)
    # ------------------------------------------------------------------
    df_combined = pd.read_csv(combined_path)
    df_combined = df_combined[['instruction', 'category']].copy()
    df_combined.dropna(subset=['instruction', 'category'], inplace=True)
    df_combined = df_combined[df_combined['instruction'].astype(str).str.strip() != '']
    df_combined = df_combined[df_combined['category'].astype(str).str.strip() != '']
    df_combined.drop_duplicates(subset=['instruction'], inplace=True)

    orig_instructions_set = set(df_orig['instruction'])
    df_aug60 = df_combined[~df_combined['instruction'].isin(orig_instructions_set)].copy()
    print(f"Extracted 60-example augmentation: {len(df_aug60)}")
    assert len(df_aug60) == 60, f"Expected exactly 60 augmentation examples, found {len(df_aug60)}"

    df_aug60['cleaned_text'] = df_aug60['instruction'].apply(preprocess_text)

    # ------------------------------------------------------------------
    # 4. Prepare the 110 multi-topic examples
    #    (realistic multi-clause complaints, imported from multi_topic_data.py)
    # ------------------------------------------------------------------
    df_multi = pd.DataFrame(MULTI_TOPIC_TRAINING_DATA, columns=['instruction', 'category'])
    df_multi['cleaned_text'] = df_multi['instruction'].apply(preprocess_text)
    df_multi = df_multi[df_multi['cleaned_text'].str.strip() != '']
    print(f"Multi-topic training examples: {len(df_multi)}")

    # ------------------------------------------------------------------
    # 5. Combine: original training + 60 augmented + 110 multi-topic
    #    All augmentation goes into training ONLY — zero test leakage
    # ------------------------------------------------------------------
    X_aug60   = df_aug60['cleaned_text'].values
    y_aug60   = df_aug60['category'].values
    X_multi   = df_multi['cleaned_text'].values
    y_multi   = df_multi['category'].values

    X_train = np.concatenate([X_train_orig, X_aug60, X_multi])
    y_train = np.concatenate([y_train_orig, y_aug60, y_multi])

    total_aug = len(X_aug60) + len(X_multi)
    print(
        f"Final partition → Train: {len(X_train)} "
        f"({len(X_train_orig)} original + {total_aug} augmented), "
        f"Test: {len(X_test)} (strictly original holdout)"
    )
    assert len(X_train) == 19878, f"Expected 19,878 training samples, got {len(X_train)}"
    assert len(X_test)  == 4927,  f"Expected 4,927 testing samples, got {len(X_test)}"

    # Verify zero test-set leakage
    test_instr_set = set(instr_test)
    for label, instr in [("60-aug", set(df_aug60['instruction'])),
                          ("110-multi", set(df_multi['instruction']))]:
        overlap = test_instr_set.intersection(instr)
        assert len(overlap) == 0, f"Leakage detected in {label}: {len(overlap)} samples in test set!"

    labels = sorted(list(set(y_train).union(set(y_test))))

    # ------------------------------------------------------------------
    # 6. TF-IDF Vectorizer — ngram_range (1,3), max_features 15,000
    #    Fitted on training data ONLY; test data only transformed.
    # ------------------------------------------------------------------
    print("Fitting TF-IDF Vectorizer (ngram_range=(1,3), max_features=15000, sublinear_tf=True)...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=15000,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf  = vectorizer.transform(X_test)

    # ------------------------------------------------------------------
    # 7. Models
    # ------------------------------------------------------------------
    models = {
        'naive_bayes': {
            'display_name': 'Multinomial Naive Bayes',
            'model': MultinomialNB(alpha=0.1)
        },
        'logistic_regression': {
            'display_name': 'Logistic Regression',
            'model': LogisticRegression(max_iter=1000, random_state=42, C=2.0)
        },
        'linear_svm': {
            'display_name': 'Linear Support Vector Machine',
            'model': LinearSVC(random_state=42, C=1.0)
        }
    }

    results = {
        'categories': labels,
        'dataset_stats': {
            'total_samples':              int(len(X_train) + len(X_test)),
            'train_samples':              int(len(X_train)),
            'test_samples':              int(len(X_test)),
            'augmented_samples_in_train': int(total_aug),
            'challenge_samples':          33,
            'num_categories':             int(len(labels)),
        },
        'models': {}
    }

    os.makedirs('models', exist_ok=True)

    # Save vectorizer
    vectorizer_path = os.path.join('models', 'tfidf_vectorizer.pkl')
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Saved TF-IDF vectorizer to {vectorizer_path}")

    best_model_key = None
    best_f1 = -1.0

    for key, item in models.items():
        name = item['display_name']
        clf  = item['model']
        print(f"\n--- Training {name} ---")
        clf.fit(X_train_tfidf, y_train)

        y_pred = clf.predict(X_test_tfidf)

        acc  = float(accuracy_score(y_test, y_pred))
        prec = float(precision_score(y_test, y_pred, average='macro', zero_division=0))
        rec  = float(recall_score(y_test,  y_pred, average='macro', zero_division=0))
        f1   = float(f1_score(y_test,  y_pred, average='macro', zero_division=0))
        cm   = confusion_matrix(y_test, y_pred, labels=labels).tolist()
        report = classification_report(y_test, y_pred, labels=labels,
                                       output_dict=True, zero_division=0)

        print(f"{name}: Accuracy={acc:.4f}, Precision={prec:.4f}, Recall={rec:.4f}, F1={f1:.4f}")

        model_save_path = os.path.join('models', f"{key}.pkl")
        joblib.dump(clf, model_save_path)
        print(f"Saved model to {model_save_path}")

        results['models'][key] = {
            'name':             name,
            'key':              key,
            'accuracy':         round(acc,  4),
            'precision':        round(prec, 4),
            'recall':           round(rec,  4),
            'f1_score':         round(f1,   4),
            'confusion_matrix': cm,
            'category_metrics': {
                cat: {
                    'precision': round(report[cat]['precision'], 4),
                    'recall':    round(report[cat]['recall'],    4),
                    'f1-score':  round(report[cat]['f1-score'],  4),
                    'support':   int(report[cat]['support'])
                }
                for cat in labels if cat in report
            }
        }

        if f1 > best_f1:
            best_f1 = f1
            best_model_key = key

    results['best_model'] = best_model_key
    print(f"\nBest model (macro F1): {models[best_model_key]['display_name']} (F1={best_f1:.4f})")

    # ------------------------------------------------------------------
    # 8. Challenge set evaluation
    # ------------------------------------------------------------------
    try:
        challenge_data = build_challenge_set()
        ch_texts  = [preprocess_text(item['complaint']) for item in challenge_data]
        ch_labels = [item['expected_category'] for item in challenge_data]
        X_ch = vectorizer.transform(ch_texts)

        challenge_results = {}
        for key, item in models.items():
            clf = item['model']
            ch_pred = clf.predict(X_ch)
            ch_acc = float(accuracy_score(ch_labels, ch_pred))
            ch_f1  = float(f1_score(ch_labels, ch_pred, average='macro', zero_division=0))
            challenge_results[key] = {
                'accuracy': round(ch_acc, 4),
                'macro_f1': round(ch_f1,  4),
                'prompt_case_1': clf.predict(vectorizer.transform([
                    preprocess_text("I want a refund for the damaged product I received.")
                ]))[0],
                'prompt_case_2': clf.predict(vectorizer.transform([
                    preprocess_text(
                        "I want a refund for the damaged product I received. "
                        "And the order ID is 268824 and I made the payment through online with the UPI ID 335i39iq9935."
                    )
                ]))[0],
                'prompt_case_3': clf.predict(vectorizer.transform([
                    preprocess_text(
                        "I want a refund for the damaged product I received. "
                        "And the order ID is 268824 and I made the transaction through online with the UPI ID 335i39iq9935."
                    )
                ]))[0],
            }
            print(f"Challenge [{item['display_name']}]: Accuracy={ch_acc:.4f}, Macro F1={ch_f1:.4f}")

        results['challenge_results'] = challenge_results
    except Exception as e:
        print(f"Warning: challenge set evaluation skipped — {e}")

    # ------------------------------------------------------------------
    # 9. Save evaluation results
    # ------------------------------------------------------------------
    eval_json_path = os.path.join('models', 'evaluation_results.json')
    with open(eval_json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved evaluation results to {eval_json_path}")

    return results


if __name__ == '__main__':
    train_and_evaluate()
