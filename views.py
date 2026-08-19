from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from orders.models import Order, OrderStatusHistory
from .models import Payment

# ---------------------------------------------------------------------------
# Razorpay integration
# ---------------------------------------------------------------------------
# This module is wired for the Razorpay Checkout flow end-to-end. To go
# live: `pip install razorpay`, set RAZORPAY_KEY_ID / RAZORPAY_KEY_SECRET
# in your environment (or settings.py), and uncomment the client calls
# marked below. Without real API keys, this view runs in DEMO MODE: it
# creates a local Payment record and simulates a successful transaction
# so the full checkout flow can be tested end-to-end offline.
# ---------------------------------------------------------------------------


@login_required
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment, _ = Payment.objects.get_or_create(
        order=order,
        defaults={'amount': order.total, 'status': 'created'}
    )

    # --- LIVE MODE (uncomment once razorpay package + real keys are set) ---
    # import razorpay
    # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # razorpay_order = client.order.create({
    #     'amount': int(order.total * 100),  # amount in paise
    #     'currency': 'INR',
    #     'payment_capture': 1,
    # })
    # payment.razorpay_order_id = razorpay_order['id']
    # payment.save()

    context = {
        'order': order,
        'payment': payment,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'demo_mode': True,
    }
    return render(request, 'payments/payment_page.html', context)


@login_required
def payment_success(request, order_id):
    """
    In LIVE mode this would verify the Razorpay signature server-side
    before marking the order paid. In DEMO mode we simulate success.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = get_object_or_404(Payment, order=order)

    # --- LIVE MODE signature verification (uncomment with real keys) ---
    # import razorpay
    # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    # params = {
    #     'razorpay_order_id': request.POST.get('razorpay_order_id'),
    #     'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
    #     'razorpay_signature': request.POST.get('razorpay_signature'),
    # }
    # client.utility.verify_payment_signature(params)

    payment.status = 'success'
    payment.razorpay_payment_id = request.POST.get('razorpay_payment_id', 'demo_pay_' + str(order.id))
    payment.save()

    order.is_paid = True
    order.status = 'processing'
    order.save()
    OrderStatusHistory.objects.create(order=order, status='processing', note='Payment received.')

    messages.success(request, f'Payment successful! Order #{order.id} is now being processed.')
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment = Payment.objects.filter(order=order).first()
    if payment:
        payment.status = 'failed'
        payment.save()
    messages.error(request, 'Payment failed or was cancelled. You can retry from your order page.')
    return redirect('orders:order_detail', order_id=order.id)
