from django.conf import settings

def plausible_config(request):
    return {
        'PLAUSIBLE_URL': getattr(settings, 'PLAUSIBLE_URL', '')
    }