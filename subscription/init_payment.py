from django.http import HttpResponseRedirect, JsonResponse
import requests
import random
import json
from django.shortcuts import render, redirect, get_object_or_404
from subscription.models import SubscriptionPlan 


def initiate_payment(request, plan_id, school_id, sub_type, period):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    price=None
    duration=0
    if period=='monthly':
        price=plan.price
        duration='30 days'
    elif period == 'half_year':
        price=plan.half_year_price
        duration='6 months'
    elif period == 'yearly':
        price=plan.yearly_price
        duration='1 year'
    tx_ref=str(random.randint(1000000000, 9999999999))
    """
    Function to initiate a payment using PayChangu API.
    """
    url = "https://api.paychangu.com/payment"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer SEC-WOOcgseY3K2yPwHoM7Ba78NUhJJZXubZ",  # Replace {secret_key} with your actual secret key
    }
    data = {
        "amount": f"{price}",
        "currency": "MWK",
        "email": "malembohanneck@gmail.com",
        "first_name": f"{request.user.first_name}",
        "last_name": f"{request.user.last_name};",
        "callback_url": f"http://127.0.0.1/payment-success/{plan_id}-{school_id}-{sub_type}-{period}",
        "return_url": "https://webhook.site",
        "tx_ref": tx_ref,
        "customization": {
            "title": "Subscription Payment",
            "description": f"Subscription payment for {plan.name} plan with {duration} Period",
            # "plan_id":f"{plan_id}",
            # "school_id":f"{school_id}",
            # "sub_type":f"{sub_type}",
            # "period":f"{period}",
        },
        # "meta": ("uuid"="uuid","response"="Response",)
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.json())
        result = response.json()

        if result['status'] == 'success' and 'checkout_url' in result['data']:
            # Redirect to the checkout URL
            checkout_url = result['data']['checkout_url']
            trans_id = result['data']['tx_ref']
            return {'checkout_url':checkout_url, 'trans_id':trans_id, 'price':price, 'duration':duration}
        else:
            # Handle unexpected API response
            return JsonResponse({"error": "Failed to generate payment session", "details": result}, status=400)


    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
