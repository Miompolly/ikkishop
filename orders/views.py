import datetime
import json
from django.contrib import messages
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from store.models import Product
from .models import Order, OrderProduct, Payment
from carts.models import CartItem,Cart
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, Payment, OrderProduct
from carts.models import CartItem
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_SECRET_KEY



def payments(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Order {}'.format(order.order_number),
                        },
                        'unit_amount': int(order.order_total * 100),  # Stripe expects amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('order_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('order_cancel')),
            )

            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=403)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'status': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'status': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment_success(session)

    return JsonResponse({'status': 'success'}, status=200)

def handle_payment_success(session):
    order_number = session['client_reference_id']
    order = Order.objects.get(order_number=order_number)
    payment = Payment.objects.create(
        user=order.user,
        payment_id=session['payment_intent'],
        payment_method='Stripe',
        amount_paid=order.order_total,
        status='Completed'
    )

    order.payment = payment
    order.is_ordered = True
    order.save()

    cart_items = CartItem.objects.filter(user=order.user)
    for item in cart_items:
        order_product = OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=order.user,
            product=item.product,
            quantity=item.quantity,
            product_price=item.product.price,
            ordered=True,
        )
        order_product.variations.set(item.variations.all())
        order_product.save()

        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=order.user).delete()

    # Send order received email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_received_email.html', {
        'user': order.user,
        'order': order,
    })
    to_email = order.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')

@login_required
def order_cancel(request):
    return render(request, 'orders/order_cancel.html')
@login_required
def place_order(request):
    if request.method == 'POST':
        # Extracting form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        sector = request.POST.get('sector')
        cell = request.POST.get('cell')
        grand_total = request.POST.get('grand_total')
        tax = request.POST.get('tax')
        ip = request.META.get('REMOTE_ADDR')
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Retrieve cart items from session
        cart = get_object_or_404(Cart)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        # Create a new Order
        order = Order(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            district=district,
            sector=sector,
            cell=cell,
            order_total=grand_total,
            tax=tax,
            ip=ip,
            order_number=order_number,
            is_ordered=False  
        )
        order.save()

        # Clear the cart session
        request.session['cart'] = {}

        # Pass context to the template
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': grand_total,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = new_status
        order.save()
        return redirect('order_success', order_id=order.id)
    
def order_success(request):
    return render(request, 'orders/order_success.html') 

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')