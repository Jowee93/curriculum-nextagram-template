import braintree
from config import Config

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user


donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')

gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            braintree.Environment.Sandbox,
            merchant_id=Config.BT_MERCHANT_ID,
            public_key=Config.BT_PUBLIC_KEY,
            private_key=Config.BT_PRIVATE_KEY
        )
    )

amount = 0

@donations_blueprint.route('/client_token', methods=['POST'])
def new():
    global amount
    
    amount = request.form.get('amount')
    
    token = gateway.client_token.generate()
    
    return render_template('donations/new.html', token=token)


@donations_blueprint.route('/pay', methods=['POST'])
def create():
    donation_amount = amount
    testing = request.form.get('test')
    
    nonce_from_the_client = request.form.get("nonce")
    
    result = gateway.transaction.sale({
        "amount": "100",
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })
    
    print(result)
      
    
    if result.is_success:
        flash("Successfully donated !", "success")
        return  redirect(f'images/{current_user.id}/images')