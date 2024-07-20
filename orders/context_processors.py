# context_processors.py

from django.conf import settings

def stripe_settings(request):
    return {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    }
