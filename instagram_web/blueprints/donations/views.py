import braintree
from config import Config

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from models.donations import Donation


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

@donations_blueprint.route('/checkout', methods=['POST'])
def new():
    image_id = request.form.get('image_id')
    
    token = gateway.client_token.generate()
    
    return render_template('donations/new.html', token=token, image_id=image_id)


@donations_blueprint.route('/pay', methods=['POST'])
def create():
    amount = request.form.get('amount')
    
    image_id = request.form.get('image_id')
    
    nonce_from_the_client = request.form.get("nonce")
    
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })
      
    if result.is_success:
        flash("Successfully donated !", "success")
        donation = Donation(username=current_user.id, image=image_id, amount=amount)
        donation.save()
        return  redirect(f'images/{current_user.id}/images')
    
    else:
        flash("Error has occured, please try again", "danger")
        return render_template(url_for('donations.new'))