from prediction import ComplaintPredictor

predictor = ComplaintPredictor()
test_inputs = [
    "My payment was deducted, but my order was not confirmed.",
    "I paid for my order, but the amount was deducted and my order is still showing as unpaid.",
    "Can you please change my delivery shipping address?",
    "I want a refund for the damaged product I received.",
    "I forgot my account password and cannot log in."
]

for model_key in ['naive_bayes', 'logistic_regression', 'linear_svm']:
    print(f"=== Testing Model: {model_key} ===")
    for text in test_inputs:
        res = predictor.predict(text, model_key)
        print(f"Text: '{text[:45]}...' -> Category: {res.get('category')} (Conf: {res.get('confidence_percent')})")
    print()

