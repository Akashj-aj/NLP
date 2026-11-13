import re

NEGATION_WORDS = {
    'not', 'no', 'nor', 'neither', 'never', 'none',
    'cannot', "can't", "don't", "didn't", "doesn't",
    "won't", "wouldn't", "shouldn't", "couldn't",
    "isn't", "aren't", "wasn't", "weren't", "haven't",
    "hasn't", "hadn't"
}

CONTRACTIONS = {
    "can't": "cannot",
    "won't": "will not",
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'d": " would",
    "'ll": " will",
    "'t": " not",
    "'ve": " have",
    "'m": " am"
}

def get_custom_stopwords():
    try:
        from nltk.corpus import stopwords
        nltk_stopwords = set(stopwords.words('english'))
    except Exception:
        nltk_stopwords = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
            "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
            'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
            'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
            'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
            'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
            'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
            'about', 'against', 'between', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
            'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will',
            'just', 'should', "now"
        }
    return nltk_stopwords - NEGATION_WORDS

def normalize_identifiers(text: str) -> str:
    """
    Normalizes metadata identifiers, reference numbers, UPI IDs, emails, URLs, and phone numbers.
    Also collapses composite ID references (e.g. 'order id ORD123', 'payment through online with the upi id 335i39iq9935')
    into standardized neutral tokens so arbitrary codes do not distort classification.
    """
    if not isinstance(text, str):
        return ""

    # 1. URLs
    text = re.sub(r'https?://\S+|www\.\S+', ' <url> ', text)

    # 2. Template placeholders from Bitext, e.g. {{Order Number}}, {{Email}}, etc.
    text = re.sub(r'\{\{[^}]+\}\}', ' <ref_id> ', text)

    # 3. Contextual Order ID mentions — MUST have an actual code after the keyword.
    # e.g. "order ID 268824", "order number ORD-9923", "tracking number 12345678"
    # Does NOT match bare "my order" or "order is unpaid" (no code follows).
    text = re.sub(
        r'\b(?:order|tracking|ticket|invoice|booking)\s*(?:id|number|no|#)\s*(?:is|was)?\s*[:#-]?\s*[A-Za-z0-9\-_]{4,}\b',
        ' <order_id> ', text, flags=re.IGNORECASE
    )
    # Also catch patterns where ID/# comes first: "ID: ORD-99234"
    text = re.sub(
        r'(?<!payment )(?<!transaction )(?<!reference )(?<!ref )\b(?:id|no|#)\s*[:#-]?\s*[A-Za-z]{0,3}\d{4,}[A-Za-z0-9\-_]*\b',
        ' <order_id> ', text, flags=re.IGNORECASE
    )

    # 4. Contextual Transaction / UPI ID mentions:
    # e.g. "UPI ID 335i39iq9935", "payment through online with the UPI ID 335i39iq9935", "transaction ID 992834"
    text = re.sub(r'\b(?:payment\s+(?:through|via|using)?\s*)?(?:online\s+with\s+(?:the\s+)?)?upi\s*(?:id|ref)?\s*(?:is|was)?\s*[:#-]?\s*[A-Za-z0-9\-_@\.]{4,}\b', ' <upi_id> ', text, flags=re.IGNORECASE)
    text = re.sub(
        r'\b(?:(?:transaction|payment)\s+(?:id|number|no|ref)|reference|utr)'
        r'\s*(?:is|was)?\s*[:#-]?\s*[A-Za-z0-9\-_]{4,}\b',
        ' <txn_id> ',
        text,
        flags=re.IGNORECASE
    )

    # 5. Direct UPI handles (e.g., user@okhdfcbank, name@upi)
    text = re.sub(r'\b[\w\.\-]+@(?:upi|okhdfcbank|okaxis|oksbi|okicici|paytm|ybl|ibl|axl)\b', ' <upi_id> ', text, flags=re.IGNORECASE)

    # 6. Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ' <email> ', text)

    # 7. Phone numbers
    text = re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', ' <phone> ', text)

    # 8. Isolated alphanumeric / long numeric codes (4+ digits)
    text = re.sub(r'\b[A-Za-z]*\d{4,}[A-Za-z0-9]*\b', ' <num_code> ', text)

    # 9. Currency amounts (e.g., $50, USD 100, Rs. 500, 50 dollars)
    text = re.sub(r'(?:[\$\€\£\₹]|rs\.?|inr|usd)\s*\d+(?:\.\d{1,2})?', ' <amount> ', text, flags=re.IGNORECASE)
    text = re.sub(r'\b\d+(?:\.\d{1,2})?\s*(?:dollars?|rupees?|bucks?|cents?|euros?)\b', ' <amount> ', text, flags=re.IGNORECASE)

    return text

def preprocess_text(text: str) -> str:
    """
    Standardized NLP Preprocessing pipeline:
    1. Normalize identifiers, references, UPI, emails, phone numbers.
    2. Expand common contractions.
    3. Lowercase.
    4. Remove punctuation while preserving special tokens (<order_id>, etc.) and word characters.
    5. Filter stopwords while strictly preserving negation tokens.
    """
    if not isinstance(text, str):
        return ""

    # 1. Normalize non-informative identifiers
    text = normalize_identifiers(text)

    # 2. Lowercase
    text = text.lower()

    # 3. Expand contractions
    for contraction, expansion in CONTRACTIONS.items():
        text = text.replace(contraction, expansion)

    # 4. Clean symbols (preserve alphanumeric and placeholder angle brackets for tokens)
    text = re.sub(r"[^a-z0-9_<>'\s]", ' ', text)

    # 5. Tokenize
    tokens = text.split()

    # 6. Filter stopwords while preserving negation words and normalized tags
    stop_words = get_custom_stopwords()
    cleaned_tokens = [
        t for t in tokens 
        if (t not in stop_words or t in NEGATION_WORDS) and (len(t) > 1 or t in {'no'})
    ]

    return " ".join(cleaned_tokens)
