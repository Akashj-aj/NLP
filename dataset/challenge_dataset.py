# Challenge evaluation dataset containing realistic multi-topic customer complaints with mixed keywords
# Total: 33 diverse examples (3 per category across all 11 categories)

CHALLENGE_TEST_CASES = [
    # REFUND with order, payment, and item details
    ("I want a refund for the damaged product I received. And the order ID is 268824 and I made the payment through online with the UPI ID 335i39iq9935.", "REFUND"),
    ("I want a refund for the damaged product I received. And the order ID is 268824 and I made through online with the UPI ID 335i39iq9935.", "REFUND"),
    ("I sent back the returned package for order #99214 yesterday, when will my refund be processed back to my card?", "REFUND"),

    # PAYMENT with order and cart context
    ("My payment was deducted, but my order was not confirmed on the checkout page.", "PAYMENT"),
    ("I paid for my order through Google Pay, but the payment gateway timed out and my bank was debited.", "PAYMENT"),
    ("My credit card was charged twice for transaction ref #88219, please rectify the double deduction.", "PAYMENT"),

    # ORDER with payment and delivery mentions
    ("I placed an order yesterday and payment was deducted, but I want to cancel it before it gets shipped.", "ORDER"),
    ("Can you check the current status of order ID 881293? I completed checkout this morning.", "ORDER"),
    ("I want to add another item to my order #33190 before fulfillment begins, is that possible?", "ORDER"),

    # DELIVERY with delayed arrival or tracking code
    ("My package for order #44918 is delayed and I want to know when it will arrive at my address.", "DELIVERY"),
    ("The courier tracking states parcel delivered, but no one arrived at my doorstep.", "DELIVERY"),
    ("Can I change the delivery time window for package #88219 to tomorrow afternoon?", "DELIVERY"),

    # SHIPPING with address modification
    ("I need to update my delivery shipping address for order #55120 because I entered the wrong apartment number.", "SHIPPING"),
    ("Can you change the courier shipping method for my order to express air delivery?", "SHIPPING"),
    ("Is international shipping available to Australia for products in purchase #99182?", "SHIPPING"),

    # CANCEL with reasons
    ("Please cancel my order #77124 immediately, I no longer want this item.", "CANCEL"),
    ("I want to cancel my purchase right now before the merchant processes it.", "CANCEL"),
    ("Kindly cancel order #33190, I found the same item at a local store.", "CANCEL"),

    # INVOICE with tax / business details
    ("I need an official GST tax invoice for order #44192 for my business reimbursement claim.", "INVOICE"),
    ("Can you email me the itemized purchase receipt and invoice for order ID 88192?", "INVOICE"),
    ("There is a calculation error on the sales tax shown on invoice #INV-55120.", "INVOICE"),

    # ACCOUNT with credential / profile issues
    ("I forgot my account login password and cannot access my saved order history.", "ACCOUNT"),
    ("My customer profile account was locked due to incorrect password attempts, please help me unlock it.", "ACCOUNT"),
    ("How can I update my registered email address and phone number on my account profile?", "ACCOUNT"),

    # CONTACT asking for live assistance
    ("Can I speak with a live human customer support representative over the phone right now?", "CONTACT"),
    ("Please connect me with a human agent, the automated chat bot is not understanding my question.", "CONTACT"),
    ("What is your customer service helpline telephone number and email address?", "CONTACT"),

    # FEEDBACK reviews on experience
    ("I want to register a formal complaint regarding the rude behavior of your delivery executive.", "FEEDBACK"),
    ("Your mobile application interface keeps freezing during payment checkout, please improve it.", "FEEDBACK"),
    ("Excellent customer service from agent David today, thank you for resolving my issue so quickly!", "FEEDBACK"),

    # SUBSCRIPTION renewal and cancellation
    ("I want to cancel my monthly premium subscription before it auto renews next week.", "SUBSCRIPTION"),
    ("Why was my credit card billed for an annual membership subscription renewal without my consent?", "SUBSCRIPTION"),
    ("Can I switch my recurring subscription plan from basic tier to premium family tier?", "SUBSCRIPTION")
]

