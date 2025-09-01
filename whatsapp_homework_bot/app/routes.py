from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, db, Subscription, Grade
from .forms import LoginForm, SubscriptionForm
from datetime import datetime, timedelta
from .services.wompi_service import verify_wompi_signature
import re


bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    """Displays the main admin dashboard with a list of subscriptions."""
    # DEBUG: Temporarily remove database query to isolate the 500 error.
    subscriptions = []
    return render_template('dashboard.html', title='Dashboard', subscriptions=subscriptions)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handles admin user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña inválidos', 'info')
            return redirect(url_for('main.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.dashboard'))

    return render_template('login.html', title='Iniciar Sesión', form=form)

@bp.route('/logout')
@login_required
def logout():
    """Handles admin user logout."""
    logout_user()
    return redirect(url_for('main.login'))

@bp.route('/new_subscription', methods=['GET', 'POST'])
@login_required
def new_subscription():
    """Handles the creation of a new subscription."""
    form = SubscriptionForm()
    if form.validate_on_submit():
        end_date = datetime.utcnow() + timedelta(days=30)

        subscription = Subscription(
            whatsapp_number=form.whatsapp_number.data,
            customer_email=form.customer_email.data,
            grade_id=form.grade.data,
            subscription_end_date=end_date,
            status='pending'
        )
        db.session.add(subscription)
        db.session.commit()

        fake_wompi_link = f"https://checkout.wompi.co/l/test_sub_{subscription.id}"
        flash(f"Suscripción para '{subscription.customer_email}' creada. Enlace de pago simulado: {fake_wompi_link}", 'info')

        return redirect(url_for('main.dashboard'))

    return render_template('new_subscription.html', title='Nueva Suscripción', form=form)


@bp.route('/subscription/activate/<int:subscription_id>', methods=['POST'])
@login_required
def activate_subscription(subscription_id):
    """Manually activates a pending subscription."""
    sub = Subscription.query.get_or_404(subscription_id)

    if sub.status == 'pending':
        sub.status = 'active'
        db.session.commit()
        flash(f"La suscripción para {sub.customer_email} ha sido activada manualmente.", 'info')
    else:
        flash(f"La suscripción ya se encontraba activa o en otro estado.", 'warning')

    return redirect(url_for('main.dashboard'))


@bp.route('/webhooks/wompi', methods=['POST'])
def wompi_webhook():
    """Receives and processes webhook events from Wompi."""
    # 1. Get data and signature from the request
    request_data_bytes = request.get_data()
    # This is an example header name, the actual one should be verified from Wompi's docs
    signature_from_header = request.headers.get('X-Wompi-Signature', '')

    # 2. Verify the signature (currently simulated)
    # In a real app, you would block requests with invalid signatures.
    # if not verify_wompi_signature(request_data_bytes, signature_from_header):
    #     print("Webhook signature verification failed!")
    #     return jsonify({'status': 'error', 'message': 'invalid signature'}), 403

    # 3. Process the event payload
    payload = request.get_json()
    if not payload:
        return jsonify({'status': 'error', 'message': 'missing payload'}), 400

    event_type = payload.get('event')
    data = payload.get('data', {})

    print(f"Webhook recibido: {event_type}")

    if event_type == 'transaction.updated':
        transaction = data.get('transaction', {})
        trans_status = transaction.get('status')
        reference = transaction.get('reference', '')

        # Extract subscription ID from reference, e.g., "test_sub_1"
        match = re.search(r'test_sub_(\d+)', reference)
        if not match:
            return jsonify({'status': 'error', 'message': 'invalid reference format'}), 400

        subscription_id = int(match.group(1))
        sub = Subscription.query.get(subscription_id)

        if not sub:
            return jsonify({'status': 'error', 'message': 'subscription not found'}), 404

        if trans_status == 'APPROVED':
            sub.status = 'active'
            # Assume the payment source ID is in the payload and store it for renewals
            payment_source_id = transaction.get('payment_method', {}).get('token')
            if payment_source_id:
                sub.wompi_payment_source_id = payment_source_id

            db.session.commit()
            print(f"Webhook: Suscripción {sub.id} activada via pago.")

        elif trans_status in ['DECLINED', 'ERROR', 'VOIDED']:
            sub.status = 'inactive'
            db.session.commit()
            print(f"Webhook: Suscripción {sub.id} marcada como inactiva debido a pago {trans_status}.")

    # 4. Acknowledge receipt of the event to Wompi
    return jsonify({'status': 'success'}), 200
