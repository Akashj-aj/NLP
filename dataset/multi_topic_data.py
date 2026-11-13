# 110 Realistic Multi-Topic Training Examples across all 11 Categories
# Format: (instruction, category, intent)

MULTI_TOPIC_TRAINING_DATA = [
    # 1. REFUND (10 examples with contextual order/payment details)
    ("I want a refund for the damaged product I received. And the order ID is 268824 and I made the payment through online with the UPI ID 335i39iq9935.", "REFUND", "get_refund"),
    ("Please process a full refund for purchase ORD-88912 because the item arrived broken, I paid via debit card.", "REFUND", "get_refund"),
    ("I need my money back for order 992831, the shirt size is wrong and I want reimbursement to my credit card.", "REFUND", "get_refund"),
    ("When will my refund be credited for canceled order #55123? It has been 5 business days since the cancellation.", "REFUND", "track_refund"),
    ("Can I get a refund for order ref 7721? The delivery was delayed by two weeks so I returned it.", "REFUND", "get_refund"),
    ("I returned the package for order ID 881234 yesterday, please confirm when the refunded amount will reflect in my bank account.", "REFUND", "track_refund"),
    ("The seller sent the wrong product for order #44192. I request an immediate refund back to my UPI wallet.", "REFUND", "get_refund"),
    ("I want a refund for order 12984, the box was torn open and items were missing, transaction was completed online.", "REFUND", "get_refund"),
    ("Kindly check the refund status for order 39912, my payment was made via netbanking and funds are not reversed yet.", "REFUND", "track_refund"),
    ("I am entitled to a refund under your policy for order #88219 because the package never reached my address.", "REFUND", "get_refund"),

    # 2. PAYMENT (10 examples with order/gateway context)
    ("My payment was deducted at checkout, but my order was not confirmed on the confirmation screen.", "PAYMENT", "payment_issue"),
    ("I paid for my order with UPI ID user@upi, but the payment gateway timed out and money was debited.", "PAYMENT", "payment_issue"),
    ("My credit card was charged twice for transaction TXN9912, please fix this duplicate billing deduction.", "PAYMENT", "payment_issue"),
    ("The payment went through on my netbanking app for order 22194, but your portal shows payment failed.", "PAYMENT", "payment_issue"),
    ("Amount of $85 was deducted from my account, but no payment receipt or order reference was generated.", "PAYMENT", "payment_issue"),
    ("I was billed twice on my debit card statement for one checkout attempt, transaction ID 441029.", "PAYMENT", "payment_issue"),
    ("Why is your payment gateway rejecting my mastercard during checkout for order #99281?", "PAYMENT", "payment_issue"),
    ("Money left my bank account via Google Pay, but the merchant portal says payment not received.", "PAYMENT", "payment_issue"),
    ("My wallet balance was deducted during payment verification, but the system displayed an authentication error.", "PAYMENT", "payment_issue"),
    ("I have an unauthorized charge on my credit card from your website for $120, please investigate the transaction.", "PAYMENT", "payment_issue"),

    # 3. ORDER (10 examples with payment / cancellation / tracking context)
    ("I placed order 994812 yesterday, can you tell me the current dispatch and processing status?", "ORDER", "track_order"),
    ("I need to cancel order ID 77234 before it ships out, please do not dispatch this package.", "ORDER", "cancel_order"),
    ("Can you check if my order #88231 was successfully registered? My screen froze right after clicking buy.", "ORDER", "track_order"),
    ("I want to change the items in order 44192, can I add another quantity before fulfillment?", "ORDER", "change_order"),
    ("Please cancel my recent order #12093, I selected the wrong color variant during checkout.", "ORDER", "cancel_order"),
    ("Where is order number 33912 currently located in your fulfillment center?", "ORDER", "track_order"),
    ("I placed an order earlier today, but I cannot see purchase #99182 under my active orders list.", "ORDER", "track_order"),
    ("Can I modify the order details for order ID 44819 before it gets dispatched to courier?", "ORDER", "change_order"),
    ("I want to stop and cancel purchase order 88310 immediately, I no longer need these products.", "ORDER", "cancel_order"),
    ("Please confirm whether order #66219 has been packed and scheduled for courier pickup.", "ORDER", "track_order"),

    # 4. DELIVERY (10 examples with order / address / schedule context)
    ("My package for order #29918 is delayed, can you provide the updated delivery arrival date?", "DELIVERY", "track_order"),
    ("The courier tracking indicates package delivered for order 88219, but I have not received it at my doorstep.", "DELIVERY", "track_order"),
    ("When will the delivery agent arrive with order ID 44120? I need an estimated delivery window.", "DELIVERY", "track_order"),
    ("My parcel for order #10928 has been stuck at the local delivery hub for three days without movement.", "DELIVERY", "track_order"),
    ("Can I schedule the delivery time for order 88123 to tomorrow afternoon after 3 PM?", "DELIVERY", "track_order"),
    ("The delivery boy called but did not deliver my parcel for order #55192, please check with logistics.", "DELIVERY", "track_order"),
    ("Why is my delivery shipment for order 77123 showing delayed in transit?", "DELIVERY", "track_order"),
    ("I was home all day, but the delivery driver marked order 33192 as delivery attempted failed.", "DELIVERY", "track_order"),
    ("Please expedite the delivery of order #99482, it is a birthday gift needed by Friday.", "DELIVERY", "track_order"),
    ("The courier left order 88190 outside in the rain and the outer carton was soaked.", "DELIVERY", "track_order"),

    # 5. SHIPPING (10 examples with shipping address / shipping method context)
    ("I need to update my shipping address for order #44918 because I moved to a new apartment.", "SHIPPING", "change_shipping_address"),
    ("Can you change the shipping destination address for order ID 88231 before it leaves the warehouse?", "SHIPPING", "change_shipping_address"),
    ("I entered the wrong postal pin code during checkout for order 19924, please correct my shipping address.", "SHIPPING", "change_shipping_address"),
    ("How do I switch to express shipping for my order #55192? Standard shipping is too slow.", "SHIPPING", "check_shipping_options"),
    ("Do you offer international shipping to Canada for items in order 88210?", "SHIPPING", "check_shipping_options"),
    ("Please update the street number on the shipping label for order #33918 immediately.", "SHIPPING", "change_shipping_address"),
    ("What are the available courier shipping methods and delivery speeds for my location?", "SHIPPING", "check_shipping_options"),
    ("I want to change the delivery address for order 77129 to my office address instead.", "SHIPPING", "change_shipping_address"),
    ("Is overnight shipping available for order #66219 if I pay the extra freight fee?", "SHIPPING", "check_shipping_options"),
    ("Can I change the recipient contact number and shipping address on order 12903?", "SHIPPING", "change_shipping_address"),

    # 6. CANCEL (10 examples with cancellation requests and reasons)
    ("I want to cancel my entire order purchase immediately, please do not process it.", "CANCEL", "cancel_order"),
    ("Please cancel my subscription membership starting from next billing cycle.", "CANCEL", "cancel_order"),
    ("I need to cancel this order because I found a cheaper alternative elsewhere.", "CANCEL", "cancel_order"),
    ("Kindly cancel order #99281, I placed it accidentally while browsing.", "CANCEL", "cancel_order"),
    ("How do I cancel my pending order request before the seller confirms it?", "CANCEL", "cancel_order"),
    ("Cancel order #44192 right now, I do not want to proceed with this purchase.", "CANCEL", "cancel_order"),
    ("I want to revoke and cancel my booking order #88210 as soon as possible.", "CANCEL", "cancel_order"),
    ("Please terminate and cancel order 55193, I have changed my mind.", "CANCEL", "cancel_order"),
    ("I am requesting the immediate cancellation of purchase order #33912.", "CANCEL", "cancel_order"),
    ("Can customer support please cancel my order #77128 from your system?", "CANCEL", "cancel_order"),

    # 7. INVOICE (10 examples with tax / invoice / receipt details)
    ("I need a copy of the tax invoice for order #44129 for my corporate accounting records.", "INVOICE", "check_invoice"),
    ("Can you email me the official VAT invoice and receipt for order ID 88192?", "INVOICE", "check_invoice"),
    ("There is a pricing mistake on invoice #INV-9921, the sales tax was calculated incorrectly.", "INVOICE", "check_invoice"),
    ("Where can I download the GST invoice and billing statement for purchase 33190?", "INVOICE", "check_invoice"),
    ("I did not receive an itemized invoice with my parcel for order #66129.", "INVOICE", "check_invoice"),
    ("Please correct the billing name and company tax registration number on invoice 88214.", "INVOICE", "check_invoice"),
    ("Can you provide the commercial invoice for order 77120 needed for customs clearance?", "INVOICE", "check_invoice"),
    ("The invoice total on order #99182 does not match the final checkout summary, please review it.", "INVOICE", "check_invoice"),
    ("How do I access and print previous monthly invoices from my billing portal?", "INVOICE", "check_invoice"),
    ("I need an updated invoice showing the payment completion stamp for order 55219.", "INVOICE", "check_invoice"),

    # 8. ACCOUNT (10 examples with login / password / profile details)
    ("I forgot my account login password and the reset link is not arriving in my inbox.", "ACCOUNT", "recover_password"),
    ("I cannot log into my customer account, the system says invalid email or credentials.", "ACCOUNT", "recover_password"),
    ("How can I change the registered email address and mobile number on my account profile?", "ACCOUNT", "edit_account"),
    ("My account has been locked due to multiple incorrect password attempts, please unlock it.", "ACCOUNT", "recover_password"),
    ("I want to update my profile information and save a new default address on my account.", "ACCOUNT", "edit_account"),
    ("Can you help me enable two factor authentication for my user account security?", "ACCOUNT", "edit_account"),
    ("I want to delete my account and permanently remove all my stored personal data.", "ACCOUNT", "delete_account"),
    ("Why is my account deactivated? I cannot view my order history or saved settings.", "ACCOUNT", "edit_account"),
    ("Please assist me in recovering access to my account associated with email user@example.com.", "ACCOUNT", "recover_password"),
    ("I need to update my account username and security questions on my customer profile.", "ACCOUNT", "edit_account"),

    # 9. CONTACT (10 examples requesting representative / human support)
    ("Can I speak with a live human customer support representative right now?", "CONTACT", "contact_human_agent"),
    ("Please provide your customer service helpline telephone number and operating hours.", "CONTACT", "contact_customer_service"),
    ("I have an urgent issue and need to connect with an customer support supervisor directly.", "CONTACT", "contact_human_agent"),
    ("Is there a toll free phone number where I can talk to an agent regarding my issue?", "CONTACT", "contact_customer_service"),
    ("Transfer my chat session to a real human agent, the automated answers are not helpful.", "CONTACT", "contact_human_agent"),
    ("What is the official email address to reach your customer care escalations team?", "CONTACT", "contact_customer_service"),
    ("Can someone from customer support call me back on my phone number +1-800-555-0199?", "CONTACT", "contact_customer_service"),
    ("I want to contact your head office support department regarding unresolved complaints.", "CONTACT", "contact_customer_service"),
    ("Connect me with live chat support agent immediately to resolve this matter.", "CONTACT", "contact_human_agent"),
    ("How can I get in touch with a customer service executive over phone?", "CONTACT", "contact_customer_service"),

    # 10. FEEDBACK (10 examples with reviews / ratings / complaints on service)
    ("I want to submit positive feedback for agent Sarah who helped me resolve my issue today.", "FEEDBACK", "leave_feedback"),
    ("Your mobile application keeps crashing during checkout, please fix this terrible user experience.", "FEEDBACK", "leave_feedback"),
    ("I had an extremely disappointing experience with your courier service and want to register a formal complaint.", "FEEDBACK", "leave_feedback"),
    ("Great customer service! The replacement product arrived quickly and in perfect condition.", "FEEDBACK", "leave_feedback"),
    ("Where can I leave a product review and rate the service quality of my recent purchase?", "FEEDBACK", "leave_feedback"),
    ("I want to complain about the rude behavior of the delivery personnel who brought my order.", "FEEDBACK", "leave_feedback"),
    ("Your website interface is very slow and difficult to navigate on mobile devices.", "FEEDBACK", "leave_feedback"),
    ("I appreciate how fast your team responded to my inquiry, thank you for the excellent support.", "FEEDBACK", "leave_feedback"),
    ("I want to lodge a complaint regarding misleading product descriptions on your catalog page.", "FEEDBACK", "leave_feedback"),
    ("Submitting feedback: the packaging quality has degraded significantly compared to last year.", "FEEDBACK", "leave_feedback"),

    # 11. SUBSCRIPTION (10 examples with recurring billing / membership details)
    ("I want to cancel my premium monthly subscription so it does not auto renew next month.", "SUBSCRIPTION", "cancel_order"),
    ("How do I upgrade my subscription plan from basic tier to family annual membership?", "SUBSCRIPTION", "change_order"),
    ("Why was my credit card charged for an annual subscription renewal without prior notice?", "SUBSCRIPTION", "track_order"),
    ("Please pause my subscription membership for two months while I am traveling abroad.", "SUBSCRIPTION", "change_order"),
    ("When does my current free trial subscription end and when will the paid billing start?", "SUBSCRIPTION", "track_order"),
    ("I want to switch my subscription billing cycle from monthly payments to annual discount billing.", "SUBSCRIPTION", "change_order"),
    ("Can I get a pro-rated refund for the remaining months of my canceled annual subscription?", "SUBSCRIPTION", "cancel_order"),
    ("My subscription perks are not showing as active even though my monthly payment was charged.", "SUBSCRIPTION", "track_order"),
    ("How can I reactivate my expired subscription membership on my account?", "SUBSCRIPTION", "change_order"),
    ("Please unsubscribe me from the recurring newsletter and VIP membership tier immediately.", "SUBSCRIPTION", "cancel_order")
]

