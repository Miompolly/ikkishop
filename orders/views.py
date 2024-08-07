import datetime
import json
from django.contrib import messages
import random
import string
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from carts.views import _cart_id
from django.core.mail import send_mail
from orders.form import OrderStatusForm

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
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY



def send_payment_confirmation_email(user_email, order_number, order_total):
    subject = 'Order Confirmation'
    
    # HTML email content with inline CSS
    html_message = f"""
   <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f8f9fa;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header img {{
                max-width: 100px;
                height: auto;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.5;
                color: #333;
            }}
            .order-number {{
                color: #007bff;  /* Blue color for order number */
                font-weight: bold;
            }}
            .total-amount {{
                font-weight: bold;
            }}
            .contact-info {{
                margin-top: 20px;
                font-size: 16px;
                font-weight: bold;
            }}
            hr {{
                border: 0;
                height: 1px;
                background: #e9ecef;
                margin: 20px 0;
            }}
            .title {{
                color: #28a745;  /* Green color for the title */
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="https://private-user-images.githubusercontent.com/104558335/350699386-a81429a9-ed45-45c0-8d74-577c8f8bb38e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjE0ODU3ODYsIm5iZiI6MTcyMTQ4NTQ4NiwicGF0aCI6Ii8xMDQ1NTgzMzUvMzUwNjk5Mzg2LWE4MTQyOWE5LWVkNDUtNDVjMC04ZDc0LTU3N2M4ZjhiYjM4ZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwNzIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDcyMFQxNDI0NDZaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0wZWQ2ODg0MDUwMTBmYmM3ZWYxOWQzZWYyMGFjMzNiZWU3YjY2YzljOGRkMjkzNjI3M2Y1ZmExNjFiMzBiMGE2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.iqK_0H37jNhgk4sj-Jysbeq9xWfB1tnF8TRtwReDlrQ" alt="Company Logo">
            </div>
            <div class="content">
                <h1 class="title" style="text-align: center;">Order Confirmation</h1>
                <p>
                    Thank you for your purchase!<br><br>
                    <strong>Order Number:</strong> <span class="order-number">{order_number}</span><br>
                    <strong>Total Amount:</strong> <span class="total-amount">{order_total} Rwf</span><br><br>
                    Your order has been received and is being processed.<br><br>
                    <hr>
                    <div class="contact-info">
                        <strong>InaFood Contact:</strong> +250780036022
                    </div>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    email = EmailMessage(
        subject,
        html_message,
        from_email,
        recipient_list
    )
    email.content_subtype = 'html' 
    email.send()

@login_required
def payments(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body.get('orderID'))
        

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'rwf',  # Use 'rwf' for Rwandan Francs
                        'product_data': {
                            'name': f'Order {order.order_number}',
                            'description': f'Total amount: {order.order_total} Rwf',
                        },
                        'unit_amount': int(order.order_total * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('order_success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('order_cancel')),
            )

            # Send payment confirmation email
            send_payment_confirmation_email(
                user_email=request.user.email,
                order_number=order.order_number,
                order_total=order.order_total
            )

            # Delete the cart after successful payment
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart.delete()

            return JsonResponse({'id': session.id})
        
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order does not exist'}, status=404)
        
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
        grand_total = float(request.POST.get('grand_total', 0))  # Convert to float
        tax = float(request.POST.get('tax', 0))  # Convert to float
        ip = request.META.get('REMOTE_ADDR')
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # Retrieve cart items from session
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
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
        
        # Calculate total price without tax
        totalprice = grand_total - tax
        
        for item in cart_items:
            if item.product.stock >= item.quantity:
                order_product = OrderProduct(
                    order=order,
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True
                )
                order_product.save()
                
                # Reduce product stock
                item.product.stock -= item.quantity
                item.product.save()
            else:
                # Handle insufficient quantity case (optional)
                messages.error(request, f'Not enough stock for {item.product.product_name}')
                return redirect('cart')  # Redirect to cart or handle as needed

        context = {
            'order': order,
            'cart_items': cart_items,
            'totalprice': totalprice,
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
    
@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user    
    # Get all OrderProduct instances where the product's user is the logged-in user
    order_products = OrderProduct.objects.filter(product__user=user)    
    # Extract distinct orders from the filtered order products
    orders = Order.objects.filter(orderproduct__in=order_products).distinct()
    
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            
            # Prepare the email content
            subject = 'Order Status Updated'
            html_message = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{subject}</title>
                <style>
                    body {{
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        background-color: #f8f9fa;
                    }}
                    .container {{
                        width: 100%;
                        max-width: 600px;
                        margin: auto;
                        padding: 20px;
                        background-color: #ffffff;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .header img {{
                        max-width: 100px;
                        height: auto;
                    }}
                    .content {{
                        font-size: 16px;
                        line-height: 1.5;
                        color: #333;
                    }}
                    .order-number {{
                        color: #007bff;  /* Blue color for order number */
                        font-weight: bold;
                    }}
                    .status {{
                        color: #28a745;  /* Green color for status */
                        font-weight: bold;
                    }}
                    .contact-info {{
                        margin-top: 20px;
                        font-size: 16px;
                        font-weight: bold;
                    }}
                    hr {{
                        border: 0;
                        height: 1px;
                        background: #e9ecef;
                        margin: 20px 0;
                    }}
                    .title {{
                        color: #007bff;  /* Blue color for the title */
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <img src="https://private-user-images.githubusercontent.com/104558335/350699386-a81429a9-ed45-45c0-8d74-577c8f8bb38e.png" alt="Company Logo">
                    </div>
                    <div class="content">
                        <h1 class="title" style="text-align: center;">Order Status Updated</h1>
                        <p>
                            Your order status has been updated.<br><br>
                            <strong>Order Number:</strong> <span class="order-number">{order.order_number}</span><br>
                            <strong>New Status:</strong> <span class="status">{order.status}</span><br><br>
                            Thank you for your attention.<br><br>
                            <hr>
                            <div class="contact-info">
                                <strong>InaFood Contact:</strong> +250780036022
                            </div>
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.email]  # Use the buyer's email from the order
            
            email = EmailMessage(
                subject,
                html_message,
                from_email,
                recipient_list
            )
            email.content_subtype = 'html'  # Specify the email type as HTML
            email.send()

            # Add success message
            messages.success(request, 'Order status updated and email notification sent successfully.')

            return render(request, 'dashboard/order.html', {'orders': orders, 'order_products': order_products})
    else:
        form = OrderStatusForm(instance=order)
    
    return render(request, 'dashboard/update_order_status.html', {'form': form, 'order': order})


